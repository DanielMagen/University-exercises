/**
 * @file my_cos.c
 * @author Daniel Magen
 * @version 1.0
 *
 * @brief receives a number in radians and prints its cos value
 *
 * @section DESCRIPTION
 * uses the formula we were given to calculate the cos value of a double number
 * if receives any other inputs prints an error message and exits
 *
 * Input  : no command line input
 * Process: receives a single double number
 * Output : the given number cos value
 */

// ------------------------------ includes ------------------------------
#include <stdio.h>

// -------------------------- const definitions -------------------------
#define MINIMUM_VALUE_TO_RETURN_ITSELF_IN_SIN 0.01
#define ERROR 1
#define EXPECTED_NUMBER_OF_INPUTS 1
#define INVALID_INPUT "the given input is not valid"
#define PI 3.141529

// ------------------------------ functions -----------------------------

/**
 *
 * @brief receives a number and a power and return number^power
 * @param num the number to multiply
 * @param power the number of times to multiply the number
 * @return number^power
 */
static double power(double num, int power);

/**
 * @brief receives a number in radians and returns its sin value
 * @param number a double
 * @return number sin value
 */
static double sin(double number);

/**
 * @brief receives a number in radians and returns its cos value
 * @param number a double
 * @return number cos value
 */
static double cos(double number);

/**
 * @brief The main function, receives a valid double number and prints its
 * cos value.
 * @return 0, to tell the system the execution ended without errors, 1 otherwise.
 */
int main() {
    int amountOfNumbersGiven;
    double numberGiven;
    amountOfNumbersGiven = scanf("%lf", &numberGiven);
    if (amountOfNumbersGiven != EXPECTED_NUMBER_OF_INPUTS) {
        fprintf(stderr, INVALID_INPUT);
        return ERROR;
    }

    numberGiven = cos(numberGiven);
    printf("%lf", numberGiven);

    return 0;
}

static double power(double num, int power) {
    double result = num;
    for (int var = 1; var < power; ++var) {
        result = result * num;
    }

    return result;
}

static double sin(double number) {
    double multiplyResultBy = 1.0;

    if (number < 0) {
        multiplyResultBy = -1.0;
        number = number * multiplyResultBy;

    }

    if (number < MINIMUM_VALUE_TO_RETURN_ITSELF_IN_SIN) {
        return multiplyResultBy * number;
    }

    double sinOfValueDividedBy3 = sin(number / 3.0);
    double result = 3.0 * sinOfValueDividedBy3 - 4.0 * power(sinOfValueDividedBy3, 3);
    return multiplyResultBy * result;
}

static double cos(double number) {
    return sin((PI / 2.0) + number);
}
