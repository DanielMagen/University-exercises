/**
 * @file battleships.h
 * @author Daniel Magen
 * @version 1.0
 *
 * @brief
 * contains the needed constants and function signatures needed to operate a battleships game
 *
 * @section DESCRIPTION
 * this file contains all needed function signatures and constants that are in turn implemented
 * in the battleships.c file
 *
 * Input  : none
 * Process: none
 * Output : none
 */

// -------------------------- const definitions -------------------------
#ifndef EX2_BATTLESHIPS_H
#define EX2_BATTLESHIPS_H

#define MINIMUM_BOARD_SIZE 5
#define MAXIMUM_BOARD_SIZE 26
#define DIMENSION_OF_BOARD 2
#define BAD_BOARD_SIZE 9
#define NO_MEMORY_FOR_BOARD 10

#define EMPTY_SPOT_CODE 0
#define HIT_AND_MISS_SPOT_CODE 1
#define HIT_SUCCESS_SPOT_CODE 2
#define SHIP_SPOT_CODE (-1)
// ths ship code will be multiplied, such that all ships will have a negative code

#define ILLEGAL_HIT_SPOT 6
#define SPOT_HIT_EARLIER 7
#define SUNK_SHIP 8

#define FAILURE_CODE 1
#define SUCCESS_CODE 0

#define NUMBER_OF_SHIPS 5

/**
 * a struct representing a ship on the board
 */
typedef struct {
    int length;
    int location[DIMENSION_OF_BOARD];
    int orientation;
    int code; // the unique code of the ship
    int hits; // how many hits the ship has sustained
} Ship;

/**
 * a struct representing the field of the game
 * includes the play board and all the ships in the game
 */
typedef struct {
    int size;
    int **board;
    Ship ships[NUMBER_OF_SHIPS];
} Field;

// ------------------------------ functions -----------------------------
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
Field startBoard(int sizeOfBoard, int *failed);

/**
 * @brief check if all ships were sunk
 * @param gameField a pointer to a Field object
 * @return SUCCESS_CODE if all ships were sunk and FAILURE_CODE otherwise
 */
int sunkAllShips(Field *gameField);


/**
 * @brief clears all the memory that was taken by the field
 * @param gameField a pointer to a Field object
 * should be called whenever the game is existed
 */
void exitBoard(Field *gameField);


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
int hit(Field *gameField, int *location);


/**
 *  @brief prints the board to the user
 * @param gameField a pointer to a Field object
 */
void printBoard(Field *gameField);


#endif //EX2_BATTLESHIPS_H
