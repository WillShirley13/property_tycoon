class InsufficientFundsError(Exception):
    pass

class BankCannotSellPropertyError(Exception):
    pass

class CannotSellPropertyError(Exception):
    pass

class PropertyAlreadyMortgagedError(Exception):
    pass

class PropertyNotInPortfolioError(Exception):
    pass

class NoGetOutOfJailCardsError(Exception):
    pass

class PlayerAlreadyInJailError(Exception):
    pass

class PropertyAlreadyInPortfolioError(Exception):
    pass

class PropertyNotInPortfolioError(Exception):
    pass

class PropertyNotOwnedByBankError(Exception):
    pass

class NoHousesOrHotelsToSellError(Exception):
    pass

class MaxHousesOrHotelsError(Exception):
    pass
