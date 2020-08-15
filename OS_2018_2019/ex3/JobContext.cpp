//
// Created by  on 5/5/19.
//

#include "JobContext.h"

JobContext::JobContext(GlobalVariables *gv, std::vector<ThreadContext *> *contexts) :
        _gv(gv),
        _contexts(contexts) {}

int JobContext::getNumberOfThreads() {
    return _gv->getNumberOfThreads();
}

JobContext::~JobContext() {
    // delete all ThreadContexts
    for (int i = 1; i < _gv->getNumberOfThreads(); ++i) {
        delete (_contexts->back());
        _contexts->pop_back();
    }
    delete ((ShuffleThreadContext *) (_contexts->back()));
    delete (_contexts);
    _contexts = nullptr;

    // delete all global variables
    delete (_gv);

}

std::vector<ThreadContext *> *JobContext::getContexts() {
    return _contexts;
}

pthread_mutex_t *JobContext::getWaitForJobMutex() {
    return _gv->getWaitForJobMutex();
}

pthread_cond_t *JobContext::getWaitForJobCv() {
    return _gv->getWaitForJobCv();
}

void JobContext::setTerminateFlagToTrue() {
    _gv->setTerminateFlagToTrue();
}

std::vector <pthread_t> *JobContext::getThreads() {
    return _gv->getThreads();
}
