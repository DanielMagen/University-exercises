#include "LinkedList.h"

/**
 * Pushes a new node to the back (the tail) of  the list
 * @return- The tail
 */
Node *LinkedList::push(int newElem) {
    if (_head == nullptr) {
        _head = new Node(newElem);
        _tail = _head;
        return _head;
    }

    _tail->setPrev(new Node(newElem));
    _tail->getPrev()->setNext(_tail);
    _tail = _tail->getPrev();
    return _tail;
}

/**
 * A default constructor
 */
LinkedList::LinkedList() : _head(nullptr), _tail(nullptr) {}

/**
 * Erases a node from the list
 * @param toDelete- The node we'd like to remove
 * @return- 0 on success, -1 otherwise
 */
int LinkedList::erase(Node *toDelete) {
    if (toDelete == nullptr) {
        return SUCCESS;
    }

    if (_head == toDelete) {
        if (_tail == toDelete) {
            delete _head;
            _head = nullptr;
            _tail = nullptr;
            return SUCCESS;
        }
        _head = _head->getPrev();
        delete _head->getNext();
        _head->setNext(nullptr);
        return SUCCESS;
    }

    if (_tail == toDelete) {
        _tail = _tail->getNext();
        delete _tail->getPrev();
        _tail->setPrev(nullptr);
        return SUCCESS;
    }
    toDelete->getPrev()->setNext(toDelete->getNext());
    toDelete->getNext()->setPrev(toDelete->getPrev());
    delete toDelete;
    return SUCCESS;
}

/**
 * @return- The list's head
 */
Node *LinkedList::getHead() {
    return _head;
}

/**
 * @return- The list's tail
 */
Node *LinkedList::getTail() {
    return _tail;
}

/**
 * Pops the list's head
 * @return- the head data
 */
int LinkedList::pop() {
    int toReturn = _head->getData();
    erase(_head);
    return toReturn;

}

/**
 * @return- true for empty, false otherwise
 */
bool LinkedList::isEmpty() {
    return _head == nullptr;
}

/**
 * A destructor
 */
LinkedList::~LinkedList() {
    Node *temp = _head;
    while (temp != nullptr) {
        temp = temp->getNext();
        delete temp->getPrev();
    }
}

