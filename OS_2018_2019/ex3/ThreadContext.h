//
// Created by  on 5/5/19.
//

#ifndef EX3_THREADCONTEXT_H
#define EX3_THREADCONTEXT_H

#include "MapReduceFramework.h"
#include "GlobalVariables.h"
#include <pthread.h>
#include <atomic>
#include <algorithm>
#include <semaphore.h>
#include <string>


/**
 * this class is responsible to save all needed information for the thread object
 */
class ThreadContext {
protected:
    /**
     * A pointer to the object that holds all the important
     * data for the threads for the "MapReduce" process
     */
    GlobalVariables *_gv;

private:

    const int _id;

    /**
     * A pointer to the client that created for the required job
     */
    const MapReduceClient &_client;

    /**
     * A vector of <K1, V1> pairs
     */
    const InputVec &_inputVec;

    /**
     * A vector of <K3, V3> pairs that we will eventually
     * return as the result of the "MapReduce" process
     */
    OutputVec *_outputVec;

    /**
     * A vector of <K2, V2> pairs. Each thread holds the pairs
     * that it got form "inputVec" and were mapped.
     */
    IntermediateVec _intermediateResults;

    /**
     * A vector of <K2, V2> pairs that were taken by
     * this thread from the jobPool to the "Reduce" stage
     */
    IntermediateVec *_intermediateVectorBeingReduced;

    // indicator if the thread failed in a system call during an emit function
    int _successFlag;

    /**
     * a flag to check if the work was finished
     */
    bool _finishedWork;

public:
    /**
     * A constructor
     * @param gv- A pointer to the "GlobalVariables" object that all the threads point to
     * @param id- This thread's id
     * @param client- A pointer to the "client" object that all threads point to
     * @param inputVec- The input vector
     * @param outputVec- The output vector
     * @param intermediateVectorBeingReduced- The vector for pairs taken from the jobPool
     */
    ThreadContext(
            GlobalVariables *gv,
            int id,
            const MapReduceClient &client,
            const InputVec &inputVec,
            OutputVec *outputVec,
            IntermediateVec *intermediateVectorBeingReduced);

    /**
     * @return The thread's id
     */
    int getId();

    /**
     * sets the finished flag to true
     */
    void setFinishedTrue();

    /**
     * @return A pointer to the jobHandle object
     */
    void *getJobHandlerPointer();

    /**
     * @return A flag that indicates if the "emit" function had succeeded
     */
    int *getEmitSuccessFlag();

    /**
     * adds 1 to the atomicCounter and returns its old value
     * @return
     */
    unsigned long fetchAndAddAtomicCounter(int *result);

    /**
     * @return The "MapReduceClient" object that all the threads point to
     */
    const MapReduceClient &getClient();

    /**
     * @return The input vector
     */
    const InputVec &getInputVec();

    /**
     * @return The output vector
     */
    OutputVec *getOutputVec();

    /**
     * @return The length of "inputVec"
     */
    unsigned long getLengthOfItemsToWorkOn();

    /**
     * Adds a single <K2, V2> pair to the "_intermediateResults" field of this vector
     * @param resultsPair
     */
    void addToIntermediateResults(IntermediatePair resultsPair);

    /**
     * A comperator for the "IntermediatePair" object
     * @param lhs- A pair
     * @param rhs- A pair
     * @return The value returned from the "operator <" function of the ".first" values of
     * the pairs
     */
    static bool comparePairs(const IntermediatePair &lhs, const IntermediatePair &rhs);

    /**
     * Sorts the "_intermediateResults" vector of this thread
     */
    void sortIntermediateResults();

    /**
     * @return The "intermediateResults" vector
     */
    IntermediateVec &getIntermediateResults();

    /**
     * @return The jobPool that all the threads point to
     */
    std::vector<IntermediateVec *> *getJobPool();

    /**
     * @return The semaphore of the jobPool
     */
    sem_t *getJobPoolSemaphore();

    /**
     * @return The jobPool mutex
     */
    pthread_mutex_t *getJobPoolMutex();

    /**
     * @return The barrier
     */
    Barrier *getAfterSortBarrier();

    /**
     * @return The emit mutex
     */
    pthread_mutex_t *getEmitMutex();

    pthread_mutex_t *getChangeNumberOfItemsCompletedMutex();

    /**
     * @param successFlag if the operation failed it sets this flag to FAILURE
     * @return A copy of the current stage
     */
    stage_t getCopyOfCurrentStage(int *successFlag);

    /**
     *  Sets the threads "_intermediateVectorBeingReduced" field of this vector
     * @param intermediateVectorBeingReduced- The new vector
     */
    void setIntermediateVectorBeingReduced(IntermediateVec *intermediateVectorBeingReduced);

    /**
     * Frees the memory that was allocated for the "_intermediateVectorBeingReduced" field
     * @return The size of "_intermediateVectorBeingReduced" of this thread
     */
    unsigned long deleteIntermediateVectorBeingReduced();

    /**
     * Resets the number of items processed
     */
    void resetNumberOfItemsProcessed();

    /**
     * increases the nubmer of items processed by "addTo"
     * @param addTo- The number we increase by
     */
    void addToNumberOfItemsProcessed(unsigned long addTo);

    /**
     * Converts from fraction to precents
     * @param numerator- The numerator
     * @param denominator- The denominator
     * @return The Percentage
     */
    static float fracToPercentage(unsigned long numerator, unsigned long denominator);

    /**
     * @return The Percentage of in items That were already processed (depends on the stage)
     */
    float getPercentageOfItemsProcessed();

    /**
     * @return The terminate flag
     */
    bool getTerminateFlag();

    /**
     * Sets the current stage
     * @param new_stage- The new stage
     * @param successFlag if the operation failed it sets this flag to FAILURE
     */
    std::string setCurrentStage(stage_t new_stage, int *successFlag);

    /**
     * @return The "waitForJob" cv
     */
    pthread_cond_t *getWaitForJobCv();


    /**
     * sets the Terminate Flag To True
     */
    void setTerminateFlagToTrue();

    /**
     * @return true if the signal to woke every thread that called wait for job has been sent
     */
    bool checkIfWokeEveryoneUp();

    /**
     * set the signal to indicate that every thread that called wait for job has been woken up
     */
    void setWokeEveryoneUpToTrue();

    /**
     * @return the ShuffleFinished flag
     */
    bool getShuffleFinished();

};


#endif //EX3_THREADCONTEXT_H
