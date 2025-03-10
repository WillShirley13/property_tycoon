from typing import TYPE_CHECKING, override
from ..property_owners.property_holder import PropertyHolder
from ..enums.game_token import GameToken
from ..enums.property_group import PropertyGroup
from ..constants import *
from ..ownables.property import Property
from .. import errors
import random

if TYPE_CHECKING:
    from ..non_ownables.go import Go
    from ..non_ownables.jail import Jail
    from ..ownables.ownable import Ownable
    from ..property_owners.bank import Bank

class Player(PropertyHolder):
    def __init__(self, game_token: GameToken, name: str):
        super().__init__(initial_cash=1_500)
        self.name: str = name
        self.game_token: GameToken = game_token
        self.get_out_of_jail_cards: int = 0
        self.is_in_jail: bool = False
        self.rounds_in_jail: int = 0
        self.is_first_circuit_complete: bool = False
        self.has_passed_go_flag: bool = False
        self.current_position: int = 0  
        self.doubles_rolled: int = 0
        self.is_bankrupt: bool = False
        self.recent_dice_rolls: list[int] = []
        
    # Name and token methods
    def get_name(self) -> str:
        return self.name
    
    def get_game_token(self) -> GameToken:
        return self.game_token

    # Jail card methods
    def get_get_out_of_jail_cards(self) -> int:
        return self.get_out_of_jail_cards
    
    def add_get_out_of_jail_card(self) -> None:
        self.get_out_of_jail_cards += 1
        
    def use_get_out_of_jail(self, jail: 'Jail') -> None:
        if self.get_out_of_jail_cards > 0:
            jail.release_from_jail(self)
            self.get_out_of_jail_cards -= 1
    
    # Jail status methods
    def get_is_in_jail(self) -> bool:
        return self.is_in_jail
    
    def get_rounds_in_jail(self) -> int:
        return self.rounds_in_jail
        
    def set_rounds_in_jail(self, rounds: int) -> None:
        self.rounds_in_jail = rounds
    
    # Position and movement methods
    def get_current_position(self) -> int:
        return self.current_position
    
    def get_is_first_circuit_complete(self) -> bool:
        return self.is_first_circuit_complete
    
    def set_is_first_circuit_complete(self) -> None:
        self.is_first_circuit_complete = True
    
    def get_has_passed_go_flag(self) -> bool:
        if self.has_passed_go_flag:
            self.has_passed_go_flag = False
        return self.has_passed_go_flag
    
    def set_has_passed_go_flag(self, has_passed_go_flag: bool) -> None:
        self.has_passed_go_flag = has_passed_go_flag
    
    # functionality has been moved above to get_has_passed_go_flag
    # def reset_has_passed_go_flag(self) -> None:
    #     self.has_passed_go_flag = False

    # Property transaction methods
    def purchase_property(self, property: 'Ownable', bank: 'Bank') -> None:      
        property_cost = property.get_cost()
        if self.cash_balance < property_cost:
            raise errors.InsufficientFundsError
        
        # Pay for property
        self.sub_cash_balance(property_cost)
        bank.add_cash_balance(property_cost)
        
        # update property portfolios
        self._add_property_to_portfolio(property)
        bank.remove_property_from_portfolio(property)
        
        # update ownership
        property.set_owner(self)
        
    def sell_property(self, property: 'Ownable', bank: 'Bank') -> None:
        if property.is_mortgaged:
            # update property portfolios
            self.add_cash_balance(property.get_cost() / 2)
            bank.sub_cash_balance(property.get_cost() / 2)
            property.set_is_mortgaged(False)
        else:
            self.add_cash_balance(property.get_cost())
            bank.sub_cash_balance(property.get_cost())
        self._remove_property_from_portfolio(property)
        bank.add_property_to_portfolio(property)
    
    def mortgage_property(self, property: 'Ownable', bank: 'Bank') -> None:    
        property.set_is_mortgaged(True)
        property.set_owner(bank)
        
        total_value = 0
        
        if type(property) == Property:
            total_value += property.get_houses() * PROPERTY_BUILD_COSTS[property.get_property_group().value]["house"]
            total_value += property.get_hotel() * PROPERTY_BUILD_COSTS[property.get_property_group().value]["hotel"]
        
        self.sub_cash_balance(total_value / 2)
        bank.add_cash_balance(total_value / 2)
        
    def pay_off_mortgage(self, property: 'Ownable', bank: 'Bank') -> None:
        try:
            property.set_is_mortgaged(False)
            property.set_owner(self)
            
            total_value = 0
            
            if type(property) == Property:
                total_value += property.get_houses() * PROPERTY_BUILD_COSTS[property.get_property_group().value]["house"]
                total_value += property.get_hotel() * PROPERTY_BUILD_COSTS[property.get_property_group().value]["hotel"]
                
            self.sub_cash_balance(total_value)
            bank.add_cash_balance(total_value)
        except:
            raise errors.InsufficientFundsError
    
    @override
    def _add_property_to_portfolio(self, property: 'Ownable') -> None:
        self.owned_properties[property.property_group].append(property)

        match property.get_property_group():
            case PropertyGroup.BROWN:
                if len(self.owned_properties[PropertyGroup.BROWN]) == TOTAL_BROWN_PROPERTIES:
                    for prop in self.owned_properties[PropertyGroup.BROWN]:
                        prop.set_owner_owns_all_properties_in_group(True)
                        prop.set_is_eligible_for_house_upgrade_or_downgrade(True)
            case PropertyGroup.BLUE:
                if len(self.owned_properties[PropertyGroup.BLUE]) == TOTAL_BLUE_PROPERTIES:
                    for prop in self.owned_properties[PropertyGroup.BLUE]:
                        prop.set_owner_owns_all_properties_in_group(True)
                        prop.set_is_eligible_for_house_upgrade_or_downgrade(True)
            case PropertyGroup.PURPLE:
                if len(self.owned_properties[PropertyGroup.PURPLE]) == TOTAL_PURPLE_PROPERTIES:
                    for prop in self.owned_properties[PropertyGroup.PURPLE]:
                        prop.set_owner_owns_all_properties_in_group(True)
                        prop.set_is_eligible_for_house_upgrade_or_downgrade(True)
            case PropertyGroup.ORANGE:
                if len(self.owned_properties[PropertyGroup.ORANGE]) == TOTAL_ORANGE_PROPERTIES:
                    for prop in self.owned_properties[PropertyGroup.ORANGE]:
                        prop.set_owner_owns_all_properties_in_group(True)
                        prop.set_is_eligible_for_house_upgrade_or_downgrade(True)
            case PropertyGroup.RED:
                if len(self.owned_properties[PropertyGroup.RED]) == TOTAL_RED_PROPERTIES:
                    for prop in self.owned_properties[PropertyGroup.RED]:
                        prop.set_owner_owns_all_properties_in_group(True)
                        prop.set_is_eligible_for_house_upgrade_or_downgrade(True)
            case PropertyGroup.YELLOW:
                if len(self.owned_properties[PropertyGroup.YELLOW]) == TOTAL_YELLOW_PROPERTIES:
                    for prop in self.owned_properties[PropertyGroup.YELLOW]:
                        prop.set_owner_owns_all_properties_in_group(True)
                        prop.set_is_eligible_for_house_upgrade_or_downgrade(True)
            case PropertyGroup.GREEN:
                if len(self.owned_properties[PropertyGroup.GREEN]) == TOTAL_GREEN_PROPERTIES:
                    for prop in self.owned_properties[PropertyGroup.GREEN]:
                        prop.set_owner_owns_all_properties_in_group(True)
                        prop.set_is_eligible_for_house_upgrade_or_downgrade(True)
            case PropertyGroup.DEEP_BLUE:
                if len(self.owned_properties[PropertyGroup.DEEP_BLUE]) == TOTAL_DEEP_BLUE_PROPERTIES:
                    for prop in self.owned_properties[PropertyGroup.DEEP_BLUE]:
                        prop.set_owner_owns_all_properties_in_group(True)
                        prop.set_is_eligible_for_house_upgrade_or_downgrade(True)
            case PropertyGroup.STATION:
                property.num_of_stations_owned_by_owner += 1
                if len(self.owned_properties[PropertyGroup.STATION]) == TOTAL_STATIONS:
                    for prop in self.owned_properties[PropertyGroup.STATION]:
                        prop.set_owner_owns_all_stations(True)
            case PropertyGroup.UTILITY:
                property.num_of_utilities_owned_by_owner += 1
                if len(self.owned_properties[PropertyGroup.UTILITY]) == TOTAL_UTILITIES:
                    for prop in self.owned_properties[PropertyGroup.UTILITY]:
                        prop.set_owner_owns_all_utilities(True)
            case _:
                pass

    @override
    def _remove_property_from_portfolio(self, property: 'Ownable') -> None:
        if property not in self.owned_properties[property.property_group]:
            raise errors.PropertyNotInPortfolioError
        
        self.owned_properties[property.property_group].remove(property)

        match property.property_group:
            case PropertyGroup.BROWN:
                if len(self.owned_properties[PropertyGroup.BROWN]) != TOTAL_BROWN_PROPERTIES:
                    for prop in self.owned_properties[PropertyGroup.BROWN]:
                        prop.set_owner_owns_all_properties_in_group(False)
            case PropertyGroup.BLUE:
                if len(self.owned_properties[PropertyGroup.BLUE]) != TOTAL_BLUE_PROPERTIES:
                    for prop in self.owned_properties[PropertyGroup.BLUE]:
                        prop.set_owner_owns_all_properties_in_group(False)
                        prop.set_is_eligible_for_house_upgrade_or_downgrade(False)
                        prop.set_is_eligible_for_hotel_upgrade_or_downgrade(False)
            case PropertyGroup.PURPLE:
                if len(self.owned_properties[PropertyGroup.PURPLE]) != TOTAL_PURPLE_PROPERTIES:
                    for prop in self.owned_properties[PropertyGroup.PURPLE]:
                        prop.set_owner_owns_all_properties_in_group(False)
                        prop.set_is_eligible_for_house_upgrade_or_downgrade(False)
                        prop.set_is_eligible_for_hotel_upgrade_or_downgrade(False)
            case PropertyGroup.ORANGE:
                if len(self.owned_properties[PropertyGroup.ORANGE]) != TOTAL_ORANGE_PROPERTIES:
                    for prop in self.owned_properties[PropertyGroup.ORANGE]:
                        prop.set_owner_owns_all_properties_in_group(False)
                        prop.set_is_eligible_for_house_upgrade_or_downgrade(False)
                        prop.set_is_eligible_for_hotel_upgrade_or_downgrade(False)
            case PropertyGroup.RED:
                if len(self.owned_properties[PropertyGroup.RED]) != TOTAL_RED_PROPERTIES:
                    for prop in self.owned_properties[PropertyGroup.RED]:
                        prop.set_owner_owns_all_properties_in_group(False)
                        prop.set_is_eligible_for_house_upgrade_or_downgrade(False)
                        prop.set_is_eligible_for_hotel_upgrade_or_downgrade(False)
            case PropertyGroup.YELLOW:
                if len(self.owned_properties[PropertyGroup.YELLOW]) != TOTAL_YELLOW_PROPERTIES:
                    for prop in self.owned_properties[PropertyGroup.YELLOW]:
                        prop.set_owner_owns_all_properties_in_group(False)
                        prop.set_is_eligible_for_house_upgrade_or_downgrade(False)
                        prop.set_is_eligible_for_hotel_upgrade_or_downgrade(False)
            case PropertyGroup.GREEN:
                if len(self.owned_properties[PropertyGroup.GREEN]) != TOTAL_GREEN_PROPERTIES:
                    for prop in self.owned_properties[PropertyGroup.GREEN]:
                        prop.set_owner_owns_all_properties_in_group(False)
                        prop.set_is_eligible_for_house_upgrade_or_downgrade(False)
                        prop.set_is_eligible_for_hotel_upgrade_or_downgrade(False)
            case PropertyGroup.DEEP_BLUE:
                if len(self.owned_properties[PropertyGroup.DEEP_BLUE]) != TOTAL_DEEP_BLUE_PROPERTIES:
                    for prop in self.owned_properties[PropertyGroup.DEEP_BLUE]:
                        prop.set_owner_owns_all_properties_in_group(False)
                        prop.set_is_eligible_for_house_upgrade_or_downgrade(False)
                        prop.set_is_eligible_for_hotel_upgrade_or_downgrade(False)
            case PropertyGroup.STATION:
                property.num_of_stations_owned_by_owner -= 1
                if len(self.owned_properties[PropertyGroup.STATION]) != TOTAL_STATIONS:
                    for prop in self.owned_properties[PropertyGroup.STATION]:
                        prop.set_owner_owns_all_stations(False)
            case PropertyGroup.UTILITY:
                property.num_of_utilities_owned_by_owner -= 1
                if len(self.owned_properties[PropertyGroup.UTILITY]) != TOTAL_UTILITIES:
                    for prop in self.owned_properties[PropertyGroup.UTILITY]:
                        prop.set_owner_owns_all_utilities(False)
            case _:
                pass

    # Movement methods
    ### CURRENTLY MOVING PLAYER METHODS DO NOT PAY PLAYER FOR PASSING GO ###
    # Updates current_position and is_first_circuit_complete and returns new position
    # Returns a list of dice rolls and the new position
    def move_player(self) -> list[list[int], int] | None:
        dice_rolls: list[int] = [random.randint(1, 6) for _ in range(2)]
        if dice_rolls[0] == dice_rolls[1]:
            self.set_doubles_rolled(self.get_doubles_rolled() + 1)
        else:
            self.set_doubles_rolled(0)
        if self.get_doubles_rolled() == 3:
            self.set_doubles_rolled(0)
            # return None to indicate that the player has rolled three doubles and should go to jail
            return None
    
        # Faciliate circular board
        if self.current_position + sum(dice_rolls) > 39:
            if not self.get_is_first_circuit_complete():
                self.set_is_first_circuit_complete()
                self.set_has_passed_go_flag(True)
            self.current_position = (self.current_position + sum(dice_rolls)) % 40    
        else:
            self.current_position += sum(dice_rolls)
        self.set_recent_dice_rolls(dice_rolls)
        return [dice_rolls, self.current_position]

    # Updates current_position to a specified position
    def move_player_to_position(self, position: int) -> None:
        self.current_position = position
    
    def get_recent_dice_rolls(self) -> list[int]:
        return self.recent_dice_rolls
    
    def set_recent_dice_rolls(self, recent_dice_rolls: list[int]) -> None:
        self.recent_dice_rolls = recent_dice_rolls
    
    # Doubles methods
    def get_doubles_rolled(self) -> int:
        return self.doubles_rolled
    
    def set_doubles_rolled(self, doubles_rolled: int) -> None:
        self.doubles_rolled = doubles_rolled
    
    def reset_doubles_rolled(self) -> None:
        self.doubles_rolled = 0
    
    # Player status methods
    def retire_player(self, bank: 'Bank') -> None:
        self.sub_cash_balance(self.get_cash_balance())
        bank.add_cash_balance(self.get_cash_balance())
        for property_group in self.owned_properties:
            for property in property_group:
                property.set_owner(bank)

    def get_player_net_worth(self) -> int:
        net_worth = self.cash_balance
        for property_group in self.owned_properties.values():
            for property in property_group:
                if property.is_mortgaged:
                    net_worth += property.value / 2
                else:
                    net_worth += property.value
        return net_worth
    
        
    # Bankruptcy methods
    def get_is_bankrupt(self) -> bool:
        return self.is_bankrupt
    
    def set_is_bankrupt(self) -> None:
        self.is_bankrupt = True
    