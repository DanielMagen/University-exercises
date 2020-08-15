//
// Created by  on 5/5/19.
//

#include "GlobalVariables.h"


GlobalVariables::GlobalVariables(
        std::vector <pthread_t> *threads, int numberOfThreads, Barrier *afterSortBarrier,
        sem_t *jobPoolSemaphore, std::vector<IntermediateVec *> *jobPool,
        pthread_mutex_t *jobPoolMutex, pthread_mutex_t *emitMutex, stage_t *currentStage,
        pthread_mutex_t *stageAccessMutex, std::atomic<unsigned long> *indexOfNextItemToMap,
        std::atomic<unsigned long> *numberOfItemsProcessed, unsigned long lengthOfInputVec,
        pthread_mutex_t *waitForJobMutex, pthread_cond_t *waitForJobCv,
        bool *shuffleFinished,
        pthread_mutex_t *changeNumberOfItemsCompletedMutex) :
        _threads(threads),
        _numberOfThreads(numberOfThreads),
        _afterSortBarrier(afterSortBarrier),
        _jobPoolSemaphore(jobPoolSemaphore),
        _jobPool(jobPool),
        _jobPoolMutex(jobPoolMutex),
        _emitMutex(emitMutex),
        _currentStage(currentStage),
        _stageAccessMutex(stageAccessMutex),
        _jobHandlerPointer(nullptr),
        _terminateFlag(false),
        _indexOfNextItemToMap(indexOfNextItemToMap),
        _numberOfItemsProcessed(numberOfItemsProcessed),
        _lengthOfItemsToWorkOn(lengthOfInputVec),
        _calledClosed(false),
        _waitForJobMutex(waitForJobMutex),
        _waitForJobCv(waitForJobCv),
        _wokeEveryoneUp(false),
        _shuffleFinished(shuffleFinished),
        _changeNumberOfItemsCompletedMutex(changeNumberOfItemsCompletedMutex) {}


void GlobalVariables::setJobHandlerPointer(void *newJobHandlerPointer) {
    _jobHandlerPointer = newJobHandlerPointer;
}

void GlobalVariables::setShuffleFinishedTrue() {
    *_shuffleFinished = true;
}

bool GlobalVariables::getShuffleFinished() {
    return *_shuffleFinished;
}

void GlobalVariables::changeResult(int tmpResult, int *result) {
    if (tmpResult == FAILURE) {
        *result = FAILURE;
    }
}

unsigned long GlobalVariables::getLengthOfItemsToWorkOn() {
    return _lengthOfItemsToWorkOn;
}

void GlobalVariables::setLengthOfItemsToWorkOn(unsigned long setTo) {
    _lengthOfItemsToWorkOn = setTo;
}

JobHandle GlobalVariables::getJobHandlerPointer() {
    return _jobHandlerPointer;
}

std::vector<IntermediateVec *> *GlobalVariables::getJobPool() {
    return _jobPool;
}

pthread_mutex_t *GlobalVariables::getJobPoolMutex() {
    return _jobPoolMutex;
}

pthread_mutex_t *GlobalVariables::getChangeNumberOfItemsCompletedMutex() {
    return _changeNumberOfItemsCompletedMutex;
}

sem_t *GlobalVariables::getJobPoolSemaphore() {
    return _jobPoolSemaphore;
}

int GlobalVariables::getNumberOfThreads() {
    return _numberOfThreads;
}

Barrier *GlobalVariables::getAfterSortBarrier() {
    return _afterSortBarrier;
}

pthread_mutex_t *GlobalVariables::getEmitMutex() {
    return _emitMutex;
}

stage_t GlobalVariables::getCopyOfCurrentStage(int *successFlag) {
    int tmpResults;

    tmpResults = pthread_mutex_lock(_stageAccessMutex);
    changeResult(tmpResults, successFlag);

    stage_t toReturn = *_currentStage;

    tmpResults = pthread_mutex_unlock(_stageAccessMutex);
    changeResult(tmpResults, successFlag);

    return toReturn;
}

std::string GlobalVariables::setCurrentStage(stage_t new_stage, int *successFlag) {
    int tmpResults;
    std::string errorMsg;

    tmpResults = pthread_mutex_lock(_stageAccessMutex);
    changeResult(tmpResults, successFlag);
    errorMsg = ERROR_MSG_LOCK_MUTEX;

    *_currentStage = new_stage;

    tmpResults = pthread_mutex_unlock(_stageAccessMutex);
    changeResult(tmpResults, successFlag);
    errorMsg = ERROR_MSG_UNLOCK_MUTEX;

    return errorMsg;
}

GlobalVariables::~GlobalVariables() {

    delete (_threads);
    _threads = nullptr;

    int result = SUCCESS;
    int tmpResults;
    std::string errorMsg = ERROR_SYSTEM_CALL;

    tmpResults = sem_destroy(_jobPoolSemaphore);
    delete (_jobPoolSemaphore);
    _jobPoolSemaphore = nullptr;

    changeResult(tmpResults, &result);
    errorMsg = ERROR_MSG_DESTROY_SEMAPHORE;

    delete (_jobPool);
    _jobPool = nullptr;

    tmpResults = pthread_mutex_destroy(_jobPoolMutex);
    delete (_jobPoolMutex);
    _jobPoolMutex = nullptr;
    changeResult(tmpResults, &result);
    errorMsg = ERROR_MSG_DESTROY_MUTEX;

    tmpResults = pthread_mutex_destroy(_emitMutex);
    delete (_emitMutex);
    _emitMutex = nullptr;
    changeResult(tmpResults, &result);
    errorMsg = ERROR_MSG_DESTROY_MUTEX;

    delete (_currentStage);
    _currentStage = nullptr;

    tmpResults = pthread_mutex_destroy(_stageAccessMutex);
    delete (_stageAccessMutex);
    _stageAccessMutex = nullptr;
    changeResult(tmpResults, &result);
    errorMsg = ERROR_MSG_DESTROY_MUTEX;

    delete (_indexOfNextItemToMap);

    delete (_numberOfItemsProcessed);

    tmpResults = pthread_mutex_destroy(_waitForJobMutex);
    delete (_waitForJobMutex);
    _waitForJobMutex = nullptr;
    changeResult(tmpResults, &result);

    tmpResults = pthread_cond_destroy(_waitForJobCv);
    delete (_waitForJobCv);
    _waitForJobCv = nullptr;
    changeResult(tmpResults, &result);

    delete (_afterSortBarrier);
    _afterSortBarrier = nullptr;

    delete (_shuffleFinished);


    tmpResults = pthread_mutex_destroy(_changeNumberOfItemsCompletedMutex);
    delete (_changeNumberOfItemsCompletedMutex);
    _changeNumberOfItemsCompletedMutex = nullptr;
    changeResult(tmpResults, &result);

    if (result != SUCCESS) {
        std::cerr << errorMsg << '\n';
        exit(EXIT_FAILURE);
    }
}

void GlobalVariables::setTerminateFlagToTrue() {
    _terminateFlag = true;
}

bool GlobalVariables::getTerminateFlag() {
    return _terminateFlag;
}

pthread_mutex_t *GlobalVariables::getWaitForJobMutex() {
    return _waitForJobMutex;
}

pthread_cond_t *GlobalVariables::getWaitForJobCv() {
    return _waitForJobCv;
}

unsigned long GlobalVariables::fetchAndAddAtomicCounter(int *result) {
    unsigned long toReturn = 0;
    int tmpResult;

    pthread_mutex_t *emitMutex = getEmitMutex();

    // add 1 to the overall numbers processed
    tmpResult = pthread_mutex_lock(emitMutex);
    changeResult(tmpResult, result);

    toReturn = (*(_indexOfNextItemToMap))++;

    tmpResult = pthread_mutex_unlock(emitMutex);
    changeResult(tmpResult, result);

    return toReturn;

}

void GlobalVariables::resetNumberOfItemsProcessed() {
    (*_numberOfItemsProcessed) = 0;
}

unsigned long GlobalVariables::getNumberOfItemsProcessed() {
    return *_numberOfItemsProcessed;
}

std::vector <pthread_t> *GlobalVariables::getThreads() {
    return _threads;
}

bool GlobalVariables::checkIfWokeEveryoneUp() {
    return _wokeEveryoneUp;
}

void GlobalVariables::setWokeEveryoneUpToTrue() {
    _wokeEveryoneUp = true;
}
