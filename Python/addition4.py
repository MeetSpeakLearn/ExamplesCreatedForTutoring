# © 2023, Stephen DeVoy, All rights reserved.

import sys

# Grade School Addition Version 4 - Using lists instead of strings to represent digit sequences.

def bung(anyObj, anyList: list) -> list:
    anyList.insert(1, anyObj)
    return anyList

# digitToInt accepts a single character string whose first (and only) character is a digit.
# It returns the integer value of that digit
def digitToInt(digit: str) -> int:
    return ord(digit) - ord("0")

# intToDigit accepts an integer whose value should be between 0 and 9, and return a single character string
# whose only character is the character representing the digit.
def intToDigit(val: int) -> str:
    return chr(val + ord("0"))

# digitStringToList accepts a string of digits and a minimum size. No checking is done to ensure that
# the strings only contain digits. Filtering should be enforced by validating input.
# All returned lists will have at least minSize elements. Padding with 0 is used to extend a list
# of lesser size to minSize length.
# Example: digitStringToList("1234", 6) -> [4, 3, 2, 1, 0, 0]
def digitStringToList(val: str, minSize: int) -> list:
    result = []    
    padCount = minSize - len(val)
    for i in range (0, padCount):
        result.append(0)
    for i in range(0, len(val)):
        c = val[i]
        result.insert(0, digitToInt(c))
    return result

# digitListToString accepts a list produced by digitStringToList and converts it back to a digit string.
# Example: digitListToString([4, 3, 2, 1, 0, 0]) -> "1234"
def digitListToString(val: list) -> str:
    reversedList = list(val)
    reversedList.reverse()
    result = ""
    encounteredNonZero = False
    for digitValue in reversedList:
        if (digitValue == 0):
            if (encounteredNonZero):
                result += '0'
        else:
            encounteredNonZero = True 
            result += intToDigit(digitValue)
    return result

# maxStringLength, given a list of strings, returns the lenth of the longest string in the list.
def maxStringLength(numberStrings: list) -> int:
    maxLength = 0
    for numberString in numberStrings:
        maxLength = max(maxLength, len(numberString))
    return maxLength

# numberStringsToAddends transforms a list of digit strings to a list of digit lists appropriate for the
# gradeSchoolAddition function.
def numberStringsToAddends(numberStrings: list) -> list:
    addends = []
    maxLength = maxStringLength(numberStrings)
    for numberString in numberStrings:
        addends.append(digitStringToList(numberString, maxLength))
    return addends

# gradeSchoolAddition performs "long hand addition" of the type used in gradeschool.
# It recursively processes columns. The carry value is passed down through recursion,
# but defaults to zero for the first column processed.
def gradeSchoolAddition(addends: list, carry: int = 0) -> list:
    digitSum = carry                                                    # Initialize the sum of digits to whatever is carried
    reducedAddends = []                                                 # We will recurse over the rest of the addends
    for addend in addends:
        if (len(addend) == 0):                                          # All addends are of the same length. If we encounter an empty addend, we've finished recursing.
            if (carry == 0):                                            # If carry is zero, there is nothing more to add to the result, if it is not zero, add the carry.
                return []
            else:
                return [carry]
        thisDigit, *reducedAddend = addend                              # Destructure the addend.
        digitSum += thisDigit                                           # Add the first digit of the addend into digitSum
        reducedAddends.append(reducedAddend)                            # Add the reduced addend to the list of addends over which we'll recurse
    carry = digitSum // 10                                              # Set carry to the carry value of the next level of recursion
    digit = digitSum % 10                                               # Compute the digit for this partial result
    restOfSum = [digit]                                                 # Add the digit to the beginning of the rest of the result
    restOfSum.extend(gradeSchoolAddition(reducedAddends, carry))        # Extend the result by recursing over the reduced addends with parameter carry
    return restOfSum                                                    # Return the sum of this set of addends

affirmativeReplies = ["y", "Y", "yes", "Yes"]
outerPrompt = "Would you like sum some numbers? "
innerPrompt = "Type a positive integer or type 'end': "
    

# As the user whether he would like to compute the sum of some numbers.
userResponse = input(outerPrompt)
userResponseToNumberRequest = ""

# So long as the user wishes to sum numbers, do so, otherwise end summing numbers.
while (userResponse in affirmativeReplies):
    stringsToAdd = []               # We will save the numbers as string, in the array stringsToAdd
    
    # Ask the user whether he wants to enter another number, or to quit providing numbers to add.
    userResponseToNumberRequest = input(innerPrompt)    
    
    # So long as the user wishes to enter numbers, continue gathering numbers for addition.
    while (userResponseToNumberRequest != "end"):
        
        # Add the most recently added number to our list of numbers.
        stringsToAdd.append(userResponseToNumberRequest)
        
        # Ask the user whether he wants to enter another number, or to quit providing numbers to add.
        userResponseToNumberRequest = input(innerPrompt)
        
    # The user has finished entering numbers.
        
    if (len(stringsToAdd) > 0):
        # If the user provided at least one number to add, begin adding them.
        
       result = digitListToString(gradeSchoolAddition(numberStringsToAddends(stringsToAdd)))
        
    # Show the user the results.
    print("The sum of:")
    for numAsString in stringsToAdd:
        print("       " + numAsString)
    print("...is: " + result)
    
    # As the user whether he would like to compute the sum of some numbers.
    userResponse = input(outerPrompt)
    
