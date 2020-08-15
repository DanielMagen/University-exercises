//
// Created by  on 5/5/19.
//

#ifndef EX3_GLOBALVARIABLES_H
#define EX3_GLOBALVARIABLES_H

#define FAILURE -1
#define SUCCESS 0

#include "MapReduceFramework.h"
#include <pthread.h>
#include "Barrier.h"
#include <semaphore.h>
#include <atomic>
#include <string>
#include <iostream>

#define ERROR_SYSTEM_CALL "error in system function"
#define ERROR_MSG_DESTROY_SEMAPHORE "system error: could not destroy semaphore"
#define ERROR_MSG_LOCK_MUTEX "system error: could not lock mutex"
#define ERROR_MSG_UNLOCK_MUTEX "system error: could not unlock mutex"
#define FAILURE_MSG_EMIT2 "MapReduce error: emit2 function error"
#define FAILURE_MSG_EMIT3 "MapReduce error: emit3 function error"
#define ERROR_MSG_COND_WAIT "system error: could not make thread wait with given cv"
#define ERROR_MSG_BROADCAST "system error: could not broadcast threads"
#define FAILURE_MSG_SEMAPHORE_POST "system error: could not up semaphore"


/**
 * A class that holds all the data that is
 * required for the threads and the job during "MapReduce" process
 */
class GlobalVariables {
private:
    /**
     * a pointer to a vector that will contain pointers to all threads
     */
    std::vector <pthread_t> *_threads;
    int _numberOfThreads;
    /**
     * The barrier object for making sure that we do not continue
     * to the "Reduce" stage before some thread didn't
     * finish mapping
     */
    Barrier *_afterSortBarrier;
    sem_t *_jobPoolSemaphore;
    /**
     * A vector that contains the <K2*, V2*> pairs that will be
     * moved to "Reduce" by the threads. Each thread takes
     * a pair when it can until there are no available pairs
     */
    std::vector<IntermediateVec *> *_jobPool;
    pthread_mutex_t *_jobPoolMutex;
    pthread_mutex_t *_emitMutex;
    stage_t *_currentStage;
    pthread_mutex_t *_stageAccessMutex;

    // this pointer will be used in case of a system call error during execution
    JobHandle _jobHandlerPointer;

    // this will indicate if the need to close the job arose
    bool _terminateFlag;

    /**
     * The index in the "inputVec" of the next <K1, V1> pair that we'd like to map
     */
    std::atomic<unsigned long> *_indexOfNextItemToMap;

    /**
     * The number of <K1, V1> pairs that we have already mapped.
     * Used in the calculation of the Percentage of the work
     */
    std::atomic<unsigned long> *_numberOfItemsProcessed;

    /**
     * the number of items to work on in this stage
     */
    unsigned long _lengthOfItemsToWorkOn;

    /**
     * a flag to know if close was called
     */
    bool _calledClosed;

    /**
     * A mutex that is used by the function "waitForJob".
     * generally, makes the program the executed the "MapReduce" to
     * wait until it end (if the user uses the "waitForJob" function
     */
    pthread_mutex_t *_waitForJobMutex;
    /**
     * A cv that releases the former mutex
     */
    pthread_cond_t *_waitForJobCv;

    /**
     * Indicates that we woke all that called wait for job
     */
    bool _wokeEveryoneUp;

    /**
     * a flag to check that shuffle is finished
     */
    bool *_shuffleFinished;

    pthread_mutex_t *_changeNumberOfItemsCompletedMutex;

public:
    /**
     * A constructor
     * @param threads- The threads
     * @param numberOfThreads- The number of the threads
     * @param afterSortBarrier- The barrier object
     * @param jobPoolSemaphore- The semaphore for the pool of <K2*, V2*> pairs
     * @param jobPool- The <K2*, V2*> pairs vector
     * @param jobPoolMutex- The mutex for entering the job pool
     * @param emitMutex- The emit mutex
     * @param currentStage- The initial stage that will be later changed
     * @param stageAccessMutex- The mutex for changing the stage without any interrputs
     * @param indexOfNextItemToMap- The index of the next item to map
     * @param numberOfItemsProcessed- The number of items that were already Mapped / reduced
     */
    GlobalVariables(
            std::vector <pthread_t> *threads,
            int numberOfThreads,
            Barrier *afterSortBarrier,
            sem_t *jobPoolSemaphore,
            std::vector<IntermediateVec *> *jobPool,
            pthread_mutex_t *jobPoolMutex,
            pthread_mutex_t *emitMutex,
            stage_t *currentStage,
            pthread_mutex_t *stageAccessMutex,
            std::atomic<unsigned long> *indexOfNextItemToMap,
            std::atomic<unsigned long> *numberOfItemsProcessed,
            unsigned long lengthOfInputVec,
            pthread_mutex_t *waitForJobMutex,
            pthread_cond_t *waitForJobCv,
            bool *shuffleFinished,
            pthread_mutex_t *changeNumberOfItemsCompletedMutex);


    /**
     * sets the JobHandlerPointer to the pointer given
     * @param newJobHandlerPointer a new pointer
     */
    void setJobHandlerPointer(void *newJobHandlerPointer);

    /**
     * sets the ShuffleFinished to True
     */
    void setShuffleFinishedTrue();

    /**
     * @return returns ShuffleFinished
     */
    bool getShuffleFinished();

    /**
     * if tmpResult==FAILURE changes result to FAILURE
     * @param tmpResult an integer indicating SUCCESS or FAILURE
     * @param result a pointer to an int
     */
    static void changeResult(int tmpResult, int *result);

    /**
     * @return return the Length Of the Items To Work On
     */
    unsigned long getLengthOfItemsToWorkOn();

    /**
     * @param setTo the length to set the number of items to work
     */
    void setLengthOfItemsToWorkOn(unsigned long setTo);

    /**
     * @return the JobHandlerPointer
     */
    JobHandle getJobHandlerPointer();

    /**
     * @return the jobPool
     */
    std::vector<IntermediateVec *> *getJobPool();

    /**
     * @return The jobPool mutex
     */
    pthread_mutex_t *getJobPoolMutex();

    /**
     * @return The jobPool semaphore
     */
    sem_t *getJobPoolSemaphore();

    /**
     * @return The number of threads
     */
    int getNumberOfThreads();

    /**
     * @return The barrier
     */
    Barrier *getAfterSortBarrier();

    /**
     * @return The emit mutex
     */
    pthread_mutex_t *getEmitMutex();

    /**
     * @param successFlag if the operation failed it sets this flag to FAILURE
     * @return current stage
     */
    stage_t getCopyOfCurrentStage(int *successFlag);

    /**
     * Sets the current stage
     * @param new_stage- The stage we'd like to update our field "_currentStage" to
     * @param successFlag if the operation failed it sets this flag to FAILURE
     */
    std::string setCurrentStage(stage_t new_stage, int *successFlag);

    /**
     * A destructor. Deletes all the objects that we hold and frees the memory we took
     */
    ~GlobalVariables();


    /**
     * sets the terminate flag to true
     */
    void setTerminateFlagToTrue();

    /**
     * @return the terminate flag
     */
    bool getTerminateFlag();

    /**
     * @return The "waitForJob" mutex
     */
    pthread_mutex_t *getWaitForJobMutex();


    /**
     * @return The "waitForJob" cv
     */
    pthread_cond_t *getWaitForJobCv();

    /**
     * @return the threads vector
     */
    std::vector <pthread_t> *getThreads();

    /**
     * adds 1 to the atomicCounter and returns its old value
     * @param result a pointer to an int that indicates if an error occurred
     * @return atomicCounter old value
     */
    unsigned long fetchAndAddAtomicCounter(int *result);

    /**
     * Resets the number of items processed
     */
    void resetNumberOfItemsProcessed();

    /**
     * increases the nubmer of items processed by "addTo"
     * @param addTo- The number we increase by
     */
    void addToNumberOfItemsProcessed(unsigned long addTo) {
        (*_numberOfItemsProcessed) += addTo;
    }

    /**
     * @return the number of items processed
     */
    unsigned long getNumberOfItemsProcessed();

    /**
     * @return returns true if the woke up flag is true
     */
    bool checkIfWokeEveryoneUp();

    /**
     * sets the woke up flag to true
     */
    void setWokeEveryoneUpToTrue();

    pthread_mutex_t *getChangeNumberOfItemsCompletedMutex();
};

#endif //EX3_GLOBALVARIABLES_H
