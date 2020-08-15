/**
 * @file encrypt.c
 * @author Daniel Magen
 * @version 1.0
 *
 * @brief encrypts given text using Caesar Cipher
 *
 * @section DESCRIPTION
 * receives an encryption key between -25 and 23 and a continues stream of
 * characters from the user up to an EOF flag,
 * after which it prints the stream of characters after they had
 * been encrypted using the cesar shift encryption.
 *
 * Input  : no command line input
 * Process: receives a continues stream of characters
 * Output : the given characters cesar shifted by the amount specified
 */

// ------------------------------ includes ------------------------------
#include <stdio.h>


// -------------------------- const definitions -------------------------
#define MIN_ENCRYPTION_KEY -25
#define MAX_ENCRYPTION_KEY 25
#define ARRAY_SIZE 1024 // the size of the array which holds all the characters
#define ERROR 1
#define EXPECTED_NUMBER_OF_INPUT_KEYS 1
#define INVALID_ENCRYPTION_KEY "the given key is invalid"

// ------------------------------ functions -----------------------------


/**
 * @brief prints the given char array up to the given point
 * @param charArray an array of chars
 * @param upTo the maximum index to print up to
 */
static void printCharArray(const char charArray[], int upTo);


/**
 * @brief returns the number mod the second number given
 * @param number an integer
 * @param mod an integer
 */
static int modulo(int number, int mod);


/**
 * @brief encrypts the array according to the given key using cesar
 * encryption
 * @param charArray an array of chars
 * @param size the size of the given array
 * @param encryptionConstant the constant by which to encrypt
 */
static void encryptArray(char charArray[], int size, int encryptionKey);


/**
 * @brief receives an undetermined amount of characters and encrypts them
 * using caesar shifting
 * @param encryptionKey the encryption key that will be used in the
 * encryption
 */
static void caesarShiftInput(int encryptionKey);


/**
 * @brief The main function, receives a valid encryption key and calls
 * caesarShiftInput with it
 * @return 0, to tell the system the execution ended without errors, 1 otherwise.
 */
int main() {
    int encryptionKey = MAX_ENCRYPTION_KEY + 1;
    int amountOfNumbersGiven = scanf("%d ", &encryptionKey);
    if (encryptionKey > MAX_ENCRYPTION_KEY
        || encryptionKey < MIN_ENCRYPTION_KEY
        || amountOfNumbersGiven != EXPECTED_NUMBER_OF_INPUT_KEYS) {
        fprintf(stderr, INVALID_ENCRYPTION_KEY);
        return ERROR;
    }

    caesarShiftInput(encryptionKey);

    return 0;

}


static void printCharArray(const char charArray[], int upTo) {
    for (int i = 0; i < upTo; i++) {
        printf("%c", charArray[i]);
    }
}


static int modulo(int number, int mod) {
    return (number % mod + mod) % mod;
}

static void encryptArray(char charArray[], int size, int encryptionKey) {
    char startFrom, endWith;
    int toEncrypt;
    for (int i = 0; i < size; i++) {
        toEncrypt = 0; // don't encrypt this round if 0
        if (charArray[i] >= 'a' && charArray[i] <= 'z') {
            startFrom = 'a';
            endWith = 'z';
            toEncrypt = 1; // encrypt this letter
        } else if (charArray[i] >= 'A' && charArray[i] <= 'Z') {
            startFrom = 'A';
            endWith = 'Z';
            toEncrypt = 1; // encrypt this letter
        }

        if (toEncrypt) {
            // encrypt the character
            charArray[i] = charArray[i] - startFrom + encryptionKey;
            charArray[i] = modulo(charArray[i], endWith - startFrom + 1);
            charArray[i] = charArray[i] + startFrom;
        }
    }
}

static void caesarShiftInput(int encryptionKey) {
    char toEncrypt[ARRAY_SIZE] = {0}; // will hold all that needs to be encrypted
    int numberOfElementsGiven = 0;
    while (scanf("%1000c%n", toEncrypt, &numberOfElementsGiven) != EOF) {
        encryptArray(toEncrypt, numberOfElementsGiven, encryptionKey);
        printCharArray(toEncrypt, numberOfElementsGiven);
    }
}
