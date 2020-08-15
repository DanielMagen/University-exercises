/**
 * @file battleships_game.c
 * @author Daniel Magen
 * @version 1.0
 *
 * @brief
 * this file manages an entire battleships game
 *
 * @section DESCRIPTION
 * this program receives a continues input from the user and converts them to commands in the
 * battleships game. if any problem arise during the game it tells the user about it and
 * exits gracefully.
 *
 * Input  : continues input from the user
 * Process: manages a battleships game
 * Output : prints the result of the game. returns 0 if everything went OK, 1 otherwise
 */


// ------------------------------ includes ------------------------------
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <ctype.h>
#include "battleships.h"

// -------------------------- const definitions -------------------------
#define ALREADY_HIT_MESSAGE "Already been Hit.\n"
#define MISS_MESSAGE "Miss.\n"
#define HIT_MESSAGE "Hit.\n"
#define SUNK_MESSAGE "Hit and sunk.\n"
#define ILLEGAL_INPUT "Invalid move, try again.\n"
#define START_GAME "Ready to play\n"
#define GAME_OVER "Game over"
#define EXIT_STRING "exit"

#define ENTER_SIZE_MESSAGE "enter board size: "
#define ENTER_LOCATION_MESSAGE "enter coordinates: "
#define ERROR 1
#define NO_ERROR 0
#define EXIT_CODE 2

#define TRUE 1
#define FALSE 0

#define BAD_BOARD_SIZE_MESSAGE "the size given should be between 5 and 26"
#define NOT_ENOUGH_MEMORY_MESSAGE "there is not enough memory to create the board"

#define START_ROW_FROM 'a'
#define START_COL_FROM 0

#define HANDLE_INPUT_UP_TO_LENGTH 5
#define INPUT_RECEIVE "%4[^\n]"
// the number should be the same as in HANDLE_INPUT_UP_TO_LENGTH - 1
// it takes all non newline characters

// ------------------------------ functions -----------------------------

/**
 * @brief prints the error msg given to the stderr
 * @param errorMsg the error to print
 */
void printError(char *errorMsg) {
    fprintf(stderr, "%s", errorMsg);
}

/**
 * @brief converts the given text to a location in the board and inserts it into location array
 * @param row the row given by the user
 * @param col the col given by the user
 * @param location an array of size DIMENSION_OF_BOARD
 */
void getLocationFromText(char row, int col, int *location) {
    int rowNumber = row - START_ROW_FROM;
    location[0] = rowNumber;
    location[1] = col - 1;
}

/**
 * @brief handles the input to the program
 * @param row a pointer to a char
 * @param col a pointer to a int
 * @return receives an input from the user and enters that input into the given variables
 * if the input is legal it sends back NO_ERROR
 * if the input is exit it sends back EXIT_CODE
 * if the input is legal it sends back ERROR
 */
int handleInput(char *row, int *col) {
    printf(ENTER_LOCATION_MESSAGE);
    char string[HANDLE_INPUT_UP_TO_LENGTH] = {0};
    scanf("\n");
    scanf(INPUT_RECEIVE, string);

    if ((strcmp(string, EXIT_STRING)) == 0) {
        return EXIT_CODE;
    }

    if (!isalpha(string[0])) {
        // the first char wasn't a valid letter
        return ERROR;
    }

    *row = string[0];
    *col = atoi(string + 1);

    return NO_ERROR;
}

/**
 * @brief this function handles the result we got from the handleInput function
 * if needed it prints to the screen an informative message
 * @param gameField a pointer to a Field object
 * @param resultOfInput the result got from the handleInput function
 * @param row a pointer to a char representing a row in the gameField board
 * @param col a pointer to an int representing a col in the gameField board
 * @param lastMoveWasLegal a pointer to an integer, sets it to FALSE if the move
 * made by the user was illegal
 */
void handleResultOfInput(Field *gameField,
                         int resultOfInput,
                         const char *row,
                         const int *col,
                         int *lastMoveWasLegal) {
    int location[DIMENSION_OF_BOARD] = {0};
    int resultOfHit = 0; // the result we got from the hit function

    if (resultOfInput == ERROR) {
        printError(ILLEGAL_INPUT);
    } else if (resultOfInput == NO_ERROR) {

        getLocationFromText(*row, *col, location);
        resultOfHit = hit(gameField, location);

        if (resultOfHit == ILLEGAL_HIT_SPOT) {
            printError(ILLEGAL_INPUT);
            *lastMoveWasLegal = FALSE;
        } else {
            *lastMoveWasLegal = TRUE;
            if (resultOfHit == EMPTY_SPOT_CODE) {
                printf(MISS_MESSAGE);
            } else if (resultOfHit == SHIP_SPOT_CODE) {
                printf(HIT_MESSAGE);
            } else if (resultOfHit == SUNK_SHIP) {
                printf(SUNK_MESSAGE);
            } else if (resultOfHit == SPOT_HIT_EARLIER) {
                printf(ALREADY_HIT_MESSAGE);
            }
        }
    }
}

/**
 * @brief the main function
 * @return NO_ERROR if everything went OK, ERROR otherwise
 */
int main() {
    // start board
    int failed = SUCCESS_CODE; // will hold an indicator to if we failed during a stage
    int sizeOfBoard = 0;
    printf(ENTER_SIZE_MESSAGE);
    scanf("%d", &sizeOfBoard);
    Field gameField = startBoard(sizeOfBoard, &failed);

    if (failed != SUCCESS_CODE) {
        if (failed == BAD_BOARD_SIZE) {
            printError(BAD_BOARD_SIZE_MESSAGE);
        } else if (failed == NO_MEMORY_FOR_BOARD) {
            printError(NOT_ENOUGH_MEMORY_MESSAGE);
        }
        return ERROR;
    }

    //start to play
    char row = START_ROW_FROM;
    int col = START_COL_FROM;
    int lastMoveWasLegal = TRUE;
    int resultOfInput = 0; // the result we got from the input-handle function
    int printGameOver = TRUE;

    printf(START_GAME);

    while (sunkAllShips(&gameField) == FAILURE_CODE) // there is at least one ship standing
    {
        if (lastMoveWasLegal == TRUE) {
            printBoard(&gameField);
        }

        resultOfInput = handleInput(&row, &col);
        if (resultOfInput == EXIT_CODE) {
            printGameOver = FALSE;
            break;
        }
        handleResultOfInput(&gameField, resultOfInput, &row, &col, &lastMoveWasLegal);
    }

    if (printGameOver == TRUE) {
        printf(GAME_OVER);
    }

    exitBoard(&gameField); // clear memory

    return NO_ERROR;

}