#!/usr/bin/env python
import argparse
import matplotlib.pyplot as plt
import numpy as np
from pathlib import Path


# Dictionary used to translate certain German characters
# (umalate) to an equivalent character in the English alphabet
# The Eszett (ß) is also here, but won't be used ever because Python
# replaces the character with SS when upper() is called. Very cool :)
germanDictionary = {
    '\u00DF': 'S',  # ß -> S
    '\u00C4': 'A',  # Ä -> A
    '\u00D6': 'O',  # Ö -> O
    '\u00DC': 'U',  # Ü -> U
}

# Will store each charater pair with their frequency
pairDictionary = {}


def main():
    # Parse arguments for script. Path to text file should be passed as
    # argument. Sample command for running file:
    # python analyse_pair_freq.py -f sample.txt
    parser = argparse.ArgumentParser(
        description='Perform frequency analysis of character pairs with '
                    'text files (English and German)')
    parser.add_argument(
        '-f',
        '--file',
        type=str,
        help='Path to text file used for analysis')
    args = parser.parse_args()

    if args.file is None:
        print('No file path provided! Exiting...')
        quit()

    # Convert path string into path object because
    # it's more stable and reliable
    pathToFile = Path(args.file)

    if pathToFile.exists() and not pathToFile.is_dir():
        # Path provided is correct, so we can continue with the given file
        getFrequencies(pathToFile)


def getFrequencies(pathToFile):
    # Keep track of number of characters (nice to know)
    charCount = 0

    # Open file with context manager so we don't need to worry about
    # closing or error handling
    with pathToFile.open(encoding='UTF-8') as f:
        # Read 1 line, convert to uppercase and remove apostrophes
        # e.x. I'm -> IM
        currentLine = ((f.readline()).upper()).replace('\'', '')

        # Continually read lines until we reach EOF
        while currentLine:
            for i in range(0, len(currentLine) - 1):
                if not currentLine[i].isalpha() or \
                        not currentLine[i+1].isalpha():
                    # Skip any non-alphabetical characters
                    # (Will not skip special German characters)
                    charCount += 1
                    continue

                if i == 0 and currentLine[i] in germanDictionary.keys():
                    # Check if first character is a special German
                    # charcter. If so, replace with English equivalent
                    currentLine = currentLine[:i] + \
                                  germanDictionary[currentLine[i]] + \
                                  currentLine[i + 1:]

                if currentLine[i+1] in germanDictionary.keys():
                    # Check if next character is a special German
                    # charcter. If so, replace with English equivalent
                    currentLine = currentLine[:i + 1] + \
                                  germanDictionary[currentLine[i + 1]] + \
                                  currentLine[i + 2:]

                if currentLine[i] + currentLine[i+1] in pairDictionary.keys():
                    # If current pair was already recorded previously,
                    # increment the value at that key in the dictionary
                    pairDictionary[currentLine[i] + currentLine[i+1]] += 1

                else:
                    # Pair of characters was not previously found. Add a new
                    # key pair to the dictionary
                    pairDictionary[currentLine[i] + currentLine[i+1]] = 1

                charCount += 1

            # Read next line
            currentLine = ((f.readline()).upper()).replace('\'', '')

    # Find top 20 pairs in dictionary. If the total number of encountered
    # pairs is less than 20, return all of them
    topPairs = sorted(pairDictionary,
                      key=pairDictionary.get,
                      reverse=True)[:20]
    topValues = [pairDictionary[x] for x in topPairs]

    print('Total characters read: ' + str(charCount))

    # Print out top 20
    print(str(len(topPairs)) + ' most common character pairs: ')
    for i in range(0, len(topPairs)):
        print(str(topPairs[i]) + ': ' + str(topValues[i]))

    # Visualise top 20 pairs using a bar chart
    yPos = np.arange(len(topPairs))
    plt.bar(yPos, topValues, align='center')
    plt.xticks(yPos, topPairs)
    plt.ylabel('Frequency')
    plt.title('Frequency distribution of letter pairs found in: ' +
              str(pathToFile))
    plt.show()


if __name__ == '__main__':
    main()
