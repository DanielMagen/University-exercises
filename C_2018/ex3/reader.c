/**
 * @file reader.c
 * @author daniel magen
 *
 * @brief
 * this file gets a filename, reads its content which contain the instructions for creating a grid
 * and prints the grid created.
 *
 * @section DESCRIPTION
 * this file contains needed function and constants for the creation and display of a grid r
 * epresenting a heat flow. in the command line it gets a file name with the format
 * as was required in the instructions, and applies the calculate function on the grid
 * which was described in the file, until it reaches a critical point.
 *
 */
// ------------------------------ includes ------------------------------
#include "calculator.h"
#include "heat_eqn.h"
#include <stdio.h>
#include <string.h>
#include <math.h>

// -------------------------- const definitions -------------------------

#define ERROR 1
#define NO_ERROR 0
#define TRUE 1
#define FALSE 0
#define NUMBER_OF_ARGUMENTS_EXPECTED 2
#define NEW_LINE_CHAR '\n'
#define CARRIER_RETURN '\r'
#define NULL_TERMINATOR '\0'
#define SEPARATOR ", "
#define EMPTY_STRING ""
#define ARGUMENT_SEPARATOR "----"
#define HOW_MANY_POSSIBLE_CYCLIC_VALUES 2

#define START_LINE_SIZES 10
#define INCREASE_LINE_BY 10
#define MAXIMUM_LINE_SIZE 30

#define START_NUMBERS_ARRAY 3
#define INCREASE_NUMBERS_ARRAY_BY 5

#define START_POINTS_ARRAY 10
#define INCREASE_POINTS_ARRAY_BY 10

#define INVALID_NUMBER_OF_ARGUMENTS_MESSAGE "program should receive only a file name"
#define NOT_ENOUGH_MEMORY_MESSAGE "there is not enough memory available"
#define NO_SUCH_FILE "there is no such file"
#define ILLEGAL_FILE_FORMAT "the file given is of invalid format"

// ------------------------------ functions -----------------------------
/**
 * @brief prints the error msg given to the stderr
 * @param errorMsg the error to print
 */
static void printError(char *errorMsg) {
    fprintf(stderr, "%s", errorMsg);
}

/**
 * @brief this function prints the grid and the value given
 * @param grid a 2d array of doubles
 * @param n number of rows in the grid
 * @param m number of cols in the grid
 * @param resultOfCalculation a value to print before the grid
 */
static void printGrid(double **grid, size_t n, size_t m, double resultOfCalculation) {
    static const char *SEPARATE_BY = ",";
    printf("%lf\n", resultOfCalculation); // 2 numbers before the point, 4 after
    for (size_t i = 0; i < n; ++i) {
        for (size_t j = 0; j < m; ++j) {
            printf("%2.4lf", grid[i][j]); // 2 numbers before the point, 4 after
            printf(SEPARATE_BY);
        }
        printf("\n");
    }
}

/**
 * @brief returns a new grid with the sizes specified
 * @param n number of rows in the grid
 * @param m number of cols in the grid
 * @return a new grid with the sizes specified.
 * if not enough memory is available it will return NULL
 * note that the grid should be freed after usage using the freeGrid function
 */
static double **createGrid(size_t n, size_t m) {
    double **grid = (double **) malloc(sizeof(double *) * n);
    if (grid == NULL) {
        printError(NOT_ENOUGH_MEMORY_MESSAGE);
        return NULL;
    }
    for (size_t i = 0; i < n; ++i) {
        grid[i] = (double *) malloc(sizeof(double) * m);
        if (grid[i] == NULL) {
            // we don't have enough memory
            printError(NOT_ENOUGH_MEMORY_MESSAGE);
            // free what we got up to now
            for (size_t j = 0; j < i; ++j) {
                free(grid[j]);
            }
            free(grid);
            // return NULL to indicate not enough memory
            return NULL;
        }
        // initialize all values to 0
        for (size_t j = 0; j < m; ++j) {
            grid[i][j] = 0;
        }
    }

    return grid;
}

/**
 * @brief frees the grid given from memory
 * @param grid a pointer to a 2d array of doubles
 * @param n number of rows in the grid
 * @param m number of cols in the grid
 */
static void freeGrid(double ***grid, size_t n) {
    for (size_t i = 0; i < n; ++i) {
        free((*grid)[i]);
    }
    free(*grid);
    *grid = NULL;
}

/**
 * @brief reads a single file line by line. this function does not work with various files,
 * only one each run
 * @param file a file object
 * @param succeeded a pointer to an integer
 * @return each time we pass it the the file it returns the next line it haven't read yet
 * if there was a problem or reached the end of the file it returns NULL
 * if the line read was longer than MAXIMUM_LINE_SIZE it returns NULL and it is an ERROR
 * if there was a problem it sets succeeded to ERROR, otherwise it's set to NO_ERROR
 * note that this line should be freed after usage.
 */
static char *getNextLineFromFile(FILE *file, int *succeeded) {
    static size_t currentCharNum = 0; // will hold the last place we haven't read yet

    *succeeded = NO_ERROR;

    // go to last char you haven't read yet
    int resultOfSeek = fseek(file, currentCharNum, SEEK_SET);

    if (resultOfSeek != 0) {
        // reached end of file
        *succeeded = ERROR;
        return NULL;
    }

    int currentAllocationSize = START_LINE_SIZES;
    int currentLengthOfLine = 0;
    char *line = (char *) malloc(sizeof(char) * currentAllocationSize);
    char nextChar;

    if (line == NULL) {
        printError(NOT_ENOUGH_MEMORY_MESSAGE);
        *succeeded = ERROR;
        return NULL;
    }

    while ((nextChar = (char) fgetc(file)) != EOF && nextChar != NEW_LINE_CHAR &&
           nextChar != CARRIER_RETURN) {
        line[currentLengthOfLine] = nextChar;
        currentLengthOfLine++; // we increased the line size by 1
        currentCharNum++;

        if (currentLengthOfLine >= MAXIMUM_LINE_SIZE) {
            printError(ILLEGAL_FILE_FORMAT);
            *succeeded = ERROR;
            free(line);
            return NULL;
        }

        if (currentLengthOfLine == currentAllocationSize) {
            currentAllocationSize += INCREASE_LINE_BY; // new memory allocation size
            char *extendedLine = (char *) realloc(line, sizeof(char) * currentAllocationSize);

            if (extendedLine == NULL) {
                printError(NOT_ENOUGH_MEMORY_MESSAGE);
                *succeeded = ERROR;
                free(line);
                return NULL;
            }
            line = extendedLine;
        }
    }
    currentCharNum++;
    // if we stopped at NEW_LINE we need to advance it by 1
    // if we stopped at EOF increasing by 1 doesn't change anything because fseek will still fail
    if (nextChar == CARRIER_RETURN) {
        // for the program to work on windows
        currentCharNum++;
    }

    line[currentLengthOfLine] = NULL_TERMINATOR;
    currentLengthOfLine++;

    char *smallerLine = (char *) realloc(line,
                                         sizeof(char) * currentLengthOfLine); // don't need mem
    if (smallerLine == NULL) {
        printError(NOT_ENOUGH_MEMORY_MESSAGE);
        *succeeded = ERROR;
        free(line);
        return NULL;
    }
    return smallerLine;
}

/**
 * @brief this function receives a string that contains only a number
 * and extracts the number from it
 * @param string the string containing the numberng
 * @param succeededGettingNumber a pointer to an int. if there was no problem it sets it to NO_ERROR
 * otherwise it is set to ERROR
 * @return if there was no problem, returns the number in the string, otherwise returns 0
 * and sets succeeded to ERROR.
 * note that the string given should contain the double number and nothing else
 */
static double extractSingleNumberFromString(char *string, int *succeededGettingNumber) {
    *succeededGettingNumber = NO_ERROR;

    char *nonNumberValue;
    double numberExtracted = strtod(string, &nonNumberValue);
    if (strcmp(nonNumberValue, EMPTY_STRING) != 0) {
        // what we got wasn't a valid number
        *succeededGettingNumber = ERROR;
        return 0;
    }
    return numberExtracted;
}

/**
 * @brief extract a list of numbers from the given string, all separated by SEPARATOR
 * @param string the the string to extract the list of numbers from it assumes its length is
 * less than or equal to MAXIMUM_LINE_SIZE
 * @param lengthOfString the length of the given string
 * @param length a pointer to an integer, will be set to be the length of
 * the returned array
 * @return list of numbers from the given string all separated by SEPARATOR
 * if there was a problem, it returns NULL
 * note that the returned value should be freed after usage
 */
static double *extractNumbersFromString(const char *string, int *length) {
    *length = 0;
    if (string == NULL) {
        return NULL;
    }

    double *numbers = (double *) malloc(sizeof(double) * START_NUMBERS_ARRAY);
    if (numbers == NULL) {
        return NULL;
    }
    char stringCopy[MAXIMUM_LINE_SIZE] = {0};

    // now copy the given string so you could use the strtok function on it
    strcpy(stringCopy, string);
    int currentAllocationSize = START_NUMBERS_ARRAY;
    int currentLengthOfNumbers = 0;
    int succeededInGettingNumber = 0;
    char *nextNumber = strtok(stringCopy, SEPARATOR);

    while (nextNumber != NULL) {
        numbers[currentLengthOfNumbers] = extractSingleNumberFromString(nextNumber,
                                                                        &succeededInGettingNumber);
        if (succeededInGettingNumber == ERROR) {
            printError(ILLEGAL_FILE_FORMAT);
            free(numbers);
            return NULL;
        }
        currentLengthOfNumbers++; // we increased the numbers array size by 1

        if (currentLengthOfNumbers == currentAllocationSize) {
            currentAllocationSize += INCREASE_NUMBERS_ARRAY_BY; // new memory allocation size
            double *extendedNumbers = (double *) realloc(numbers,
                                                         sizeof(double) * currentAllocationSize);

            if (extendedNumbers == NULL) {
                printError(NOT_ENOUGH_MEMORY_MESSAGE);
                free(numbers);
                return NULL;
            }
            numbers = extendedNumbers;
        }

        nextNumber = strtok(NULL, SEPARATOR); // advance to the next number in the string
    }

    double *smallerNumbers = (double *) realloc(numbers,
                                                sizeof(double) * currentLengthOfNumbers);
    if (smallerNumbers == NULL) {
        printError(NOT_ENOUGH_MEMORY_MESSAGE);
        free(numbers);
        return NULL;
    }

    *length = currentLengthOfNumbers;
    return smallerNumbers;

}

/**
 * @brief checks the array given contains only integers up to upTo not inclusive
 * @param numbers an array of doubles
 * @param upTo check up to this index not inclusive
 * @return TRUE positive integer value, FALSE otherwise
 */
static int checkAllNumbersAreWhole(double *numbers, int upTo) {
    double fractionPart, integerPart;
    for (int i = 0; i < upTo; ++i) {
        fractionPart = modf(numbers[i], &integerPart);
        if (fractionPart != 0 || integerPart < 0) {
            return FALSE;
        }
    }

    return TRUE;
}

/**
 * @brief reads the grid creation parameters from the file given.
 * creates a new grid and places the relevant data into the variables given
 * @param file a file object
 * @param grid a pointer to a 2d array of doubles
 * @param n a pointer to number of rows in the grid
 * @param m a pointer to number of cols in the grid
 * @return ERROR if there was a problem, NO_ERROR otherwise
 */
static int handleGridCreationFromFile(FILE *file, double ***grid, size_t *n, size_t *m) {
    const int EXPECTED_AMOUNT_OF_NUMBERS = 2;
    int succeeded; // will hold if we managed to get data from the file given
    char *line = getNextLineFromFile(file, &succeeded);

    if (succeeded == ERROR) {
        // no line was allocated so we don't need to free it
        return ERROR;
    }


    int howManyNumbers = 0; // will hold the length of numbersInLine
    double *numbersInLine = extractNumbersFromString(line, &howManyNumbers);
    if (numbersInLine == NULL || howManyNumbers != EXPECTED_AMOUNT_OF_NUMBERS) {
        free(line);
        free(numbersInLine);
        return ERROR;
    }


    // now check all numbers are integers
    int allNumbersAreWhole = checkAllNumbersAreWhole(numbersInLine, howManyNumbers);
    if (allNumbersAreWhole == FALSE) {
        printError(ILLEGAL_FILE_FORMAT);
        free(line);
        free(numbersInLine);
        return ERROR;
    }



    // create a new grid and set n, m to be what they should be
    *n = (size_t) numbersInLine[0];
    *m = (size_t) numbersInLine[1];
    *grid = createGrid(*n, *m);

    free(line);
    free(numbersInLine);

    return NO_ERROR;

}

/**
 * @brief checks if the next line is ARGUMENT_SEPARATOR or not
 * @param file a file object
 * @param nextLine a pointer to a pointer to a char,
 * it will insert the line read from the file into it
 * note that it does not free the line an as such it should be freed by whoever called the function
 * @return TRUE if the next line is ARGUMENT_SEPARATOR and FALSE otherwise
 */
static int nextLineIsSeparator(FILE *file, char **nextLine) {
    int succeeded;
    *nextLine = getNextLineFromFile(file, &succeeded);
    if (succeeded == NO_ERROR && strcmp(*nextLine, ARGUMENT_SEPARATOR) == 0) {
        return TRUE;
    }
    return FALSE;
}

/**
 * @brief checks if the point coordinates are valid
 * @param p a point object
 * @param n number of rows in a grid
 * @param m number of cols in a grid
 * @return TRUE if the point given is the bounds given, FALSE otherwise
 */
static int pointIsInBounds(source_point *p, size_t n, size_t m) {
    if (p->x >= 0 && (size_t) p->x < n) {
        if (p->y >= 0 && (size_t) p->y < m) {
            return TRUE;
        }
    }
    return FALSE;
}

/**
 * @brief reads the given line and inserts the data given into it
 * @param p a pointer to a point object
 * @param grid  a 2d array of doubles
 * @param n the number of rows in the grid
 * @param m the number of cols in the grid
 * @param line the string to read data from
 * @return ERROR if there was a problem, NO_ERROR otherwise
 */
static int insertDataFromLineToPoint(source_point *p,
                                     double **grid,
                                     size_t n,
                                     size_t m,
                                     char *line) {
    static const int EXPECTED_AMOUNT_OF_NUMBERS = 3; // expects 3 values
    static const int EXPECTED_AMOUNT_OF_INTEGERS = 2; // expects 2 dimensional coordinates
    int howManyNumbersGot;
    // extractNumbersFromString will handle the case of a null line
    double *data = extractNumbersFromString(line, &howManyNumbersGot);
    if (data == NULL) {
        return ERROR;
    }
    if (howManyNumbersGot != EXPECTED_AMOUNT_OF_NUMBERS) {
        free(data);
        return ERROR;
    }

    int allNumbersAreWhole = checkAllNumbersAreWhole(data, EXPECTED_AMOUNT_OF_INTEGERS);
    if (allNumbersAreWhole == FALSE) {
        free(data);
        return ERROR;
    }

    p->x = (int) data[0];
    p->y = (int) data[1];
    p->value = data[2];

    if (pointIsInBounds(p, n, m) == FALSE) {
        free(data);
        return ERROR;
    }

    grid[p->x][p->y] = p->value;
    free(data);
    return NO_ERROR;
}

/**
 * @brief reads the sources creation parameters from the file given.
 * creates the sources and places the relevant data into the variables given
 * @param file a file object
 * @param grid  a 2d array of doubles
 * @param n the number of rows in the grid
 * @param m the number of cols in the grid
 * @param sources a pointer to an array of points, it will inserts the sources into there
 * @param num_sources a pointer to the length of sources, it will
 * insert into it the number of sources
 * @return ERROR if there was a problem, NO_ERROR otherwise
 * note that the sources should be freed after usage
 */
static int handleSourcesCreationFromFile(FILE *file,
                                         double **grid,
                                         size_t n,
                                         size_t m,
                                         source_point **sources,
                                         size_t *num_sources) {
    *sources = (source_point *) malloc(sizeof(source_point) * START_POINTS_ARRAY);
    size_t currentAllocationSize = START_POINTS_ARRAY;
    size_t currentLengthOfSources = 0;
    char *nextLine = NULL;
    int resultOfTryingToInsertData;


    while (nextLineIsSeparator(file, &nextLine) == FALSE) // while the next line is not a separator
    {
        // insertDataFromLineToPoint will handle the case of a null line
        resultOfTryingToInsertData = insertDataFromLineToPoint(
                &((*sources)[currentLengthOfSources]),
                grid, n, m, nextLine);

        if (resultOfTryingToInsertData == ERROR) {
            printError(ILLEGAL_FILE_FORMAT);
            free(*sources);
            free(nextLine);
            return ERROR;
        }
        currentLengthOfSources++; // we increased the array size by 1

        if (currentLengthOfSources == currentAllocationSize) {
            currentAllocationSize += INCREASE_POINTS_ARRAY_BY; // new memory allocation size
            source_point *extendedSources = (source_point *) realloc(*sources,
                                                                     sizeof(source_point) *
                                                                     currentAllocationSize);

            if (extendedSources == NULL) {
                printError(NOT_ENOUGH_MEMORY_MESSAGE);
                free(*sources);
                free(nextLine);
                return ERROR;
            }
            *sources = extendedSources;
        }

        free(nextLine); // free the line given before going to the next one
    }

    free(nextLine); // free the separator line

    source_point *smallerSources = (source_point *) realloc(*sources,
                                                            sizeof(source_point) *
                                                            currentLengthOfSources);
    if (smallerSources == NULL) {
        printError(NOT_ENOUGH_MEMORY_MESSAGE);
        free(*sources);
        return ERROR;
    }

    *num_sources = currentLengthOfSources;
    *sources = smallerSources;
    return NO_ERROR;

}

/**
 * @brief reads the next line in the file and inserts the number that is there into the given number
 * @param file a file object
 * @param insertNumberTo a pointer to an integer. inserts the read number into here
 * @param shouldBeInteger if equals TRUE it checks that the given number is an integer
 * @return ERROR if there was a problem, NO_ERROR otherwise
 * a problem could be
 * - problem reading the next line
 * - more than a single number in the line
 * - isn't an integer when it should be
 */
static int getNextNumberFromFile(FILE *file, double *insertNumberTo, int shouldBeInteger) {
    static const int EXPECTED_AMOUNT_OF_NUMBERS = 1; // expects 1 value
    int howManyNumbersGot;
    int succeeded;
    char *line = getNextLineFromFile(file, &succeeded);

    if (succeeded == ERROR) {
        return ERROR;
    }

    double *numbers = extractNumbersFromString(line, &howManyNumbersGot);
    if (numbers == NULL || howManyNumbersGot != EXPECTED_AMOUNT_OF_NUMBERS) {
        free(line);
        free(numbers);
        return ERROR;
    }

    if (shouldBeInteger == TRUE) {
        succeeded = checkAllNumbersAreWhole(numbers, EXPECTED_AMOUNT_OF_NUMBERS);
        if (succeeded == FALSE) {
            free(line);
            free(numbers);
            return ERROR;
        }
    }

    *insertNumberTo = numbers[0];

    free(line);
    free(numbers);
    return NO_ERROR;
}

/**
 * @brief checks that cyclic number given is ok
 * @param is_cyclic the number to check
 * @return TRUE if the cyclic number given is ok
 * FALSE otherwise
 */
static int cyclicNumberIsOk(int is_cyclic) {
    const int EXPECTED_NUMBERS[HOW_MANY_POSSIBLE_CYCLIC_VALUES] = {0, 1};
    for (int i = 0; i < HOW_MANY_POSSIBLE_CYCLIC_VALUES; ++i) {
        if (is_cyclic == EXPECTED_NUMBERS[i]) {
            return TRUE;
        }
    }
    return FALSE;
}

/**
 * @brief reads data from file and inserts it into the arguments given
 * @param grid a pointer to a 2d array of doubles
 * @param n a pointer to number of rows in the grid
 * @param m a pointer to number of cols in the grid
 * @param sources a pointer to an array of points on which the process will not take place
 * @param num_sources a pointer to the length of sources
 * @param terminate a pointer to the difference between resulting heat
 * that will halt the function if n_iter < 0
 * @param n_iter a pointer to the number of iterations the function will go,
 * if less than 0 it will halt only
 * once the difference between resulting heat will be less than terminate
 * @param is_cyclic a pointer to a variable that if non 0,
 * it will consider negative indices as indices starting from the end
 * @return ERROR if there was a problem, NO_ERROR otherwise
 * note that the following should be freed after usage
 * - grid - using the freeGrid function
 * - sources
 */
static int getDataFromFile(
        char *fileName,
        double ***grid,
        size_t *n,
        size_t *m,
        source_point **sources,
        size_t *num_sources,
        double *terminate,
        unsigned int *n_iter,
        int *is_cyclic) {
    FILE *file = fopen(fileName, "r");
    if (file == NULL) {
        printError(NO_SUCH_FILE);
        return ERROR;
    }


    int resultOfTryingToReadData;
    resultOfTryingToReadData = handleGridCreationFromFile(file, grid, n, m); // creates the grid

    if (resultOfTryingToReadData == ERROR) {
        fclose(file);
        return ERROR;
    }

    // now next line should be a separator line
    char *nextLine = NULL;
    int isNextLineSeparator = nextLineIsSeparator(file, &nextLine);
    // we do not need the actual line, only the if its a separator or not
    free(nextLine);
    nextLine = NULL;
    if (isNextLineSeparator == FALSE) {
        // next line is not a separator line unlike what we expected
        printError(ILLEGAL_FILE_FORMAT);
        freeGrid(grid, *n);
        fclose(file);
        return ERROR;
    }


    resultOfTryingToReadData = handleSourcesCreationFromFile(file,
                                                             *grid, *n, *m, sources, num_sources);

    if (resultOfTryingToReadData == ERROR) {
        freeGrid(grid, *n);
        fclose(file);
        return ERROR;
    }

    // no need checking that next line is separator because handleSourcesCreationFromFile checked

    resultOfTryingToReadData = getNextNumberFromFile(file, terminate, FALSE);

    if (resultOfTryingToReadData == ERROR) {
        printError(ILLEGAL_FILE_FORMAT);
        freeGrid(grid, *n);
        free(*sources);
        fclose(file);
        return ERROR;
    }

    double doubleN_iter;
    resultOfTryingToReadData = getNextNumberFromFile(file, &doubleN_iter, TRUE);
    *n_iter = (unsigned int) doubleN_iter;


    if (resultOfTryingToReadData == ERROR) {
        printError(ILLEGAL_FILE_FORMAT);
        freeGrid(grid, *n);
        free(*sources);
        fclose(file);
        return ERROR;
    }

    double doubleIs_cyclic;
    resultOfTryingToReadData = getNextNumberFromFile(file, &doubleIs_cyclic, TRUE);
    *is_cyclic = (int) doubleIs_cyclic;

    if (resultOfTryingToReadData == ERROR || cyclicNumberIsOk(*is_cyclic) == FALSE) {
        printError(ILLEGAL_FILE_FORMAT);
        freeGrid(grid, *n);
        free(*sources);
        fclose(file);
        return ERROR;
    }

    fclose(file);
    return NO_ERROR;

}

/**
 * @brief checks if |num1| < num2
 * @param num1 a double number
 * @param num2 a double number
 * @return TRUE if |num1| < num2, FALSE otherwise
 */
static int isAbsLessThan(double num1, double num2) {
    if (num1 < 0) {
        num1 = num1 * (-1);
    }
    if (num1 < num2) {
        return TRUE;
    }
    return FALSE;
}

int main(int argc, char **argv) {
    if (argc != NUMBER_OF_ARGUMENTS_EXPECTED) {
        printError(INVALID_NUMBER_OF_ARGUMENTS_MESSAGE);
        return ERROR;
    }

    char *fileName = argv[NUMBER_OF_ARGUMENTS_EXPECTED - 1];


    double **grid;
    size_t n;
    size_t m;
    source_point *sources;
    size_t num_sources;
    double terminate;
    unsigned int n_iter;
    int is_cyclic;

    int resultOfTryingToReadData = getDataFromFile(fileName,
                                                   &grid,
                                                   &n,
                                                   &m,
                                                   &sources,
                                                   &num_sources,
                                                   &terminate,
                                                   &n_iter,
                                                   &is_cyclic);


    if (resultOfTryingToReadData == ERROR) {
        return ERROR;
    }

    // now print the grid. if n_iter < 0 then the while condition will be false
    double resultOfCalc = 0;
    do {
        resultOfCalc = calculate(heat_eqn,
                                 grid,
                                 n,
                                 m,
                                 sources,
                                 num_sources,
                                 terminate,
                                 n_iter,
                                 is_cyclic);
        printGrid(grid, n, m, resultOfCalc);
    } while (isAbsLessThan(resultOfCalc, terminate) == FALSE);


    // free all memory which was allocated
    freeGrid(&grid, n);
    free(sources);


    return NO_ERROR;
}