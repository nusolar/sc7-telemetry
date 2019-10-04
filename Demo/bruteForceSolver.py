# NUSolar 2019 new members activity
# Uses brute force to solve a Caesar cypher

MAX_KEY_SIZE = 26

def getTranslatedMessage(message, key):
    for symbol in message:
        translated = ''

    # Checks each character in message
    for symbol in message:
        # Checks if character is a letter, ignore otherwise
        if symbol.isalpha():
            num = ord(symbol)
            num += key # Key is the cypher offset
            
            # If original symbol is uppercase, 
            # check if offset char falls within range of upper case letters
            # Includes check for lower bound if key is negative
            if symbol.isupper():
                if num > ord('Z'):
                    num -= 26
                elif num < ord('A'):
                    num += 26
                    
            # If original symbol is uppercase, 
            # check if offset char falls within range of lower case letters
            elif symbol.islower():
                if num > ord('z'):
                    num -= 26
                elif num < ord('a'):
                    num += 26
            
            # After correcting offset, 
            # add offsetted char to end of translated str
            translated += chr(num)
        
        # Directly append all non-alphabetic chars
        else:
            translated += symbol
            
    # Return the completed string, with all chars appended
    return translated

def bruteForceSolve(message):
    for ii in range(2, MAX_KEY_SIZE):
        print (getTranslatedMessage(message, ii))
        
bruteForceSolve('Dlsjvtl av aol UBZvshy Lsljaypjhs Alht')
