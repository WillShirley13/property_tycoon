from typing import TYPE_CHECKING, Union
from ..enums.property_group import PropertyGroup
from .. import errors

if TYPE_CHECKING:
    from ..property_owners.player import Player
    from ..property_owners.bank import Bank

class Ownable:
    def __init__(self, value: int, rent_cost: int, property_group: PropertyGroup, name: str):
        self.name: str = name
        self.owned_by = None  # Will be Player or Bank
        self.cost_to_buy: int = value
        self.value: int = value
        self.rent_cost: int = rent_cost
        self.is_mortgaged: bool = False
        self.property_group: PropertyGroup = property_group
        
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
        if player.is_in_jail:
            return 0
        player.sub_cash_balance(self.rent_cost)
        self.owned_by.add_cash_balance(self.rent_cost)
        return self.rent_cost      
