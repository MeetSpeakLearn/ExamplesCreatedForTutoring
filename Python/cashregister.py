# © 2024, Stephen DeVoy, All rights reserved.

import enum
import sys

# Enumeration of cash types. This enumeration plays no current role, beyond its types being associated
# with units within currencies. I've included this because I assume I will leverage off of it later.
# I plan a future extension where a currency is associated with a cash drawer and the cash drawer's
# inventory records the number of bills and coins of each unit type. Many currencies have coins and
# notes with the same face value. For example, there exists both a $1 note and a $1 coin in US currency.
# It may become useful to distingish between the two when paying out cash. For example, one type may have
# special uses that the other type does not. A person may prefer one form over the other. A store may
# wish not get rid of one form as quickly as it can because some customers may shun it.
# There also exists the possibility of local currencies that stand in for another currency on a
# one to one basis. The Panamanian Balboa is an example. The Balboa is issued by the government of Panama,
# though the official currency is the US dollar. One balboa equals one dollar. A business may wish to get
# rid of balboas in favor of retaining dollars. Distinguishing between these things may be useful. Thus,
# there may be more than one kind of note for the value within the defacto currency of a location.
# The choice of which to dole out may not be insignificant, depending upon the circumstances.
# A customer may wish to be paid only in coins, if that customer needs coins for vending machines,
# for example. It make sense to add this type from the beginning, even if we do not yet use it.
class NoteOrCoin(enum.Enum):
    COIN = 0
    NOTE = 1

# This class will be expanded in the future. At the moment, it only contains two kinds of information:
#   A breakdown of the kinds of monetary instruments that may be paid out in a currency and a value
#   indicating a decimal factor for converting external values to internal values.
#   All amounts associated with monetary instruments are stored in the lowest unit of the currency.
#   For the US dollar, this is the cent. Thus, all amounts stored and associated with the various bills
#   and coins is expressed in cents. The decimal value allows us to convert from $100 dollars to
#   10,000 cents by multiplying by self.decimal, which is 100 for the US dollar. Some currencies use
#   three decimal places. For those, self.decimal would be 1000, etc.
class Currency:
    # Class method for creating a dictionary for a specific monetary instrument.
    def createNoteOrCoinDict(name: str, value: int, type: NoteOrCoin) -> dict:
        return {'name': name, 'value': value, 'type': type}
    
    # Constructor method
    def __init__(self, decimal: int):
        self.notesAndCoins = []         # A list of NoteOrCount dictionaries always maintained in decreasing order of value.
        self.decimal = decimal          # Multiply actual currency values by this amount to obtain units used within this class.
                                        # Divide by this amount to translate from units used within the class to those used as currency.
    
    # Add a monetary instrument to the currency
    def addNoteOrCoin(self, name: str, value: int, type: NoteOrCoin):
        count: int = len(self.notesAndCoins)
        newItem: dict = Currency.createNoteOrCoinDict(name, value, type)
        if count == 0:
            self.notesAndCoins.append(newItem)
        elif count == 1:
            if value > self.notesAndCoins[0]['value']:
                self.notesAndCoins.insert(0, newItem)
            else:
                self.notesAndCoins.append(newItem)
        else:
            index: int = 0
            for noteOrCoinDict in self.notesAndCoins:
                if value > noteOrCoinDict['value']:
                    self.notesAndCoins.insert(0, newItem)
                    return
                index += 1
            self.notesAndCoins.insert(index, newItem)
        return
    
    # After all monetary instruments have been added, call this method to verify that
    # there is only one monetary instrument for each associated currency amount.
    # Note, this may change in future versions. The current assumption is that
    # future versions will allow different NoteOrCount type value for the same
    # monetary amount.
    def validate(self) -> bool:
        if len(self.notesAndCoins) == 0:
            return False
        previousValue = -1
        for item in self.notesAndCoins:
            value = item['value']
            if (value == previousValue): return False
            previousValue = value
        return True
    
    # Given an amount, represented in internal form, return a list of payouts.
    # Each payout is a two item list. The first item is a quantity and the second
    # is a monetary instrument dictionary. Quantity species how many instances of
    # the monetary instrument are to be paid out. The monetary instrument dictionary,
    # describes that monetary instrument.
    def payOut(self, amount: int) -> list:
        if (amount == 0): return []
        selectedUnit: dict = None
        quantityOfUnit: int = 0
        for unit in self.notesAndCoins:
            if (quantityOfUnit := (amount // unit['value'])):
                selectedUnit = unit
                break
        if (selectedUnit):
            newAmount = amount - quantityOfUnit * selectedUnit['value']
            subresult = self.payOut(newAmount)
            subresult.insert(0, [quantityOfUnit, selectedUnit])
            return subresult
        else:
            return []
    
    # Accepts a currency value in external units and converts it to internal units.
    # For example, give one dollar it converts the amount to 100 cents.
    def convertToUnits(self, amount: float) -> int:
        return int(amount * self.decimal)
    
    # Accepts a quantity in internal units and converts it to the external amount
    # used in transactions. For example, it translates 100 cents into 1 dollar.
    def convertFromUnits(self, amount: int) -> float:
        return int(amount / self.decimal)
        
USDollars = Currency(100)
USDollars.addNoteOrCoin("Hundred Dollar Bill", 10000, NoteOrCoin.NOTE)
USDollars.addNoteOrCoin("Fifty Dollar Bill", 5000, NoteOrCoin.NOTE)
USDollars.addNoteOrCoin("Twenty Dollar Bill", 2000, NoteOrCoin.NOTE)
USDollars.addNoteOrCoin("Ten Dollar Bill", 1000, NoteOrCoin.NOTE)
USDollars.addNoteOrCoin("Five Dollar Bill", 500, NoteOrCoin.NOTE)
USDollars.addNoteOrCoin("One Dollar Bill", 100, NoteOrCoin.NOTE)
USDollars.addNoteOrCoin("Half Dollar Coin", 50, NoteOrCoin.COIN)
USDollars.addNoteOrCoin("Quarter", 25, NoteOrCoin.COIN)
USDollars.addNoteOrCoin("Dime", 10, NoteOrCoin.COIN)
USDollars.addNoteOrCoin("Nickle", 5, NoteOrCoin.COIN)
USDollars.addNoteOrCoin("Penny", 1, NoteOrCoin.COIN)

if USDollars.validate():
    print("Currency verified!")
else:
    print("Currency invalid!")

finished: bool = False

while not finished:
    amountInCurrency = input("How much should I pay out in this currency? ")
    amountInUnits = USDollars.convertToUnits(float(amountInCurrency))
    notesOrCoins = USDollars.payOut(amountInUnits)
    
    if (notesOrCoins):    
        print("Pay out the following:")
        
        for noteOrCoin in notesOrCoins:
            quantity, medium = noteOrCoin
            print(f"  {quantity} {medium['name']}(s)")
    else:
        print("Unable to make payout.")
    
    again = input("Make another payout? (Y/N): ")
    finished = again in ['N', 'n', 'No', 'NO', 'no']
