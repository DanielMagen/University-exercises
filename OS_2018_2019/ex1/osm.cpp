#include <iostream>
#include <sys/time.h>
#include "stdio.h"
#include "osm.h"

#define ERROR_MESSAGE "the program should receive a single positive integer"
#define ERROR_RETURN -1
#define DEFAULT_NUMBER_OF_RUNS 1000
timeval startTime; // will contain the start time of the operation
timeval endTime; // will contain the end time of the operation
int divisionFactor = 10;

/* Initialization function that the user must call
 * before running any other library function.
 * The function may, for example, allocate memory or
 * create/open files.
 * Pay attention: this function may be empty for some desings. It's fine.
 * Returns 0 uppon success and -1 on failure
 */
int osm_init() {
    return 0;
}


/* finalizer function that the user must call
 * after running any other library function.
 * The function may, for example, free memory or
 * close/delete files.
 * Returns 0 uppon success and -1 on failure
 */
int osm_finalizer() {
    return 0;
}


/* Time measurement function for a simple arithmetic operation.
   returns time in nano-seconds upon success,
   and -1 upon failure.
   */
double osm_operation_time(unsigned int iterations) {
    if (iterations == 0) {
        iterations = DEFAULT_NUMBER_OF_RUNS;
    }

    int temp = 0;
    if (gettimeofday(&startTime, nullptr) == -1) {
        return -1;
    }
    for (unsigned int i = 0; i <= iterations; i += divisionFactor) {
        temp = 1 + 1;
        temp = 1 + temp;
        temp = 1 + temp;
        temp = 1 + temp;
        temp = 1 + temp;
        temp = 1 + temp;
        temp = 1 + temp;
        temp = 1 + temp;
        temp = 1 + temp;
        temp = 1 + temp;
    }

    if (gettimeofday(&endTime, nullptr) == -1) {
        return -1;
    }

    double resultsWithLoop = endTime.tv_sec * 1000000 + endTime.tv_usec;
    resultsWithLoop = resultsWithLoop - (startTime.tv_sec * 1000000 + startTime.tv_usec);
    resultsWithLoop = resultsWithLoop / iterations;


    // now run only the loop and subtract the loop running time to get only the operation running time
    if (gettimeofday(&startTime, nullptr) == -1) {
        return -1;
    }
    for (unsigned int i = 0; i <= iterations; i += divisionFactor) {
    }

    if (gettimeofday(&endTime, nullptr) == -1) {
        return -1;
    }

    double onlyLoop = endTime.tv_sec * 1000000 + endTime.tv_usec;
    onlyLoop = onlyLoop - (startTime.tv_sec * 1000000 + startTime.tv_usec);
    onlyLoop = onlyLoop / iterations;

    return (resultsWithLoop - onlyLoop) * 1000; // turn microseconds to nanoseconds
}


void emptyFunction() {
}

/* Time measurement function for an empty function call.
   returns time in nano-seconds upon success,
   and -1 upon failure.
   */
double osm_function_time(unsigned int iterations) {
    if (iterations == 0) {
        iterations = DEFAULT_NUMBER_OF_RUNS;
    }

    if (gettimeofday(&startTime, nullptr) == -1) {
        return -1;
    }
    for (unsigned int i = 0; i <= iterations; i += divisionFactor) {
        emptyFunction();
        emptyFunction();
        emptyFunction();
        emptyFunction();
        emptyFunction();
        emptyFunction();
        emptyFunction();
        emptyFunction();
        emptyFunction();
        emptyFunction();
    }

    if (gettimeofday(&endTime, nullptr) == -1) {
        return -1;
    }

    double resultsWithLoop = endTime.tv_sec * 1000000 + endTime.tv_usec;
    resultsWithLoop = resultsWithLoop - (startTime.tv_sec * 1000000 + startTime.tv_usec);
    resultsWithLoop = resultsWithLoop / iterations;


    // now run only the loop and subtract the loop running time to get only the operation running time
    if (gettimeofday(&startTime, nullptr) == -1) {
        return -1;
    }
    for (unsigned int i = 0; i <= iterations; i += divisionFactor) {
    }

    if (gettimeofday(&endTime, nullptr) == -1) {
        return -1;
    }


    double onlyLoop = endTime.tv_sec * 1000000 + endTime.tv_usec;
    onlyLoop = onlyLoop - (startTime.tv_sec * 1000000 + startTime.tv_usec);
    onlyLoop = onlyLoop / iterations;

    return (resultsWithLoop - onlyLoop) * 1000; // turn microseconds to nanoseconds

}

double osm_syscall_time(unsigned int iterations) {
    if (iterations == 0) {
        iterations = DEFAULT_NUMBER_OF_RUNS;
    }

    if (gettimeofday(&startTime, nullptr) == -1) {
        return -1;
    }
    for (unsigned int i = 0; i <= iterations; i += divisionFactor) {
        OSM_NULLSYSCALL;
        OSM_NULLSYSCALL;
        OSM_NULLSYSCALL;
        OSM_NULLSYSCALL;
        OSM_NULLSYSCALL;
        OSM_NULLSYSCALL;
        OSM_NULLSYSCALL;
        OSM_NULLSYSCALL;
        OSM_NULLSYSCALL;
        OSM_NULLSYSCALL;
    }

    if (gettimeofday(&endTime, nullptr) == -1) {
        return -1;
    }

    double resultsWithLoop = endTime.tv_sec * 1000000 + endTime.tv_usec;
    resultsWithLoop = resultsWithLoop - (startTime.tv_sec * 1000000 + startTime.tv_usec);
    resultsWithLoop = resultsWithLoop / iterations;


    // now run only the loop and subtract the loop running time to get only the operation running time
    if (gettimeofday(&startTime, nullptr) == -1) {
        return -1;
    }
    for (unsigned int i = 0; i <= iterations; i += divisionFactor) {
    }

    if (gettimeofday(&endTime, nullptr) == -1) {
        return -1;
    }


    double onlyLoop = endTime.tv_sec * 1000000 + endTime.tv_usec;
    onlyLoop = onlyLoop - (startTime.tv_sec * 1000000 + startTime.tv_usec);
    onlyLoop = onlyLoop / iterations;

    return (resultsWithLoop - onlyLoop) * 1000; // turn microseconds to nanoseconds
}

