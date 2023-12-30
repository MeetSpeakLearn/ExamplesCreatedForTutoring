# © 2023, Stephen DeVoy, All rights reserved.

import sys

# Grade School Multiplication Version 1 - Using lists instead of strings to represent digit sequences.

# Adds an element to the biginning of a list and then returns the list.
def bung(anyObj, anyList: list) -> list:
    result = [anyObj]
    result.extend(anyList)
    return result

# Adds all of the elements from a list to the beginning of a second list and returns the list.
def bungAndMerge(oneList: list, anotherList: list) -> list:
    oneList.extend(anotherList)
    return oneList

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
    if (result == ""): result = "0"
    return result

# maxStringLength, given a list of strings, returns the lenth of the longest string in the list.
def maxStringLength(numberStrings: list) -> int:
    maxLength = 0
    for numberString in numberStrings:
        maxLength = max(maxLength, len(numberString))
    return maxLength

# numberStringsToDigitStrings transforms a list of digit strings to a list of digit lists appropriate for the
# gradeSchoolAddition function.
def numberStringsToDigitStrings(numberStrings: list) -> list:
    addends = []
    maxLength = maxStringLength(numberStrings)
    for numberString in numberStrings:
        addends.append(digitStringToList(numberString, maxLength))
    return addends

# Adds "positions" 0s to the beginning of the list if "positions" is positive.
# Removes "positions" digits from the beginning of the list if "positions" is negative.
# If "positions" is zero, it does nothing.
# A list is returned reflecting the changes to the list.
def shiftDigitList(positions: int, digitList: list) -> list:
    if (positions == 0): return digitList
    elif (positions > 0): return bungAndMerge([0]*positions, digitList)
    else: return digitList[positions:]

# Adds n 0s to the end of the digit list. If n is 0, it does nothing.
def padBy(n: int, digitList: list):
    if (n == 0): return
    digitList.extend([0]*n)

# Adds n 0s to the end of all of the lists in digitListList.
# If n is 0, nothing is added.
def padAllBy(n :int, digitListList: list):
    for digitList in digitListList:
        padBy(n, digitList)

# gradeSchoolAddition performs "long hand addition" of the type used in gradeschool.
# It recursively processes columns. The carry value is passed down through recursion,
# but defaults to zero for the first column processed.
def gradeSchoolAddition(addends: list, carry: int = 0) -> list:
    digitSum = carry                                                    # Initialize the multiply of digits to whatever is carried
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
    return bung(digit, gradeSchoolAddition(reducedAddends, carry))      # Return a new list, the head of which is the digit and the tail of which is the solution to the reduced addends.

# Given a digit and a list of digits, multiples the list of digits by digit and returns the result of the multiplication as a digit list.
# All digits in the result are mod 10 the product. The carry, which is added, is int div the product.
def gradeSchoolMultiplicationOfDigitAndDigitList(digit: int, digitList: list, carry: int = 0) -> list:
    if len(digitList) == 0: return [] if (carry == 0) else [carry]
    else:
        product = digit * digitList[0]
        return bung(product % 10 + carry, gradeSchoolMultiplicationOfDigitAndDigitList(digit, digitList[1:], product // 10))

# Given two digitLists, multiplies the two digit lists in the same way that would be done in grade school.
def gradeSchoolMultiplicationOf2Multiplicands(multiplicand1: list, multiplicand2: list):
    addends = []
    position = 0
    for digit in multiplicand1:
        padAllBy(1, addends)
        addends.append(shiftDigitList(position, gradeSchoolMultiplicationOfDigitAndDigitList(digit, multiplicand2)))
        position += 1
    return gradeSchoolAddition(addends)

# Given a list of digit lists, multiples all of the digit lists together. The first digit list in the list
# is multiplied by the next digit list in the list, resulting in a product, which is then multiplied with
# the next digit list in the list, and so on, until the product becomes the product of all multipled together.
def gradeSchoolMultiplication(multiplicands: list) -> list:
    match len(multiplicands):
        case 0: return []
        case 1: return multiplicands
        case 2: return gradeSchoolMultiplicationOf2Multiplicands(multiplicands[0], multiplicands[1])
        case _:
            product = multiplicands[0]
            for multiplicand in multiplicands[1:]:
                product = gradeSchoolMultiplicationOf2Multiplicands(product, multiplicand)
            return product

affirmativeReplies = ["y", "Y", "yes", "Yes"]
outerPrompt = "Would you like to multiply some numbers? "
innerPrompt = "Type a non negative integer or type 'end': "
    

# As the user whether he would like to compute the multiply of some numbers.
userResponse = input(outerPrompt)
userResponseToNumberRequest = ""

# So long as the user wishes to multiply numbers, do so, otherwise end multiplying numbers.
while (userResponse in affirmativeReplies):
    stringsToMultiply = []               # We will save the numbers as string, in the array stringsToMultiply
    
    # Ask the user whether he wants to enter another number, or to quit providing numbers to add.
    userResponseToNumberRequest = input(innerPrompt)    
    
    # So long as the user wishes to enter numbers, continue gathering numbers for addition.
    while (userResponseToNumberRequest != "end"):
        
        # Add the most recently added number to our list of numbers.
        stringsToMultiply.append(userResponseToNumberRequest)
        
        # Ask the user whether he wants to enter another number, or to quit providing numbers to add.
        userResponseToNumberRequest = input(innerPrompt)
        
    # The user has finished entering numbers.
        
    if (len(stringsToMultiply) > 0):
        # If the user provided at least one number to add, begin adding them.
        
       result = digitListToString(gradeSchoolMultiplication(numberStringsToDigitStrings(stringsToMultiply)))
        
    # Show the user the results.
    print("The product of:")
    for numAsString in stringsToMultiply:
        print("       " + numAsString)
    print("...is: " + result)
    
    # As the user whether he would like to compute the multiply of some numbers.
    userResponse = input(outerPrompt)
    
