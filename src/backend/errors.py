class InsufficientFundsError(Exception):
    """Raised when a player doesn't have enough money to perform an action"""
    pass

class BankCannotSellPropertyError(Exception):
    """Raised when attempting to sell a property that belongs to the bank"""
    pass

class CannotSellPropertyError(Exception):
    """Raised when a property cannot be sold (e.g., has houses/hotels)"""
    pass

class PropertyAlreadyMortgagedError(Exception):
    """Raised when trying to mortgage a property that is already mortgaged"""
    pass

class PropertyNotInPortfolioError(Exception):
    """Raised when trying to perform an action on a property not owned by the player"""
    pass

class NoGetOutOfJailCardsError(Exception):
    """Raised when trying to use a Get Out of Jail card when the player has none"""
    pass

class PlayerAlreadyInJailError(Exception):
    """Raised when trying to send a player to jail who is already in jail"""
    pass

class PropertyAlreadyInPortfolioError(Exception):
    """Raised when trying to acquire a property that the player already owns"""
    pass

class PropertyNotInPortfolioError(Exception):
    """Raised when trying to perform an action on a property not in the player's portfolio"""
    pass

class PropertyNotOwnedByBankError(Exception):
    """Raised when trying to buy a property that isn't owned by the bank"""
    pass

class NoHousesOrHotelsToSellError(Exception):
    """Raised when trying to sell houses/hotels from a property that has none"""
    pass

class MaxHousesOrHotelsError(Exception):
    """Raised when trying to build more houses/hotels than allowed on a property"""
    pass

class MaxDifferenceBetweenHousesOrHotelsError(Exception):
    """Raised when trying to build houses/hotels that would create an illegal imbalance in a color set"""
    pass

class FirstCircuitNotCompleteError(Exception):
    """Raised when trying to buy a property before the first circuit is complete"""
    pass

class MustOwnAllPropertiesInGroupError(Exception):
    """Raised when trying to build houses/hotels on a property that the player doesn't own all of the properties in the group"""
    pass

class PropertyNotOwnedByPlayerError(Exception):
    """Raised when trying to sell a property that isn't owned by the player"""
    pass


