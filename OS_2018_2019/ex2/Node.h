#ifndef EX2_NODE_H
#define EX2_NODE_H

/**
 * an implementation of a "Node" object. Used by the class "LinkedList"
 */
class Node {
private:
    int _data;
    Node *_prev;
    Node *_next;
public:
    /**
     * A default constructor
     */
    Node();

    /**
     * A default constructor
     * @param data- The data
     */
    Node(int data);

    /**
     * A constructor
     * @param data- The data
     * @param next- The next thread
     */
    Node(int data, Node *next);

    /**
     * A constructor
     * @param data- The data
     * @param next- The next thread
     * @param prev- The previous thread
     */
    Node(int data, Node *prev, Node *next);

    /**
     * @return- This node's data
     */
    int getData();

    /**
     * Sets the node's data
     * @param newData- The new data
     */
    void setData(int newData);

    /**
     * @return- This node's prev
     */
    Node *getPrev();

    /**
     * Sets the node's data
     * @param newData- The new data
     */
    void setPrev(Node *newNext);

    /**
     * @return- This node's next
     */
    Node *getNext();

    /**
     * Sets the node's prev
     * @param newData- The new prev
     */
    void setNext(Node *newPrev);
};

#endif //EX2_NODE_H