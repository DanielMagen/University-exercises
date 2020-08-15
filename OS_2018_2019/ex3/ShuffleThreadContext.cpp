//
// Created by  on 5/5/19.
//

#include "ShuffleThreadContext.h"

ShuffleThreadContext::ShuffleThreadContext(
        GlobalVariables *gv, int id, const MapReduceClient &client,
        const InputVec &inputVec, OutputVec *outputVec,
        IntermediateVec *intermediateVectorBeingReduced,
        std::vector<ThreadContext *> *contexts) :
        ThreadContext(gv,
                      id,
                      client,
                      inputVec,
                      outputVec,
                      intermediateVectorBeingReduced),
        _contexts(contexts) {}

std::vector<ThreadContext *> *ShuffleThreadContext::getContexts() {
    return _contexts;
}

void ShuffleThreadContext::setLengthOfItemsToWorkOn(unsigned long setTo) {
    _gv->setLengthOfItemsToWorkOn(setTo);
}

int ShuffleThreadContext::getNumberOfThreads() {
    return _gv->getNumberOfThreads();
}

void ShuffleThreadContext::setShuffleFinishedTrue() {
    _gv->setShuffleFinishedTrue();
}

