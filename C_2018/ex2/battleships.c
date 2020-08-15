/**
 * @file battleships.c
 * @author Daniel Magen
 * @version 1.0
 *
 * @brief contains all the needed function to operate a battleships game
 *
 * @section DESCRIPTION
 * this file contains all needed implementations of the function that were given in
 * the battleships.h file
 *
 * Input  : none
 * Process: each function has its own process by which it helps to manage the game
 * Output : none
 */

// ------------------------------ includes ------------------------------
#include <stdio.h>
#include <stdlib.h>
#include <assert.h>
#include "battleships.h"

// -------------------------- const definitions -------------------------
#define AIRPLANE_CARRIER_LENGTH 5
#define PATROL_LENGTH 4
#define MISSILE_SHIP_LENGTH 3
#define SUBMARINE_LENGTH 3
#define DESTROYER_LENGTH 2

#define HIT_AND_MISS_SPOT_SYMBOL "o "
#define HIT_SUCCESS_SPOT_SYMBOL "x "
#define UNKNOWN_SPOT_SYMBOL "_ "

#define HORIZONTAL 1
#define VERTICAL (-1)
#define NO_ORIENTATION 2

// ------------------------------ functions -----------------------------
/**
 * @brief prints the board to the user
 * @param gameField a pointer to a Field object
 */
void printBoard(Field *gameField) {
    int **board = gameField->board;
    int size = gameField->size;

    // print first row
    printf(" ");
    for (int k = 0; k < size; ++k) {
        printf(",%d", (k + 1));
    }
    printf("\n");

    // print rest of board
    for (int i = 0; i < size; ++i) {
        char row = 'a' + i;
        printf("%c ", row);
        for (int j = 0; j < size; ++j) {
            if (board[i][j] == HIT_AND_MISS_SPOT_CODE) {
                printf(HIT_AND_MISS_SPOT_SYMBOL);
            } else if (board[i][j] == HIT_SUCCESS_SPOT_CODE) {
                printf(HIT_SUCCESS_SPOT_SYMBOL);
            } else {
                printf(UNKNOWN_SPOT_SYMBOL);
            }
        }
        printf("\n");
    }
}

/**
 * @brief fill tha array with random number up to "upTo", non inclusive
 * @param array an array of ints
 * @param lengthOfArray the length of the array
 * @param upTo fill tha array with random number up to this number
 * non inclusive
 */
static void fillArrayWithRandomInt(int *array, int lengthOfArray, int upTo) {
    static int seedInitialized = 0;
    if (!seedInitialized) {
        // random seed
        seedInitialized = 1;
    }

    for (int i = 0; i < lengthOfArray; ++i) {
        array[i] = rand() % upTo;
    }
}

/**
 * @brief checks if there is an open horizontal slot for a ship
 * @param gameField a pointer to a Field object
 * @param location an array of 2 integers representing a starting location
 * on the gameField board
 * @param lengthOfShip the length of the ship we want to place in the board
 * @return FAILURE_CODE if no open horizontal slot was found SUCCESS_CODE otherwise
 */
static int isHorizontalOpen(Field *gameField, const int *location, int lengthOfShip) {
    int **board = gameField->board;

    int failed = 0;
    for (int col = location[1]; (col - location[1]) < lengthOfShip; ++col) {
        if (col >= gameField->size || board[location[0]][col] != EMPTY_SPOT_CODE) {
            failed = 1;
            break;
        }
    }
    if (!failed) {
        return SUCCESS_CODE;
    }
    return FAILURE_CODE;
}

/**
 * @brief checks if there is an open vertical slot for a ship
 * @param gameField a pointer to a Field object
 * @param location an array of 2 integers representing a starting location
 * on the gameField board
 * @param lengthOfShip the length of the ship we want to place in the board
 * @return FAILURE_CODE if no open vertical slot was found SUCCESS_CODE otherwise
 */
static int isVerticalOpen(Field *gameField, const int *location, int lengthOfShip) {
    int **board = gameField->board;

    int failed = 0;
    for (int row = location[0]; (row - location[0]) < lengthOfShip; ++row) {
        if (row >= gameField->size || board[row][location[1]] != EMPTY_SPOT_CODE) {
            failed = 1;
            break;
        }
    }
    if (!failed) {
        return SUCCESS_CODE;
    }
    return FAILURE_CODE;

}

/**
 * @brief checks if there is an open horizontal or vertical slot for a ship
 * @param gameField a pointer to a Field object
 * @param location an array of 2 integers representing a starting location
 * on the gameField board
 * @param lengthOfShip the length of the ship we want to place in the board
 * @param orientation a pointer to an int representing the orientation of the ship
 * if an orientation with a free slot was found, it will be set to the correct orientation
 * @return FAILURE_CODE if no open slot was found SUCCESS_CODE otherwise
 */
static int isOpen(Field *gameField, int *location, int lengthOfShip, int *orientation) {
    int failed = 0;

    assert(HORIZONTAL != VERTICAL); // if not then the function is useless

    // we will use a random number to decide if we check if the vertical or horizontal
    // direction is checked first
    int randomNumber[1] = {0};
    fillArrayWithRandomInt(randomNumber, 1, 2);

    if (randomNumber[0] % 2) {
        // we check horizontal first
        failed = isHorizontalOpen(gameField, location, lengthOfShip);
        if (!failed) {
            *orientation = HORIZONTAL;
            return SUCCESS_CODE;
        }
        failed = isVerticalOpen(gameField, location, lengthOfShip);
        if (!failed) {
            *orientation = VERTICAL;
            return SUCCESS_CODE;
        }
        return FAILURE_CODE;
    }

    // else we check vertical first
    failed = isVerticalOpen(gameField, location, lengthOfShip);
    if (!failed) {
        *orientation = VERTICAL;
        return SUCCESS_CODE;
    }
    failed = isHorizontalOpen(gameField, location, lengthOfShip);
    if (!failed) {
        *orientation = HORIZONTAL;
        return SUCCESS_CODE;
    }
    return FAILURE_CODE;

}


/**
 * @brief this function signs the board in the location of the ship given with the given code
 * @param gameField a pointer to a Field object
 * @param ship a pointer to a Ship item with initialized length, location and orientation
 * @param previousCode the code that should be where we want to insert the ship to
 * @param codeToPut the code to insert into the ship location
 * @return FAILURE_CODE if there was a failure in the process SUCCESS_CODE otherwise
 */
static int insertCodeIntoShipLocation(Field *gameField, Ship *ship, int previousCode, int codeToPut) {
    int *location = ship->location;
    int length = ship->length;
    int **board = gameField->board;

    // inserts the code into the relevant slots in the board according to the ship orientation
    if (ship->orientation == HORIZONTAL) {
        for (int col = location[1]; (col - location[1]) < length; ++col) {
            if (col >= gameField->size || board[location[0]][col] != previousCode) {
                return FAILURE_CODE;
            }
            board[location[0]][col] = codeToPut;
        }
    } else if (ship->orientation == VERTICAL) {
        for (int row = location[0]; row < gameField->size && (row - location[0]) < length; ++row) {
            if (row >= gameField->size || board[row][location[1]] != previousCode) {
                return FAILURE_CODE;
            }
            board[row][location[1]] = codeToPut;
        }
    }

    return SUCCESS_CODE;
}

/**
 * @brief deletes a ship from the board
 * @param gameField a pointer to a Field object
 * @param ship a pointer to a Ship item with initialized length, location, orientation and code
 * @return FAILURE_CODE if there was a failure in the ship deletion SUCCESS_CODE otherwise
 */
static int deleteShip(Field *gameField, Ship *ship) {
    int result = insertCodeIntoShipLocation(gameField, ship, ship->code, EMPTY_SPOT_CODE);
    ship->orientation = NO_ORIENTATION;
    return result;
}

/**
 * @brief places a ship in the board
 * @param gameField a pointer to a Field object which has its ships initialized
 * @return FAILURE_CODE if there was a failure in the ship deletion SUCCESS_CODE otherwise
 */
static int placeShipsInField(Field *gameField) {

    Ship *ships = gameField->ships;
    int tries[NUMBER_OF_SHIPS] = {0}; // will hold how many times we tried to put each ship
    const int MAXIMUM_NUMBER_OF_TRIES = (gameField->size) * (gameField->size);
    // will try to randomly place item on board this many times before giving up
    // and go backwards


    // try placing all ships
    int i = 0;
    while (i < NUMBER_OF_SHIPS && i >= 0) {
        int randomLocation[DIMENSION_OF_BOARD] = {0};
        while (tries[i] < MAXIMUM_NUMBER_OF_TRIES) {
            ++tries[i];
            fillArrayWithRandomInt(randomLocation, DIMENSION_OF_BOARD, gameField->size);


            int shipOrientation = NO_ORIENTATION;
            if (isOpen(gameField, randomLocation, ships[i].length, &shipOrientation) ==
                SUCCESS_CODE) {
                // we found a place for the current ship
                ships[i].orientation = shipOrientation;
                for (int j = 0; j < DIMENSION_OF_BOARD; ++j) {
                    ships[i].location[j] = randomLocation[j];
                }
                insertCodeIntoShipLocation(gameField, &ships[i], EMPTY_SPOT_CODE, ships[i].code);

                i++; // now we move on to the next ship
                break;
            }
        }

        if (i < NUMBER_OF_SHIPS && tries[i] == MAXIMUM_NUMBER_OF_TRIES) {
            // we never found a place for the ship, we try to change the location
            // of the previous ship, but first we delete the previous ship from the board
            --i;
            if (i >= 0) {
                deleteShip(gameField, &ships[i]);
            } else {
                // we tried placing the first hip too many times and never found a position
                // that works
                break;
            }
        }
    }

    return SUCCESS_CODE;

}

/**
 * @brief converts an index in the ship list of the field to a ship code
 * @param index an index in the field array of ships
 * @return the ship code that corresponds to the ship at that index
 */
static int indexToShipCode(int index) {
    return SHIP_SPOT_CODE * (index + 1);
}

/**
 * @brief converts a ship code to an index in the ship list of the field
 * @param shipCode a ship code
 * @return the index in the field array of ships that corresponds to the ship code
 */
static int shipCodeToIndex(int shipCode) {
    return (shipCode / SHIP_SPOT_CODE) - 1;
}

/**
 * @brief initialize all ships in the game
 * @param gameField a pointer to a Field object
 */
static void initializeShips(Field *gameField) {
    static const int SHIP_LENGTHS[NUMBER_OF_SHIPS] =
            {
                    AIRPLANE_CARRIER_LENGTH,
                    PATROL_LENGTH,
                    MISSILE_SHIP_LENGTH,
                    SUBMARINE_LENGTH,
                    DESTROYER_LENGTH
            };

    Ship *ships = gameField->ships;
    for (int i = 0; i < NUMBER_OF_SHIPS; ++i) {
        Ship newShip = {0};
        newShip.length = SHIP_LENGTHS[i];
        newShip.orientation = NO_ORIENTATION;
        newShip.code = indexToShipCode(i);
        newShip.hits = 0;
        ships[i] = newShip;
    }

}

/**
 * @brief creates a new empty board with the size requested
 * @param sizeOfBoard the requested size of the board
 * @param failed a pointer to an int, will be set to NO_MEMORY_FOR_BOARD if failed
 * and SUCCESS_CODE if succeeded.
 * @return a 2d array of ints with the requested size.
 */
static int **createEmptyBoard(int sizeOfBoard, int *failed) {
    // creates a new board in the heap
    int **board = (int **) malloc((sizeof(int *)) * sizeOfBoard);
    if (board == NULL) {
        *failed = NO_MEMORY_FOR_BOARD;
        return board;
    }
    for (int i = 0; i < sizeOfBoard; ++i) {
        board[i] = (int *) malloc((sizeof(int)) * sizeOfBoard);
        if (board[i] == NULL) {
            *failed = NO_MEMORY_FOR_BOARD;
            return board;
        }
    }

    *failed = SUCCESS_CODE;

    // we initialize all slots to be EMPTY_SPOT_CODE
    for (int j = 0; j < sizeOfBoard; ++j) {
        for (int i = 0; i < sizeOfBoard; ++i) {
            board[j][i] = EMPTY_SPOT_CODE;
        }
    }

    return board;
}

/**
 * @brief initiates the game by creating a play field
 * @param sizeOfBoard the requested size of the board
 * @param failed a pointer to an int,
 * if succeeded will be set to SUCCESS_CODE
 * if given size is too big will be set to BAD_BOARD_SIZE
 * if no memory to create the board will be set to NO_MEMORY_FOR_BOARD
 * and SUCCESS_CODE if succeeded.
 * @return a new Field with the requested size of board
 */
Field startBoard(int sizeOfBoard, int *failed) {
    Field emptyField = {0}; // an empty board, in case something goes wrong we return it
    if (sizeOfBoard < MINIMUM_BOARD_SIZE) {
        *failed = BAD_BOARD_SIZE;
        return emptyField;
    }
    if (sizeOfBoard > MAXIMUM_BOARD_SIZE) {
        *failed = BAD_BOARD_SIZE;
        return emptyField;
    }

    // initiate the field
    Field gameField;
    gameField.size = sizeOfBoard;
    // initiate the board
    gameField.board = createEmptyBoard(sizeOfBoard, failed);

    if (*failed == NO_MEMORY_FOR_BOARD) {
        return emptyField;
    }

    // initiate the ships
    initializeShips(&gameField);
    *failed = placeShipsInField(&gameField);
    while (*failed == FAILURE_CODE) {
        // there is a chance that placement will fail
        // since we know that some placement must succeed
        // we call the function until it succeeds
        *failed = placeShipsInField(&gameField);
    }
    return gameField;
}

/**
 * @brief clears all the memory that was taken by the field
 * @param gameField a pointer to a Field object
 * should be called whenever the game is existed
 */
void exitBoard(Field *gameField) {
    int **board = gameField->board;
    for (int i = 0; i < gameField->size; ++i) {
        free(board[i]);
    }
    free(board);
    gameField->board = NULL;
}

/**
 * @brief checks if the location given is legal
 * @param gameField a pointer to a Field object
 * @param location an array of size
 * @return SUCCESS_CODE if location is legal and FAILURE_CODE otherwise
 */
static int locationLegal(Field *gameField, const int *location) {
    for (int i = 0; i < DIMENSION_OF_BOARD; ++i) {
        if (location[i] >= gameField->size || location[i] < 0) {
            return FAILURE_CODE;
        }
    }

    return SUCCESS_CODE;
}

/**
 * @brief returns the item in that location in the board
 * @param gameField a pointer to a Field object
 * @param location an array of size
 * @param failed a pointer to an int, will be set to FAILURE_CODE if the location given was illegal
 * and SUCCESS_CODE otherwise.
 * @return the int saved in the location given
 * if could not access the location will return ILLEGAL_HIT_SPOT and will set failed to FAILURE_CODE
 */
static int getItemInLocation(Field *gameField, int *location, int *failed) {
    *failed = locationLegal(gameField, location);
    if (*failed == FAILURE_CODE) {
        return ILLEGAL_HIT_SPOT;
    }

    int **board = gameField->board;
    assert(DIMENSION_OF_BOARD == 2); // if it isn't then this line is not right
    return board[location[0]][location[1]];
}

/**
 * @brief sets the item in that location in the board to the given value
 * @param gameField a pointer to a Field object
 * @param location an array of size
 * @param insertIntoLocation the int we wish to insert into the location
 * @return SUCCESS_CODE if location is legal and FAILURE_CODE otherwise
 */
static int setItemInLocation(Field *gameField, int *location, int insertIntoLocation) {
    int result = locationLegal(gameField, location);
    if (result == FAILURE_CODE) {
        return result;
    }

    int **board = gameField->board;
    // assumes DIMENSION_OF_BOARD == 2
    board[location[0]][location[1]] = insertIntoLocation;
    return result;
}

/**
 * @brief checks if the ship was sunk
 * @param ship a pointer to a ship struct
 * @return SUCCESS_CODE if the ship was sunk and FAILURE_CODE otherwise
 */
static int shipWasSunk(Ship *ship) {
    if (ship->length == ship->hits) {
        return SUCCESS_CODE;
    }
    return FAILURE_CODE;
}

/**
 * @brief handles the hitting of the board
 * @param gameField a pointer to a Field object
 * @param location an array of size
 * @return
 * EMPTY_SPOT_CODE if hit an empty spot
 * SHIP_SPOT_CODE if hit a ship
 * SUNK_SHIP if hit a ship and sunk it
 * SPOT_HIT_EARLIER if hit a spot that was hit earlier
 * ILLEGAL_HIT_SPOT if the given location is not within the board bounds
 */
int hit(Field *gameField, int *location) {
    int failed = SUCCESS_CODE;
    int chosenLocation = getItemInLocation(gameField, location, &failed);
    if (failed == FAILURE_CODE) {
        // the location is illegal
        return ILLEGAL_HIT_SPOT;
    }
    if (chosenLocation == EMPTY_SPOT_CODE) {
        // we checked earlier that the location is legal so there is no need to save the result
        setItemInLocation(gameField, location, HIT_AND_MISS_SPOT_CODE);
        return EMPTY_SPOT_CODE;
    } else if (chosenLocation == HIT_AND_MISS_SPOT_CODE) {
        return EMPTY_SPOT_CODE;
    } else if (chosenLocation == HIT_SUCCESS_SPOT_CODE) {
        return SPOT_HIT_EARLIER;
    }

    // the current location contains a ship

    // we checked earlier that the location is legal so there is no need to save the result
    setItemInLocation(gameField, location, HIT_SUCCESS_SPOT_CODE);

    Ship *ships = gameField->ships;
    // the index of the ship in the list of ships
    int shipIndex = shipCodeToIndex(chosenLocation);

    ++ships[shipIndex].hits;
    if (shipWasSunk(&(ships[shipIndex])) == SUCCESS_CODE) {
        return SUNK_SHIP;
    }

    // if the ship didn't sink we only indicate we hit it
    return SHIP_SPOT_CODE;

}

/**
 * @brief check if all ships were sunk
 * @param gameField a pointer to a Field object
 * @return SUCCESS_CODE if all ships were sunk and FAILURE_CODE otherwise
 */
int sunkAllShips(Field *gameField) {
    Ship *ships = gameField->ships;
    for (int i = 0; i < NUMBER_OF_SHIPS; ++i) {
        if (shipWasSunk(&(ships[i])) == FAILURE_CODE) {
            return FAILURE_CODE;
        }
    }
    return SUCCESS_CODE;
}