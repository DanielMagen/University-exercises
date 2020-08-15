#ifndef IDDD_IDMANAGER_H
#define IDDD_IDMANAGER_H

#include <vector>

class IdManager {

private:
    /**
     * the list will hold a list of ranges of the form [a,b],[c,d],[e,f],...
     * in order to save space declaring useless lists the ranges will be held
     * consecutively as such: a,b,c,d,e,f,...
     */
    std::vector<int> ranges; // was unsigned long

    int _maxLength; // this will hold the max id that can be given
    // was unsigned long

    /**
     * uses a binary insertion algorithm
     * @param idToInsert an id number to insert
     * @return the index of the number inserted
     */
    unsigned long insertIdIntoRanges(int idToInsert); //was unsigned long

public:
    /**
     * a constructor for the class
     * @param maxNumberOfThreads the maximum number of possible threads
     */
    IdManager(int maxNumberOfThreads);

    /**
     * @return a new available id number for
     * @throws invalid_argument if the there are no available ids
     */
    int getNewId(); // was unsigned long

    /**
     * returns the id back into the list of available ids
     * @param idReturned
     * @throws invalid_argument if the id is greater than allowed
     */
    void giveIdBack(int idReturned); // was unsgined long
};


#endif //IDDD_IDMANAGER_H
