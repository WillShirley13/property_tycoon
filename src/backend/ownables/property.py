from typing import TYPE_CHECKING, List, Optional, Union
from ..enums.property_group import PropertyGroup
from ..constants import PROPERTY_BUILD_COSTS, PROPERTY_DATA
from .ownable import Ownable
from .. import errors
if TYPE_CHECKING:
    from ..property_owners.player import Player
    from ..property_owners.bank import Bank

class Property(Ownable):
    def __init__(self, name: str, cost: int, property_group: PropertyGroup, owner: "Bank"):
        super().__init__(name=name, cost=cost, property_group=property_group, owner=owner)
        self.houses: int = 0
        self.hotel: bool = False
        self.next_upgrade_cost: int = PROPERTY_BUILD_COSTS[self.property_group.value]["house"]
        self.owner_owns_all_properties_in_group: bool = False
        self.is_eligible_for_house_upgrade: bool = False
        self.is_eligible_for_hotel_upgrade: bool = False
        
    def get_property_group(self) -> PropertyGroup:
        return self.property_group
    
    def get_houses(self) -> int:
        return self.houses
    
    def get_hotel(self) -> bool:
        return self.hotel
    
    def get_is_eligible_for_house_upgrade(self) -> bool:
        return self.is_eligible_for_house_upgrade
    
    def get_is_eligible_for_hotel_upgrade(self) -> bool:
        return self.is_eligible_for_hotel_upgrade
    
    

    def upgrade_property(self, bank) -> None:
        """
        Upgrades a property by adding a house or hotel.
        A property can have up to 4 houses, after which a hotel can be purchased.
        """      
        try:
            # If we have 4 houses, upgrade to a hotel
            if self.houses == 4 and self.is_eligible_for_hotel_upgrade:
                cost = PROPERTY_BUILD_COSTS[self.property_group.value]["hotel"]
                self.owned_by.sub_cash_balance(cost)
                bank.add_cash_balance(cost)
                self.houses = 0
                self.hotel = True
                self.is_eligible_for_hotel_upgrade = False
                self.value = self.value + self.hotel_cost
            
            # Otherwise, add a house if eligible
            elif self.houses < 4 and self.is_eligible_for_house_upgrade:                   
                cost = PROPERTY_BUILD_COSTS[self.property_group.value]["house"]
                self.owned_by.sub_cash_balance(cost)
                bank.add_cash_balance(cost)
                self.houses += 1
                self.value = self.value + self.house_cost
                self.check_max_difference_between_houses_owned_is_1_within_property_group(self.houses + 1)
                
                # Update eligibility flags
                if self.houses == 4:
                    self.is_eligible_for_hotel_upgrade = True
                    self.is_eligible_for_house_upgrade = False
            
            # Update rent cost after upgrade
            self.set_rent_cost()
            
        except errors.InsufficientFundsError:
            raise errors.InsufficientFundsError
        except Exception as e:
            raise e

    def downgrade_property(self, bank) -> None:
        """
        Downgrades a property by removing a hotel or house.
        When a hotel is removed, 4 houses are placed on the property.
        """
        try:
            # If we have a hotel, downgrade to 4 houses
            if self.hotel:
                cost = PROPERTY_BUILD_COSTS[self.property_group.value]["hotel"]
                self.owned_by.add_cash_balance(cost)
                bank.sub_cash_balance(cost)
                self.hotel = False
                self.houses = 4
                self.is_eligible_for_hotel_upgrade = True
                self.value = self.value - self.hotel_cost
            
            # Otherwise, remove a house if we have any
            elif self.houses > 0:                  
                cost = PROPERTY_BUILD_COSTS[self.property_group.value]["house"]
                self.owned_by.add_cash_balance(cost)
                bank.sub_cash_balance(cost)
                self.houses -= 1
                self.value = self.value - self.house_cost
                self.check_max_difference_between_houses_owned_is_1_within_property_group(self.houses - 1)
                
                # Update eligibility flags
                self.is_eligible_for_house_upgrade = True
                if self.houses < 4:
                    self.is_eligible_for_hotel_upgrade = False
            else:
                raise errors.NoHousesOrHotelsToSellError
            
            # Update rent cost after downgrade
            self.set_rent_cost()
            
        except Exception as e:
            raise e

    def set_rent_cost(self) -> None:
        if not self.owner_owns_all_properties_in_group:
            self.rent_cost = PROPERTY_DATA[self.name]["rents"][0]
        elif self.owner_owns_all_properties_in_group and self.houses == 0 and self.hotel == 0:
            self.rent_cost = self.rent_cost * 2
        elif self.houses == 1:
            self.rent_cost = PROPERTY_DATA[self.name]["rents"][1]
        elif self.houses == 2:
            self.rent_cost = PROPERTY_DATA[self.name]["rents"][2]
        elif self.houses == 3:
            self.rent_cost = PROPERTY_DATA[self.name]["rents"][3]
        elif self.houses == 4:
            self.rent_cost = PROPERTY_DATA[self.name]["rents"][4]
        elif self.hotel == 1:
            self.rent_cost = PROPERTY_DATA[self.name]["rents"][5]

    # Checks if the max difference between the houses owned by the player in the property group is 1
    def check_max_difference_between_houses_owned_is_1_within_property_group(self, this_props_houses_after_change: int) -> bool:
        houses_for_property_in_group = [(property.name, property.houses) for property in self.owned_by.owned_properties[self.property_group]]
        for property in houses_for_property_in_group:
            if abs(property[1] - this_props_houses_after_change) > 1:
                self.is_eligible_for_house_upgrade = False
                return False
        self.is_eligible_for_house_upgrade = True
        return True
        
