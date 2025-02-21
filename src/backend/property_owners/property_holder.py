from backend.enums.property_group import PropertyGroup
from backend.ownables.ownable import Ownable
import errors

class PropertyHolder:
    def __init__(self, initial_cash: int):
        self.cash_balance: int = initial_cash
        self.owned_properties: dict[PropertyGroup, list[Ownable]] = {}

    def get_cash_balance(self) -> int:
        return self.cash_balance

    def add_cash_balance(self, amount: int) -> None:
        self.cash_balance += amount

    def sub_cash_balance(self, amount: int) -> None:
        if self.cash_balance - amount < 0:
            raise errors.InsufficientFundsError
        self.cash_balance -= amount
        
    def get_owned_properties(self) -> dict[PropertyGroup, list[Ownable]]:
        return self.owned_properties

    def add_property_to_portfolio(self, property: Ownable) -> None:
        # Check if property is already in portfolio
        if property in self.owned_properties[property.property_group]:
            raise errors.PropertyAlreadyInPortfolioError
        
        # Check if property group exists in portfolio
        if property.property_group not in self.owned_properties:
            self.owned_properties[property.property_group] = []
        
        # Add property to portfolio
        self.owned_properties[property.property_group].append(property)
    
    def remove_property_from_portfolio(self, property: Ownable) -> None:
        # Check if property group exists in portfolio
        if property.property_group not in self.owned_properties:
            raise errors.PropertyNotInPortfolioError
        
        self.owned_properties[property.property_group].remove(property)