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
        self.hotel: int = 0
        self.next_upgrade_cost: int = PROPERTY_BUILD_COSTS[self.property_group.value]["house"]
        self.owner_owns_all_properties_in_group: bool = False
        self.is_eligible_for__upgrade: bool = False
        self.is_eligible_for__downgrade: bool = False
        
    def get_property_group(self) -> PropertyGroup:
        return self.property_group
    
    def get_houses(self) -> int:
        return self.houses
    
    def set_houses(self, houses: int) -> None:
        self.houses = houses
    
    def get_hotel(self) -> int:
        return self.hotel
    
    def set_hotel(self, hotel: int) -> None:
        self.hotel = hotel
    
    def get_is_eligible_for_upgrade(self) -> bool:
        return self.is_eligible_for_house_upgrade
    
    def set_is_eligible_for_upgrade(self, is_eligible_for_upgrade: bool) -> None:
        self.is_eligible_for_upgrade = is_eligible_for_upgrade
    
    def get_is_eligible_for_downgrade(self) -> bool:
        return self.is_eligible_for_downgrade
    
    def set_is_eligible_for_downgrade(self, is_eligible_for_downgrade: bool) -> None:
        self.is_eligible_for_downgrade = is_eligible_for_downgrade
    
    
    def upgrade_property(self, bank) -> None:
        """
        Upgrades a property by adding a house or hotel.
        A property can have up to 4 houses, after which a hotel can be purchased.
        """      
        try:
            # If we have 4 houses, upgrade to a hotel
            if self.get_houses() == 4 and self.get_is_eligible_upgrade():
                # Check if upgrading to a hotel would violate the max difference rule
                if not self.check_max_difference_between_houses_owned_is_1_within_property_group(5):
                    return
                    
                hotel_cost = PROPERTY_BUILD_COSTS[self.property_group.value]["hotel"]
                self.get_owner().sub_cash_balance(hotel_cost)
                bank.add_cash_balance(hotel_cost)
                self.set_hotel(1)
                self.set_value(self.get_value() + hotel_cost)
                self.set_is_eligible_for_upgrade(False)
                self.set_is_eligible_for_downgrade(True)
            
            # Otherwise, add a house if eligible
            elif self.get_houses() < 4 and self.get_is_eligible_for_upgrade():
                # Check if adding a house would violate the max difference rule
                if not self.check_max_difference_between_houses_owned_is_1_within_property_group(self.get_houses() + 1):
                    return
                    
                house_cost = PROPERTY_BUILD_COSTS[self.property_group.value]["house"]
                self.get_owner().sub_cash_balance(house_cost)
                bank.add_cash_balance(house_cost)
                self.set_houses(self.get_houses() + 1)
                self.set_value(self.get_value() + house_cost)
                self.set_is_eligible_for_upgrade(True)
                self.set_is_eligible_for_downgrade(True)
                # Update eligibility flags
                if self.houses == 4:
                    self.is_eligible_for_hotel_upgrade_or_downgrade = True
                    self.is_eligible_for_house_upgrade_or_downgrade = False
            
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
            if self.hotel == 1:
                cost = PROPERTY_BUILD_COSTS[self.property_group.get_value()]["hotel"]
                self.get_owner().add_cash_balance(cost)
                bank.sub_cash_balance(cost)
                self.set_hotel(0)
                self.set_houses(4)
                self.set_value(self.get_value() - cost)
                # Check if downgrading to 4 houses would violate the max difference rule 
                self.check_max_difference_between_houses_owned_is_1_within_property_group(4)
            
            # Otherwise, remove a house if we have any
            elif self.houses > 0:
                # Check if removing a house would violate the max difference rule
                cost = PROPERTY_BUILD_COSTS[self.property_group.get_value()]["house"]
                self.get_owner().add_cash_balance(cost)
                bank.sub_cash_balance(cost)
                self.set_houses(self.get_houses() - 1)
                self.set_value(self.get_value() - cost)
                self.check_max_difference_between_houses_owned_is_1_within_property_group(self.get_houses() - 1)
                
                if self.houses < 4:
                    self.is_eligible_for_hotel_upgrade_or_downgrade = False
            else:
                self.set_is_eligible_for_house_upgrade_or_downgrade(False)
                self.set_is_eligible_for_hotel_upgrade_or_downgrade(False)
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

    def check_max_difference_between_houses_owned_is_1_within_property_group(self, this_props_houses_after_change: int) -> bool:
        properties_in_group = self.owned_by.owned_properties[self.property_group]
        
        # Check the difference between each property's houses and the proposed change
        for prop in properties_in_group:
            # Skip comparing the property to itself
            if prop == self:
                continue                
                
            # Check if the difference would exceed 1
            if (this_props_houses_after_change - prop.get_houses()) > 1:
                self.set_is_eligible_for_upgrade(False)
                self.set_is_eligible_for_downgrade(True)
                return False
            elif (prop.get_houses() - this_props_houses_after_change) > 1:
                self.set_is_eligible_for_upgrade(True)
                self.set_is_eligible_for_downgrade(False)
                return False
        # If we get here, the difference is at most 1 for all properties
        return True
    
    def get_owner_owns_all_properties_in_group(self) -> bool:
        return self.owner_owns_all_properties_in_group
    
    def set_owner_owns_all_properties_in_group(self, owner_owns_all_properties_in_group: bool) -> None:
        self.owner_owns_all_properties_in_group = owner_owns_all_properties_in_group
    
    
