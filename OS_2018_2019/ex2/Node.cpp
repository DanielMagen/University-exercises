#include "Node.h"

/**
 * A default constructor
 */
Node::Node() : _data(0), _prev(nullptr), _next(nullptr) {}

/**
 * A default constructor
 * @param data- The data
 */
Node::Node(int data, Node *prev, Node *next) :
        _data(data), _prev(prev), _next(next) {}

/**
 * A constructor
 * @param data- The data
 * @param next- The next thread
 */
Node::Node(int data, Node *next) :
        _data(data), _prev(nullptr), _next(next) {}

/**
* A constructor
* @param data- The data
* @param next- The next thread
* @param prev- The previous thread
*/
Node::Node(int data) : _data(data), _prev(nullptr), _next(nullptr) {}

/**
 * @return- This node's data
 */
int Node::getData() {
    return _data;
}

/**
 * Sets the node's data
 * @param newData- The new data
 */
void Node::setData(int newData) {
    _data = newData;
}

/**
 * @return- This node's prev
 */
Node *Node::getPrev() {
    return _prev;
}

/**
 * Sets the node's prev
 * @param newData- The new prev
 */
void Node::setNext(Node *newNext) {
    _next = newNext;
}

/**
 * @return- This node's next
 */
Node *Node::getNext() {
    return _next;
}

/**
 * Sets the node's prev
 * @param newData- The new prev
 */
void Node::setPrev(Node *newPrev) {
    _prev = newPrev;
}



