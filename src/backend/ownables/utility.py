from typing import TYPE_CHECKING, override
from .ownable import Ownable
from ..constants import ONE_UTILITY_RENT_DICE_MULTIPLIER, TWO_UTILITY_RENT_DICE_MULTIPLIER
from ..enums.property_group import PropertyGroup
if TYPE_CHECKING:
    from ..property_owners.player import Player
    from ..property_owners.bank import Bank

class Utility(Ownable):
    def __init__(self, name: str, cost: int, property_group: PropertyGroup, owner: "Bank"):
        super().__init__(name=name, cost=cost, property_group=property_group, owner=owner)
        self.owner_owns_all_utilities: bool = False
        self.num_of_utilities_owned_by_owner: int = 0
    
    @override
    def get_rent_due_from_player(self, player: 'Player') -> int:
        # If property is mortgaged, no rent is due
        if self.is_mortgaged:
            return 0
        # Calculate rent due
        if self.num_of_utilities_owned_by_owner == 1:
            rent = sum(player.get_recent_dice_rolls()) * ONE_UTILITY_RENT_DICE_MULTIPLIER
        elif self.num_of_utilities_owned_by_owner == 2:
            rent = sum(player.get_recent_dice_rolls()) * TWO_UTILITY_RENT_DICE_MULTIPLIER
        else:
            rent = 0
        player.sub_cash_balance(rent)
        self.owned_by.add_cash_balance(rent)
        return rent
    
    def get_owner_owns_all_utilities(self) -> bool:
        return self.owner_owns_all_utilities
    
    def set_owner_owns_all_utilities(self, owner_owns_all_utilities: bool) -> None:
        self.owner_owns_all_utilities = owner_owns_all_utilities
        
    def get_num_of_utilities_owned_by_owner(self) -> int:
        return self.num_of_utilities_owned_by_owner
    
    def set_num_of_utilities_owned_by_owner(self, num_of_utilities_owned_by_owner: int) -> None:
        self.num_of_utilities_owned_by_owner = num_of_utilities_owned_by_owner
        
        
        

