/**
 * a generic Matrix class
 */
#include <vector>
#include <iostream>
#include "Complex.h"

#define DEFAULT_SIZE 1
#define PRINTING_SEPARATOR "\t"

#define ERROR_SIZE_MSG "the matrix size cannot be less than 1"
#define ERROR_CELLS_MSG "the cells given do not contain enough items"
#define ERROR_MATCH_SIZE_MSG "the sizes of the given matrices do not match"
#define ERROR_SQUARE_MSG "the matrix should be a square matrix"
#define ERROR_RANGE_MSG "the given coordinates are outside the matrix range"

/**
 * a generic class which holds and operates on a matrix object
 * @tparam T the type of the matrix
 */
template<class T>
class Matrix {

private:
    unsigned int _rows;
    unsigned int _cols;
    std::vector <T> _values;

    /**
     * throws an invalid_argument if the size of the other matrix does
     * not match the size of this matrix
     * @param other another matrix object
     * @throws invalid_argument if other size does not match this matrix size
     */
    void _checkSizesMatch(const Matrix<T> &other) const;

public:
    typedef typename std::vector<T>::const_iterator const_iterator;

    /**
     * default constructor
     */
    Matrix();

    /**
     * creates a new matrix with 0s
     * @param rows the number of rows in the created matrix
     * @param cols the number of cols in the created matrix
     * @throws invalid_argument if rows or cols are less than 1
     */
    Matrix(unsigned int rows, unsigned int cols);

    /**
     * copy constructor
     * @param other the matrix to copy from
     */
    Matrix(const Matrix<T> &other);

    /**
     * creates a new matrix with values given by the cells
     * @param rows the number of rows in the created matrix
     * @param cols the number of cols in the created matrix
     * @param cells contain the values to insert into the matrix
     * @throws invalid_argument if rows or cols are less than 1 or if the given vector
     * capacity is less than the expected size of the matrix
     */
    Matrix(unsigned int rows, unsigned int cols, const std::vector <T> &cells);

    /**
     * destructor
     */
    ~Matrix() = default;

    /**
     * copies other into this matrix
     * @param other the matrix to copy from
     * @return a reference to this matrix
     */
    Matrix<T> &operator=(const Matrix<T> &other);

    /**
     * @param other the matrix to add
     * @return the result of adding other to this matrix
     * @throws invalid_argument if other size does not match this matrix size
     */
    Matrix<T> operator+(const Matrix<T> &other) const;

    /**
     * @param other the matrix to subtract
     * @return the result of subtracting other from this matrix
     * @throws invalid_argument if other size does not match this matrix size
     */
    Matrix<T> operator-(const Matrix<T> &other) const;

    /**
     * @param other the matrix to multiply by
     * @return the result of this * other
     * @throws invalid_argument if this matrix rows does not equal other cols
     */
    Matrix<T> operator*(const Matrix<T> &other) const;

    /**
     * @param other the matrix to compare to
     * @return false if this matrix elements are different from other elements
     */
    bool operator==(const Matrix<T> &other) const;

    /**
     * @param other the matrix to compare to
     * @return true if this matrix elements are different from other elements
     */
    bool operator!=(const Matrix<T> &other) const;

    /**
     * @return the transpose of this matrix
     * @throws invalid_argument if this.rows != this.cols
     */
    Matrix<T> trans() const;

    /**
     * @return true if this.rows = this.cols
     */
    bool isSquareMatrix() const;

    /**
     * @tparam S the type of the given matrix
     * @param output the output stream
     * @param mat the matrix to print
     * @return the given output stream
     */
    template<class S>
    friend std::ostream &operator<<(std::ostream &output, const Matrix<S> &mat);

    /**
     * @param row the row coordinate of the requested element
     * @param col the col coordinate of the requested element
     * @return a const reference to the requested element
     * @throws out_of_range if the given coordinates are out of the matrix range
     */
    const T &operator()(unsigned int row, unsigned int col) const;

    /**
     * @param row the row coordinate of the requested element
     * @param col the col coordinate of the requested element
     * @return a reference to the requested element
     * @throws out_of_range if the given coordinates are out of the matrix range
     */
    T &operator()(unsigned int row, unsigned int col);

    /**
     * @return a starting iterator for the matrix
     */
    inline const_iterator begin() const {
        _values.cbegin();
    }

    /**
     * @return the ending iterator for the matrix
     */
    inline const_iterator end() const {
        _values.cend();
    }

    /**
     * @return the number of rows in the matrix
     */
    inline unsigned int rows() const {
        return _rows;
    }

    /**
     * @return the number of cols in the matrix
     */
    inline unsigned int cols() const {
        return _cols;
    }
};

// ------------------ implementation ------------------------
/**
 * throws an invalid_argument if the size of the other matrix does
 * not match the size of this matrix
 * @tparam T the type of the matrix
 * @param other another matrix object
 * @throws invalid_argument if other size does not match this matrix size
 */
template<class T>
void Matrix<T>::_checkSizesMatch(const Matrix<T> &other) const {
    if (_rows != other._rows || _cols != other._cols) {
        throw std::invalid_argument(ERROR_MATCH_SIZE_MSG);
    }
}

/**
 * default constructor
 * @tparam T the type of the matrix
 */
template<class T>
Matrix<T>::Matrix() : _rows(DEFAULT_SIZE),
                      _cols(DEFAULT_SIZE),
                      _values(DEFAULT_SIZE, T(0)) {
}


/**
 * creates a new matrix with 0s
 * @tparam T the type of the matrix
 * @param rows the number of rows in the created matrix
 * @param cols the number of cols in the created matrix
 * @throws invalid_argument if rows or cols are less than 1
 */
template<class T>
Matrix<T>::Matrix(unsigned int rows, unsigned int cols) : _rows(rows),
                                                          _cols(cols),
                                                          _values(rows * cols, T(0)) {
    if (rows == 0 || cols == 0) {
        throw std::invalid_argument(ERROR_SIZE_MSG);
    }
}

/**
 * copy constructor
 * @tparam T the type of the matrix
 * @param other the matrix to copy from
 */
template<class T>
Matrix<T>::Matrix(const Matrix<T> &other) : Matrix(other._rows, other._cols, other._values) {
}

/**
 * creates a new matrix with values given by the cells
 * @tparam T the type of the matrix
 * @param rows the number of rows in the created matrix
 * @param cols the number of cols in the created matrix
 * @param cells contain the values to insert into the matrix
 * @throws invalid_argument if rows or cols are less than 1 or if the given vector
 * capacity is less than the expected size of the matrix
 */
template<class T>
Matrix<T>::Matrix(unsigned int rows, unsigned int cols, const std::vector <T> &cells) : _rows(rows),
                                                                                        _cols(cols) {
    if (rows == 0 || cols == 0) {
        throw std::invalid_argument(ERROR_SIZE_MSG);
    }

    if (cells.capacity() < _rows * cols) {
        throw std::invalid_argument(ERROR_CELLS_MSG);
    }

    _values.reserve(rows * cols);
    for (auto it = cells.begin(); it != cells.end(); ++it) {
        _values.push_back(*it);
    }
}

/**
 * copies other into this matrix
 * @tparam T the type of the matrix
 * @param other the matrix to copy from
 * @return a reference to this matrix
 */
template<class T>
Matrix<T> &Matrix<T>::operator=(const Matrix<T> &other) {
    if (this != &other) {
        _rows = other._rows;
        _cols = other._cols;
        _values = other._values;
    }
    return *this;
}

/**
 * @tparam T the type of the matrix
 * @param other the matrix to add
 * @return the result of adding other to this matrix
 * @throws invalid_argument if other size does not match this matrix size
 */
template<class T>
Matrix<T> Matrix<T>::operator+(const Matrix<T> &other) const {
    _checkSizesMatch(other);
    Matrix<T> result(_rows, _cols);
    for (unsigned int i = 0; i < _values.size(); ++i) {
        result._values[i] = _values[i] + other._values[i];
    }
    return result;
}

/**
 * @tparam T the type of the matrix
 * @param other the matrix to subtract
 * @return the result of subtracting other from this matrix
 * @throws invalid_argument if other size does not match this matrix size
 */
template<class T>
Matrix<T> Matrix<T>::operator-(const Matrix<T> &other) const {
    _checkSizesMatch(other);
    Matrix<T> result(_rows, _cols);
    for (int i = 0; i < _values.size(); ++i) {
        result._values[i] = _values[i] - other._values[i];
    }
    return result;
}

/**
 * @tparam T the type of the matrix
 * @param other the matrix to multiply by
 * @return the result of this * other
 * @throws invalid_argument if this matrix rows does not equal other cols
 */
template<class T>
Matrix<T> Matrix<T>::operator*(const Matrix<T> &other) const {
    if (_cols != other._rows) {
        throw std::invalid_argument(ERROR_MATCH_SIZE_MSG);
    }

    Matrix<T> result(_rows, other._cols);
    unsigned int lResult = 0; // the index for the resulting matrix

    // use the iterative algorithm to calculate the resulting matrix
    for (unsigned int i = 0; i < _rows; ++i) {
        for (unsigned int j = 0; j < other._cols; ++j) {
            T sum(0);
            for (unsigned int k = 0; k < _cols; ++k) {
                sum += (*this)(i, k) * other(k, j);
            }

            result._values[lResult] = sum;
            ++lResult;
        }
    }

    return result;
}


/**
 * @tparam T the type of the matrix
 * @param other the matrix to compare to
 * @return false if this matrix elements are different from other elements
 */
template<class T>
bool Matrix<T>::operator==(const Matrix<T> &other) const {
    if (_rows != other._rows || _cols != other._cols) {
        return false;
    }

    for (auto it1 = _values.begin(), it2 = other._values.begin();
         it1 != _values.end(); ++it1, ++it2) {
        if (*it1 != *it2) {
            return false;
        }
    }

    return true;
}

/**
 * @tparam T the type of the matrix
 * @param other the matrix to compare to
 * @return true if this matrix elements are different from other elements
 */
template<class T>
bool Matrix<T>::operator!=(const Matrix<T> &other) const {
    return !(*this == other);
}

/**
 * @tparam T the type of the matrix
 * @return the transpose of this matrix
 * @throws invalid_argument if this.rows != this.cols
 */
template<class T>
Matrix<T> Matrix<T>::trans() const {
    if (!isSquareMatrix()) {
        throw std::invalid_argument(ERROR_SQUARE_MSG);
    }

    Matrix<T> result(_cols, _rows); // the transpose
    for (unsigned int row = 0; row < _rows; ++row) {
        for (unsigned int col = 0; col < _cols; ++col) {
            result(col, row) = (*this)(row, col);
        }
    }
    return result;
}

/**
 * @tparam T the type of the matrix
 * @return true if this.rows = this.cols
 */
template<class T>
bool Matrix<T>::isSquareMatrix() const {
    return _rows == _cols;
}

/**
 * @tparam S the type of the given matrix
 * @param output the output stream
 * @param mat the matrix to print
 * @return the given output stream
 */
template<class S>
std::ostream &operator<<(std::ostream &output, const Matrix<S> &mat) {
    for (unsigned int i = 0; i < mat._rows; ++i) {
        for (unsigned int j = 0; j < mat._cols; ++j) {
            output << mat(i, j) << PRINTING_SEPARATOR;
        }

        output << std::endl;
    }
    return output;
}

/**
 * @tparam T the type of the matrix
 * @param row the row coordinate of the requested element
 * @param col the col coordinate of the requested element
 * @return a const reference to the requested element
 * @throws out_of_range if the given coordinates are out of the matrix range
 */
template<class T>
const T &Matrix<T>::operator()(unsigned int row, unsigned int col) const {
    if (_rows <= row || row < 0 || col < 0 || _cols <= col) {
        throw std::out_of_range(ERROR_RANGE_MSG);
    }

    return _values[(row * _cols) + col];
}

/**
 * @tparam T the type of the matrix
 * @param row the row coordinate of the requested element
 * @param col the col coordinate of the requested element
 * @return a reference to the requested element
 * @throws out_of_range if the given coordinates are out of the matrix range
 */
template<class T>
T &Matrix<T>::operator()(unsigned int row, unsigned int col) {
    if (_rows <= row || row < 0 || col < 0 || _cols <= col) {
        throw std::out_of_range(ERROR_RANGE_MSG);
    }

    return _values[(row * _cols) + col];
}

/**
 * @return the transpose of this matrix
 * @throws invalid_argument if this.rows != this.cols
 */
template<>
Matrix<Complex> Matrix<Complex>::trans() const {
    if (!isSquareMatrix()) {
        throw std::invalid_argument(ERROR_SQUARE_MSG);
    }

    Matrix<Complex> result(_cols, _rows); // the transpose
    for (unsigned int row = 0; row < _rows; ++row) {
        for (unsigned int col = 0; col < _cols; ++col) {
            result._values[(col * _rows) + row] = (*this)(row, col).conj();
        }
    }
    return result;
}