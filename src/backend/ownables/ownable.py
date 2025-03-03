from typing import TYPE_CHECKING, Union
from ..enums.property_group import PropertyGroup
from .. import errors
from ..constants import PROPERTY_DATA
if TYPE_CHECKING:
    from ..property_owners.player import Player
    from ..property_owners.bank import Bank

class Ownable:
    def __init__(self, cost: int, property_group: PropertyGroup, name: str, owner: "Bank"):
        self.name: str = name
        self.owned_by = owner  # Will be Player or Bank
        self.cost_to_buy: int = cost
        self.value: int = cost
        self.rent_cost: int = PROPERTY_DATA[self.name]["rents"][0]
        self.is_mortgaged: bool = False
        self.property_group: PropertyGroup = property_group
        
    def get_name(self) -> str:
        return self.name
    
    def get_cost(self) -> int:
        return self.cost_to_buy

    def get_owner(self) -> Union['Player', 'Bank']:
        return self.owned_by

    def set_owner(self, new_owner: Union['Player', 'Bank']) -> None:
        self.owned_by = new_owner

    def get_rent_due_from_player(self, player: 'Player') -> int:
        # If property is mortgaged, no rent is due
        if self.is_mortgaged:
            return 0
        # If player is in jail, no rent is due
        if self.owned_by.is_in_jail:
            return 0
        player.sub_cash_balance(self.rent_cost)
        self.owned_by.add_cash_balance(self.rent_cost)
        return self.rent_cost      
