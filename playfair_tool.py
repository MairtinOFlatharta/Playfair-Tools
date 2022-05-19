#!/usr/bin/env python
import re


def main():
    # First generate the Playfair table
    key = input('Please enter the cipher key. '
                '(Press return to use table with no key): ')
    table = generateTable(key)

    # Print formatted Playfair table for demonstration purposes
    print('Generated cipher table: ')
    for row in table:
        print(row)

    while True:
        mode = input('To encrypt a plaintext message, enter E. '
                     'To decrypt a message, enter D: ')

        if mode == 'e' or mode == 'E':
            # Encryption mode
            plaintext = input('Please enter the plaintext '
                              'you wish to encrypt: ')
            plaintext = processPlaintext(plaintext)
            encrypted = encryptMessage(table, plaintext)
            print('Encrypted message: ' + encrypted)
            break

        elif mode == 'd' or mode == 'D':
            # Decryption mode
            ciphertext = input('Please enter the ciphertext '
                               'you wish to decrypt: ')
            decrypted = decryptMessage(table, ciphertext)
            print('Decrypted message: ' + decrypted)
            break

        else:
            # Something other than e or d was entered. Try again
            print('Invalid character entered!')


def processPlaintext(plaintext):
    # Sanitize plaintext
    plaintext = sanitizeInput(plaintext)

    # Detect duplicate pairs and replace second character with 'X'
    for i in range(0, len(plaintext)+1, 2):
        if i < len(plaintext) - 1:
            if plaintext[i] == plaintext[i+1]:
                plaintext = plaintext[:i+1] + 'X' + plaintext[i+1:]

    # Append space character if number of plaintext characters is odd
    if len(plaintext) % 2 != 0:
        plaintext = plaintext + ' '

    return plaintext


def processKey(key):
    # Sanitize key
    key = sanitizeInput(key)

    # Remove all duplicate characters from key. Ensure first occurance of
    # character remains
    key = ''.join(dict.fromkeys(key))

    return key


def sanitizeInput(text):
    # Bring text to uppercase and replace characters 'J' and 'K'
    # with 'I' and 'C' respectively
    text = (text.upper()).replace('J', 'I').replace('K', 'C')

    # Will match any non-alphabetical character except for a space
    # i.e. will match numbers and special characters
    regex = re.compile('[^ A-Z]')

    # Remove all non-alphabetical characters except for spaces
    text = regex.sub('', text)

    return text


def generateTable(key):
    # Parse key and store in character list
    tableCharacters = list(processKey(key))

    # Append all other remaining character in tableCharacters using ASCII
    for i in range(65, 91):
        if i == 74 or i == 75:
            # Skip 'J' and 'K'
            continue
        elif chr(i) not in tableCharacters:
            tableCharacters.append(chr(i))

    # Append space character if we haven't reached the needed character
    # count (25)
    if len(tableCharacters) < 25:
        tableCharacters.append(' ')

    # This represents the Playfair grid needed for encrypting and decrypting
    table = [
        [0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0]
    ]

    # This will be needed to use pop() while adding characters to table
    tableCharacters.reverse()

    # Transfer characters in list to table
    for i in range(0, 5):
        for j in range(0, 5):
            table[i][j] = tableCharacters.pop()

    return table


def encryptMessage(table, plaintext):
    ciphertext = []

    pos1 = pos2 = (-1, -1)

    # Cycle through each pair of characters
    for i in range(0, len(plaintext)+1, 2):
        if i < len(plaintext) - 1:
            # Get table positions of both characters in current pair
            pos1 = getPosInTable(plaintext[i], table)
            pos2 = getPosInTable(plaintext[i+1], table)

            if pos1[0] == pos2[0]:
                # Both characters in same row. Replace the character with the
                # next one on the right
                ciphertext.extend((table[pos1[0]][(pos1[1]+1) % 5],
                                   table[pos2[0]][(pos2[1]+1) % 5]))

            elif pos1[1] == pos2[1]:
                # Both characters in same column. Replace the character with
                # the next one below
                ciphertext.extend((table[(pos1[0]+1) % 5][pos1[1]],
                                   table[(pos2[0]+1) % 5][pos2[1]]))

            else:
                # Characters in different rows and columns. Replace character
                # with another character in the same row but with the index
                # of the other character in the pair
                ciphertext.extend((table[pos1[0]][pos2[1]],
                                   table[pos2[0]][pos1[1]]))

    # Convert ciphertext list to a string and return
    return ''.join(ciphertext)


def decryptMessage(table, ciphertext):
    ciphertext = sanitizeInput(ciphertext)
    plaintext = []

    pos1 = pos2 = (-1, -1)

    if len(ciphertext) % 2 != 0:
        # If ciphertext isn't an even length, let's assume that a
        # space character was accidentally omitted and add it back in
        # Otherwise, the ciphertext is mutilated and the final charcater
        # can't be decrypted properly anyways
        ciphertext = ciphertext + ' '

    # Cycle through each pair of characters
    for i in range(0, len(ciphertext)+1, 2):
        if i < len(ciphertext) - 1:
            # Get table positions of both characters in current pair
            pos1 = getPosInTable(ciphertext[i], table)
            pos2 = getPosInTable(ciphertext[i+1], table)

            if pos1[0] == pos2[0]:
                # Both characters in same row. Replace the character with the
                # next one on the left
                plaintext.extend((table[pos1[0]][(pos1[1]-1) % 5],
                                  table[pos2[0]][(pos2[1]-1) % 5]))

            elif pos1[1] == pos2[1]:
                # Both characters in same column. Replace the character with
                # the next one above
                plaintext.extend((table[(pos1[0]-1) % 5][pos1[1]],
                                  table[(pos2[0]-1) % 5][pos2[1]]))

            else:
                # Characters in different rows and columns. Replace character
                # with another character in the same row but with the index
                # of the other character in the pair
                plaintext.extend((table[pos1[0]][pos2[1]],
                                  table[pos2[0]][pos1[1]]))

    # Convert plaintext list back to a string
    return ''.join(plaintext)


def getPosInTable(char, table):
    # Returns position in Playfair table of a given character (row, column)
    row = column = -1

    for i in range(0, 5):
        if char in table[i]:
            row = i
            column = table[i].index(char)

    return(row, column)


if __name__ == '__main__':
    main()
