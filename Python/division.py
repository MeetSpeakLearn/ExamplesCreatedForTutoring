# © 2024, Stephen DeVoy, All rights reserved.

import sys
import random

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
def digitStringToList(val: str, minSize: int = 1) -> list:
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

def intToDigitList(val: int) -> list:
    result = []
    while (val != 0):
        result.append(val % 10)
        val = val // 10
    return result

def digitListToInt(val: list) -> int:
    result = 0
    for digit in reversed(val):
        result = result * 10 + digit
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
    if isZero(multiplicand1) or isZero(multiplicand2):
        return [0]
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

# Given a list of digits, we subtract 1 from the first digit, if it is greater than 0,
# otherwise, we borrow from the rest of the digits and bung 9 onto the result.
def borrow(digits: list) -> list:
    if (len(digits) == 0): return []
    digit, *rest = digits
    if (digit > 0):
        alteredDigit: int = digit - 1
        if (alteredDigit == 0) and (len(rest) == 0): return []
        else: return bung(alteredDigit, rest)
    else: return bung(9, borrow(rest))

# Perform grade school subtraction the way your teacher did it on the blackboard.
# The subtrahend must be less than the minuend.
# If we are at the outermost level of the function (not recursing when returning)
# we need to make sure that an empty list is not returned. When numbers are represented
# as lists of digits, an empty list is the same as zero, so a zero result may have
# been represented as an empty list. At the top level, we always wish the result to
# represent a zero as a list containing only zero. This makes it easier to read when
# debugging.
def gradeSchoolSubtraction(minuend: list, subtrahend: list, nested: bool = False) -> list:
    if (len(subtrahend) == 0):
        if (nested): return minuend
        else: return minuend if len(minuend) > 0 else [0]
    else:
        minuendDigit, *minuendDigits = minuend
        subtrahendDigit, *subtrahendDigits = subtrahend
        difference = []
        
        if (minuendDigit >= subtrahendDigit):
            difference = bung(minuendDigit - subtrahendDigit,
                            gradeSchoolSubtraction(minuendDigits, subtrahendDigits, True))
        else:
            borrowResult = borrow(minuendDigits)
            if (len(borrowResult) == 0):
                print("Nothing to borrow!")
                difference = [(minuendDigit + 10) - subtrahendDigit]
            else:
                difference = bung((minuendDigit + 10) - subtrahendDigit,
                                gradeSchoolSubtraction(borrowResult, subtrahendDigits, True))
            
        return normalize(difference) if len(difference) > 0 else [0]
        
def normalize(digitList: list) -> list:
    reversedList = list(digitList)
    reversedList.reverse()
    result = []
    encounteredNonZero = False
    for digitValue in reversedList:
        if (digitValue == 0):
            if (encounteredNonZero):
                result.insert(0, 0)
        else:
            encounteredNonZero = True 
            result.insert(0, digitValue)
            
    if (len(result) == 0):
        return [0]
    else:
        return result
    
def compareOfEqualLength(digitList1: list, digitList2: list)-> int:
    for d1, d2 in zip(reversed(digitList1), reversed(digitList2)):
        if (d1 != d2): return d1 - d2
    return 0
        
def compare(digitList1: list, digitList2: list)-> int:
    digits1 = normalize(digitList1)
    digits2 = normalize(digitList2)
    result = len(digits1) - len(digits2)
    
    if (result == 0):
        return compareOfEqualLength(digits1, digits2)
    return result

def canDivide(dividend: list, divisor: list) -> bool:
    result = compare(dividend, divisor) >= 0
    return result

def goesInto(dividend: list, divisor: list) -> int:
    result = 0
    dividend = dividend[::]
    while (compare(dividend, divisor) >= 0):
        dividend = gradeSchoolSubtraction(dividend, divisor)
        result += 1
    return result

def isZero(digitList: list) -> bool:
    digitCount = len(digitList)
    if digitCount == 0: return True
    elif digitCount == 1 and digitList[0] == 0: return True
    else: return False

def gradeSchoolDivisionWithoutChecks(dividend: list, divisor: list) -> (list, list):
    lengthOfDividend = len(dividend)
    lengthOfDivisor = len(divisor)
    
    # Find the sublist of dividend that we can divide
    
    shortestDivisibleDividendPrefix = None
    restOfDividend = None
    
    if (lengthOfDividend == lengthOfDivisor):
        shortestDivisibleDividendPrefix = dividend[::]
        restOfDividend = []
    if (canDivide(candidate := dividend[lengthOfDividend - lengthOfDivisor : ], divisor)):
        shortestDivisibleDividendPrefix = candidate
        restOfDividend = dividend[0 : lengthOfDividend - lengthOfDivisor]
    else:
        shortestDivisibleDividendPrefix = dividend[lengthOfDividend - (lengthOfDivisor + 1) : ]
        restOfDividend = dividend[0 : lengthOfDividend - (lengthOfDivisor + 1)]
        
    if (shortestDivisibleDividendPrefix is None): return ()
    
    digit = goesInto(shortestDivisibleDividendPrefix, divisor)
    subtrahend = gradeSchoolMultiplicationOf2Multiplicands([digit], divisor)
    
    if len(shortestDivisibleDividendPrefix) == 0: return ()
    
    leftOver = gradeSchoolSubtraction(shortestDivisibleDividendPrefix, subtrahend)
    
    if (len(restOfDividend) == 0): return ([digit], leftOver)
    
    subDividend = restOfDividend[::]
    subDividend.extend(leftOver)
    
    comparison = compare(divisor, subDividend)
    
    if (comparison > 0):
        q = [0]*len(restOfDividend)
        q.append(digit)
        return (q, subDividend)
    
    subResult = gradeSchoolDivisionWithoutChecks(subDividend, divisor)
    
    if (subResult == ()): return ([0], [0])
    
    subQuotient, remainder = subResult
    subQuotient.append(digit) 
    
    return (subQuotient, remainder)

def gradeSchoolDivision(dividend: list, divisor: list) -> (list, list):
    dividend = normalize(dividend)
    divisor = normalize(divisor)
    divisorLength = len(divisor)    
    
    if (divisorLength > len(dividend)):
        return ([0], divisor[::])
    
    comparison = compare(divisor, dividend)
    
    if comparison == 0: return ([1], [0])                   # If dividend and divisor are equal, the result is 1
    elif isZero(dividend): return([0], divisor[::])
    else:
        if (divisorLength == 0): return ()                  # An empty list is equal to zero. Division by zero is an error.
        elif (divisorLength == 1) and (divisor[0] == 0):
            return ()                                       # Division by zero is an error.
        else:
            quotient, remainder = gradeSchoolDivisionWithoutChecks(dividend, divisor)
            return (quotient, remainder)

def createTestSuite(n: int) -> list:
    testCases = []
    errorCount = 0
    failureCount = 0
    
    for caseCount in range(0, n):
        divisor = 1 + int(random.random() * 1000)
        dividend = divisor + int(random.random() * divisor * 100)
        
        testCase = {}
        testCase["dividend"] = dividend
        testCase["divisor"] = divisor
        testCase["quotient"] = dividend // divisor
        testCase["remainder"] = dividend % divisor
        
        gsd_dividend = intToDigitList(dividend)
        gsd_divisor = intToDigitList(divisor)
        print("Performing gradSchoolDivision(" + digitListToString(gsd_dividend) + ", " + digitListToString(gsd_divisor) + ")")
        gsd_result = gradeSchoolDivision(gsd_dividend, gsd_divisor)
        
        if gsd_result != ():
            testCase["error"] = False
            gsd_quotient, gsd_remainder = gsd_result
            testCase["gsd_quotient"] = gsd_quotient
            testCase["gsd_remainder"] = gsd_remainder
            
            if testCase["quotient"] == digitListToInt(gsd_quotient) and testCase["remainder"] == digitListToInt(gsd_remainder):
                testCase["passed"] = True
            else:
                print("Failure")
                failureCount += 1
                testCase["passed"] = False
        else:
            print("Error")
            errorCount += 1
            testCase["error"] = True
            
        testCases.append(testCase)
        
    print(f"{errorCount} errors out of {n} tests.")
    print(f"{failureCount} failures out of {n} tests.")
    
    return testCases
     
# testResults = createTestSuite(1000)
    
affirmativeReplies = ["y", "Y", "yes", "Yes"]
outerPrompt = "Would you like divide two numbers? "
innerPrompt1 = "Provide the dividend: "
innerPrompt2 = "Provide the divisor: "
    

# As the user whether he would like to compute the multiply of some numbers.
userResponse = input(outerPrompt)
userResponseToNumberRequest = ""

# So long as the user wishes to multiply numbers, do so, otherwise end multiplying numbers.
while (userResponse in affirmativeReplies):
    
    dividendAsText = input(innerPrompt1)    
    divisorAsText = input(innerPrompt2)    
        
    # The user has finished entering numbers.
        
    dividendAsDigitList = digitStringToList(dividendAsText)
    divisorAsDigitList = digitStringToList(divisorAsText)
    quotientRemainderTuple = gradeSchoolDivision(dividendAsDigitList, divisorAsDigitList)
    
    if (quotientRemainderTuple == ()):
        print("Division failed.")
    else:
        quotient, remainder = quotientRemainderTuple
        quotientAsText = digitListToString(quotient)
        remainderAsText = digitListToString(remainder)
        
        # Show the user the results.
        print("The quotient of:")
        print("       " + dividendAsText)
        print("       " + divisorAsText)
        print("...is: " + quotientAsText + " with a remainder of " + remainderAsText)
    
    # As the user whether he would like to compute the multiply of some numbers.
    userResponse = input(outerPrompt)
    
