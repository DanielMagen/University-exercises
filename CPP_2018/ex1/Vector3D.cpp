//
// Created by Daniel on 08/12/18.
//

#include "Vector3D.h"
#include <cmath>

using namespace std;

// --------------------------------------------------------------------------------------
// This file contains the implementation of the class Vector3D.
// --------------------------------------------------------------------------------------

/**
 * a constructor
 * initializes the vector to 0
 */
Vector3D::Vector3D() {
    for (int i = 0; i < S_DIMENSION; ++i) {
        _coordinates[i] = 0;
    }
}

/**
 * a constructor
 * @param x the x coordinate
 * @param y the y coordinate
 * @param z the z coordinate
 */
Vector3D::Vector3D(double x, double y, double z) {
    _coordinates[0] = x;
    _coordinates[1] = y;
    _coordinates[2] = z;
}

/**
 *  a constructor
 * @param coordinates the wanted coordinates
 */
Vector3D::Vector3D(double coordinates[3]) : Vector3D(coordinates[0], coordinates[1], coordinates[2]) {}

/**
 * a copy constructor
 * @param copyFrom the Vector3D object to copy the data from
 */
Vector3D::Vector3D(const Vector3D &copyFrom) {
    for (int i = 0; i < S_DIMENSION; ++i) {
        _coordinates[i] = copyFrom._coordinates[i];
    }
}

/**
 * @param other another Vector3D object
 * @return a new Vector3D which is the sum of both vectors
 */
Vector3D Vector3D::operator+(const Vector3D &other) const {
    Vector3D newVec;
    newVec += *this;
    newVec += other;
    return newVec;
}

/**
 * @param other another Vector3D object
 * @return a new Vector3D which is the subtraction of both vectors
 */
Vector3D Vector3D::operator-(const Vector3D &other) const {
    Vector3D newVec;
    newVec += *this;
    newVec -= other;
    return newVec;
}

/**
 * @param other another Vector3D object
 * @return a reference to this vector which is the sum of both vectors
 */
Vector3D &Vector3D::operator+=(const Vector3D &other) {
    for (int i = 0; i < S_DIMENSION; ++i) {
        _coordinates[i] += other._coordinates[i];
    }
    return *this;
}

/**
 * @param other another Vector3D object
 * @return a reference to this vector which is the subtraction of both vectors
 */
Vector3D &Vector3D::operator-=(const Vector3D &other) {
    for (int i = 0; i < S_DIMENSION; ++i) {
        _coordinates[i] -= other._coordinates[i];
    }
    return *this;
}

/**
 * @param number a double number
 * @return a reference to this vector which is the sum the vector
 * and the number
 */
Vector3D &Vector3D::operator+=(const double number) {
    for (int i = 0; i < S_DIMENSION; ++i) {
        _coordinates[i] += number;
    }
    return *this;
}

/**
 * @param number another Vector3D object
 * @return a reference to this vector which is the subtraction
 * of the number from the vector
 */
Vector3D &Vector3D::operator-=(const double number) {
    for (int i = 0; i < S_DIMENSION; ++i) {
        _coordinates[i] -= number;
    }
    return *this;
}

/**
 * @return a new Vector3D which is the minus of the current vectors
 */
Vector3D Vector3D::operator-() const {
    Vector3D newVec;
    newVec += *this;
    for (int i = 0; i < S_DIMENSION; ++i) {
        newVec._coordinates[i] = -newVec._coordinates[i];
    }
    return newVec;
}

/**
 * @param number a double number
 * @return a new Vector3D which is the result of multiplying
 * all coordinates by the given number
 */
Vector3D Vector3D::operator*(const double number) const {
    Vector3D newVec;
    newVec += *this;
    for (int i = 0; i < S_DIMENSION; ++i) {
        newVec._coordinates[i] *= number;
    }
    return newVec;
}

/**
 * @param number a double number
 * @return a new Vector3D which is the result of dividing
 * all coordinates by the given number
 */
Vector3D Vector3D::operator/(const double number) const {
    Vector3D newVec;
    newVec += *this;
    newVec /= number;
    return newVec;
}

/**
 * @param number a double number
 * @param vector a Vector3D object
 * @return a new Vector3D which is the result of multiplying
 * all coordinates of vector by the given number
 */
Vector3D operator*(const double number, const Vector3D &vector) {
    Vector3D newVec;
    newVec += vector;
    newVec *= number;
    return newVec;
}

/**
 * @param number a double number
 * @return a reference to this vector which is the result of multiplying
 * all coordinates by the given number
 */
Vector3D &Vector3D::operator*=(const double number) {
    for (int i = 0; i < S_DIMENSION; ++i) {
        _coordinates[i] *= number;
    }
    return *this;
}

/**
 * @param number another Vector3D object
 * @return a reference to this vector which is the result of dividing
 * all coordinates by the given number
 */
Vector3D &Vector3D::operator/=(const double number) {
    if (number == 0) {
        cerr << DIVISION_BY_ZERO;
    } else {
        for (int i = 0; i < S_DIMENSION; ++i) {
            _coordinates[i] /= number;
        }

    }
    return *this;
}

/**
 * @param other a Vector3D object
 * @return the distance between this vector and other
 */
double Vector3D::operator|(const Vector3D &other) const {
    return this->dist(other);
}

/**
 * @param other a Vector3D object
 * @return the scalar product between the current vector and other
 */
double Vector3D::operator*(const Vector3D &other) const {
    double scalarProduct = 0;
    for (int i = 0; i < S_DIMENSION; ++i) {
        scalarProduct += _coordinates[i] * other._coordinates[i];
    }
    return scalarProduct;
}

/**
 * @param other a Vector3D object
 * @return the angle in radians between the current vector and other
 */
double Vector3D::operator^(const Vector3D &other) const {
    if ((*this)._isZero() || other._isZero()) {
        cerr << ZERO_VECTOR_NO_ANGLE;
        return 0;
    } else {
        double angle;
        angle = *this * other;
        angle = angle / this->norm();
        angle = angle / other.norm();
        return acos(angle);
    }
}

/**
 * reads the vector from the input stream
 * @param input the input stream
 * @param vector the vector to insert the values into
 * @return the input stream
 */
istream &operator>>(istream &input, Vector3D &vector) {
    input >> vector._coordinates[0] >> vector._coordinates[1] >> vector._coordinates[2];
    return input;
}

/**
 * prints the vector to the output stream
 * @param output the output stream
 * @param vector the vector to print the values of
 * @return the output stream
 */
ostream &operator<<(ostream &output, const Vector3D &vector) {
    char SEPARATOR = ' ';
    for (int i = 0; i < vector.S_DIMENSION - 1; ++i) {
        output << vector._coordinates[i] << SEPARATOR;
    }
    output << vector._coordinates[vector.S_DIMENSION - 1] << endl;
    return output;
}

/**
* @param other a Vector3D object
* @return a reference to this vector which is the result of copying
* all coordinates of the given vector
*/
Vector3D &Vector3D::operator=(const Vector3D &other) {
    for (int i = 0; i < S_DIMENSION; ++i) {
        _coordinates[i] = other._coordinates[i];
    }
    return *this;
}

/**
 * @param index the index in the vector
 * @return the coordinate the user asked for
 */
double &Vector3D::operator[](const int index) {
    if (index > S_DIMENSION || index < 0) {
        cerr << OUT_OF_BOUNDS;
        return _coordinates[0];
    } else {
        return _coordinates[index];
    }
}

/**
 * @param index the index in the vector
 * @return the coordinate the user asked for
 */
double Vector3D::operator[](const int index) const {
    if (index > S_DIMENSION || index < 0) {
        cerr << OUT_OF_BOUNDS;
        return _coordinates[0];
    } else {
        return _coordinates[index];
    }
}

/**
 * @return the length of the vector
 */
double Vector3D::norm() const {
    double norm = 0;
    for (int i = 0; i < S_DIMENSION; ++i) {
        norm += _coordinates[i] * _coordinates[i];
    }
    return sqrt(norm);
}

/**
 *
 * @param other a Vector3D object
 * @return the distance between this vector and the other vector
 */
double Vector3D::dist(const Vector3D &other) const {
    Vector3D dis;
    dis += *this;
    dis -= other;
    return dis.norm();
}

/**
 * @return true if this vector is the zero vector
 */
bool Vector3D::_isZero() const {
    for (int i = 0; i < S_DIMENSION; ++i) {
        if (_coordinates[i] != 0) {
            return false;
        }
    }
    return true;
}