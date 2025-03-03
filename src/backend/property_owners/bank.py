from typing import Dict, List

from ..ownables.ownable import Ownable
from ..constants import BANK_STARTING_CASH
from ..property_owners.property_holder import PropertyHolder
from ..enums.property_group import PropertyGroup

class Bank(PropertyHolder):
    def __init__(self):
        super().__init__(BANK_STARTING_CASH)
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
        self.cash_balance -= amount
    
    def get_owned_properties(self) -> List['Ownable']:
        return self.owned_properties
    
    def add_property_to_portfolio(self, property: 'Ownable') -> None:
        self.owned_properties[property.property_group].append(property)
    
    def remove_property_from_portfolio(self, property: 'Ownable') -> None:
        self.owned_properties[property.property_group].remove(property)
    
