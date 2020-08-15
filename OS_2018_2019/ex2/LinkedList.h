#ifndef EX2_LINKED_LIST_H
#define EX2_LINKED_LIST_H

#include "Node.h"

#define FAILURE -1
#define SUCCESS 0

/**
 * An implementation to the abstract data struture "doubly linked list"
 */
class LinkedList {
private:
    Node *_head;
    Node *_tail;

public:
    /**
     * A default constructor
     */
    LinkedList();

    /**
     * Erases a node from the list
     * @param toDelete- The node we'd like to remove
     * @return- 0 on success, -1 otherwise
     */
    int erase(Node *toDelete);

    /**
     * @return- The list's head
     */
    Node *getHead();

    /**
     * @return- The list's tail
     */
    Node *getTail();

    /**
     * Pops the list's head
     * @return- the head data
     */
    int pop();

    /**
     * Pushes a new node to the back (the tail) of  the list
     * @return- The tail
     */
    Node *push(int newElem);

    /**
     * @return- true for empty, false otherwise
     */
    bool isEmpty();

    /**
     * A destructor
     */
    ~LinkedList(); // doooooo
};

#endif //EX2_LINKED_LIST_H
