//
// Created by  on 5/5/19.
//

#ifndef EX3_SHUFFLETHREADCONTEXT_H
#define EX3_SHUFFLETHREADCONTEXT_H

#include "ThreadContext.h"

/**
 * A special type of thread -The thread that shuffles
 */
class ShuffleThreadContext : public ThreadContext {
private:
    /**
     * A pointer to all the existing threads
     */
    std::vector<ThreadContext *> *_contexts;
public:
    /**
     * A constructor
     * @param gv- A pointer to the "GlobalVariables" object that all the threads point to
     * @param id- This thread's id
     * @param client- A pointer to the "client" object that all threads point to
     * @param inputVec- The input vector
     * @param outputVec- The output vector
     * @param intermediateVectorBeingReduced- The vector for pairs taken from the jobPool
     * @param contexts- All the threads
     */
    ShuffleThreadContext(
            GlobalVariables *gv,
            int id,
            const MapReduceClient &client,
            const InputVec &inputVec,
            OutputVec *outputVec,
            IntermediateVec *intermediateVectorBeingReduced,
            std::vector<ThreadContext *> *contexts);


    /**
     * @return A pointer ot all the threads
     */
    std::vector<ThreadContext *> *getContexts();

    /**
     * Set the Length Of The Items To Work On
     * @param setTo- The length to set to
     */
    void setLengthOfItemsToWorkOn(unsigned long setTo);

    /**
     * @return The number of all existing threads
     */
    int getNumberOfThreads();

    /**
     * sets the ShuffleFinished flag to True
     */
    void setShuffleFinishedTrue();


};

#endif //EX3_SHUFFLETHREADCONTEXT_H
