//
// Created by  on 5/5/19.
//

#ifndef EX3_JOBCONTEXT_H
#define EX3_JOBCONTEXT_H

#include "GlobalVariables.h"
#include "ThreadContext.h"
#include "ShuffleThreadContext.h"


/**
 * this class is responsible to save all data that is relevant to the MapReduceJob
 */
class JobContext {
private:
    /**
     * Holds all the relevant data
     */
    GlobalVariables *_gv;
    /**
     * A poitner to all the threads
     */
    std::vector<ThreadContext *> *_contexts;


public:
    /**
     * A constructor
     * @param gv- A pointer to the "GlobalVariables" object
     * @param contexts- A pointer to the threads
     * @param waitForJobMutex- A pointer to the mutex makes the
     * outside program to wait for the job to end
     * @param waitForJobCv- A cv releases the outside program
     */
    JobContext(
            GlobalVariables *gv,
            std::vector<ThreadContext *> *contexts);


    /**
     * returns the numbers of threads
     */
    int getNumberOfThreads();

    /**
     * a destructor
     */
    ~JobContext();

    /**
     * @return A pointer to all the threads
     */
    std::vector<ThreadContext *> *getContexts();

    /**
     * @return The "waitForJob" mutex
     */
    pthread_mutex_t *getWaitForJobMutex();

    /**
     * @return The "waitForJob" cv
     */
    pthread_cond_t *getWaitForJobCv();

    /**
     * @return Literally returns the threads
     */
    std::vector <pthread_t> *getThreads();

    /**
     * Sets the TerminateFlag To True
     */
    void setTerminateFlagToTrue();

};


#endif //EX3_JOBCONTEXT_H
