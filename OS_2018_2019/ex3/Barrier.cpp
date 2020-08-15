#include "Barrier.h"
#include <cstdlib>
#include <cstdio>
#include <string>
#include <iostream>


Barrier::Barrier(int numThreads) : count(0), numThreads(numThreads) {
    mutex = new pthread_mutex_t(PTHREAD_MUTEX_INITIALIZER);
//    exitInCaseOfFailure(pthread_mutex_init(mutex, nullptr), FAILURE_MSG_MUTEX_INIT);

    cvForShuffleThread = new pthread_cond_t(PTHREAD_COND_INITIALIZER);
//    exitInCaseOfFailure(pthread_cond_init(cvForShuffleThread, nullptr), FAILURE_MSG_COND_INIT);

    cvForNonShuffleThread = new pthread_cond_t(PTHREAD_COND_INITIALIZER);
//    exitInCaseOfFailure(pthread_cond_init(cvForNonShuffleThread, nullptr), FAILURE_MSG_COND_INIT);
}


Barrier::~Barrier() {
    if (pthread_mutex_destroy(mutex) != SUCCESS) {
        std::cerr << ERROR_MSG_DESTROY_MUTEX << '\n';
    }
    delete (mutex);

    if (pthread_cond_destroy(cvForShuffleThread) != SUCCESS) {
        std::cerr << ERROR_MSG_DESTROY_COND_MUTEX << '\n';
    }
    delete (cvForShuffleThread);

    if (pthread_cond_destroy(cvForNonShuffleThread) != SUCCESS) {
        std::cerr << ERROR_MSG_DESTROY_COND_MUTEX << '\n';
    }

    delete (cvForNonShuffleThread);
}


int Barrier::barrier(int threadId) {

    if (pthread_mutex_lock(mutex) != SUCCESS) {
        return LOCK_FAILURE;
    }
    if (++count < numThreads) {
        if (threadId == 0) {
            if (pthread_cond_wait(cvForShuffleThread, mutex) != SUCCESS) {
                return WAIT_FAILURE;
            }
        } else {
            if (pthread_cond_wait(cvForNonShuffleThread, mutex) != SUCCESS) {
                return WAIT_FAILURE;
            }
        }

    } else {
        count = 0;
        if (pthread_cond_broadcast(cvForNonShuffleThread) != SUCCESS) {
            return BROADCAST_FAILURE;
        }
        if (pthread_cond_broadcast(cvForShuffleThread) != SUCCESS) {
            return BROADCAST_FAILURE;
        }
    }
    if (pthread_mutex_unlock(mutex) != SUCCESS) {
        return UNLOCK_FAILURE;
    }

    return SUCCESS;
}
