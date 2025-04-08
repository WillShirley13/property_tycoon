from typing import TYPE_CHECKING, List, Optional, Union

from .. import errors
from ..constants import PROPERTY_BUILD_COSTS, PROPERTY_DATA
from ..enums.property_group import PropertyGroup
from .ownable import Ownable

if TYPE_CHECKING:
    from ..property_owners.bank import Bank
    from ..property_owners.player import Player


class Property(Ownable):
    def __init__(self, name: str, cost: int,
                 property_group: PropertyGroup, owner: "Bank" = None):
        super().__init__(name=name, cost=cost, property_group=property_group, owner=owner)
        self.houses: int = 0
        self.hotel: int = 0
        self.next_upgrade_cost: int = PROPERTY_BUILD_COSTS[self.property_group.value]["house"]
        self.owner_owns_all_properties_in_group: bool = False
        self.is_eligible_for_upgrade: bool = False
        self.is_eligible_for_downgrade: bool = False

    # Getters and Setters
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
        return self.is_eligible_for_upgrade

    def set_is_eligible_for_upgrade(
            self, is_eligible_for_upgrade: bool) -> None:
        self.is_eligible_for_upgrade = is_eligible_for_upgrade

    def get_is_eligible_for_downgrade(self) -> bool:
        return self.is_eligible_for_downgrade

    def set_is_eligible_for_downgrade(
            self, is_eligible_for_downgrade: bool) -> None:
        self.is_eligible_for_downgrade = is_eligible_for_downgrade

    def get_owner_owns_all_properties_in_group(self) -> bool:
        return self.owner_owns_all_properties_in_group

    def set_owner_owns_all_properties_in_group(
            self, owner_owns_all_properties_in_group: bool) -> None:
        self.owner_owns_all_properties_in_group = owner_owns_all_properties_in_group

    def set_current_sell_value(self, new_value: int = None,
                               downgrade: bool = False, upgrade: bool = False) -> None:
        if downgrade:
            self.current_sell_value.pop()
        elif upgrade:
            self.current_sell_value.append(new_value)

    # Property Management
    def upgrade_property(self, bank) -> None:
        try:
            # Check if property is eligible for upgrade
            if not self.get_is_eligible_for_upgrade():
                return False

            # If we have 4 houses, upgrade to a hotel
            if self.get_houses() == 4:
                # Check if upgrading to a hotel would violate the max difference rule
                if not self.check_max_difference_between_houses_owned_is_1_within_property_group(5):
                    return False

                hotel_cost = PROPERTY_BUILD_COSTS[self.property_group.value]["hotel"]
                self.get_owner().sub_cash_balance(hotel_cost)
                bank.add_cash_balance(hotel_cost)
                self.set_hotel(1)
                self.set_houses(0)  # Reset houses when upgrading to hotel
                self.set_total_value(hotel_cost, increase=True)
                self.set_current_sell_value(hotel_cost, upgrade=True)
                self.set_is_eligible_for_upgrade(False)
                self.set_is_eligible_for_downgrade(True)

            # Otherwise, add a house if eligible
            elif self.get_houses() < 4:
                # Check if adding a house would violate the max difference rule
                if not self.check_max_difference_between_houses_owned_is_1_within_property_group(
                        self.get_houses() + 1):
                    return False

                house_cost = PROPERTY_BUILD_COSTS[self.property_group.value]["house"]
                self.get_owner().sub_cash_balance(house_cost)
                bank.add_cash_balance(house_cost)
                self.set_houses(self.get_houses() + 1)
                self.set_total_value(house_cost, increase=True)
                self.set_current_sell_value(house_cost, upgrade=True)
                
                # Update eligibility flags
                if self.houses == 4:
                    self.set_is_eligible_for_upgrade(True)  # Can upgrade to hotel
                else:
                    self.set_is_eligible_for_upgrade(True)  # Can add more houses
                self.set_is_eligible_for_downgrade(True)  # Can always downgrade after upgrade

            # Update rent cost after upgrade
            self.set_rent_cost()
            
            # Update eligibility for all properties in the same group after upgrade
            self.update_eligibility_for_all_properties_in_group()
            
            return True

        except errors.InsufficientFundsError:
            raise errors.InsufficientFundsError
        except Exception as e:
            raise e

    def update_eligibility_for_all_properties_in_group(self) -> None:
        """Update eligibility flags for all properties in the same group after an upgrade/downgrade."""
        if not hasattr(self, 'owned_by') or self.owned_by is None:
            return
            
        properties_in_group = self.owned_by.owned_properties[self.property_group]
        
        # First, update the current property's eligibility based on all other properties
        current_houses = self.get_houses()
        has_hotel = self.get_hotel() == 1
        
        # Check current property's upgrade eligibility
        self_can_upgrade = True
        if has_hotel:
            # If it has a hotel, it can't be upgraded further
            self_can_upgrade = False
        elif current_houses < 4:
            # For each other property in the group
            for other_prop in properties_in_group:
                if other_prop == self:
                    continue
                    
                other_houses = other_prop.get_houses()
                other_hotel = other_prop.get_hotel()
                
                # If upgrading would create a difference > 1
                if (current_houses + 1) - other_houses > 1:
                    self_can_upgrade = False
                    break
                    
        self.set_is_eligible_for_upgrade(self_can_upgrade)
        
        # Then update all other properties
        for prop in properties_in_group:
            if prop == self:
                continue  # Skip the current property as we've already updated it
                
            current_houses = prop.get_houses()
            has_hotel = prop.get_hotel() == 1
            
            # Check if this property can be upgraded (won't violate max difference rule)
            can_upgrade = True
            if has_hotel:
                # If it has a hotel, it can't be upgraded further
                can_upgrade = False
            elif current_houses < 4:
                # Check if adding a house would violate max difference with ANY other property
                for other_prop in properties_in_group:
                    if other_prop == prop:
                        continue
                    
                    other_houses = other_prop.get_houses()
                    other_hotel = other_prop.get_hotel()
                    
                    # Convert hotel to equivalent houses (5) for comparison
                    other_level = 5 if other_hotel == 1 else other_houses
                    
                    # Check both directions of difference:
                    # 1. If upgrading would put this property too far ahead of others
                    if (current_houses + 1) - other_level > 1:
                        can_upgrade = False
                        break
                    # 2. If this property is too far behind others to be upgraded just once
                    if other_level - (current_houses + 1) > 1:
                        can_upgrade = False
                        break
            
            # Update the property's eligibility flags
            prop.set_is_eligible_for_upgrade(can_upgrade)
            
            # Also update downgrade eligibility
            can_downgrade = (has_hotel or current_houses > 0)
            if can_downgrade:
                # Check if downgrading would violate max difference
                downgrade_level = 4 if has_hotel else current_houses - 1
                for other_prop in properties_in_group:
                    if other_prop == prop:
                        continue
                    
                    other_houses = other_prop.get_houses()
                    other_hotel = other_prop.get_hotel()
                    
                    # Convert hotel to equivalent houses (5)
                    other_level = 5 if other_hotel == 1 else other_houses
                    
                    # Check if downgrading would create a difference > 1
                    if other_level - downgrade_level > 1:
                        can_downgrade = False
                        break
            
            prop.set_is_eligible_for_downgrade(can_downgrade)

    def downgrade_property(self, bank) -> None:
        try:
            # Check if property is eligible for downgrade
            if not self.get_is_eligible_for_downgrade():
                return False

            # If we have a hotel, downgrade to 4 houses
            if self.hotel == 1:
                # Check if downgrading to 4 houses would violate the max difference rule
                if not self.check_max_difference_between_houses_owned_is_1_within_property_group(4):
                    return False

                hotel_cost = PROPERTY_BUILD_COSTS[self.property_group.value]["hotel"]
                self.get_owner().add_cash_balance(hotel_cost)
                bank.sub_cash_balance(hotel_cost)
                self.set_hotel(0)
                self.set_houses(4)
                self.set_total_value(hotel_cost, increase=False)
                self.set_current_sell_value(downgrade=True)
                self.set_is_eligible_for_upgrade(True)  # Can upgrade back to hotel
                self.set_is_eligible_for_downgrade(True)  # Can downgrade houses

            # Otherwise, remove a house if we have any
            elif self.houses > 0:
                # Check if removing a house would violate the max difference rule
                if not self.check_max_difference_between_houses_owned_is_1_within_property_group(
                        self.get_houses() - 1):
                    return False

                house_cost = PROPERTY_BUILD_COSTS[self.property_group.value]["house"]
                self.get_owner().add_cash_balance(house_cost)
                bank.sub_cash_balance(house_cost)
                self.set_houses(self.get_houses() - 1)
                self.set_total_value(house_cost, increase=False)
                self.set_current_sell_value(downgrade=True)

                # Update eligibility flags
                if self.houses == 0:
                    self.set_is_eligible_for_upgrade(True)  # Can add houses
                    self.set_is_eligible_for_downgrade(False)  # No more houses to remove
                else:
                    self.set_is_eligible_for_upgrade(True)  # Can add more houses
                    self.set_is_eligible_for_downgrade(True)  # Can remove more houses

            # Update rent cost after downgrade
            self.set_rent_cost()
            
            # Update eligibility for all properties in the same group after downgrade
            self.update_eligibility_for_all_properties_in_group()
            
            return True

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

    def check_max_difference_between_houses_owned_is_1_within_property_group(
            self, this_props_houses_after_change: int) -> bool:
        properties_in_group = self.owned_by.owned_properties[self.property_group]

        # Check the difference between each property's houses and the proposed
        # change
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
