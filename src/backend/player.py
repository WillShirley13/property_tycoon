from backend.bank import Bank
import errors
from backend.enums.game_token import GameToken
from backend.property_holder import PropertyHolder
from backend.enums.property_group import PropertyGroup
from backend.ownables.ownable import Ownable
from backend.non_ownables.jail import Jail
from backend.constants import *
from typing import override

class Player(PropertyHolder):
    def __init__(self, game_token: GameToken, name: str):
        super().__init__(initial_cash=1_500)
        self.name: str = name
        self.game_token: GameToken = game_token
        self.get_out_of_jail_cards: int = 0
        self.is_in_jail: bool = False
        self.is_first_circuit_complete: bool = False
        self.current_position: int = 0
        self.num_of_stations_owned: int = 0
        self.num_of_utilities_owned: int = 0
        self.owns_all_utilities: bool = False
        self.owns_all_stations: bool = False
        # Flags for ownership of all properties in each group
        # self.owns_all_brown: bool = False
        # self.owns_all_blue: bool = False
        # self.owns_all_purple: bool = False
        # self.owns_all_orange: bool = False
        # self.owns_all_red: bool = False
        # self.owns_all_yellow: bool = False
        # self.owns_all_green: bool = False
        # self.owns_all_deep_blue: bool = False
        
        self.is_bankrupt: bool = False

    def use_get_out_of_jail(self, jail: Jail) -> None:
        if self.get_out_of_jail_cards > 0:
            jail.remove_player(self)
            self.get_out_of_jail_cards -= 1
        else:
            raise errors.NoGetOutOfJailCardsError

    def go_to_jail(self, jail: Jail) -> None:
        if self.is_in_jail:
            raise errors.PlayerAlreadyInJailError
        self.is_in_jail = True
        jail.put_in_jail(self)

    def purchase_property(self, property: Ownable, bank: Bank) -> None:
        if property.owned_by != bank:
            raise errors.PropertyNotOwnedByBankError
        
        property_cost = property.get_cost()
        if self.cash_balance < property_cost:
            raise errors.InsufficientFundsError
        
        # Pay for property
        self.sub_cash_balance(property_cost)
        bank.add_cash_balance(property_cost)
        
        # update property portfolios
        self.add_property_to_portfolio(property)
        bank.remove_property_from_portfolio(property)
        
        # update ownership
        property.set_owner(self)
        
    def sell_property(self, property: Ownable, bank: Bank) -> None:
        if property.owned_by != self:
            raise errors.PropertyNotOwnedByPlayerError
        
        if property.is_mortgaged:
            
        
        property_cost = property.get_cost()
        self.add_cash_balance(property_cost)
        bank.sub_cash_balance(property_cost)
        
    def move_player(self, steps: int) -> int:
        # Faciliate circular board
        if self.current_position + steps > 40:
            self.is_first_circuit_complete = True
            self.current_position = (self.current_position + steps) % 40
        else:
            self.current_position += steps
        return self.current_position

    def get_current_position(self) -> int:
        return self.current_position

    def get_num_of_stations_owned(self) -> int:
        return self.num_of_stations_owned

    def get_num_of_utilities_owned(self) -> int:
        return self.num_of_utilities_owned

    def retire_player(self, bank) -> None:
        pass

    def get_player_net_worth(self) -> int:
        pass 
    
    @override
    def add_property_to_portfolio(self, property: Ownable) -> None:
        if property in self.owned_properties[property.property_group]:
            raise errors.PropertyAlreadyInPortfolioError
        
        self.owned_properties[property.property_group].append(property)
        
        if property.property_group == PropertyGroup.BROWN:
            if len(self.owned_properties[property.property_group]) == TOTAL_BROWN_PROPERTIES:
                for property in self.owned_properties[property.property_group]:
                    property.owner_owns_all_properties = True
                # self.owns_all_brown = True
        elif property.property_group == PropertyGroup.BLUE:
            if len(self.owned_properties[property.property_group]) == TOTAL_BLUE_PROPERTIES:
                for property in self.owned_properties[property.property_group]:
                    property.owner_owns_all_properties = True
                # self.owns_all_blue = True
        elif property.property_group == PropertyGroup.PURPLE:
            if len(self.owned_properties[property.property_group]) == TOTAL_PURPLE_PROPERTIES:
                for property in self.owned_properties[property.property_group]:
                    property.owner_owns_all_properties = True
                # self.owns_all_purple = True
        elif property.property_group == PropertyGroup.ORANGE:
            if len(self.owned_properties[property.property_group]) == TOTAL_ORANGE_PROPERTIES:
                for property in self.owned_properties[property.property_group]:
                    property.owner_owns_all_properties = True
                # self.owns_all_orange = True
        elif property.property_group == PropertyGroup.RED:
            if len(self.owned_properties[property.property_group]) == TOTAL_RED_PROPERTIES:
                for property in self.owned_properties[property.property_group]:
                    property.owner_owns_all_properties = True
                # self.owns_all_red = True
        elif property.property_group == PropertyGroup.YELLOW:
            if len(self.owned_properties[property.property_group]) == TOTAL_YELLOW_PROPERTIES:
                for property in self.owned_properties[property.property_group]:
                    property.owner_owns_all_properties = True
                # self.owns_all_yellow = True
        elif property.property_group == PropertyGroup.GREEN:
            if len(self.owned_properties[property.property_group]) == TOTAL_GREEN_PROPERTIES:
                for property in self.owned_properties[property.property_group]:
                    property.owner_owns_all_properties = True
                # self.owns_all_green = True
        elif property.property_group == PropertyGroup.DEEP_BLUE:
            if len(self.owned_properties[property.property_group]) == TOTAL_DEEP_BLUE_PROPERTIES:
                for property in self.owned_properties[property.property_group]:
                    property.owner_owns_all_properties = True
                # self.owns_all_deep_blue = True
        elif property.property_group == PropertyGroup.STATION:
            property.num_of_stations_owned_by_owner += 1
            if self.num_of_stations_owned == TOTAL_STATIONS:
                for property in self.owned_properties[property.property_group]:
                    property.owner_owns_all_stations = True
                # self.owns_all_stations = True
        elif property.property_group == PropertyGroup.UTILITY:
            property.num_of_utilities_owned_by_owner += 1
            if self.num_of_utilities_owned == TOTAL_UTILITIES:
                for property in self.owned_properties[property.property_group]:
                    property.owner_owns_all_utilities = True
                # self.owns_all_utilities = True
        
        
    @override
    def remove_property_from_portfolio(self, property: Ownable) -> None:
        if property not in self.owned_properties[property.property_group]:
            raise errors.PropertyNotInPortfolioError
        
        self.owned_properties[property.property_group].remove(property)
        
        if property.property_group == PropertyGroup.BROWN:
            if len(self.owned_properties[property.property_group]) != TOTAL_BROWN_PROPERTIES:
                for property in self.owned_properties[property.property_group]:
                    property.owner_owns_all_properties = False
                # self.owns_all_brown = False
        elif property.property_group == PropertyGroup.BLUE:
            if len(self.owned_properties[property.property_group]) != TOTAL_BLUE_PROPERTIES:
                for property in self.owned_properties[property.property_group]:
                    property.owner_owns_all_properties = False
                # self.owns_all_blue = False
        elif property.property_group == PropertyGroup.PURPLE:
            if len(self.owned_properties[property.property_group]) != TOTAL_PURPLE_PROPERTIES:
                for property in self.owned_properties[property.property_group]:
                    property.owner_owns_all_properties = False
                # self.owns_all_purple = False
        elif property.property_group == PropertyGroup.ORANGE:
            if len(self.owned_properties[property.property_group]) != TOTAL_ORANGE_PROPERTIES:
                for property in self.owned_properties[property.property_group]:
                    property.owner_owns_all_properties = False
                # self.owns_all_orange = True
        elif property.property_group == PropertyGroup.RED:
            if len(self.owned_properties[property.property_group]) != TOTAL_RED_PROPERTIES:
                for property in self.owned_properties[property.property_group]:
                    property.owner_owns_all_properties = False
                # self.owns_all_red = True
        elif property.property_group == PropertyGroup.YELLOW:
            if len(self.owned_properties[property.property_group]) != TOTAL_YELLOW_PROPERTIES:
                for property in self.owned_properties[property.property_group]:
                    property.owner_owns_all_properties = False
                # self.owns_all_yellow = True
        elif property.property_group == PropertyGroup.GREEN:
            if len(self.owned_properties[property.property_group]) != TOTAL_GREEN_PROPERTIES:
                for property in self.owned_properties[property.property_group]:
                    property.owner_owns_all_properties = False
                # self.owns_all_green = True
        elif property.property_group == PropertyGroup.DEEP_BLUE:
            if len(self.owned_properties[property.property_group]) != TOTAL_DEEP_BLUE_PROPERTIES:
                for property in self.owned_properties[property.property_group]:
                    property.owner_owns_all_properties = False
                # self.owns_all_deep_blue = True
        elif property.property_group == PropertyGroup.STATION:
            property.num_of_stations_owned_by_owner -= 1
            if self.num_of_stations_owned != TOTAL_STATIONS:
                for property in self.owned_properties[property.property_group]:
                    property.owner_owns_all_stations = False
                # self.owns_all_stations = True
        elif property.property_group == PropertyGroup.UTILITY:
            property.num_of_utilities_owned_by_owner -= 1
            if self.num_of_utilities_owned != TOTAL_UTILITIES:
                for property in self.owned_properties[property.property_group]:
                    property.owner_owns_all_utilities = False
                # se
