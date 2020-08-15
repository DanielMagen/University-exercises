#include "MapReduceFramework.h"
#include <pthread.h>
#include <atomic>
#include <vector>
#include <algorithm>
#include <semaphore.h>
#include "Barrier.h"
#include <string>
#include <iostream>
#include "GlobalVariables.h"
#include "ThreadContext.h"
#include "ShuffleThreadContext.h"
#include "JobContext.h"


/**
 * The semaphore threshold
 */
#define REDUCED_SEMAPHORE_SIZE 0

#define FAILURE -1
#define SUCCESS 0
#define SEM_POST_FAILURE -7
#define SEM_WAIT_FAILURE -8
#define EXIT_FAILURE 1
#define LOCK_FAILURE -3
#define WAIT_FAILURE -4
#define BROADCAST_FAILURE -5
#define UNLOCK_FAILURE -6


#define ERROR_MSG_DESTROY_SEMAPHORE "system error: could not destroy semaphore"
#define ERROR_MSG_LOCK_MUTEX "system error: could not lock mutex"
#define ERROR_MSG_UNLOCK_MUTEX "system error: could not unlock mutex"
#define ERROR_MSG_COND_WAIT "system error: could not make thread wait with given cv"
#define ERROR_MSG_BROADCAST "system error: could not broadcast threads"
#define FAILURE_MSG_SEMAPHORE_POST "system error: could not up semaphore"
#define FAILURE_MSG_SEMAPHORE_WAIT "system error: could not down semaphore"
#define FAILURE_MSG_SEMAPHORE_INIT "system error: could not init new semaphore"
#define GENERAL_ERROR_MSG "an error occurred"


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
    exit(EXIT_FAILURE);
}

static std::string getErrorMsgForError(int errorNum) {
    switch (errorNum) {
        case LOCK_FAILURE:
            return ERROR_MSG_LOCK_MUTEX;

        case WAIT_FAILURE:
            return ERROR_MSG_COND_WAIT;

        case BROADCAST_FAILURE:
            return ERROR_MSG_BROADCAST;

        case UNLOCK_FAILURE:
            return ERROR_MSG_UNLOCK_MUTEX;

        case SEM_POST_FAILURE:
            return FAILURE_MSG_SEMAPHORE_POST;

        case SEM_WAIT_FAILURE:
            return FAILURE_MSG_SEMAPHORE_WAIT;

        default:
            return GENERAL_ERROR_MSG;
    }
}

/**
 * if tmpResult==FAILURE changes result to FAILURE
 * @param tmpResult an integer indicating SUCCESS or FAILURE
 * @param result a pointer to an int
 */
static void changeResult(int tmpResult, int *result) {
    if (tmpResult != SUCCESS) {
        *result = tmpResult;
    }
}

/**
 * simply closes the job
 * @param job A JobHandle object that represents the current job
 */
void closeJobHandleWithoutChecking(JobHandle job) {
    auto currentJob = (JobContext *) job;
    currentJob->setTerminateFlagToTrue();
    auto threads = *(currentJob->getThreads());
    auto contexts = *(currentJob->getContexts());
    ThreadContext *tc = (contexts)[0];

    sem_t *jobPoolSemaphore = tc->getJobPoolSemaphore();

    // does up to semaphore n times to wake up all sleeping threads
    for (int i = 0; i < currentJob->getNumberOfThreads(); ++i) {
        sem_post(jobPoolSemaphore);
    }

    // make sure all threads finish

    for (unsigned long j = 0; j < contexts.size(); ++j) {
        pthread_join(threads[j], nullptr);
    }

    // now delete the currentJob, it wakes up all threads that called waitForJob
    delete (currentJob);

}

/**
 * For a given "IntermediateVec" vector, returns the key with the largest value
 * @param curVec- The vector
 * @return The key with the largest value
 */
K2 *getLargestKeyFromIntermediateVec(IntermediateVec &curVec) {
    if (curVec.empty()) {
        return nullptr;
    }
    return curVec.back().first;
}

/**
 * Checks if to K2 objects are equal using "<" operator
 * @param k1- The first key
 * @param k2 The seond key
 * @return true iff the keys are equal
 */
bool keysAreEqual(const K2 &k1, const K2 &k2) {
    return ((!(k1.operator<(k2))) and (!(k2.operator<(k1))));
}

/**
 * Given a vector and a key, returns the amount of pairs with the same key
 * @param vec- The vector
 * @param maxK2- The key
 * @return how many times to pop the vector to get all the pairs with maxK2 key
 */
unsigned long howManyToPop(const IntermediateVec &vec, const K2 &maxK2) {

    if (vec.empty()) {
        return 0;
    }

    if (!keysAreEqual(*vec[vec.size() - 1].first, maxK2)) {
        return 0;
    }

    unsigned long howManyToPop = 0;

    for (long i = vec.size() - 1; i > -1; --i) {
        if (keysAreEqual(*vec[i].first, maxK2)) {
            howManyToPop += 1;
            continue;
        }
        return howManyToPop;
    }

    return howManyToPop;
}


void calculateHowManyPairsToWorkOn(ShuffleThreadContext *threadZeroContext) {
    std::vector < ThreadContext * > threadsContexts = *(threadZeroContext->getContexts());
    int howManyContexts = threadZeroContext->getNumberOfThreads();
    unsigned long NumberOfPairsToWorkOn = 0;

    for (int i = 0; i < howManyContexts; ++i) {
        NumberOfPairsToWorkOn += threadsContexts[i]->getIntermediateResults().size();
    }

    threadZeroContext->setLengthOfItemsToWorkOn(NumberOfPairsToWorkOn);

}

/**
 * this function should be called only from thread 0 and receive its context
 * it will shuffle the pairs from the map stage and insert them into the job pool
 * each time it will insert a new job into the job pool it will up the jobPoolSemaphore
 * @param threadZeroContext
 * @return SUCCESS if never failed in a system call, otherwise it returns a matching failure value
 */
int shuffle(ShuffleThreadContext *threadZeroContext) {
    std::vector < ThreadContext * > threadsContexts = *(threadZeroContext->getContexts());
    std::vector < IntermediateVec * > *jobPool = threadZeroContext->getJobPool();
    pthread_mutex_t *jobPoolMutex = threadZeroContext->getJobPoolMutex();
    sem_t *jobPoolSemaphore = threadZeroContext->getJobPoolSemaphore();
    int howManyContexts = threadZeroContext->getNumberOfThreads();
    int nextIndexWithNonEmptyIntermediateVec = 0;
    int result = SUCCESS;
    int tmpResult;


    // first calculate how many pairs needs to be shuffled
    calculateHowManyPairsToWorkOn(threadZeroContext);

    // Every iteration of the following loop does the following:
    // 1) extracts a key "maxK2" from some vector
    // 2) finds all the pairs with the same key in all the existing vectors
    // 3) puts all of those pairs in a vector called "toAddToJobPool",
    // which eventually will be, added to "jobPool"
    while (nextIndexWithNonEmptyIntermediateVec < howManyContexts) {

        // this is in case close job was called during the shuffle stage
        // now check if the terminateFlag is true, if so then simply return
        if (threadZeroContext->getTerminateFlag()) {
            threadZeroContext->setShuffleFinishedTrue();
            return SUCCESS;
        }

        K2 *maxK2 = getLargestKeyFromIntermediateVec(
                threadsContexts[nextIndexWithNonEmptyIntermediateVec]->getIntermediateResults());
        K2 *currentK2;

        int currentIndex = nextIndexWithNonEmptyIntermediateVec;

        // This loop helps us knowing if there are
        // any vectors which aren't empty left (if not, we finished shuffling)
        while (maxK2 == nullptr and currentIndex < howManyContexts - 1) {
            ++currentIndex;
            maxK2 = getLargestKeyFromIntermediateVec(
                    threadsContexts[currentIndex]->getIntermediateResults());
        }
        if (maxK2 == nullptr) {
            ++currentIndex;
        }

        // we will start looking for the max key from the first vector which isn't empty
        nextIndexWithNonEmptyIntermediateVec = currentIndex;

        if (currentIndex == howManyContexts) {
            threadZeroContext->setShuffleFinishedTrue();
            return SUCCESS;
        }

        // now find the key with maximum value from all vectors of all threads
        for (int i = currentIndex; i < howManyContexts; ++i) {
            currentK2 = getLargestKeyFromIntermediateVec(
                    threadsContexts[i]->getIntermediateResults());
            if (currentK2 == nullptr) {
                continue;
            }

            if (maxK2->operator<(*currentK2)) {
                maxK2 = currentK2;
            }
        }

        auto toAddToJobPool = new IntermediateVec();

        // now get all the pairs that have the max key
        for (int j = nextIndexWithNonEmptyIntermediateVec; j < howManyContexts; ++j) {
            // no need for mutex since we are the only thread that access the contexts vectors

            IntermediateVec &currentVector = threadsContexts[j]->getIntermediateResults();
            unsigned long howManyPairsToPop = howManyToPop(currentVector, *maxK2);

            // add all pairs with the key to the toAddToJobPool vector
            for (unsigned long i = 0; i < howManyPairsToPop; ++i) {
                toAddToJobPool->push_back(currentVector.back());
                currentVector.pop_back();
            }
        }

        // add the toAddToJobPool to the job pool
        tmpResult = pthread_mutex_lock(jobPoolMutex) * 3;
        changeResult(tmpResult, &result);

        jobPool->push_back(toAddToJobPool);
        tmpResult = sem_post(jobPoolSemaphore) * 7;
        changeResult(tmpResult, &result);

        tmpResult = pthread_mutex_unlock(jobPoolMutex) * 6;
        changeResult(tmpResult, &result);

        if (result != SUCCESS) {
            threadZeroContext->setShuffleFinishedTrue();
            return result;
        }

    }

    threadZeroContext->setShuffleFinishedTrue();
    return SUCCESS;

}

/**
 * This function is the next stage after the "sort" process.
 * every thread that gets here takes a job from jobPool and operates "reduce" on it".
 * MoreOver, if the thread that got here is "ShuffleThreadContext",
 * thread 0, then it starts the "shuffle" stage.
 * Note 1: in order to get a job from the job pool,
 * a thread needs to get into the "jobPoolSemaphore"- if there are 'n'
 * jobs in the pool job, lets only to 'n' threads to pass the semaphore.
 *
 * Note 2: The operation of extracting a job from the pool job
 * (which is taking a vector from the jobPool object) is a critical code section,
 * and we lock it with "jobPoolMutex"
 * @param tc- The thread that is going to extract a job From "jobPool" and operates "reduce" on it
 * @return SUCCESS if never failed in a system call, otherwise it returns a matching failure value
 */
int reduceStage(ThreadContext *tc) {
    std::vector < IntermediateVec * > *jobPool = tc->getJobPool();
    sem_t *jobPoolSemaphore = tc->getJobPoolSemaphore();
    pthread_mutex_t *jobPoolMutex = tc->getJobPoolMutex();
    pthread_mutex_t *changeNumberOfItemsCompletedMutex = tc->getChangeNumberOfItemsCompletedMutex();

    int result = SUCCESS;
    unsigned long numberOfPairsProcessed = 0;

    // check if the terminateFlag is true, if so then simply return
    // this is in case close job was called before the reduce stage
    if (tc->getTerminateFlag()) {
        return SUCCESS;
    }

    // after all threads pass the barrier
    if (tc->getId() == 0) {
        auto threadZeroContext = (ShuffleThreadContext *) tc;
        // first reset the NumberOfItemsProcessed counter
        threadZeroContext->resetNumberOfItemsProcessed();

        // now set the stage to REDUCE
        threadZeroContext->setCurrentStage(REDUCE_STAGE, &result);

        // start shuffling. After finishing, joins all the other thread to the job pool
        result = shuffle(threadZeroContext);
        if (result != SUCCESS) {
            return result;
        }
        // check if the terminate flag arose
        if (tc->getTerminateFlag()) {
            return SUCCESS;
        }
    }

    while (true) {
        // check if a previous emit call failed
        result = *(tc->getEmitSuccessFlag());
        if (result != SUCCESS) {
            return result;
        }

        if (tc->getPercentageOfItemsProcessed() == 100 and tc->getShuffleFinished()) {
            // wake up all threads that called waitForJob

            tc->setFinishedTrue();

            if (tc->checkIfWokeEveryoneUp()) {
                return SUCCESS;
            } else {
                tc->setWokeEveryoneUpToTrue();
                result = pthread_cond_broadcast(tc->getWaitForJobCv());
                return result;
            }
        }

        // check if there is an open job to take, if not, sleep
        result = sem_wait(jobPoolSemaphore) * 8;
        if (result != SUCCESS) {
            return result;
        }


        // this is in case close job was called during the reduce stage
        // now check if the terminateFlag is true or the job is finished, if so then simply return
        if (tc->getTerminateFlag() or tc->getPercentageOfItemsProcessed() == 100) {
            break;
        }

        result = pthread_mutex_lock(jobPoolMutex) * 3;
        if (result != SUCCESS) {
            return result;
        }

        // take the vector of pairs to be your vector, and pop it from the job pool
        IntermediateVec *vectorToActUpon = jobPool->back();
        jobPool->pop_back();
        tc->setIntermediateVectorBeingReduced(vectorToActUpon);


        result = pthread_mutex_unlock(jobPoolMutex) * 6;
        if (result != SUCCESS) {
            return result;
        }

        tc->getClient().reduce(vectorToActUpon, tc);

        result = pthread_mutex_lock(changeNumberOfItemsCompletedMutex) * 3;
        if (result != SUCCESS) {
            return result;
        }
        numberOfPairsProcessed = tc->deleteIntermediateVectorBeingReduced();


        tc->addToNumberOfItemsProcessed(numberOfPairsProcessed);
        result = pthread_mutex_unlock(changeNumberOfItemsCompletedMutex) * 6;
        if (result != SUCCESS) {
            return result;
        }

    }

    return SUCCESS;

}


/**
 * This function is called by the "reduce" function.
 * It puts the <K3, V3> pair in the given thread ("context").
 * Note: We use "emitMutex" for getting the pair into the thread's vector,
 * for it is critical that we won't have a context switch during doing that
 * @param key- The key
 * @param value- The value
 * @param context- The thread
 */
void emit3(K3 *key, V3 *value, void *context) {
    auto tc = (ThreadContext *) context;
    int tmpResult;
    int *threadEmitSuccessFlag = tc->getEmitSuccessFlag();
    OutputVec *outputVec = tc->getOutputVec();
    pthread_mutex_t *emitMutex = tc->getEmitMutex();

    tmpResult = pthread_mutex_lock(emitMutex);
    changeResult(tmpResult, threadEmitSuccessFlag);

    // delete the vector that was taken from the jobPool and get how many pairs were processed
    OutputPair pair(key, value);
    outputVec->push_back(pair);

    tmpResult = pthread_mutex_unlock(emitMutex);
    changeResult(tmpResult, threadEmitSuccessFlag);
}

/**
 * This function is responsible of executing the "MapAndReduce" operation.
 * It checks for the next <K1, V1> pair that we should map's index and puts it in the thread's
 * vector. Then, the vector is being sorted. When all threads are
 * finished with sorting, "Reduce" stage kicks in.
 * @param args - the context of the thread
 * @return FAILURE if failed in a system call, SUCCESS otherwise
 */
int mapAndSortStage(void *args) {
    auto tc = (ThreadContext *) args;
    int result = SUCCESS;
    bool continueMapping = true;
    pthread_mutex_t *emitMutex = tc->getEmitMutex();
    int tmpResult;
    Barrier *afterSortBarrier = tc->getAfterSortBarrier();
    std::string errorMsg;

    errorMsg = tc->setCurrentStage(MAP_STAGE, &result);
    if (result != SUCCESS) {
        return result;
    }

    while (continueMapping) {
        // check if the terminate flag arose
        if (tc->getTerminateFlag()) {
            return SUCCESS;
        }

        // check if a previous emit call failed
        result = *(tc->getEmitSuccessFlag());
        if (result != SUCCESS) {
            return result;
        }

        // get next available input pair
        unsigned long indexOfNextAvailablePair = tc->fetchAndAddAtomicCounter(&result);

        if (indexOfNextAvailablePair >= tc->getLengthOfItemsToWorkOn()) {
            // Now, the thread should sort it's intermediate vector
            tc->sortIntermediateResults();

            // now all threads should go through the barrier
            result = afterSortBarrier->barrier(tc->getId());

            // check the result from the barrier usage
            if (result != SUCCESS) {
                return result;
            }


            result = reduceStage(tc);
            // check if the terminate flag arose
            if (tc->getTerminateFlag()) {
                return SUCCESS;
            }

            // now check if the reduce stage has completed successfully
            if (result != SUCCESS) {
                return result;
            } else {
                continueMapping = false;
            }
        } else {
            InputPair pairToWorkOn = tc->getInputVec()[indexOfNextAvailablePair];
            tc->getClient().map(pairToWorkOn.first, pairToWorkOn.second, tc);

            int *threadEmitSuccessFlag = tc->getEmitSuccessFlag();

            // add 1 to the overall numbers processed
            tmpResult = pthread_mutex_lock(emitMutex) * 3;
            changeResult(tmpResult, threadEmitSuccessFlag);

            tc->addToNumberOfItemsProcessed(1);

            tmpResult = pthread_mutex_unlock(emitMutex) * 6;
            changeResult(tmpResult, threadEmitSuccessFlag);

            if (result != SUCCESS) {
                return result;
            }
        }
    }
    return SUCCESS;
}


/**
 * This function is called by the "map" function.
 * It puts the <K2, V2> pair in the given thread ("context").
 * Note: We use "emitMutex" for getting the pair into the thread's vector,
 * for it is critical that we won't have a context switch during doing that
 * @param key- The key
 * @param value- The value
 * @param context- The thread
 */
void emit2(K2 *key, V2 *value, void *context) {
    auto tc = (ThreadContext *) context;

    IntermediatePair pair(key, value);
    tc->addToIntermediateResults(pair);
}


/**
 * starts the map function and checks of there were errors while running
 * @param args - the context of the thread
 * @return
 */
void *startMapAndCheckErrors(void *args) {
    auto tc = (ThreadContext *) args;
    int result = mapAndSortStage(args);
    std::string errorMsg;

    // if the terminate flag arose then simply do nothing, another thread is closing the job
    if (tc->getTerminateFlag()) {
        return SUCCESS;
    }

    if (result != SUCCESS) {
        tc->setTerminateFlagToTrue();
        errorMsg = getErrorMsgForError(result);
        closeJobHandleWithoutChecking(tc->getJobHandlerPointer());
        exitInCaseOfFailure(result, errorMsg);
    }

    return SUCCESS;
}

/**
 * This function initializes the required objects for executing the "MapReduce" operation. for
 * example, creating threads, mutexes, semaphores and a JobHandle object
 * @param client- The "MapReduceClient" object that was created for this job
 * @param inputVec- The input vector
 * @param outputVec- The input vector
 * @param multiThreadLevel- The number of threads that the user would like the MapReduce operation
 * to use
 * @return A JobHandle object for the current job
 */
JobHandle startMapReduceJob(const MapReduceClient &client,
                            const InputVec &inputVec,
                            OutputVec &outputVec,
                            int multiThreadLevel) {

    int result;

    // this barrier will make sure that only after every item has been mapped and sorted
    // the reduction phase will begin
    auto afterSortBarrier = new Barrier(multiThreadLevel);

    // create an array of pointers to threads
    auto threads = new std::vector<pthread_t>();

    // create context objects for all threads
    auto contexts = new std::vector<ThreadContext *>();

    // this will hold the index of the next pair to apply map to
    auto indexOfNextItemToMap = new std::atomic<unsigned long>(0);

    // the job pool for the reduction stage
    auto jobPool = new std::vector<IntermediateVec *>;

    // the semaphore and mutex will handle job pool reading and writing
    sem_t *jobPoolSemaphore = new sem_t;
    result = sem_init(jobPoolSemaphore, 0, REDUCED_SEMAPHORE_SIZE);
    if (result != 0) {
        exitInCaseOfFailure(FAILURE, FAILURE_MSG_SEMAPHORE_INIT);
    }

    bool *shuffleFinished = new bool(false);

    pthread_mutex_t *jobPoolMutex = new pthread_mutex_t(PTHREAD_MUTEX_INITIALIZER);

    pthread_mutex_t *changeNumberOfItemsCompleted = new pthread_mutex_t(PTHREAD_MUTEX_INITIALIZER);

    // the mutex and cv will be used by the waitForJob function
    pthread_mutex_t *waitForJobMutex = new pthread_mutex_t(PTHREAD_MUTEX_INITIALIZER);


    pthread_cond_t *waitForJobCv = new pthread_cond_t(PTHREAD_COND_INITIALIZER);


    // will hold in each stage how many items have been mapped/reduced
    std::atomic<unsigned long> *numberOfItemsProcessed = new std::atomic<unsigned long>(0);


    // a mutex that will be used in both emit functions to guard among other things the change
    // of numberOfItemsProcessed
    pthread_mutex_t *emitMutex = new pthread_mutex_t(PTHREAD_MUTEX_INITIALIZER);

    // will hold the current stage of the job
    auto currentStage = new stage_t(UNDEFINED_STAGE);


    // will guards the access to the currentStage holder
    pthread_mutex_t *stageAccessMutex = new pthread_mutex_t(PTHREAD_MUTEX_INITIALIZER);

    auto gv = new GlobalVariables(threads,
                                  multiThreadLevel,
                                  afterSortBarrier,
                                  jobPoolSemaphore,
                                  jobPool,
                                  jobPoolMutex,
                                  emitMutex,
                                  currentStage,
                                  stageAccessMutex,
                                  indexOfNextItemToMap,
                                  numberOfItemsProcessed,
                                  inputVec.size(),
                                  waitForJobMutex,
                                  waitForJobCv,
                                  shuffleFinished,
                                  changeNumberOfItemsCompleted);

    // initialize JobContext
    auto currentJob = new JobContext(
            gv,
            contexts);

    gv->setJobHandlerPointer(currentJob);

    contexts->push_back(new ShuffleThreadContext(gv,
                                                 0,
                                                 client,
                                                 inputVec,
                                                 &outputVec,
                                                 nullptr,
                                                 contexts));
    for (int i = 1; i < multiThreadLevel; ++i) {
        contexts->push_back(new ThreadContext(gv,
                                              i,
                                              client,
                                              inputVec,
                                              &outputVec,
                                              nullptr));

    }

    for (int i = 0; i < multiThreadLevel; ++i) {
        pthread_t newThread;
        pthread_create(&newThread, nullptr, startMapAndCheckErrors, (*contexts)[i]);
        threads->push_back(newThread);
    }


    return currentJob;

}

/**
 * A function that gets the job handle returned by startMapReduceFramework and waits until it is
 * finished.
 * @param job- A JobHandle object that represents the current job
 * Note: For making the outside program to wait for the "MapReduce" operation to finish is a
 * critical code that we wouldn't like to be interrupted, we use a mutex
 */
void waitForJob(JobHandle job) {
    auto currentJob = (JobContext *) job;

    ThreadContext *tc = (*currentJob->getContexts())[0];

    // in case wait for job was called after the job was finished
    int mutexResult = SUCCESS;
    auto currentStage = tc->getCopyOfCurrentStage(&mutexResult);
    auto percentage = tc->getPercentageOfItemsProcessed();

    if (mutexResult != SUCCESS) {
        closeJobHandleWithoutChecking(tc->getJobHandlerPointer());
        exitInCaseOfFailure(FAILURE, getErrorMsgForError(mutexResult));
    }

    if (currentStage == REDUCE_STAGE and percentage == 100) {
        return;
    }


    pthread_mutex_t *waitForJobMutex = currentJob->getWaitForJobMutex();
    pthread_cond_t *waitForJobCv = currentJob->getWaitForJobCv();

    if (pthread_mutex_lock(waitForJobMutex) != SUCCESS) {
        closeJobHandleWithoutChecking(tc->getJobHandlerPointer());
        exitInCaseOfFailure(FAILURE, ERROR_MSG_LOCK_MUTEX);

    }
    if (pthread_cond_wait(waitForJobCv, waitForJobMutex) != SUCCESS) {
        closeJobHandleWithoutChecking(tc->getJobHandlerPointer());
        exitInCaseOfFailure(FAILURE, ERROR_MSG_COND_WAIT);
    }
}


/**
 * @param job- The job that we'd like to get the state of
 * @param state- The "state" object that we update
 */
void getJobState(JobHandle job, JobState *state) {
    auto currentJob = (JobContext *) job;
    ThreadContext *tc = (*currentJob->getContexts())[0];

    int mutexResult = SUCCESS;
    state->stage = tc->getCopyOfCurrentStage(&mutexResult);
    state->percentage = tc->getPercentageOfItemsProcessed();

    if (mutexResult != SUCCESS) {
        closeJobHandleWithoutChecking(tc->getJobHandlerPointer());
        exitInCaseOfFailure(FAILURE, getErrorMsgForError(mutexResult));
    }
}

/**
 * Terminates the given job
 * @param job- The "JobHandle" object that we'd like to close
 */
void closeJobHandle(JobHandle job) {
    auto currentJob = (JobContext *) job;

    // prevent closing if not finished
    ThreadContext *tc = (*currentJob->getContexts())[0];

    int mutexResult = SUCCESS;
    auto currentStage = tc->getCopyOfCurrentStage(&mutexResult);
    auto percentage = tc->getPercentageOfItemsProcessed();

    if (mutexResult != SUCCESS) {
        closeJobHandleWithoutChecking(tc->getJobHandlerPointer());
        exitInCaseOfFailure(FAILURE, getErrorMsgForError(mutexResult));
    }

    if (currentStage != REDUCE_STAGE or percentage != 100) {
        waitForJob(job);
        return;
    }

    // assuming that all processes are finished from here on out
    closeJobHandleWithoutChecking(job);


}