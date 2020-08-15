#include "AuthorCompare.h"
#include <iomanip>

const int DOUBLE_PRECISION = 6;
const int MINIMUM_NUMBER_OF_PARAMETERS = 3;
const std::string BEST_MATCH = "Best matching author is ";
std::string NOT_ENOUGH_AUTHORS = "not enough authors inserted";

/**
 * @param argc the number of arguments given
 * @param argv the arguments given
 * @return using the given arguments it compares the the first
 * author writing style to the other authors riting style, and prints the result
 */
int main(int argc, char *argv[]) {
    if (argc < MINIMUM_NUMBER_OF_PARAMETERS) {
        std::cerr << NOT_ENOUGH_AUTHORS << std::endl;
        return 1;
    } else {
        std::string pathToWords = argv[1];
        AuthorCompare compareTheAuthors(pathToWords);
        for (int i = 2; i < argc; ++i) {
            // insert the authors into the author compare object
            compareTheAuthors.addAuthor(argv[i]);
        }

        std::vector <std::pair<std::string, double>> authors = compareTheAuthors.getAuthors();
        for (auto author: authors) {
            // print the authors scores
            std::cout << std::setprecision(DOUBLE_PRECISION) << author.first
                      << " " << author.second << std::endl;
        }

        // print the closest author scores
        std::pair<std::string, double> closest = compareTheAuthors.getClosestAuthor();
        double scoreClosestAuthor = closest.second;
        std::cout << std::setprecision(DOUBLE_PRECISION) << BEST_MATCH;
        if (scoreClosestAuthor > 0) {
            std::cout << closest.first;
        }
        std::cout << " score " << scoreClosestAuthor << std::endl;

    }

    return 0;
}