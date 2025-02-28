from typing import TYPE_CHECKING, List, Optional, Union
from ..enums.property_group import PropertyGroup
from ..constants import HOUSE_COST, HOTEL_COST
from .ownable import Ownable

if TYPE_CHECKING:
    from ..property_owners.player import Player

class Property(Ownable):
    def __init__(self, name: str, cost: int, property_group: PropertyGroup, rent_values: List[int]):
        super().__init__(name, cost)
        self.property_group: PropertyGroup = property_group
        self.rent_values: List[int] = rent_values
        self.houses: int = 0
        self.hotel: bool = False
        
    def get_property_group(self) -> PropertyGroup:
        return self.property_group
    
    def get_rent_due_from_player(self, player: 'Player') -> int:
        # Get the rent due from a player based on the property's development
        # ... implementation details ...
        return self.rent_values[0]  # Placeholder
    
    def get_houses(self) -> int:
        return self.houses
    
    def get_hotel(self) -> bool:
        return self.hotel
    
    def add_house(self) -> None:
        if self.houses < 4:
            self.houses += 1
        else:
            raise ValueError("Cannot add more than 4 houses to a property")
    
    def add_hotel(self) -> None:
        if self.houses == 4:
            self.houses = 0
            self.hotel = True
        else:
            raise ValueError("Cannot add a hotel without 4 houses")
    
    def remove_house(self) -> None:
        if self.houses > 0:
            self.houses -= 1
        else:
            raise ValueError("Cannot remove a house when there are none")
    
    def remove_hotel(self) -> None:
        if self.hotel:
            self.hotel = False
            self.houses = 4
        else:
            raise ValueError("Cannot remove a hotel when there is none")
    
    def get_house_cost(self) -> int:
        return HOUSE_COST
    
    def get_hotel_cost(self) -> int:
        return HOTEL_COST

    def buy_house(self, bank) -> None:
        if not self.check_max_difference_between_houses_owned_is_1_within_property_group(self.houses + 1):
            raise errors.MaxDifferenceBetweenHousesOrHotelsError
        if not self.owner_owns_all_properties_in_group:
            raise errors.MustOwnAllPropertiesInGroupError
        if self.houses < 4:
            try:
                cost = PROPERTY_BUILD_COSTS[self.property_group.value]["house"]
                self.owned_by.sub_cash_balance(cost)
                bank.add_cash_balance(cost)
                self.houses += 1
                self.set_rent_cost()
                self.value = self.value + self.house_cost
            except:
                raise errors.InsufficientFundsError
        else:
            raise errors.MaxHousesOrHotelsError

    def buy_hotel(self, bank) -> None:
        if self.houses == 4 and self.hotel == 0:
            try:
                cost = PROPERTY_BUILD_COSTS[self.property_group.value]["hotel"]
                self.owned_by.sub_cash_balance(cost)
                bank.add_cash_balance(cost)
                self.hotel += 1
                self.set_rent_cost()
                self.value = self.value + self.hotel_cost
            except:
                raise errors.InsufficientFundsError
        else:
            raise errors.MaxHousesOrHotelsError

    def sell_house(self, bank) -> None:
        if not self.check_max_difference_between_houses_owned_is_1_within_property_group(self.houses - 1):
            raise errors.MaxDifferenceBetweenHousesOrHotelsError
        if self.houses > 0:
            cost = PROPERTY_BUILD_COSTS[self.property_group.value]["house"]
            self.owned_by.add_cash_balance(cost)
            bank.sub_cash_balance(cost)
            self.houses -= 1
            self.set_rent_cost()
            self.value = self.value - self.house_cost
        else:
            raise errors.NoHousesOrHotelsToSellError


    def sell_hotel(self, bank) -> None:
        if self.hotel == 1:
            cost = PROPERTY_BUILD_COSTS[self.property_group.value]["hotel"]
            self.owned_by.add_cash_balance(cost)
            bank.sub_cash_balance(cost)
            self.hotel -= 1
            self.set_rent_cost()
            self.value = self.value - self.hotel_cost
        else:
            raise errors.NoHousesOrHotelsToSellError
    
    def set_rent_cost(self, new_rent_cost: int) -> None:
        if self.owner_owns_all_properties and self.houses == 0 and self.hotel == 0:
            self.rent = self.rent * 2
        elif self.houses == 1:
            self.rent = PROPERTY_DATA[self.name]["rents"][1]
        elif self.houses == 2:
            self.rent = PROPERTY_DATA[self.name]["rents"][2]
        elif self.houses == 3:
            self.rent = PROPERTY_DATA[self.name]["rents"][3]
        elif self.houses == 4:
            self.rent = PROPERTY_DATA[self.name]["rents"][4]
        elif self.hotel == 1:
            self.rent = PROPERTY_DATA[self.name]["rents"][5]

    # Checks if the max difference between the houses owned by the player in the property group is 1
    def check_max_difference_between_houses_owned_is_1_within_property_group(self, this_props_houses_after_change: int) -> bool:
        houses_for_property_in_group = [(property.name, property.houses) for property in self.owned_by.owned_properties[self.property_group]]
        for property in houses_for_property_in_group:
            if abs(property[1] - this_props_houses_after_change) > 1:
                return False
        return True
        
