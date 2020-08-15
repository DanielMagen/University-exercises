//
// Created by  on 5/5/19.
//

#include "ThreadContext.h"

ThreadContext::ThreadContext(GlobalVariables *gv,
                             const int id,
                             const MapReduceClient &client,
                             const InputVec &inputVec,
                             OutputVec *outputVec,
                             IntermediateVec *intermediateVectorBeingReduced) :
        _gv(gv),
        _id(id),
        _client(client),
        _inputVec(inputVec),
        _outputVec(outputVec),
        _intermediateResults(),
        _intermediateVectorBeingReduced(intermediateVectorBeingReduced),
        _successFlag(SUCCESS),
        _finishedWork(false) {}

int ThreadContext::getId() {
    return _id;
}

void *ThreadContext::getJobHandlerPointer() {
    return _gv->getJobHandlerPointer();
}

int *ThreadContext::getEmitSuccessFlag() {
    return &_successFlag;
}

unsigned long ThreadContext::fetchAndAddAtomicCounter(int *result) {
    return _gv->fetchAndAddAtomicCounter(result);
}

const MapReduceClient &ThreadContext::getClient() {
    return _client;
}

const InputVec &ThreadContext::getInputVec() {
    return _inputVec;
}

OutputVec *ThreadContext::getOutputVec() {
    return _outputVec;
}

unsigned long ThreadContext::getLengthOfItemsToWorkOn() {
    return _gv->getLengthOfItemsToWorkOn();
}

void ThreadContext::addToIntermediateResults(IntermediatePair resultsPair) {
    _intermediateResults.push_back(resultsPair);
}

bool ThreadContext::comparePairs(const IntermediatePair &lhs, const IntermediatePair &rhs) {
    return lhs.first->operator<(*rhs.first);
}

void ThreadContext::sortIntermediateResults() {
    if (_intermediateResults.empty()) {
        return;
    }
    std::sort(_intermediateResults.begin(), _intermediateResults.end(), comparePairs);
}

IntermediateVec &ThreadContext::getIntermediateResults() {
    return _intermediateResults;
}

std::vector<IntermediateVec *> *ThreadContext::getJobPool() {
    return _gv->getJobPool();
}

sem_t *ThreadContext::getJobPoolSemaphore() {
    return _gv->getJobPoolSemaphore();
}

pthread_mutex_t *ThreadContext::getJobPoolMutex() {
    return _gv->getJobPoolMutex();
}

Barrier *ThreadContext::getAfterSortBarrier() {
    return _gv->getAfterSortBarrier();
}

pthread_mutex_t *ThreadContext::getEmitMutex() {
    return _gv->getEmitMutex();
}

stage_t ThreadContext::getCopyOfCurrentStage(int *successFlag) {
    return _gv->getCopyOfCurrentStage(successFlag);
}

void ThreadContext::setIntermediateVectorBeingReduced(
        IntermediateVec *intermediateVectorBeingReduced) {
    _intermediateVectorBeingReduced = intermediateVectorBeingReduced;
}

unsigned long ThreadContext::deleteIntermediateVectorBeingReduced() {
    unsigned long length = _intermediateVectorBeingReduced->size();
    delete (_intermediateVectorBeingReduced);
    _intermediateVectorBeingReduced = nullptr;
    return length;
}


void ThreadContext::resetNumberOfItemsProcessed() {
    _gv->resetNumberOfItemsProcessed();
}

void ThreadContext::addToNumberOfItemsProcessed(unsigned long addTo) {
    _gv->addToNumberOfItemsProcessed(addTo);
}

float ThreadContext::fracToPercentage(unsigned long numerator, unsigned long denominator) {
    return (((float) numerator) / ((float) denominator)) * 100;
}

float ThreadContext::getPercentageOfItemsProcessed() {
    return fracToPercentage(_gv->getNumberOfItemsProcessed(), getLengthOfItemsToWorkOn());
}

bool ThreadContext::getTerminateFlag() {
    return _gv->getTerminateFlag();
}

std::string ThreadContext::setCurrentStage(stage_t new_stage, int *successFlag) {
    return _gv->setCurrentStage(new_stage, successFlag);
}

pthread_cond_t *ThreadContext::getWaitForJobCv() {
    return _gv->getWaitForJobCv();
}

void ThreadContext::setTerminateFlagToTrue() {
    _gv->setTerminateFlagToTrue();
}

bool ThreadContext::checkIfWokeEveryoneUp() {
    return _gv->checkIfWokeEveryoneUp();
}

void ThreadContext::setWokeEveryoneUpToTrue() {
    _gv->setWokeEveryoneUpToTrue();
}

bool ThreadContext::getShuffleFinished() {
    return _gv->getShuffleFinished();
}

void ThreadContext::setFinishedTrue() {
    _finishedWork = true;
}

pthread_mutex_t *ThreadContext::getChangeNumberOfItemsCompletedMutex() {
    return _gv->getChangeNumberOfItemsCompletedMutex();
}
