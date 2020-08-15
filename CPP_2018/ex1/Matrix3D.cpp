//
// Created by Daniel on 08/12/18.
//

#include "Matrix3D.h"

using namespace std;

// --------------------------------------------------------------------------------------
// This file contains the implementation of the class Matrix3D.
// --------------------------------------------------------------------------------------

/**
 * a constructor
 * initializes the matrix to 0
 */
Matrix3D::Matrix3D() {
    for (int i = 0; i < S_DIMENSION; ++i) {
        _lines[i] = *(new Vector3D());
    }
}

/**
 * a constructor
 * initializes the matrix to have the given number
 * in its diagonal and sets the rest of the matrix to 0
 * @param number a double number
 */
Matrix3D::Matrix3D(double number) : Matrix3D() {
    for (int i = 0; i < S_DIMENSION; ++i) {
        _lines[i][i] = number;
    }
}

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
Matrix3D::Matrix3D(double num00, double num01, double num02,
                   double num10, double num11, double num12,
                   double num20, double num21, double num22) : Matrix3D() {
    _lines[0][0] = num00;
    _lines[0][1] = num01;
    _lines[0][2] = num02;
    _lines[1][0] = num10;
    _lines[1][1] = num11;
    _lines[1][2] = num12;
    _lines[2][0] = num20;
    _lines[2][1] = num21;
    _lines[2][2] = num22;
}

/**
 *  a constructor
 * @param newValues the wanted values
 */
Matrix3D::Matrix3D(double newValues[9]) : Matrix3D() {
    for (int i = 0; i < S_DIMENSION; ++i) {
        for (int j = 0; j < S_DIMENSION; ++j) {
            _lines[i][j] = newValues[(i * S_DIMENSION) + j];
        }
    }
}

/**
 *  a constructor
 * @param newValues the wanted values
 */
Matrix3D::Matrix3D(double newValues[3][3]) : Matrix3D() {
    for (int i = 0; i < S_DIMENSION; ++i) {
        for (int j = 0; j < S_DIMENSION; ++j) {
            _lines[i][j] = newValues[i][j];
        }
    }
}

/**
 * a constructor
 * @param vec0 a Vector3D object
 * @param vec1 a Vector3D object
 * @param vec2 a Vector3D object
 */
Matrix3D::Matrix3D(Vector3D &vec0, Vector3D &vec1, Vector3D &vec2) {
    _lines[0] = Vector3D(vec0);
    _lines[1] = Vector3D(vec1);
    _lines[2] = Vector3D(vec2);
}

/**
 * a copy constructor
 * @param copyFrom the Matrix3D object to copy the data from
 */
Matrix3D::Matrix3D(const Matrix3D &copyFrom) {
    for (int i = 0; i < S_DIMENSION; ++i) {
        _lines[i] = copyFrom._lines[i];
    }
}

/**
 * @param other another Matrix3D object
 * @return a reference to this Matrix3D which is the sum of both Matrix3D
 */
Matrix3D &Matrix3D::operator+=(const Matrix3D &other) {
    for (int i = 0; i < S_DIMENSION; ++i) {
        _lines[i] += other._lines[i];
    }
    return *this;
}

/**
 * @param other another Matrix3D object
 * @return a reference to this Matrix3D which is the subtraction of both Matrix3D
 */
Matrix3D &Matrix3D::operator-=(const Matrix3D &other) {
    for (int i = 0; i < S_DIMENSION; ++i) {
        _lines[i] -= other._lines[i];
    }
    return *this;
}

/**
 * @param other a Matrix3D object
 * @return a Matrix3D object which is the result of multiplying
 * this matrix by the other matrix
 */
Matrix3D &Matrix3D::operator*=(const Matrix3D other) {
    Matrix3D newMatrix;
    for (int i = 0; i < S_DIMENSION; ++i) {
        for (int j = 0; j < S_DIMENSION; ++j) {
            newMatrix._lines[i][j] = this->row(i) * other.column(j);
        }
    }

    *this = newMatrix;
    return *this;
}

/**
 * @param mat2 a Matrix3D object
 * @return the result of this matrix + mat 2
 */
Matrix3D Matrix3D::operator+(const Matrix3D &mat2) const {
    Matrix3D newMatrix(*this);
    newMatrix += mat2;
    return newMatrix;
}

/**
 * @param mat2 a Matrix3D object
 * @return the result of this*mat2
 */
Matrix3D Matrix3D::operator*(const Matrix3D &mat2) const {
    Matrix3D newMatrix(*this);
    return (newMatrix *= mat2);
}

/**
     * @param mat2 a Matrix3D object
     * @return the result of this-mat2
     */
Matrix3D Matrix3D::operator-(const Matrix3D &mat2) const {
    Matrix3D newMatrix(*this);
    newMatrix -= mat2;
    return newMatrix;
}

/**
 * @param number the number to multiply the matrix values by
 * @return a reference to this Matrix3D
 */
Matrix3D &Matrix3D::operator*=(const double number) {
    for (int i = 0; i < S_DIMENSION; ++i) {
        _lines[i] *= number;
    }
    return *this;
}

/**
 * @param number the number to divide the matrix values by
 * @return a reference to this Matrix3D
 */
Matrix3D &Matrix3D::operator/=(const double number) {
    if (number == 0) {
        cerr << DIVISION_BY_ZERO;
    } else {
        for (int i = 0; i < S_DIMENSION; ++i) {
            _lines[i] /= number;
        }
    }
    return *this;
}

/**
 * @param vec a Vector3D object
 * @return a Vector3D object which is the result of multiplying
 * this matrix by vec
 */
Vector3D Matrix3D::operator*(const Vector3D &vec) const {
    Vector3D newVec;
    for (int i = 0; i < S_DIMENSION; ++i) {
        newVec[i] = _lines[i] * vec;
    }
    return newVec;
}

/**
 * reads the matrix from the input stream
 * @param input the input stream
 * @param matrix the matrix to insert the values into
 * @return the input stream
 */
istream &operator>>(istream &input, Matrix3D &mat) {
    input >> mat._lines[0] >> mat._lines[1] >> mat._lines[2];
    return input;
}

/**
 * prints the matrix to the output stream
 * @param output the output stream
 * @param matrix the matrix to print the values of
 * @return the output stream
 */
ostream &operator<<(ostream &output, const Matrix3D &matrix) {
    for (int i = 0; i < matrix.S_DIMENSION; ++i) {
        output << matrix._lines[i];
    }
    return output;
}

/**
* @param other a Matrix3D object
* @return a reference to this matrix which is the result of copying
 * all values of the given matrix
*/
Matrix3D &Matrix3D::operator=(const Matrix3D &other) {
    for (int i = 0; i < S_DIMENSION; ++i) {
        _lines[i] = other._lines[i];
    }
    return *this;
}

/**
 * @param index the line index in the matrix
 * @return the Vector3D line the user asked for
 */
Vector3D &Matrix3D::operator[](const int index) {
    if (index > S_DIMENSION || index < 0) {
        cerr << OUT_OF_BOUNDS;
        return _lines[0];
    } else {
        return _lines[index];
    }
}

/**
 * @param index the line index in the matrix
 * @return the Vector3D line the user asked for
 */
Vector3D Matrix3D::operator[](const int index) const {
    if (index > S_DIMENSION || index < 0) {
        cerr << OUT_OF_BOUNDS;
        return NULL;
    } else {
        return _lines[index];
    }
}

/**
 * @param index the line index in the matrix
 * @return the Vector3D line the user asked for
 */
Vector3D Matrix3D::row(const short index) const {
    return (*this)[index];
}

/**
 * @param index the column index in the matrix
 * @return the Vector3D column the user asked for
 */
Vector3D Matrix3D::column(const short index) const {
    Vector3D newVec;
    if (index > S_DIMENSION || index < 0) {
        cerr << OUT_OF_BOUNDS;
    } else {
        for (int i = 0; i < S_DIMENSION; ++i) {
            newVec[i] = _lines[i][index];
        }
    }
    return newVec;
}

/**
 * @return the trace of the matrix
 */
double Matrix3D::trace() const {
    double trace = 0;
    for (int i = 0; i < S_DIMENSION; ++i) {
        trace += _lines[i][i];
    }
    return trace;
}

/**
 * uses multiplication by diagonals to calculate the determinant
 * (add the result of multiplying the values of the \\\ diagonals and
 * subtract the result of multiplying the values of the /// diagonals)
 * @return the determinant of the matrix
 */
double Matrix3D::determinant() const {
    double determinant = 0;
    determinant += _lines[0][0] * _lines[1][1] * _lines[2][2];
    determinant += _lines[0][1] * _lines[1][2] * _lines[2][0];
    determinant += _lines[0][2] * _lines[1][0] * _lines[2][1];
    determinant -= _lines[2][0] * _lines[1][1] * _lines[0][2];
    determinant -= _lines[2][1] * _lines[1][2] * _lines[0][0];
    determinant -= _lines[2][2] * _lines[1][0] * _lines[0][1];
    return determinant;
}
