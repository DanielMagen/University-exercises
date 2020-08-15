#include "Vector3D.h"
#include "Matrix3D.h"

#include <iostream>

/**
 * the main function
 */
int main() {

    Vector3D a(3.0, 2.0, 5.0);
    std::cout << "a.norm = " << a.norm() << std::endl;
    Vector3D b(7.0, 1.0, 0.0);
    std::cout << "a.dist(b) = " << a.dist(b) << std::endl;
    Vector3D c(5.0, 1.0, 4.0);

    Matrix3D m(a, b, c);
    std::cout << "Matrix m = \n" << m << std::endl;
    std::cout << "m.determinant = " << m.determinant() << std::endl;
    std::cout << "m*a = " << m * a << std::endl;
    return 0;
}