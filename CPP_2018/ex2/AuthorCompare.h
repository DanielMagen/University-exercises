//AuthorCompare_h

#ifndef EX2_AUTHORCOMPARE_H
#define EX2_AUTHORCOMPARE_H

#include <iostream>
#include <map>
#include <string>
#include <vector>

/**
 * this class is used to read and hold the word frequency
 * data about various authors, and then compare their data to the first given author data
 */

class AuthorCompare {
public:
    /**
     * a constructor
     * @param pathToWords the path to the file containing the most common words
     */
    AuthorCompare(const std::string pathToWords);

    /**
     * adds the author words frequency to the object
     * @param pathToText the path to the file containing the author text
     */
    void addAuthor(const std::string pathToText);

    /**
     * @return the name and distance of the closest author to the first author
     */
    std::pair<std::string, double> getClosestAuthor() const;

    /**
     * @return the vector of inserted authors except from the first author
     */
    std::vector <std::pair<std::string, double>> getAuthors() const;

private:

    std::map<std::string, int> _freqCounter;
    // this map will constantly change its values but its keys will stay the same
    // each time a new author is inserted it will
    // be used to count the word frequency of that author

    std::vector <std::pair<std::string, double>> _distanceKeeper;
    // will hold for each author its name and distance from the first author

    unsigned long _indexOfClosest; // the index of the author which is closest to the first author

    const unsigned long STARTING_NUMBER_OF_CLOSEST = 0;

    std::vector<double> _firstAuthorFreq; // will hold the first vector word frequency

    const std::string SEPARATORS = ";,:! \r\n\""; // the possible non space separators

    const std::string NOT_ENOUGH_AUTHORS = "not enough authors inserted";
    const std::string CANT_OPEN_FILE = "can't open the given file ";

    /**
     * @param vec1 a vector object
     * @param vec2 a vector object the same length as vec1
     * @return the scalar product between them
     */
    static double _scalarProductOfVectors(const std::vector<double> &vec1,
                                          const std::vector<double> &vec2);

    /**
     * @param vec  a vector object
     * @return the norm of the vector
     */
    static double _normOfVector(const std::vector<double> &vec);

    /**
     * @return creates a vector object from the current freqCounter and returns it
     */
    std::vector<double> _getCurrentAuthorVector() const;

    /**
     * resets the _freqCounter to zero
     */
    void _resetFreqCounter();

    /**
     * adds the author that is currently in the _freqCounter to _distanceKeeper
     * then checks if that author is closer to the first author than the current closest author
     * @param pathToText the path to the file containing the author text will
     * serve as the author name
     */
    void _updateDistanceKeeperAndClosest(const std::string pathToText);

    /**
    * reads the words from the given file
    * and initializes the object words counter fully
    * should be called before adding any authors
    * @param pathToWords the path to the file containing the most common words
    */
    void _initializeWords(const std::string pathToWords);

    /**
     * reads the text from the given file and updates the freqCounter
     * @param pathToText the path to the file containing the author text
     */
    void _readText(const std::string pathToText);

    /**
     * reads the given stream and treats all SEPARATORS as separators
     * @param wordsFile a reference to a ifstream object
     * @param output will save words it read from the file to it
     * @param lower if true will convert all text to lower case
     */
    void _readTextAndRemoveSeparators(std::ifstream &wordsFile,
                                      std::vector <std::string> &output,
                                      bool lower);

    /**
     * @param possibleSeparator a char
     * @return true if the given char was a separator
     */
    inline bool _isSeparator(char possibleSeparator) const {
        for (long unsigned i = 0; i < SEPARATORS.size(); ++i) {
            if (SEPARATORS.find(possibleSeparator) != std::string::npos) {
                return true;
            }
        }
        return false;
    }

};

#endif //EX2_AUTHORCOMPARE_H
