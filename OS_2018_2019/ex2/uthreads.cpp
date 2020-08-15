#include "uthreads.h"
#include "Thread.h"
#include <iostream>
#include <map>
#include "IdManager.h"
#include "sleeping_threads_list.h"

#define FAILURE -1
#define SUCCESS 0

#define EXIT_FAILURE 1
#define EXIT_SUCCESS 0

// wil indicate that we are currently running after setting sigsetjmp
#define I_AM_ME 0

#define MAIN_THREAD_ID 0

#define USEC_IN_SEC 1000000

// will tell the thread switching to not change the state of the curretnly running thred
#define DO_NOT_CHANGE_STATE 10

#define FAILURE_MSG_MAIN_THREAD_WRONG_STATE "thread library error: main thread cant have that state"
#define FAILURE_MSG_MAIN_THREAD_CANT_BLOCK "thread library error: main thread cant be blocked"
#define FAILURE_MSG_CANT_SET_THREAD_READY "thread library error: thread can not be set to ready"
#define FAILURE_MSG_UNKOWN_STATE "thread library error: thread can not be set to unknown state"
#define FAILURE_MSG_NONEXISTENT_ID "thread library error: no thread with given id"
#define FAILURE_MSG_NEGATIVE_QUANTAS "thread library: quantas cant be non positive"
#define FAILURE_INVALID_NUMBER_OF_THREADS "thread library: not enough available threads"
#define FAILURE_MAX_NUMBER_OF_THREADS "thread library: no more threads to give"
#define FAILURE_COULD_NOT_BLOCK "thread library: could not block"
#define FAILURE_COULD_NOT_SLEEP_MAIN "thread library: could not make main sleep"
#define ERROR_MSG_ITIMER "system error: cant set itimer"
#define ERROR_MSG_SIGPROC "system error: failed to use sigprocmask"
#define ERROR_MSG_SIGEMPTYSET "system error: sigemptyset failed"
#define ERROR_MSG_SIGADDSET "system error: sigaddset failed"
#define ERROR_MSG_SIGACTION "system error: sigaction failed"


static std::map<int, Thread *> allThreads; // a map which will contain all existing threads
static LinkedList *readyList; // a linked list which will contain all ready threads
static IdManager idGiver(MAX_THREAD_NUM); // the id manager of the threads
static SleepingThreadsList sleepingList; // an object which will contain all sleeping Threads
static struct sigaction sa = {0};
static struct itimerval timer;
static Thread *currentlyRunning;
static int totalQuantaPassed = 0;
static sigset_t signalsToIgnore;

/**
 * Deletes all the threads from the "allThreads" map
 * @param exitStatus- 0 for successful exit (for example, the main thread has ended), -1 otherwise
 * (in case of an error)
 */
static int deleteAllThreads(int exitStatus) {
    for (auto it = allThreads.begin(); it != allThreads.end(); ++it) {
        it->second->deleteFromReadyList(readyList, TERMINATED);
        delete it->second; // delete the thread
    }
    delete readyList; // We do not need to delete every not in the ready list.
    // we had did that in the previous loop
    if (exitStatus == SUCCESS) {
        exit(EXIT_SUCCESS);
    }
    exit(EXIT_FAILURE);
}

/**
 * used for system calls errors
 * Exists the program properly. If there's an error,
 * outputs an informative error msg and deletes all threads.
 * @param ReturnValue- 0 for success, -1 otherwise
 * @param errorMsg- The informative error msg
 */
static void exitInCaseOfFailure(int ReturnValue, const std::string &errorMsg) {
    if (ReturnValue == SUCCESS) {
        return;
    }
    std::cerr << errorMsg << '\n';
    deleteAllThreads(FAILURE);
}


/**
 * Calls "sigprocmask" in order to ignore signals during some critical processes
 * (for example, thread switching)
 * and raises and error if something went wrong
 */
static void ignoreTimerSignals() {
    exitInCaseOfFailure(sigprocmask(SIG_BLOCK, &signalsToIgnore, NULL), ERROR_MSG_SIGPROC);
}

/**
 * Calls "sigprocmask" in order to restore signals that were ignored earlier
 * and raises and error if something went wrong
 */
static void stopIgnoreTimerSignals() {
    exitInCaseOfFailure(sigprocmask(SIG_UNBLOCK, &signalsToIgnore, NULL), ERROR_MSG_SIGPROC);
}

/**
 * used for thread library failures
 * @param ReturnValue SUCCESS for success, FAILURE otherwise
 * @param errorMsg - The informative error msg
 * @return SUCCESS if no error was detected, FAILURE otherwise
 */
static int printErrorInCaseOfFailure(int ReturnValue, const std::string &errorMsg) {
    ignoreTimerSignals();

    if (ReturnValue == SUCCESS) {
        stopIgnoreTimerSignals();
        return SUCCESS;
    }
    std::cerr << errorMsg << '\n';
    stopIgnoreTimerSignals();
    return FAILURE;
}

/**
 * @return The thread that is represented by the head of the readyList.
 * Returns nullptr if readyList is empty
 */
static Thread *getNextThreadFromReadyList() {
    if (readyList->isEmpty()) {
        return nullptr;
    }
    int idOfNextThread = readyList->getHead()->getData();
    Thread *nextThread = allThreads[idOfNextThread];
    nextThread->deleteFromReadyList(readyList, RUNNING);
    return nextThread;
}

/**
 * @param awaken_tv a timeval object with the time it should wake up
 * @return SUCCESS if the time to wake up is due, FAILURE otherwise
 */
static int checkTimePassed() {
    if (sleepingList.peek() == nullptr) {
        return FAILURE;
    }
    timeval now;
    time_t usec_since_epoch_of_head = sleepingList.getSecondsSinceEpochOfHead();

    gettimeofday(&now, nullptr);
    time_t usec_since_epoch = now.tv_sec * 1000000 + now.tv_usec;

    if (usec_since_epoch >= usec_since_epoch_of_head) {
        return SUCCESS;
    }
    return FAILURE;
}

/**
 * checks all sleeping threads. Awakes them if necessary
 */
static void wakeUpSleeping() {
    while (checkTimePassed() == SUCCESS) {
        allThreads[sleepingList.peek()->id]->removeFromSleep(readyList);
        sleepingList.pop();
    }
}

/**
 * Switches between the running thread and the next thread to run from "readyList"
 * @param newStateForCurrentlyRunning - The state wed like to put the currently running thread in
 * @return SUCCESS if no error was detected, FAILURE otherwise
 */
static int switchThreadsUsingRoundRobin(int newStateForCurrentlyRunning) {
    ignoreTimerSignals();
    ++totalQuantaPassed;
    wakeUpSleeping(); // check all sleeping threads and wake them if need be

    // when the only existing thread is the main thread
    if (readyList->isEmpty()) {
        // try to continue with the current running thread which is the main thread
        if (newStateForCurrentlyRunning == TERMINATED) {
            // the main thread wants itself terminated
            deleteAllThreads(SUCCESS);
        }
        if (newStateForCurrentlyRunning != READY and newStateForCurrentlyRunning != RUNNING) {
            // main thread can not be in that state
            return printErrorInCaseOfFailure(FAILURE, FAILURE_MSG_MAIN_THREAD_WRONG_STATE);
        }
        // else simply keep the main thread running
        currentlyRunning->increaseRunningTimeBy(1);
        stopIgnoreTimerSignals();
        return SUCCESS;
    }

    switch (newStateForCurrentlyRunning) {
        case READY: {
            int resultFromJump = sigsetjmp(currentlyRunning->getContext(), 1);
            if (resultFromJump == I_AM_ME) {
                // we need to change to the next thread
                currentlyRunning->addToReadyList(readyList);
            } else {
                // we just returned from a different thread, no more action is needed
                stopIgnoreTimerSignals();
                return SUCCESS;
            }
            break;
        }

        case BLOCKED: {
            int resultFromJump = sigsetjmp(currentlyRunning->getContext(), 1);
            if (resultFromJump == I_AM_ME) {
                // we need to change to the next thread
                currentlyRunning->setToBlocked();
            } else {
                // we just returned from a different thread, no more action is needed
                stopIgnoreTimerSignals();
                return SUCCESS;
            }
            break;
        }

        case SLEEPING: {
            int resultFromJump = sigsetjmp(currentlyRunning->getContext(), 1);
            if (resultFromJump == I_AM_ME) {
                // we need to change to the next thread
                currentlyRunning->setToSleep();
            } else {
                // we just returned from a different thread, no more action is needed
                stopIgnoreTimerSignals();
                return SUCCESS;
            }
            break;
        }

        case TERMINATED: {
            if (currentlyRunning->getID() == MAIN_THREAD_ID) {
                // the main thread wants itself terminated
                deleteAllThreads(SUCCESS);
            } else {
                // delete from all threads holder
                allThreads.erase(currentlyRunning->getID());

                // give back the id to the id manager
                idGiver.giveIdBack(currentlyRunning->getID());

                delete currentlyRunning;
            }

            break;
        }
        case DO_NOT_CHANGE_STATE: {
            int resultFromJump = sigsetjmp(currentlyRunning->getContext(), 1);
            if (resultFromJump != I_AM_ME) {
                // we just returned from a different thread, no more action is needed
                stopIgnoreTimerSignals();
                return SUCCESS;
            }
            break;
        }
        default: {
            return printErrorInCaseOfFailure(FAILURE, FAILURE_MSG_UNKOWN_STATE);
        }
    }
    // now pull the next available thread from the ready list
    currentlyRunning = getNextThreadFromReadyList();
    currentlyRunning->increaseRunningTimeBy(1); // increase total quanta count ot thread by 1

    exitInCaseOfFailure(setitimer(ITIMER_VIRTUAL, &timer, NULL), ERROR_MSG_ITIMER);
    stopIgnoreTimerSignals();

    siglongjmp(currentlyRunning->getContext(), 1);
}

/**
 * Puts a given thread in the "allThreadMap"
 * @param t- The thread we'd like to insert
 */
static void insertThreadIntoAllThreadsMap(Thread *t) {
    allThreads.insert({t->getID(), t});
}

/**
 * Switches between the running thread and the next thread to run from "readyList"
 * @param newStateForCurrentlyRunning - The state wed like to put the currently running thread in
 */
static void timerHandler(int sig) {
    if (sig == SIGVTALRM) {
        switchThreadsUsingRoundRobin(READY);
    }
}

/**
 * Description: This function initializes the thread library.
 * You may assume that this function is called before any other thread library
 * function, and that it is called exactly once. The input to the function is
 * the length of a quantum in micro-seconds. It is an error to call this
 * function with non-positive quantum_usecs.
 * @param quantum_usecs- The amount of quantas
*/
int uthread_init(int quantum_usecs) {
    if (quantum_usecs <= 0) {
        return printErrorInCaseOfFailure(FAILURE, FAILURE_MSG_NEGATIVE_QUANTAS);
    }

    // initialize the ready list
    readyList = new LinkedList();

    // initialize the main thread
    int mainThreadID = 0;
    try {
        mainThreadID = idGiver.getNewId();
    } catch (const std::invalid_argument &ia) {
        return printErrorInCaseOfFailure(FAILURE, FAILURE_INVALID_NUMBER_OF_THREADS);
    }
    Node *mainThreadNode = readyList->push(mainThreadID);
    Thread *mainThread = new Thread(nullptr, mainThreadID, 0, mainThreadNode);

    insertThreadIntoAllThreadsMap(mainThread);
    // now set the main thread as the currently running thread
    currentlyRunning = getNextThreadFromReadyList();
    currentlyRunning->increaseRunningTimeBy(1); // increase total quanta count ot thread by 1

    // initialize the signals to ignore
    exitInCaseOfFailure(sigemptyset(&signalsToIgnore), ERROR_MSG_SIGEMPTYSET);
    exitInCaseOfFailure(sigaddset(&signalsToIgnore, SIGVTALRM), ERROR_MSG_SIGADDSET);

    // initialize the timer handler
    sa.sa_handler = &timerHandler;

    // initialize the timer
    int seconds = quantum_usecs / USEC_IN_SEC;
    int useconds = quantum_usecs % USEC_IN_SEC;
    // Configure the timer to expire after 1 sec... */
    timer.it_value.tv_sec = seconds;        // first time interval, seconds part
    timer.it_value.tv_usec = useconds;        // first time interval, microseconds part

    // configure the timer to expire every 3 sec after that.
    timer.it_interval.tv_sec = seconds;    // following time intervals, seconds part
    timer.it_interval.tv_usec = useconds;    // following time intervals, microseconds part

    exitInCaseOfFailure(sigaction(SIGVTALRM, &sa, NULL), ERROR_MSG_SIGACTION);

    // Start a virtual timer. It counts down whenever this process is executing.
    exitInCaseOfFailure(setitimer(ITIMER_VIRTUAL, &timer, NULL), ERROR_MSG_ITIMER);

    ++totalQuantaPassed;
    return SUCCESS;
}

/**
 * Description: This function creates a new thread, whose entry point is the
 * function f with the signature void f(void). The thread is added to the end
 * of the READY threads list. The uthread_spawn function should fail if it
 * would cause the number of concurrent threads to exceed the limit
 * (MAX_THREAD_NUM). Each thread should be allocated with a stack of size
 * STACK_SIZE bytes.
 * @param f - The code that the new thread will run
 * @return 0 on success, -1 otherwise
 */
int uthread_spawn(void (*f)(void)) {
    ignoreTimerSignals();
    int newID = 0;

    try {
        newID = idGiver.getNewId();
    } catch (const std::invalid_argument &ia) {
        return printErrorInCaseOfFailure(FAILURE, FAILURE_MAX_NUMBER_OF_THREADS);
    }

    Node *threadyNode = readyList->push(newID);

    Thread *newThread = new Thread(f, threadyNode->getData(), STACK_SIZE, threadyNode);
    insertThreadIntoAllThreadsMap(newThread);

    stopIgnoreTimerSignals();
    return newID;
}

/**
 * Description: This function terminates the thread with ID tid and deletes
 * it from all relevant control structures. All the resources allocated by
 * the library for this thread should be released. If no thread with ID tid
 * exists it is considered an error. Terminating the main thread
 * (tid == 0) will result in the termination of the entire process using
 * exit(0) [after releasing the assigned library memory].
 * @param tid- The thread's id
 * @return The function returns 0 if the thread was successfully
 * terminated and -1 otherwise. If a thread terminates itself or the main
 * thread is terminated, the function does not return.
 */
int uthread_terminate(int tid) {
    ignoreTimerSignals();

    if (allThreads.find(tid) == allThreads.end()) {
        // if no such thread exists
        return printErrorInCaseOfFailure(FAILURE, FAILURE_MSG_NONEXISTENT_ID);
    }

    if (currentlyRunning->getID() == tid) {
        // we dont need to stop ignoring signals because the
        // thread switching function will ignore and remove them
        switchThreadsUsingRoundRobin(TERMINATED);
        // the switch threads function will handle the case we want to terminate the main thread
        stopIgnoreTimerSignals();
        return SUCCESS;
    }

    // go through the various possibilities and delete the thread
    Thread *threadToTerminate = allThreads[tid];
    allThreads.erase(tid); // delete thread from allThreads
    idGiver.giveIdBack(tid); // give back the id to the id giver

    switch (threadToTerminate->getState()) {
        case READY: {
            threadToTerminate->deleteFromReadyList(readyList, TERMINATED);
            break;
        }
        case BLOCKED: {
            break;
        }
        case SLEEPING: {
            sleepingList.deleteFromList(tid);
            break;
        }
        case SLEEPING_AND_BLOCKED: {
            sleepingList.deleteFromList(tid);
            break;
        }
    }

    stopIgnoreTimerSignals();
    return SUCCESS;
}

/**
 * Description: This function blocks the thread with ID tid. The thread may
 * be resumed later using uthread_resume. If no thread with ID tid exists it
 * is considered as an error. In addition, it is an error to try blocking the
 * main thread (tid == 0). If a thread blocks itself, a scheduling decision
 * should be made. Blocking a thread in BLOCKED state has no
 * effect and is not considered an error.
 * @param tid- The thread's id
 * @return 0 on success, -1 otherwise
 */
int uthread_block(int tid) {
    ignoreTimerSignals();
    if (allThreads.find(tid) == allThreads.end()) {
        // if no such thread exists
        return printErrorInCaseOfFailure(FAILURE, FAILURE_MSG_NONEXISTENT_ID);
    }

    if (tid == 0) {
        return printErrorInCaseOfFailure(FAILURE, FAILURE_MSG_MAIN_THREAD_CANT_BLOCK);
    }

    if (currentlyRunning->getID() == tid) {
        // we dont need to stop ignoring signals because
        // the thread switching function will ignore and remove them
        int res = switchThreadsUsingRoundRobin(BLOCKED);
        stopIgnoreTimerSignals();
        return res;
    }

    if (allThreads[tid]->setToBlocked() == SUCCESS) {
        stopIgnoreTimerSignals();
        return SUCCESS;
    }
    // if we reach this state it must be that the state of the thread is READY

    if (allThreads[tid]->getState() == READY) {
        allThreads[tid]->deleteFromReadyList(readyList, BLOCKED);
        stopIgnoreTimerSignals();
        return SUCCESS;
    }

    stopIgnoreTimerSignals();
    return printErrorInCaseOfFailure(FAILURE, FAILURE_COULD_NOT_BLOCK);
}


static timeval calc_wake_up_timeval(int usecs_to_sleep) {

    timeval now, time_to_sleep, wake_up_timeval;
    gettimeofday(&now, nullptr);
    time_to_sleep.tv_sec = usecs_to_sleep / USEC_IN_SEC;
    time_to_sleep.tv_usec = usecs_to_sleep % USEC_IN_SEC;
    timeradd(&now, &time_to_sleep, &wake_up_timeval);
    return wake_up_timeval;
}

/*
 * Description: This function blocks the RUNNING thread for usecs micro-seconds in real time (not virtual
 * time on the cpu). It is considered an error if the main thread (tid==0) calls this function. Immediately after
 * the RUNNING thread transitions to the BLOCKED state a scheduling decision should be made.
 * After the sleeping time is over, the thread should go back to the end of the READY threads list.
 * Return value: On success, return 0. On failure, return -1.
*/
int uthread_sleep(unsigned int usec) {
    ignoreTimerSignals();
    if (currentlyRunning->getID() == 0) {
        return printErrorInCaseOfFailure(FAILURE, FAILURE_COULD_NOT_SLEEP_MAIN);
    }
    timeval awaken_tv = calc_wake_up_timeval(usec);
    sleepingList.add(currentlyRunning->getID(), awaken_tv);
    currentlyRunning->setToSleep();

    stopIgnoreTimerSignals();
    return switchThreadsUsingRoundRobin(DO_NOT_CHANGE_STATE);
}

/**
 * Description: This function blocks the RUNNING thread for usecs micro-seconds in real time (not virtual
 * time on the cpu). It is considered an error if the main thread (tid==0) calls this function. Immediately after
 * the RUNNING thread transitions to the BLOCKED state a scheduling decision should be made.
 * After the sleeping time is over, the thread should go back to the end of the READY threads list.
 * @param tid- The thread's id
 * @return On success, return 0. On failure, return -1.
 */
int uthread_resume(int tid) {
    ignoreTimerSignals();

    if (allThreads.find(tid) == allThreads.end()) {
        // if no such thread exists
        return printErrorInCaseOfFailure(FAILURE, FAILURE_MSG_NONEXISTENT_ID);
    }

    Thread *threadToResume = allThreads[tid];
    switch (threadToResume->getState()) {
        case BLOCKED: {
            wakeUpSleeping();
            // before adding threads to ready list check if others should come first
            return printErrorInCaseOfFailure(threadToResume->addToReadyList(readyList),
                                             FAILURE_MSG_CANT_SET_THREAD_READY);
        }
        case SLEEPING_AND_BLOCKED: {
            threadToResume->setToSleep();
            break;
        }
        default:
            break;
    }

    stopIgnoreTimerSignals();
    return SUCCESS;
}

/**
 * @return- The id of the currently running thread
 */
int uthread_get_tid() {
    return currentlyRunning->getID();
}

/**
 *  * Description: This function returns the total number of quantums since
 * the library was initialized, including the current quantum.
 * Right after the call to uthread_init, the value should be 1.
 * Each time a new quantum starts, regardless of the reason, this number
 * should be increased by 1.
 * @return The total number of quantums.
 */
int uthread_get_total_quantums() {
    return totalQuantaPassed;
}

/**
 * Description: This function returns the number of quantums the thread with
 * ID tid was in RUNNING state. On the first time a thread runs, the function
 * should return 1. Every additional quantum that the thread starts should
 * increase this value by 1 (so if the thread with ID tid is in RUNNING state
 * when this function is called, include also the current quantum). If no
 * thread with ID tid exists it is considered an error.
 * @param tid- The thread's id
 * @return On success, return the number of quantums of the thread with ID tid.
 * On failure, return -1.
 */
int uthread_get_quantums(int tid) {
    ignoreTimerSignals();
    if (allThreads.find(tid) == allThreads.end()) {
        // if no such thread exists
        return printErrorInCaseOfFailure(FAILURE, FAILURE_MSG_NONEXISTENT_ID);
    }

    int runningTime = allThreads[tid]->getRunningTime();

    stopIgnoreTimerSignals();
    return runningTime;
}