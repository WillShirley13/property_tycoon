from backend.enums.property_group import PropertyGroup
from backend.ownables.ownable import Ownable
from backend.property_owners.player import Player
from constants import *
import errors
class Property(Ownable):
    def __init__(self, value: int, property_group: PropertyGroup, name: str, house_cost: int, hotel_cost: int, rent: int):
        super().__init__(value, property_group, name)
        self.houses: int = 0  
        self.house_cost: int = house_cost  
        self.hotel: int = 0  
        self.hotel_cost: int = hotel_cost 
        self.rent: int = rent 
        self.owner_owns_all_properties_in_group: bool = False

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
        
