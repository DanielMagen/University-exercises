//
// Created by Daniel on 08/12/18.
//

#ifndef EX1_VECTOR3D_H
#define EX1_VECTOR3D_H

#include <iostream>
#include <string>

/**
 * a 3D vector class
 * enabling various operations to be used on the vectors
 */
class Vector3D {
public:
    /**
     * a constructor
     * initializes the vector to 0
     */
    Vector3D();

    /**
     * a constructor
     * @param x the x coordinate
     * @param y the y coordinate
     * @param z the z coordinate
     */
    Vector3D(double x, double y, double z);

    /**
     *  a constructor
     * @param coordinates the wanted coordinates
     */
    Vector3D(double coordinates[3]);

    /**
     * a copy constructor
     * @param copyFrom the Vector3D object to copy the data from
     */
    Vector3D(const Vector3D &copyFrom);

    /**
     * @param other another Vector3D object
     * @return a new Vector3D which is the sum of both vectors
     */
    Vector3D operator+(const Vector3D &other) const;

    /**
     * @param other another Vector3D object
     * @return a new Vector3D which is the subtraction of both vectors
     */
    Vector3D operator-(const Vector3D &other) const;

    /**
     * @param other another Vector3D object
     * @return a reference to this vector which is the sum of both vectors
     */
    Vector3D &operator+=(const Vector3D &other);

    /**
     * @param other another Vector3D object
     * @return a reference to this vector which is the subtraction of both vectors
     */
    Vector3D &operator-=(const Vector3D &other);

    /**
     * @param number a double number
     * @return a reference to this vector which is the sum the vector
     * and the number
     */
    Vector3D &operator+=(const double number);

    /**
     * @param number another Vector3D object
     * @return a reference to this vector which is the subtraction
     * of the number from the vector
     */
    Vector3D &operator-=(const double number);

    /**
     * @return a new Vector3D which is the minus of the current vectors
     */
    Vector3D operator-() const;

    /**
     * @param number a double number
     * @return a new Vector3D which is the result of multiplying
     * all coordinates by the given number
     */
    Vector3D operator*(const double number) const;

    /**
     * @param number a double number
     * @return a new Vector3D which is the result of dividing
     * all coordinates by the given number
     */
    Vector3D operator/(const double number) const;

    /**
     * @param number a double number
     * @param vector a Vector3D object
     * @return a new Vector3D which is the result of multiplying
     * all coordinates of vector by the given number
     */
    friend Vector3D operator*(const double number, const Vector3D &vector);

    /**
     * @param number a double number
     * @return a reference to this vector which is the result of multiplying
     * all coordinates by the given number
     */
    Vector3D &operator*=(const double number);

    /**
     * @param number another Vector3D object
     * @return a reference to this vector which is the result of dividing
     * all coordinates by the given number
     */
    Vector3D &operator/=(const double number);

    /**
     * @param other a Vector3D object
     * @return the distance between this vector and other
     */
    double operator|(const Vector3D &other) const;

    /**
     * @param other a Vector3D object
     * @return the scalar product between the current vector and other
     */
    double operator*(const Vector3D &other) const;

    /**
     * @param other a Vector3D object
     * @return the angle in radians between the current vector and other
     */
    double operator^(const Vector3D &other) const;

    /**
     * reads the vector from the input stream
     * @param input the input stream
     * @param vector the vector to insert the values into
     * @return the input stream
     */
    friend std::istream &operator>>(std::istream &input, Vector3D &vector);

    /**
     * prints the vector to the output stream
     * @param output the output stream
     * @param vector the vector to print the values of
     * @return the output stream
     */
    friend std::ostream &operator<<(std::ostream &output, const Vector3D &vector);

    /**
    * @param other a Vector3D object
    * @return a reference to this vector which is the result of copying
    * all coordinates of the given vector
    */
    Vector3D &operator=(const Vector3D &other);

    /**
     * @param index the index in the vector
     * @return the coordinate the user asked for
     */
    double &operator[](const int index);

    /**
     * @param index the index in the vector
     * @return the coordinate the user asked for
     */
    double operator[](const int index) const;

    /**
    * @return the length of the vector
    */
    double norm() const;

    /**
    * @param other a Vector3D object
    * @return the distance between this vector and the other vector
    */
    double dist(const Vector3D &other) const;

private:
    static const int S_DIMENSION = 3; // the vector dimension
    double _coordinates[S_DIMENSION]; // the vector coordinates

    std::string DIVISION_BY_ZERO = "can't divide by zero\n";
    std::string ZERO_VECTOR_NO_ANGLE = "the angle is not defined for the zero vector\n";
    std::string OUT_OF_BOUNDS = "the given index is out of bounds\n";

    /**
    * @return true if this vector is the zero vector
    */
    bool _isZero() const;
};

#endif //EX1_VECTOR3D_H
