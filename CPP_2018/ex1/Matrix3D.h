//
// Created by Daniel on 08/12/18.
//

#ifndef EX1_MATRIX3D_H
#define EX1_MATRIX3D_H

#include "Vector3D.h"
#include <iostream>

/**
 * a 3X3 matrix class
 * enabling various operations to be used on the matrices
 */
class Matrix3D {
public:
    /**
     * a constructor
     * initializes the matrix to 0
     */
    Matrix3D();

    /**
     * a constructor
     * initializes the matrix to have the given number
     * in its diagonal and sets the rest of the matrix to 0
     * @param number a double number
     */
    Matrix3D(double number);


    /**
     * a constructor
     * initializes the matrix by the given numbers
     * @param num00 the number in the [0][0] place
     * @param num01 the number in the [0][1] place
     * @param num02 the number in the [0][2] place
     * @param num10 the number in the [1][0] place
     * @param num11 the number in the [1][1] place
     * @param num12 the number in the [1][2] place
     * @param num20 the number in the [2][0] place
     * @param num21 the number in the [2][1] place
     * @param num22 the number in the [2][2] place
     */
    Matrix3D(double num00, double num01, double num02,
             double num10, double num11, double num12,
             double num20, double num21, double num22);

    /**
     *  a constructor
     * @param newValues the wanted values
     */
    Matrix3D(double newValues[9]);

    /**
     *  a constructor
     * @param newValues the wanted values
     */
    Matrix3D(double newValues[3][3]);

    /**
     * a constructor
     * @param vec0 a Vector3D object
     * @param vec1 a Vector3D object
     * @param vec2 a Vector3D object
     */
    Matrix3D(Vector3D &vec0, Vector3D &vec1, Vector3D &vec2);

    /**
     * a copy constructor
     * @param copyFrom the Matrix3D object to copy the data from
     */
    Matrix3D(const Matrix3D &copyFrom);

    /**
     * @param other another Matrix3D object
     * @return a reference to this Matrix3D which is the sum of both Matrix3D
     */
    Matrix3D &operator+=(const Matrix3D &other);

    /**
     * @param other another Matrix3D object
     * @return a reference to this Matrix3D which is the subtraction of both Matrix3D
     */
    Matrix3D &operator-=(const Matrix3D &other);

    /**
     * @param other a Matrix3D object
     * @return a Matrix3D object which is the result of multiplying
     * this matrix by the other matrix
     */
    Matrix3D &operator*=(const Matrix3D other);

    /**
     * @param mat2 a Matrix3D object
     * @return the result of this matrix + mat 2
     */
    Matrix3D operator+(const Matrix3D &mat2) const;

    /**
     * @param mat2 a Matrix3D object
     * @return the result of this*mat2
     */
    Matrix3D operator*(const Matrix3D &mat2) const;

    /**
     * @param mat2 a Matrix3D object
     * @return the result of this-mat2
     */
    Matrix3D operator-(const Matrix3D &mat2) const;

    /**
     * @param number the number to multiply the matrix values by
     * @return a reference to this Matrix3D
     */
    Matrix3D &operator*=(const double number);

    /**
     * @param number the number to divide the matrix values by
     * @return a reference to this Matrix3D
     */
    Matrix3D &operator/=(const double number);

    /**
     * @param vec a Vector3D object
     * @return a Vector3D object which is the result of multiplying
     * this matrix by vec
     */
    Vector3D operator*(const Vector3D &vec) const;

    /**
     * reads the matrix from the input stream
     * @param input the input stream
     * @param matrix the matrix to insert the values into
     * @return the input stream
     */
    friend std::istream &operator>>(std::istream &input, Matrix3D &matrix);

    /**
     * prints the matrix to the output stream
     * @param output the output stream
     * @param matrix the matrix to print the values of
     * @return the output stream
     */
    friend std::ostream &operator<<(std::ostream &output, const Matrix3D &matrix);

    /**
    * @param other a Matrix3D object
    * @return a reference to this matrix which is the result of copying
     * all values of the given matrix
    */
    Matrix3D &operator=(const Matrix3D &other);

    /**
     * @param index the line index in the matrix
     * @return the Vector3D line the user asked for
     */
    Vector3D &operator[](const int index);

    /**
     * @param index the line index in the matrix
     * @return the Vector3D line the user asked for
     */
    Vector3D operator[](const int index) const;

    /**
     * @param index the line index in the matrix
     * @return the Vector3D line the user asked for
     */
    Vector3D row(const short index) const;

    /**
     * @param index the column index in the matrix
     * @return the Vector3D column the user asked for
     */
    Vector3D column(const short index) const;

    /**
     * @return the trace of the matrix
     */
    double trace() const;

    /**
     * @return the determinant of the matrix
     */
    double determinant() const;

private:
    static const int S_DIMENSION = 3; // the matrix dimensions
    Vector3D _lines[S_DIMENSION]; // the matrix values, each Vector3D will be a new line in the matrix

    std::string DIVISION_BY_ZERO = "can't divide by zero\n";
    std::string OUT_OF_BOUNDS = "the given index is out of bounds\n";
};

#endif //EX1_MATRIX3D_H
