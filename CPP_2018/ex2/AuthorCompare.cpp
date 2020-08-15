//
// Created by Daniel on 21/12/18.
//

#include "AuthorCompare.h"
#include <numeric>
#include <cmath>
#include <fstream>

// --------------------------------------------------------------------------------------
// This file contains the implementation of the class AuthorCompare
// --------------------------------------------------------------------------------------

/**
 * a constructor
 * @param pathToWords the path to the file containing the most common words
 */
AuthorCompare::AuthorCompare(const std::string pathToWords) {
    _indexOfClosest = STARTING_NUMBER_OF_CLOSEST;
    _initializeWords(pathToWords);
}

/**
 * adds the author words frequency to the object
 * @param pathToText the path to the file containing the author text
 */
void AuthorCompare::addAuthor(const std::string pathToText) {
    _readText(pathToText);
    _updateDistanceKeeperAndClosest(pathToText);
}

/**
 * @return the name and distance of the closest author to the first author
 */
std::pair<std::string, double> AuthorCompare::getClosestAuthor() const {
    if (_indexOfClosest == STARTING_NUMBER_OF_CLOSEST) {
        std::cerr << NOT_ENOUGH_AUTHORS << std::endl;
        std::pair<std::string, double>("", 0);
    }
    return _distanceKeeper[_indexOfClosest];
}


/**
 * @return the vector of inserted authors except from the first author
 */
std::vector <std::pair<std::string, double>> AuthorCompare::getAuthors() const {
    auto first = _distanceKeeper.begin() + 1;
    auto last = _distanceKeeper.end();
    std::vector <std::pair<std::string, double>> toReturn(first, last);
    return toReturn;
}

/**
 * @param vec1 a vector object
 * @param vec2 a vector object the same length as vec1
 * @return the scalar product between them
 */
double AuthorCompare::_scalarProductOfVectors(const std::vector<double> &vec1,
                                              const std::vector<double> &vec2) {
    static const std::string NO_MATCH_FOR_WORDS = "there was no match for the given words";
    double product = std::inner_product(vec1.begin(), vec1.end(), vec2.begin(), 0.0);
    double norm1 = _normOfVector(vec1);
    double norm2 = _normOfVector(vec2);
    if (norm1 == 0 || norm2 == 0) {
        std::cerr << NO_MATCH_FOR_WORDS << std::endl;
        return 0;
    }
    product /= norm1;
    product /= norm2;
    return product;
}

/**
 * @param vec a vector object
 * @return the norm of the vector
 */
double AuthorCompare::_normOfVector(const std::vector<double> &vec) {
    return sqrt(std::inner_product(vec.begin(), vec.end(), vec.begin(), 0.0));
}

/**
 * @return creates a vector object from the current freqCounter and returns it
 */
std::vector<double> AuthorCompare::_getCurrentAuthorVector() const {
    std::vector<double> currentAuthorVector;
    currentAuthorVector.reserve(_freqCounter.size());
    for (auto iter = _freqCounter.begin(); iter != _freqCounter.end(); ++iter) {
        currentAuthorVector.push_back(iter->second);
    }
    return currentAuthorVector;
}

/**
 * resets the _freqCounter to zero
 */
void AuthorCompare::_resetFreqCounter() {
    for (auto iter = _freqCounter.begin(); iter != _freqCounter.end(); ++iter) {
        _freqCounter[iter->first] = 0;
    }
}

/**
 * adds the author that is currently in the _freqCounter to _distanceKeeper
 * then checks if that author that was added
 * is closer to the first author than the current closest author
 * if the vector that was added was the first vector, it just saves it to _firstAuthorFreq
 * @param pathToText the path to the file containing the author text will
 * serve as the author name
 */
void AuthorCompare::_updateDistanceKeeperAndClosest(const std::string pathToText) {
    std::vector<double> lastAuthor = _getCurrentAuthorVector(); // the last author added
    if (_distanceKeeper.empty()) {
        // we haven't inserted the first author yet so we just insert it now
        _firstAuthorFreq = lastAuthor;
        _distanceKeeper.push_back(std::pair<std::string, double>(pathToText, 0.0));
        return;

    }

    // insert the last author into _distanceKeeper
    double distanceFromFirst = _scalarProductOfVectors(lastAuthor, _firstAuthorFreq);
    _distanceKeeper.push_back(std::pair<std::string, double>(pathToText, distanceFromFirst));

    // now update _indexOfClosest
    if (_indexOfClosest == STARTING_NUMBER_OF_CLOSEST
        || _distanceKeeper[_indexOfClosest].second < distanceFromFirst) {
        _indexOfClosest = _distanceKeeper.size() - 1;
    }
}

/**
* reads the words from the given file
* and initializes the object words counter fully
* should be called before adding any authors
* @param pathToWords the path to the file containing the most common words
*/
void AuthorCompare::_initializeWords(const std::string pathToWords) {
    std::ifstream wordsFile(pathToWords);
    if (!wordsFile) {
        std::cerr << CANT_OPEN_FILE << pathToWords << std::endl;
    }

    std::vector <std::string> wordsList;
    _readTextAndRemoveSeparators(wordsFile, wordsList, false);
    wordsFile.close();

    for (auto iter = wordsList.begin(); iter != wordsList.end(); ++iter) {
        _freqCounter[*iter];
    }
}

/**
 * reads the text from the given file and updates the freqCounter
 * @param pathToText the path to the file containing the author text
 */
void AuthorCompare::_readText(const std::string pathToText) {
    _resetFreqCounter();

    std::ifstream wordsFile(pathToText);
    if (!wordsFile) {
        std::cerr << CANT_OPEN_FILE << pathToText << std::endl;
    }

    std::vector <std::string> wordsList;
    _readTextAndRemoveSeparators(wordsFile, wordsList, true);

    for (auto iter = wordsList.begin(); iter != wordsList.end(); ++iter) {
        if (_freqCounter.find(*iter) != _freqCounter.end()) {
            ++_freqCounter[*iter];
        }
    }

    wordsFile.close();
}

/**
 * reads the given stream and treats all SEPARATORS as separators
 * @param wordsFile a reference to a ifstream object
 * @param output will save words it read from the file to it
 * @param lower if true will convert all text to lower case
 */
void AuthorCompare::_readTextAndRemoveSeparators(std::ifstream &wordsFile,
                                                 std::vector <std::string> &output,
                                                 bool lower) {
    std::string currentWord;
    char currentChar;
    bool finish = false; // if true will stop and return

    while (!finish) {
        currentWord.clear();
        // now read the word until a separator is found
        wordsFile.get(currentChar);
        // until running into separator add to the current word
        while (!_isSeparator(currentChar)) {
            if (lower) {
                currentChar = (char) tolower(currentChar);
            }
            currentWord.push_back(currentChar);
            if (wordsFile.peek() == EOF) {
                // we reached the end of the file
                finish = true;
                break;
            }
            wordsFile.get(currentChar);
        }
        if (!currentWord.empty()) {
            output.push_back(currentWord);
        }
        // catch the separator
        while (_isSeparator(currentChar) && !finish) {
            if (wordsFile.peek() == EOF) {
                return;
            }
            wordsFile.get(currentChar);
        }
        if (currentChar != EOF) {
            wordsFile.unget();
        }
    }
}
