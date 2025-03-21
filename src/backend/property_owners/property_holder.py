from typing import TYPE_CHECKING, Dict, List
from ..enums.property_group import PropertyGroup
from .. import errors

if TYPE_CHECKING:
    from ..ownables.ownable import Ownable

class PropertyHolder:
    def __init__(self, initial_cash: int):
        self.cash_balance: int = initial_cash
        self.owned_properties: Dict[PropertyGroup, List['Ownable']] = {
        PropertyGroup.BROWN: [],
        PropertyGroup.BLUE: [],
        PropertyGroup.PURPLE: [],
        PropertyGroup.ORANGE: [],
        PropertyGroup.RED: [],
        PropertyGroup.YELLOW: [],
        PropertyGroup.GREEN: [],
        PropertyGroup.DEEP_BLUE: [],
        PropertyGroup.UTILITY: [],
        PropertyGroup.STATION: []
    }

    def get_cash_balance(self) -> int:
        return self.cash_balance

    def add_cash_balance(self, amount: int) -> None:
        self.cash_balance += amount

    def sub_cash_balance(self, amount: int) -> None:
        if self.cash_balance - amount < 0:
            raise errors.InsufficientFundsError
        self.cash_balance -= amount
        
    def get_owned_properties(self) -> Dict[PropertyGroup, List['Ownable']]:
        return self.owned_properties

    def add_property_to_portfolio(self, property: 'Ownable') -> None:
        # Check if property is already in portfolio
        if property in self.owned_properties[property.property_group]:
            raise errors.PropertyAlreadyInPortfolioError
        
        self.owned_properties[property.property_group].append(property)

    
    def remove_property_from_portfolio(self, property: 'Ownable') -> None:
        # Check if property group exists in portfolio
        if property.property_group not in self.owned_properties:
            raise errors.PropertyNotInPortfolioError
        
        self.owned_properties[property.property_group].remove(property)