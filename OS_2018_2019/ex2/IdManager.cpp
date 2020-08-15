//
// Created by  on 3/28/19.
//

#include "IdManager.h"
#include <iostream> //////////////////////////////////////////////////////////// delete iostream

/**
 * uses a binary insertion algorithm
 * @param idToInsert an id number to insert
 * @return the index of the number inserted
 */
unsigned long IdManager::insertIdIntoRanges(int idToInsert) //was unsigned long
{
    unsigned long start = 0; //was unsigned long
    unsigned long end = ranges.size(); // the start of the last range //was unsigned long
    unsigned long toCheck = 0; //was unsigned long

    // use binary search to find the needed location for the id returned
    while (start + 1 < end) {
        toCheck = (start + end) / 2;
        if (ranges[toCheck] > idToInsert) {
            end = toCheck;
        } else {
            start = toCheck;
        }
    }

    // the end variable will hold the location to push the new range
    // make sure it is a valid starting location (a valid one is divisible by 2)
    if (end % 2 != 0) {
        --end;
    }

    // now push the "range" [id, id+1] to the vector
    auto insertLocation = ranges.begin();
    insertLocation += end;
    insertLocation = ranges.insert(insertLocation, idToInsert);

    ++insertLocation;
    ranges.insert(insertLocation, idToInsert + 1);

    return end;
}

/**
 * a constructor for the class
 * @param maxNumberOfThreads the maximum number of possible threads
 */
IdManager::IdManager(int maxNumberOfThreads) // was unsigned long
{
    _maxLength = maxNumberOfThreads;
    ranges.push_back(0);
    ranges.push_back(_maxLength);
}

/**
 * @return a new available id number for
 * @throws invalid_argument if the there are no available ids
 */
int IdManager::getNewId() { // was unsigned long

    if (ranges.empty()) {
        throw std::invalid_argument("there are no available ids");
    }

    int toReturn = ranges[0]; // was unsigned long;
    ++ranges[0];
    if (ranges[0] == ranges[1]) {
        auto rangeLocation = ranges.begin();
        ranges.erase(rangeLocation);
        ranges.erase(rangeLocation);
    }

    return toReturn;
}

/**
 * returns the id back into the list of available ids
 * @param idReturned
 * @throws invalid_argument if the id is greater than allowed
 */
void IdManager::giveIdBack(int idReturned) // was unsigned long
{
    // if the id is greater than _maxLength its not valid
    if (idReturned >= _maxLength) {
        throw std::invalid_argument("the id was never given");
    }

    unsigned long index = insertIdIntoRanges(idReturned);

    // now check if the range inserted can be merged into adjacent ranges
    auto rangeLocation = ranges.begin();
    rangeLocation += index;

    // check if the range can be merged backwards
    if (index > 0) {
        if (ranges[index] == ranges[index - 1]) {
            ranges[index - 1] = ranges[index + 1];
            ranges.erase(rangeLocation);
            ranges.erase(rangeLocation);
            // update index and rangeLocation
            --index;
            --index;
            --rangeLocation;
            --rangeLocation;
        }
    }

    // now check if the range can be merged forwards
    // go to the end of the range
    ++index;
    ++rangeLocation;

    if (index < ranges.size() - 1) {
        if (ranges[index] == ranges[index + 1]) {
            ranges[index + 1] = ranges[index - 1];
            --rangeLocation;
            ranges.erase(rangeLocation);
            ranges.erase(rangeLocation);
        }
    }

}