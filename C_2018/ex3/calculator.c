/**
 * @file calculator.c
 * @author daniel magen
 *
 * @brief
 * this file contains all needed function for the calculation of the relaxation
 * on a grid.
 *
 * @section DESCRIPTION
 * this file contains one non static function which is used for the calculation of the relaxation
 * on a grid. according to the values given it either continues in a loop until a target
 * critical point is reached, or runs a constant amount of times.
 *
 */
// ------------------------------ includes ------------------------------
#include <stdio.h>
#include "calculator.h"

// -------------------------- const definitions -------------------------
#define TRUE 1
#define FALSE 0
#define NUMBER_OF_ADJACENT_CELLS 4
#define VALUE_FOR_OUT_OF_BOUNDS_CELLS 0
#define NOT_ENOUGH_MEMORY_MESSAGE "there is not enough memory available"
#define INVALID_GRID "there was a problem with the given grid"

// ------------------------------ functions -----------------------------
/**
 * @brief prints the error msg given to the stderr
 * @param errorMsg the error to print
 */
static void printError(char *errorMsg) {
    fprintf(stderr, "%s", errorMsg);
}


/**
 * @brief this function returns the sum of all elements in the grid
 * @param grid the grid to sum
 * @param n number of rows
 * @param m number of cols
 * @return the sum of all elements in the grid
 */
static double sumGrid(double **grid, size_t n, size_t m) {
    double sum = 0;
    for (size_t i = 0; i < n; ++i) {
        for (size_t j = 0; j < m; ++j) {
            sum += grid[i][j];
        }
    }
    return sum;
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

/**
 * @brief checks if given point is in the array
 * @param toCheck check if this point is in the given array
 * @param sources an array of points
 * @param num_sources the length of sources
 * @return TRUE if the given point is in the array given
 * FALSE otherwise
 */
static int pointIsInArrayOfPoints(source_point *toCheck, source_point *sources, size_t num_sources) {
    for (size_t i = 0; i < num_sources; ++i) {
        if (sources[i].x == toCheck->x) {
            if (sources[i].y == toCheck->y) {
                return TRUE;
            }
        }
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
 * @brief does modulo operation
 * @param num an integer
 * @param toMod an integer
 * @return num mod toMod
 */
static int mod(int num, int toMod) {
    int result = num % toMod;
    if (result < 0) {
        return result + toMod;
    }
    return result;
}

/**
 * @brief sets the point coordinates to be valid by cycling out of bounds points
 * @param p a point object
 * @param n number of rows in a grid
 * @param m number of cols in a grid
 */
static void cyclePoint(source_point *p, size_t n, size_t m) {
    p->x = mod(p->x, (int) n);
    p->y = mod(p->y, (int) m);
}


/**
 * @brief sets the point neighbours array given to contain valid values
 * from the given grid. if is_cyclic is 0, neighbours that go over the array limits
 * have their value set to VALUE_FOR_OUT_OF_BOUNDS_CELLS
 * @param p the point to find the neighbours of
 * @param grid a 2d array of doubles
 * @param n number of rows in the grid
 * @param m number of cols in the grid
 * @param is_cyclic if non 0, it will consider negative indices as indices starting from the end
 * @param pointNeighboursValues an array the size of NUMBER_OF_ADJACENT_CELLS which we will set
 * to contain in that order -
 * the value of the right neighbour
 * the value of the top neighbour
 * the value of the left neighbour
 * the value of the bottom neighbour
 */
static void getPointNeighboursValues(source_point *p,
                                     double **grid,
                                     size_t n,
                                     size_t m,
                                     int is_cyclic,
                                     double *pointNeighboursValues) {
    source_point pointNeighbours[NUMBER_OF_ADJACENT_CELLS];


    //right neighbour
    pointNeighbours[0].x = p->x;
    pointNeighbours[0].y = p->y + 1;

    //top neighbour
    pointNeighbours[1].x = p->x - 1;
    pointNeighbours[1].y = p->y;

    //left neighbour
    pointNeighbours[2].x = p->x;
    pointNeighbours[2].y = p->y - 1;

    //bottom neighbour
    pointNeighbours[3].x = p->x + 1;
    pointNeighbours[3].y = p->y;


    if (is_cyclic) {
        // we need to correct the indices of the points
        for (int i = 0; i < NUMBER_OF_ADJACENT_CELLS; ++i) {
            cyclePoint(&(pointNeighbours[i]), n, m);
        }
    }

    // set the points values to the needed value
    for (int i = 0; i < NUMBER_OF_ADJACENT_CELLS; ++i) {
        if (pointIsInBounds(&(pointNeighbours[i]), n, m)) {
            pointNeighboursValues[i] = grid[pointNeighbours[i].x][pointNeighbours[i].y];
        } else {
            pointNeighboursValues[i] = VALUE_FOR_OUT_OF_BOUNDS_CELLS;
        }
    }

}

/**
 * @brief changes the grid given by applying the function given on all indices in the grid
 * @param function the function to apply on each number on the grid
 * @param grid a 2d array of doubles
 * @param n number of rows in the grid
 * @param m number of cols in the grid
 * @param sources an array of points on which the process will not take place
 * @param num_sources the length of sources
 * @param n_iter the number of iterations the function will go, if less than 0 it will halt only
 * once the difference between resulting heat will be less than terminate
 * @param is_cyclic if non 0, it will consider negative indices as indices starting from the end
 * @return TRUE if succeeded in the operation and FALSE otherwise
 */
static int applyFunctionOnAllNonSources(
        diff_func function,
        double **grid,
        size_t n,
        size_t m,
        source_point *sources,
        size_t num_sources,
        int is_cyclic) {

    source_point tmpPoint;
    double tmpPointNeighboursValues[NUMBER_OF_ADJACENT_CELLS];

    for (size_t i = 0; i < n; ++i) {
        for (size_t j = 0; j < m; ++j) {
            tmpPoint.x = (int) i;
            tmpPoint.y = (int) j;
            tmpPoint.value = grid[i][j];
            if (pointIsInArrayOfPoints(&tmpPoint, sources, num_sources)) {
                // we don't apply the function on sources
                continue;
            }
            // get point neighbours from the grid copy, use the grid copy to get relevant values
            getPointNeighboursValues(&tmpPoint, grid, n, m, is_cyclic, tmpPointNeighboursValues);
            grid[i][j] = function(grid[i][j],
                                  tmpPointNeighboursValues[0],
                                  tmpPointNeighboursValues[1],
                                  tmpPointNeighboursValues[2],
                                  tmpPointNeighboursValues[3]);

        }
    }

    return TRUE;
}

/**
 * @brief applies the function given onto the grid and updates the values of
 * prevSum, nextSum, differenceBetweenSums
 * @param function the function to apply on each number on the grid
 * @param grid a 2d array of doubles
 * @param n number of rows in the grid
 * @param m number of cols in the grid
 * @param sources an array of points on which the process will not take place
 * @param num_sources the length of sources
 * once the difference between resulting heat will be less than terminate
 * @param is_cyclic if non 0, it will consider negative indices as indices starting from the end
 * @param prevSum a pointer to a double representing the previous sum of the grid
 * @param nextSum a pointer to a double representing the next sum of the grid
 * @param differenceBetweenSums a pointer to a double representing the difference between the sums
 */
static void applyFunctionOnGrid(diff_func function,
                                double **grid,
                                size_t n,
                                size_t m,
                                source_point *sources,
                                size_t num_sources,
                                int is_cyclic,
                                double *prevSum,
                                double *nextSum,
                                double *differenceBetweenSums) {
    applyFunctionOnAllNonSources(function, grid, n, m, sources, num_sources, is_cyclic);
    *nextSum = sumGrid(grid, n, m);
    *differenceBetweenSums = *nextSum - *prevSum;
    *prevSum = *nextSum;
}

/**
 * @brief applies the given function onto the given grid using the relaxation method
 * @param function the function to apply on each number on the grid
 * @param grid a 2d array of doubles
 * @param n number of rows in the grid
 * @param m number of cols in the grid
 * @param sources an array of points on which the process will not take place
 * @param num_sources the length of sources
 * @param terminate the difference between resulting heat that will halt the function if n_iter < 0
 * @param n_iter the number of iterations the function will go, if less than 0 it will halt only
 * once the difference between resulting heat will be less than terminate
 * @param is_cyclic if non 0, it will consider negative indices as indices starting from the end
 * @return the last difference between the sums of the grid
 * if the grid given was null it prints an error message and returns -1
 */
double calculate(diff_func function,
                 double **grid,
                 size_t n,
                 size_t m,
                 source_point *sources,
                 size_t num_sources,
                 double terminate,
                 unsigned int n_iter,
                 int is_cyclic) {
    const double ERROR_IN_GRID = -1;
    if (grid == NULL) {
        printError(INVALID_GRID);
        return ERROR_IN_GRID;
    }

    double prevSum = sumGrid(grid, n, m);
    double nextSum;
    // initiate the next sum such that differenceBetweenSums < terminate
    if (prevSum < 0) {
        nextSum = prevSum - terminate;
    } else {
        nextSum = prevSum + terminate;
    }
    double differenceBetweenSums = nextSum - prevSum;

    if (n_iter > 0) {
        for (unsigned int i = 0; i < n_iter; ++i) {
            applyFunctionOnGrid(function, grid, n, m, sources, num_sources, is_cyclic, &prevSum,
                                &nextSum, &differenceBetweenSums);
        }
    } else {
        while (isAbsLessThan(differenceBetweenSums, terminate) == FALSE) {
            applyFunctionOnGrid(function, grid, n, m, sources, num_sources, is_cyclic, &prevSum,
                                &nextSum, &differenceBetweenSums);
        }
    }
    return differenceBetweenSums;
}