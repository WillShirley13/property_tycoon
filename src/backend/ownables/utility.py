from backend.ownables.ownable import Ownable
from backend.property_owners.player import Player
from constants import *
from typing import override

class Utility(Ownable):
    def __init__(self, value: int, property_group, name: str):
        super().__init__(value, property_group, name)
        self.owner_owns_all_utilities: bool = False
        self.num_of_utilities_owned_by_owner: int = 0
        # No additional attributes or methods beyond Ownable 
        
    def set_rent_cost(self) -> None:
        if self.num_of_utilities_owned_by_owner == 1:
            self.rent_cost = ONE_UTILITY_RENT_DICE_MULTIPLIER
        elif self.num_of_utilities_owned_by_owner == 2:
            self.rent_cost = TWO_UTILITY_RENT_DICE_MULTIPLIER
    
    @override
    def get_rent_due_from_player(self, player: Player, dice_roll: int) -> int:
        # If property is mortgaged, no rent is due
        if self.is_mortgaged:
            return 0
        # If player is in jail, no rent is due
        if player.is_in_jail:
            return 0
        # Calculate rent due
        if self.num_of_utilities_owned_by_owner == 1:
            rent = dice_roll * ONE_UTILITY_RENT_DICE_MULTIPLIER
        elif self.num_of_utilities_owned_by_owner == 2:
            rent = dice_roll * TWO_UTILITY_RENT_DICE_MULTIPLIER
        player.sub_cash_balance(rent)
        self.owned_by.add_cash_balance(rent)
        return rent 

