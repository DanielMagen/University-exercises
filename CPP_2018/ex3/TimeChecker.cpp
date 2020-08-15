/**
 * this file is used to calculate and compare
 * our matrix implementation operation time and
 * the eigen library operation time
 */
#include <eigen3/Eigen/Dense>
#include <string>
#include <cstdlib>
#include <cassert>
#include <cstdio>
#include <cstring>
#include <fstream>
#include <iostream>
#include <vector>
#include <stack>
#include <ctime>
#include <chrono>
#include "Complex.h"
#include "Matrix.hpp"


#define MAX 500
#define MIN 1
#define EXPECTED_NUMBER_ARGUMENTS 2
#define USAGE_ERROR "should be given a number between 1 and 500"
#define ERROR_VALUE_MSG "the number should be between 1 and 500"

//std::stack<clock_t> tictoc_stack;
std::stack <std::chrono::time_point<std::chrono::system_clock>> tictoc_stack;

/**
 * tic method from the given TimeChecker file
 */
void tic() {
    tictoc_stack.push(std::chrono::system_clock::now());
}

/**
 * toc method from the given TimeChecker file
 */
void toc() {
    std::chrono::duration<double> elapsed_seconds =
            std::chrono::system_clock::now() - tictoc_stack.top();
    std::cout << elapsed_seconds.count() << std::endl;
    tictoc_stack.pop();
}

/**
 * main function
 * @param argc number of arguments given
 * @param argv arguments given
 * @return 0 if went as planned -1 otherwise
 */
int main(int argc, char *argv[]) {
    if (argc != EXPECTED_NUMBER_ARGUMENTS) {
        std::cerr << USAGE_ERROR << std::endl;
        exit(-1);
    }

    std::string givenNumberString = argv[EXPECTED_NUMBER_ARGUMENTS - 1];
    unsigned int givenNumber = std::stoi(givenNumberString);

    if (givenNumber > MAX || givenNumber < MIN) {
        std::cerr << ERROR_VALUE_MSG;
        exit(-1);
    }

    Eigen::MatrixXd eigenMatrix1 = Eigen::MatrixXd::Random(givenNumber, givenNumber);
    Eigen::MatrixXd eigenMatrix2 = Eigen::MatrixXd::Random(givenNumber, givenNumber);
    std::vector<int> values(givenNumber * givenNumber, 1);
    Matrix<int> regularMatrix(givenNumber, givenNumber, values);

    // the given matrix size
    std::cout << "size " << givenNumber << "\n";

    //multiply 2 eigen matrices
    std::cout << "eigen mult ";
    tic();
    eigenMatrix1 * eigenMatrix2;
    toc();

    //add 2 eigen matrices
    std::cout << "eigen add ";
    tic();
    eigenMatrix1 + eigenMatrix2;
    toc();

    //multiply 2 regular matrices
    std::cout << "matlib mult ";
    tic();
    try {
        regularMatrix * regularMatrix;
    }
    catch (std::exception &err) {
        std::cerr << err.what() << std::endl;
    }
    toc();

    //add 2 regular matrices
    std::cout << "matlib add ";
    tic();
    try {
        regularMatrix + regularMatrix;
    }
    catch (std::exception &err) {
        std::cerr << err.what() << std::endl;
    }
    toc();

    return 0;
}