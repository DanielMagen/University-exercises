#ifndef BARRIER_H
#define BARRIER_H

#include <pthread.h>

#define LOCK_FAILURE -3
#define WAIT_FAILURE -4
#define BROADCAST_FAILURE -5
#define UNLOCK_FAILURE -6
#define SUCCESS 0

#define ERROR_MSG_DESTROY_MUTEX "Barrier error: could not destroy mutex"
#define ERROR_MSG_DESTROY_COND_MUTEX "Barrier error: could not destroy cond"
#define FAILURE_MSG_MUTEX_INIT "Barrier error: could not init new mutex"
#define FAILURE_MSG_COND_INIT "Barrier error: could not init new cv"

/**
 * This class represents a "barrier" principle. It makes sure all threads had passed the "Sort"
 * stage
 */
class Barrier {
public:

    /**
     * A constructor
     * @param numThreads- The number of threads
     */
    Barrier(int numThreads);

    /**
     * A destructor
     */
    ~Barrier();

    /**
     * Inserts a thread into this barrier
     * @param threadId- The thread's id
     * @return 0 if the process had succeeded. Some matching failure value otherwise
     */
    int barrier(int threadId);

private:
    /**
     * A mutex for reaching inside the barrier
     */
    pthread_mutex_t *mutex;
    /**
     * A cv that is in charge of thread 0
     */
    pthread_cond_t *cvForShuffleThread;
    /**
     * A cv that is in charge of the rest of the threads
     */
    pthread_cond_t *cvForNonShuffleThread;
    /**
     * The current number of threads
     */
    int count;
    /**
     * THe number of threads
     */
    int numThreads;
};

#endif //BARRIER_H
