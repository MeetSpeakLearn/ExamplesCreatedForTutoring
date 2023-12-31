
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

romanTokens = [{"symbol" : "M",
                "value" : 1000,
                "maxRep" : -1},
               {"symbol" : "D",
                "value" : 500,
                "maxRep" : 1},
               {"symbol" : "C",
                "value" : 100,
                "maxRep" : 3},
               {"symbol" : "L",
                "value" : 50,
                "maxRep" : 1},
               {"symbol" : "X",
                "value" : 10,
                "maxRep" : 3},
               {"symbol" : "V",
                "value" : 5,
                "maxRep" : 1},
               {"symbol" : "I",
                "value" : 1,
                "maxRep" : 3}]

romanMetaTokens = ["CM", "CD", "XL", "IX", "IV"]        # Numeral pairs seen as single tokens

def getTokenInfo(name: str):
    for info in romanTokens:
        if info["symbol"] == name:
            return info
    return None

# parsed is a value that can be found in a tokenized list of Roman numerals.
# parsed must either be a string whose value can be looked up in romanTokens,
# or a list of two values, each of which can be looked up in roman tokens.
# evalRomanToken returns the value of the token.
def evalRomanToken(parsed) -> int:
    if isinstance(parsed, str):
        info = getTokenInfo(parsed)
        if info is None:
            print(parsed + " is not a value Roman numeral.")
            return 0
        return info["value"]
    elif isinstance(parsed, list):
        if (len(parsed) == 2):
            if isinstance(parsed[0], str) and isinstance(parsed[1], str):
                leftInfo = getTokenInfo(parsed[0])
                rightInfo = getTokenInfo(parsed[1])
                return rightInfo["value"] - leftInfo["value"]
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
    info = getTokenInfo("M")
    level: int = info["value"]
    allowedOccurances: int = info["maxRep"]
    occurances = 0
    result: int = 0
    for token in parsed:
        value = evalRomanToken(token)
        if (value == level):
            occurances += 1
            if (allowedOccurances != -1):
                if (occurances > allowedOccurances):
                    print(f"Numeral {token} occurs more than the allowed number of times.")
                    return 0
        elif (value > level):
            print(f"Numeral {token} is out of place.")
            return 0
        else:
            occurances = 1
            level = value
            info = getTokenInfo(token)
            if info is None:
                allowedOccurances = 1
            else:
                allowedOccurances = info["maxRep"]
        result += value
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
        info = getTokenInfo(text)
        if info: return [text]
        else:
            print(text + " is not a valid Roman numeral.")
            return []
    else:
        if text[0:2] in romanMetaTokens:
            rest = tokenizeRoman(text[2:])
            rest.insert(0, destructMetaToken(text[0:2]))
            return rest
        else:
            info = getTokenInfo(text[0:1])
            if info:
                rest = tokenizeRoman(text[1:])
                rest.insert(0, text[0:1])
                return rest
            else:                
                print(text[0:1] + " is not a valid Roman numeral.")
                return []
        
userInput = input("Enter a number using Roman Numerals: ")
tokenList = tokenizeRoman(userInput)
print("tokenList ", end="")
print(tokenList, end=" evaluates to: ")
print(str(evalRomanTokenList(tokenList)))
