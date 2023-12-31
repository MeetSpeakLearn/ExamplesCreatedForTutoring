
# © 2023, Stephen DeVoy, All rights reserved.

# There are many possible approaches to evaluating Roman numerals. The most theoretically
# valid method would be to create a grammar for the language of Roman numerals and pump
# the numerals through a parser followed by evaluating the parse tree. If I were to solve
# this problem in Prolog or by using a grammar generator, that is what I would do.

# However, the problem can be solved more efficiently in Python by looking up subsequences
# in tables. Naturally, we have a list of valid numerals and a list of their associated
# values. We use those lists to determine the individual values of the numerals.

# When a person accustomed to reading Roman numerals sees any of the metatokens listed below,
# he or she does not see them as a pair of individual tokens. Instead, the trained
# eye interprets them as single symbols. When I see "IV", for example, I don't ponder on
# the fact that it is comprised of an "I" followed by a "V", and thus a subtraction. I see it 
# the same way as I see "4". I'm sure Romans saw these pairs the same way. Had they not,
# the system would have been to complex to continue using and they would have adopted a 
# better system.

# I take advantage of that fact by using a list of metatokens. A metatoken is single
# unit. There are only a few of them in the system. I exploit this fact to make parsing
# Roman numerals easier. I still do the subtraction when evaluating them, but it would be 
# perfectly legitimate to just look up their value as a single unit. The only reason 
# I do not follow that path is to deflect criticism that this solution wouldn't reflect 
# a true understanding of how Roman numerals work.

romanTokens = ["M", "D", "C", "L", "X", "V", "I"]       # All valid numerals
romanTokenValues = [1000, 500, 100, 50, 10, 5, 1]       # The value of each numeral in the same position in romanTokens
romanMetaTokens = ["CM", "CD", "XL", "IX", "IV"]        # Numeral pairs seen as single tokens

# parsed is a value that can be found in a tokenized list of Roman numerals.
# parsed must either be a string whose value can be looked up in romanTokens,
# or a list of two values, each of which can be looked up in roman tokens.
# evalRomanToken returns the value of the token.
def evalRomanToken(parsed) -> int:
    if isinstance(parsed, str):
        if parsed in romanTokens:
            return romanTokenValues[romanTokens.index(parsed)]
        else:
            print(parsed + " is not a valid Roman numeral.")
            return 0
    elif isinstance(parsed, list):
        if (len(parsed) == 2):
            if isinstance(parsed[0], str) and isinstance(parsed[1], str):
                return evalRomanToken(parsed[1]) - evalRomanToken(parsed[0])
            else:
                print("Malformed meta token: " + ", ".join(parsed, ))
                return 0
    else:
        print("Malformed meta token: " + ", ".join(parsed, ))
        return 0

# parsed must be a list of elements where each element is either a string in romanTokens
# or a list of two elements, each of which is an element of romanTokens.
# evalRomanTokenList, steps through the list. If an element is a str, it looks its position
# up in romanTokens and then adds it to result, stored in romanTokenValues, at the same
# position. If it is a list of two strings, it looks each of those strings up in romanTokens,
# finds their values in romanTokenValues, and subtracts the first from the second, adding
# the difference result. After summing up all of the parts, the sum is returned as the value.
def evalRomanTokenList(parsed: list) -> int:
    result: int = 0
    for token in parsed:
        result += evalRomanToken(token)
    return result

# Given a valid metatoken (i.e. text must be an element of romanMetaTokens), it returns a list
# of two elements, each of which are the Roman numerals from which the metatoken is composed.
def destructMetaToken(text: str) -> list:
    if (text in romanMetaTokens):
        return [text[0], text[1]]
    else:
        print(text + " is not a valid meta token.")
        return []

# converts a Roman numeral represented within a string into a token list.
def tokenizeRoman(text: str) -> list:
    charCount = len(text)
    
    if (charCount == 0): return []
    elif (charCount == 1):
        if text in romanTokens: return [text]
        else:
            print(text + " is not a valid Roman numeral.")
            return []
    else:
        if text[0:2] in romanMetaTokens:
            rest = tokenizeRoman(text[2:])
            rest.insert(0, destructMetaToken(text[0:2]))
            return rest
        elif text[0:1] in romanTokens:
            rest = tokenizeRoman(text[1:])
            rest.insert(0, text[0:1])
            return rest
        
userInput = input("Enter a number using Roman Numerals: ")
tokenList = tokenizeRoman(userInput)
print("tokenList ", end="")
print(tokenList, end=" evaluates to: ")
print(str(evalRomanTokenList(tokenList)))
