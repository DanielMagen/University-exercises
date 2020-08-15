#include "Thread.h"
#include <iostream>

#ifdef __x86_64__
/* code for 64 bit Intel arch */

typedef unsigned long address_t;
#define JB_SP 6
#define JB_PC 7

/* A translation is required when using an address of a variable.
   Use this as a black box in your code. */
address_t translate_address(address_t addr)
{
    address_t ret;
    asm volatile("xor    %%fs:0x30,%0\n"
                 "rol    $0x11,%0\n"
    : "=g" (ret)
    : "0" (addr));
    return ret;
}

#else
/* code for 32 bit Intel arch */

typedef unsigned int address_t;
#define JB_SP 4
#define JB_PC 5

/* A translation is required when using an address of a variable.
   Use this as a black box in your code. */
address_t translate_address(address_t addr) {
    address_t ret;
    asm volatile("xor    %%gs:0x18,%0\n"
                 "rol    $0x9,%0\n"
    : "=g" (ret)
    : "0" (addr));
    return ret;
}

#endif

/**
 * A constructor
 * @param f- The code that this thread is going to perform
 * @param id- The thread's id
 * @param stackSize- The of the stack
 * @param readyNode- A node that is the current tail of the "readyList" in "uthread"
 */
Thread::Thread(void (*f)(void), int id, int stackSize, Node *readyNode) : _tid(id) {
    _state = READY;
    _nodeInReadyList = readyNode;
    _runningTime = 0;

    _stack = new char[stackSize];
    address_t sp, pc;

    sp = (address_t) _stack + STACK_SIZE - sizeof(address_t);
    pc = (address_t) f;
    sigsetjmp(_context, 1);
    (_context->__jmpbuf)[JB_SP] = translate_address(sp);
    (_context->__jmpbuf)[JB_PC] = translate_address(pc);
    sigemptyset(&_context->__saved_mask);


}

/**
* @return- This thread's id
*/
int Thread::getID() const {
    return _tid;
}

/**
 * @return- This thread's context
 */
sigjmp_buf &Thread::getContext() {
    return _context;
}

/**
 * adds this thread's node to the "readyList" in "uthread"
 * @param readyList The "readyList"
 * @return- 0 on success. -1 otherwise
 */
int Thread::addToReadyList(LinkedList *readyList) {
    int resultFromTryingToSetToReady = setToReady();
    if (resultFromTryingToSetToReady == SUCCESS) {
        _nodeInReadyList = readyList->push(_tid);
    }
    return resultFromTryingToSetToReady;
}

/**
 * Removes this thread's node from the "readyList" in "uthread"
 * @param deleteNodeFrom- The "readyList"
 * @param newState- The state we're gonna put this thread's node in
 * @return- 0 on success. -1 otherwise
 */
int Thread::deleteFromReadyList(LinkedList *deleteNodeFrom, int newState) {
    if (_state != READY) {
        return FAILURE;
    }
    if (_nodeInReadyList == nullptr) {
        return FAILURE;
    }

    int result = deleteNodeFrom->erase(_nodeInReadyList);
    _nodeInReadyList = nullptr;

    _state = newState;
    return result;
}

/**
 * Sets the state to READY
 * @return 0 on success. -1 otherwise
 */
int Thread::setToReady() {
    if (_state != SLEEPING and _state != SLEEPING_AND_BLOCKED) {
        _state = READY;
        return SUCCESS;
    }
    return FAILURE;

}


/**
 * Sets the state to RUNNING
 * @return 0 on success. -1 otherwise
 */
int Thread::setToRunning() {
    if (_state != SLEEPING and _state != BLOCKED and _state != SLEEPING_AND_BLOCKED) {
        _state = RUNNING;
        return SUCCESS;
    }
    return FAILURE;
}

/**
 * Sets the state to BLOCKED
 * @return 0 on success. -1 otherwise
 */
int Thread::setToBlocked() // Assumes that this thread is not currently running
{
    if (_tid == 0) {
        return FAILURE;
    }

    if (_state == READY) {
        return FAILURE;
    }

    if (_state == SLEEPING) {
        _state = SLEEPING_AND_BLOCKED;
    } else {
        _state = BLOCKED;
    }

    return SUCCESS;

}

/**
 * Sets the state to SLEEP
 * @return 0 on success. -1 otherwise
 */
int Thread::setToSleep() {
    if (_tid != 0) {
        if (_state != BLOCKED) {
            _state = SLEEPING;
        } else {
            _state = SLEEPING_AND_BLOCKED;
        }
        return SUCCESS;
    }
    return FAILURE;
}

/**
 * @return- This thread's node
 */
Node *Thread::getNode() {
    return _nodeInReadyList;
}

/**
 * A destructor
 */
Thread::~Thread() {
    delete[] _stack;
}

/**
 * @return- This thread's state
 */
int Thread::getState() {
    return _state;
}

/**
 * Increases the running time of this thread
 * @param increaseBy- The amount of time we'd like to increase by
 */
void Thread::increaseRunningTimeBy(int increaseBy) {
    _runningTime += increaseBy;
}

/**
 * @return- This thread's running time
 */
int Thread::getRunningTime() {
    return _runningTime;
}

int Thread::removeFromSleep(LinkedList *readyList) {
    if (_state == SLEEPING_AND_BLOCKED) {
        _state = BLOCKED;
        return SUCCESS;
    } else if (_state == SLEEPING) {
        _state = READY;
        _nodeInReadyList = readyList->push(_tid);
        return SUCCESS;
    }
    return FAILURE;
}




