#include "VirtualMemory.h"
#include "PhysicalMemory.h"

#define SUCCESS 1
#define FAILURE 0

#define START_DEPTH 1
#define ROOT_TABLE_FRAME_NUMBER 0
#define LOWEST_LEVEL_IN_PAGE_TREE 1
#define TYPE_WORD_NOT_AVAILABLE (word_t(-1))
#define TYPE_UNIT_NOT_AVAILABLE (uint64_t(-1))

#define DFS_MET_TYPE_1 2
#define DFS_MET_TYPE_3 3
#define DFS_FOUND_MATCH 4
#define DID_NOT_FOUND_MATCH 5
#define FINISHED_DFS 6

typedef uint64_t pageNumber;
typedef word_t frameNumber;


/**
 * Fills all the entries in the table with 0
 * @param frameIndex- The frame
 */
void clearTable(uint64_t frameIndex) {
    for (uint64_t i = 0; i < PAGE_SIZE; ++i) {
        PMwrite(frameIndex * PAGE_SIZE + i, 0);
    }
}


/**
 * Initializes a new table
 */
void VMinitialize() {
    clearTable(ROOT_TABLE_FRAME_NUMBER);
}

/**
 * An implementation of the 'math.pow(2, x)' function
 * @param pow- The number we'd like to raise 2 bty
 * @return- 2^pow
 */
pageNumber get2ToPower(int pow) {
    if (pow == 0) {
        return 1;
    }

    pageNumber result = 1;
    for (int i = 0; i < pow; ++i) {
        result *= 2;
    }

    return result;
}

/**
 * @param virtualAddress a full virtual address
 * @param currentDepth the current level in the page table tree
 * @return the relavent part of the address
 */
uint64_t getRelevantPartOfAddress(uint64_t virtualAddress, unsigned int currentDepth) {
    int moveBy = (TABLES_DEPTH - currentDepth + 1) * OFFSET_WIDTH;
    virtualAddress = virtualAddress >> moveBy;
    if (currentDepth == LOWEST_LEVEL_IN_PAGE_TREE) {
        return virtualAddress;
    }

    // else get the last OFFSET_WIDTH bits
    pageNumber modulo = get2ToPower(OFFSET_WIDTH); // will help get the last OFFSET_WIDTH digits
    return virtualAddress % modulo;
}

/**
 * @param virtualAddress- The page's virtual address
 * @return The page's number
 */
pageNumber getPageNumberInVirtualForAddress(uint64_t virtualAddress) {
    return virtualAddress / PAGE_SIZE; ///////////////////// check for types correction
}

/**
 * @param table- The 'parent' frame
 * @param offsetForTable- The page's offset in it's parent's table
 * @return The required address
 */
uint64_t getAddressByFrameNumberAndOffset(frameNumber table, uint64_t offsetForTable) {
    return (table * PAGE_SIZE) + offsetForTable;
}


/**
 * @return Number Of Pages In the Virtual Memory
 */
pageNumber getNumberOfPagesInVirtualMemory() {
    return get2ToPower(VIRTUAL_ADDRESS_WIDTH - OFFSET_WIDTH);
}

/**
 * @param a a pageNumber
 * @param b a pageNumber
 * @return the cyclical distance between them
 */
pageNumber getCyclicalDistance(pageNumber a, pageNumber b) {
    pageNumber straightDistance = a - b;
    if (b > a) {
        straightDistance = b - a;
    }
    pageNumber cyclicalDistance = getNumberOfPagesInVirtualMemory() - straightDistance;

    if (straightDistance < cyclicalDistance) {
        return straightDistance;
    }
    return cyclicalDistance;
}

/**
 * @param frameNumberType1Parent - The parent frame number of the Type1 that was found
 * (if was actually found)
 * @param indexOfType1InItsParent - The index of type1 that we found during the DFS
 * @param maxFrameNumberMet - The Frame with the biggest index that we had so far encountered
 * @param frameNumberType3 - The frame of type3 that we found during the DFS
 * @param frameNumberType3Parent- The parent of the frame of type3 that we found during the DFS
 * @param indexOfType3InItsParent - The index of type3 that we found during the DFS
 * @param currentFrameNumber - The base address of the frame we currently use
 * @param currentDepth - The current depth
 * @param leafDepth - The depth of the leaves
 * @param doNotChangePageFrameNumber - The parent frame of that we would like to store
 * (we should not change that)
 * @param pageNumberInVirtualOfInput - the page number of the address
 * @return That the process was finished
 */
int runDFS(frameNumber *frameNumberType1Parent,
           uint64_t *indexOfType1InItsParent,
           frameNumber *maxFrameNumberMet,
           pageNumber *pageNumberType3,
           frameNumber *frameNumberType3Parent,
           uint64_t *indexOfType3InItsParent,
           frameNumber currentFrameNumber,
           unsigned int currentDepth,
           unsigned int leafDepth,
           frameNumber doNotEvictFrameNumber,
           pageNumber pageNumberInVirtualOfInput,
           uint64_t addressByPath) {

    frameNumber nextFrameNumber = 0;
    bool currentFrameIsType1 = true;
    int resultFromDfs = 0;


    if (currentFrameNumber > *maxFrameNumberMet) {
        *maxFrameNumberMet = currentFrameNumber;
    }


    // this will save the virtual address up to the parent frame
    // this will be used to reconstruct the page number
    addressByPath = addressByPath << OFFSET_WIDTH;

    // if got to a leaf frame
    if (currentDepth == leafDepth) {
        // we got to a "leaf" frame we need to check if its cyclical distance is minimal
        pageNumber currentPageNumberInVirtual = getPageNumberInVirtualForAddress(addressByPath);

        if (*pageNumberType3 == TYPE_UNIT_NOT_AVAILABLE) {
            *pageNumberType3 = currentPageNumberInVirtual;
            return DFS_MET_TYPE_3;
        } else {
            // check if the current page is cyclically further from the page we want to insert
            pageNumber distanceOfCurrentType3 = getCyclicalDistance(*pageNumberType3,
                                                                    pageNumberInVirtualOfInput);
            pageNumber distanceOfCurrentFrame = getCyclicalDistance(currentPageNumberInVirtual,
                                                                    pageNumberInVirtualOfInput);

            if (distanceOfCurrentType3 < distanceOfCurrentFrame) {
                *pageNumberType3 = currentPageNumberInVirtual;
                return DFS_MET_TYPE_3;
            } else {
                return FINISHED_DFS;
            }
        }
    }

    for (uint64_t offset = 0; offset < PAGE_SIZE; ++offset) {
        PMread((currentFrameNumber * PAGE_SIZE) + offset, &nextFrameNumber);
        if (nextFrameNumber != 0) {
            currentFrameIsType1 = false;

            resultFromDfs = runDFS(frameNumberType1Parent,
                                   indexOfType1InItsParent,
                                   maxFrameNumberMet,
                                   pageNumberType3,
                                   frameNumberType3Parent,
                                   indexOfType3InItsParent,
                                   nextFrameNumber,
                                   currentDepth + 1,
                                   leafDepth,
                                   doNotEvictFrameNumber,
                                   pageNumberInVirtualOfInput,
                                   addressByPath);

            switch (resultFromDfs) {
                case DFS_FOUND_MATCH:
                    return DFS_FOUND_MATCH;
                case DFS_MET_TYPE_1:
                    // the frame we just run on is of type 1
                    // update the values accordingly
                    *frameNumberType1Parent = currentFrameNumber;
                    *indexOfType1InItsParent = offset;
                    return DFS_FOUND_MATCH;
                case DFS_MET_TYPE_3:
                    // the frame we just run on is of type 1
                    // update the values accordingly
                    *frameNumberType3Parent = currentFrameNumber;
                    *indexOfType3InItsParent = offset;
                default:
                    break;
            }
        }

        addressByPath += 1;

    }

    // assuming that we can touch "donottouch" sons but not himself
    if (currentFrameNumber == doNotEvictFrameNumber) {
        return DID_NOT_FOUND_MATCH;
    }

    if (currentFrameIsType1) {
        return DFS_MET_TYPE_1;
    }

    return FINISHED_DFS;

}


/**
 * Clears a table (a frame)
 * @param fn- The frame we'd like to fill with 0s
 * @return SUCCESS for succeeding
 */
int writeZeroInAllOfFrame(frameNumber fn) {
    uint64_t currentAddress = fn * PAGE_SIZE;
    for (uint64_t i = 0; i < PAGE_SIZE; ++i) {
        PMwrite(currentAddress, ROOT_TABLE_FRAME_NUMBER);
        currentAddress += 1;
    }

    return SUCCESS;
}


/**
 * this method will go over all frames and find the best one to set value to
 * types of frames are:
 * type 1) a frame containing an empty table
 * type 2) an unused frame
 * type 3) the frame furthest from you
 * @param value - a pointer to a word_t number that will be set to have the
 * next available frame number
 * @param doNotChangePageFrameNumber - a frame number which must not be evicted while looking
 * for a frame
 * @param pageNumberInVirtual - the page number of the address
 * @return SUCCESS for success and FAILURE otherwise
 */
int setValueToNextAvailableFrameNumber(word_t *value,
                                       frameNumber doNotEvictFrameNumber,
                                       pageNumber pageNumberInVirtual,
                                       uint64_t offsetInFather) {

    frameNumber frameNumberType1Parent = TYPE_WORD_NOT_AVAILABLE;
    uint64_t indexOfType1InItsParent = 0;
    frameNumber maxFrameNumberMet = TYPE_WORD_NOT_AVAILABLE;
    pageNumber pageNumberType3 = TYPE_UNIT_NOT_AVAILABLE;
    frameNumber frameNumberType3Parent = TYPE_WORD_NOT_AVAILABLE;
    uint64_t indexOfType3InItsParent = 0;

    runDFS(&frameNumberType1Parent,
           &indexOfType1InItsParent,
           &maxFrameNumberMet,
           &pageNumberType3,
           &frameNumberType3Parent,
           &indexOfType3InItsParent,
           ROOT_TABLE_FRAME_NUMBER,
           START_DEPTH,
           TABLES_DEPTH + 1,
           doNotEvictFrameNumber,
           pageNumberInVirtual,
           ROOT_TABLE_FRAME_NUMBER);

    // check if met type1
    if (frameNumberType1Parent != TYPE_WORD_NOT_AVAILABLE) {
        PMread(getAddressByFrameNumberAndOffset(frameNumberType1Parent,
                                                indexOfType1InItsParent),
               value);
        PMwrite(getAddressByFrameNumberAndOffset(frameNumberType1Parent,
                                                 indexOfType1InItsParent),
                ROOT_TABLE_FRAME_NUMBER);

        // now insert the evicted frame into its new parent
        PMwrite(getAddressByFrameNumberAndOffset(doNotEvictFrameNumber,
                                                 offsetInFather), *value);

        return SUCCESS;
    }

    // check if type2 available
    if (maxFrameNumberMet != TYPE_WORD_NOT_AVAILABLE) {
        if (maxFrameNumberMet + 1 < NUM_FRAMES) {
            *value = maxFrameNumberMet + 1;
            writeZeroInAllOfFrame(*value);

            // Updating the parent's relevant entry
            PMwrite(getAddressByFrameNumberAndOffset(doNotEvictFrameNumber, offsetInFather),
                    *value);
            return SUCCESS;
        }
    }

    // check if type3 available
    if (frameNumberType3Parent != TYPE_WORD_NOT_AVAILABLE) {
        word_t type3Frame = 0;
        PMread(getAddressByFrameNumberAndOffset(frameNumberType3Parent, indexOfType3InItsParent),
               &type3Frame);

        *value = type3Frame;

        PMevict(uint64_t(type3Frame), pageNumberType3);
        PMwrite(getAddressByFrameNumberAndOffset(frameNumberType3Parent,
                                                 indexOfType3InItsParent),
                ROOT_TABLE_FRAME_NUMBER);
        writeZeroInAllOfFrame(*value);

        // now insert the evicted frame into its new parent
        PMwrite(getAddressByFrameNumberAndOffset(doNotEvictFrameNumber,
                                                 offsetInFather), type3Frame);

        return SUCCESS;
    }

    return FAILURE;

}

/**
 *
 * @param virtualAddress - The virtual address
 * @param physicalAddressOfLine - a pointer to a uint64_t number
 * the function will change its value to be the physical address of the address given
 * @return SUCCESS for SUCCESS, FAILURE otherwise
 */
int VMAction(uint64_t virtualAddress, uint64_t *physicalAddressOfLine) {
    if (virtualAddress > VIRTUAL_MEMORY_SIZE) {
        return FAILURE;
    }

    frameNumber currentFrameNumber = ROOT_TABLE_FRAME_NUMBER; // the base of the current page table
    frameNumber tmpFrameNumber = 0;
    pageNumber pageNumberInVirtual = getPageNumberInVirtualForAddress(virtualAddress);
    bool encounteredZero = false;

    for (unsigned int currentDepth = LOWEST_LEVEL_IN_PAGE_TREE;
         currentDepth < TABLES_DEPTH + 1;
         ++currentDepth) {
        uint64_t offsetForCurrentPage = getRelevantPartOfAddress(virtualAddress,
                                                                 currentDepth);
        PMread(getAddressByFrameNumberAndOffset(currentFrameNumber,
                                                offsetForCurrentPage),
               &tmpFrameNumber);
        if (tmpFrameNumber == 0) {
            // we should get a new frame for the next level in the tree
            encounteredZero = true;
            setValueToNextAvailableFrameNumber(&tmpFrameNumber,
                                               currentFrameNumber,
                                               pageNumberInVirtual,
                                               getRelevantPartOfAddress(virtualAddress, currentDepth));
        }
        currentFrameNumber = tmpFrameNumber;
    }

    if (encounteredZero) {
        // we need to restore the value of the page
        PMrestore((uint64_t) currentFrameNumber, pageNumberInVirtual);
    }

    *physicalAddressOfLine = getAddressByFrameNumberAndOffset(currentFrameNumber,
                                                              getRelevantPartOfAddress(virtualAddress,
                                                                                       TABLES_DEPTH + 1));

    return SUCCESS;

}


/**
 * Given a virtual address, reads the value that is stored there
 * @param virtualAddress- The virtual address
 * @param value- a pointer to a word_t number
 * the value in the address given will be save to it
 * @return SUCCESS for SUCCESS, FAILURE otherwise
 */
int VMread(uint64_t virtualAddress, word_t *value) {
    uint64_t physicalAddressOfLine = 0;

    int result = VMAction(virtualAddress, &physicalAddressOfLine);
    if (result == FAILURE) {
        return FAILURE;
    }

    PMread(physicalAddressOfLine, value);

    return SUCCESS;
}


/**
 * Given a virtual address, reads the value that is stored there
 * @param virtualAddress- The virtual address
 * @param value- a to a word_t number
 * the value will be written to the address given
 * @return SUCCESS for SUCCESS, FAILURE otherwise
 */
int VMwrite(uint64_t virtualAddress, word_t value) {
    uint64_t physicalAddressOfLine = 0;

    int result = VMAction(virtualAddress, &physicalAddressOfLine);
    if (result == FAILURE) {
        return FAILURE;
    }

    PMwrite(physicalAddressOfLine, value);

    return SUCCESS;
}