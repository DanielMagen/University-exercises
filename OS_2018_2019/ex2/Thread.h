//
// Created by Admin on 03/04/2019.
//

#ifndef EX2_THREAD_H
#define EX2_THREAD_H

#include <stdio.h>
#include <setjmp.h>
#include <signal.h>
#include <unistd.h>
#include <sys/time.h>
#include "LinkedList.h"

#define RUNNING 1
#define READY 2
#define BLOCKED 3
#define SLEEPING 4
#define TERMINATED 5
#define SLEEPING_AND_BLOCKED 6


#define FAILURE -1
#define SUCCESS 0


#define STACK_SIZE 4096

class Thread {
private:
    int _tid;
    // The state the thread is in (READY, RUNNING, BLOCKED OR SLEEPED)
    int _state;
    // The memory that is for this thread only
    char *_stack;
    // The "screenshot" for this thread's context
    sigjmp_buf _context;
    // The representation of this thread in the readyList
    Node *_nodeInReadyList; // a pointer to the node in the ready list
    // The amount of quantas this thread has ran already
    int _runningTime;

public:
    /**
     * A constructor
     * @param f- The code that this thread is going to perform
     * @param id- The thread's id
     * @param stackSize- The of the stack
     * @param readyNode- A node that is the current tail of the "readyList" in "uthread"
     */
    Thread(void (*f)(void), int id, int stackSize, Node *readyNode);

    /**
     * Removes this thread's node from the "readyList" in "uthread"
     * @param deleteNodeFrom- The "readyList"
     * @param newState- The state we're gonna put this thread's node in
     * @return- 0 on success. -1 otherwise
     */
    int deleteFromReadyList(LinkedList *deleteNodeFrom, int newState);

    /**
     * adds this thread's node to the "readyList" in "uthread"
     * @param readyList The "readyList"
     * @return- 0 on success. -1 otherwise
     */
    int addToReadyList(LinkedList *readyList);

    /**
     * @return- This thread's id
     */
    int getID() const;

    /**
     * @return- This thread's state
     */
    int getState();

    /**
     * Sets the state to READY
     * @return 0 on success. -1 otherwise
     */
    int setToReady();

    /**
     * Sets the state to RUNNING
     * @return 0 on success. -1 otherwise
     */
    int setToRunning();

    /**
     * Sets the state to BLOCKED
     * @return 0 on success. -1 otherwise
     */
    int setToBlocked();

    /**
     * Sets the state to SLEEP
     * @return 0 on success. -1 otherwise
     */
    int setToSleep();

    int removeFromSleep(LinkedList *readyList);

    /**
     * @return- This thread's running time
     */
    int getRunningTime();

    /**
     * Increases the running time of this thread
     * @param increaseBy- The amount of time we'd like to increase by
     */
    void increaseRunningTimeBy(int increaseBy);

    /**
     * @return- This thread's context
     */
    sigjmp_buf &getContext();

    /**
     * @return- This thread's node
     */
    Node *getNode();

    /**
     * A destructor
     */
    ~Thread();

};


#endif //EX2_THREAD_H