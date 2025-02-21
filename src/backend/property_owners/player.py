from backend.non_ownables.go import Go
from backend.property_owners import bank
from backend.property_owners.bank import Bank
import errors
from backend.enums.game_token import GameToken
from backend.property_owners.property_holder import PropertyHolder
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
    
    def add_get_out_of_jail(self) -> None:
        self.get_out_of_jail_cards += 1

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
            self.add_cash_balance(property.get_cost() / 2)
            bank.sub_cash_balance(property.get_cost() / 2)
            property.is_mortgaged = False
        else:
            self.add_cash_balance(property.get_cost())
            bank.sub_cash_balance(property.get_cost())
        
    @override
    def add_property_to_portfolio(self, property: Ownable) -> None:
        if property in self.owned_properties[property.property_group]:
            raise errors.PropertyAlreadyInPortfolioError
        
        self.owned_properties[property.property_group].append(property)

        match property.property_group:
            case PropertyGroup.BROWN:
                if len(self.owned_properties[PropertyGroup.BROWN]) == TOTAL_BROWN_PROPERTIES:
                    for prop in self.owned_properties[PropertyGroup.BROWN]:
                        prop.owner_owns_all_properties = True
            case PropertyGroup.BLUE:
                if len(self.owned_properties[PropertyGroup.BLUE]) == TOTAL_BLUE_PROPERTIES:
                    for prop in self.owned_properties[PropertyGroup.BLUE]:
                        prop.owner_owns_all_properties = True
            case PropertyGroup.PURPLE:
                if len(self.owned_properties[PropertyGroup.PURPLE]) == TOTAL_PURPLE_PROPERTIES:
                    for prop in self.owned_properties[PropertyGroup.PURPLE]:
                        prop.owner_owns_all_properties = True
            case PropertyGroup.ORANGE:
                if len(self.owned_properties[PropertyGroup.ORANGE]) == TOTAL_ORANGE_PROPERTIES:
                    for prop in self.owned_properties[PropertyGroup.ORANGE]:
                        prop.owner_owns_all_properties = True
            case PropertyGroup.RED:
                if len(self.owned_properties[PropertyGroup.RED]) == TOTAL_RED_PROPERTIES:
                    for prop in self.owned_properties[PropertyGroup.RED]:
                        prop.owner_owns_all_properties = True
            case PropertyGroup.YELLOW:
                if len(self.owned_properties[PropertyGroup.YELLOW]) == TOTAL_YELLOW_PROPERTIES:
                    for prop in self.owned_properties[PropertyGroup.YELLOW]:
                        prop.owner_owns_all_properties = True
            case PropertyGroup.GREEN:
                if len(self.owned_properties[PropertyGroup.GREEN]) == TOTAL_GREEN_PROPERTIES:
                    for prop in self.owned_properties[PropertyGroup.GREEN]:
                        prop.owner_owns_all_properties = True
            case PropertyGroup.DEEP_BLUE:
                if len(self.owned_properties[PropertyGroup.DEEP_BLUE]) == TOTAL_DEEP_BLUE_PROPERTIES:
                    for prop in self.owned_properties[PropertyGroup.DEEP_BLUE]:
                        prop.owner_owns_all_properties = True
            case PropertyGroup.STATION:
                property.num_of_stations_owned_by_owner += 1
                if self.num_of_stations_owned == TOTAL_STATIONS:
                    for prop in self.owned_properties[PropertyGroup.STATION]:
                        prop.owner_owns_all_stations = True
            case PropertyGroup.UTILITY:
                property.num_of_utilities_owned_by_owner += 1
                if self.num_of_utilities_owned == TOTAL_UTILITIES:
                    for prop in self.owned_properties[PropertyGroup.UTILITY]:
                        prop.owner_owns_all_utilities = True
            case _:
                pass

    @override
    def remove_property_from_portfolio(self, property: Ownable) -> None:
        if property not in self.owned_properties[property.property_group]:
            raise errors.PropertyNotInPortfolioError
        
        self.owned_properties[property.property_group].remove(property)

        match property.property_group:
            case PropertyGroup.BROWN:
                if len(self.owned_properties[PropertyGroup.BROWN]) != TOTAL_BROWN_PROPERTIES:
                    for prop in self.owned_properties[PropertyGroup.BROWN]:
                        prop.owner_owns_all_properties = False
            case PropertyGroup.BLUE:
                if len(self.owned_properties[PropertyGroup.BLUE]) != TOTAL_BLUE_PROPERTIES:
                    for prop in self.owned_properties[PropertyGroup.BLUE]:
                        prop.owner_owns_all_properties = False
            case PropertyGroup.PURPLE:
                if len(self.owned_properties[PropertyGroup.PURPLE]) != TOTAL_PURPLE_PROPERTIES:
                    for prop in self.owned_properties[PropertyGroup.PURPLE]:
                        prop.owner_owns_all_properties = False
            case PropertyGroup.ORANGE:
                if len(self.owned_properties[PropertyGroup.ORANGE]) != TOTAL_ORANGE_PROPERTIES:
                    for prop in self.owned_properties[PropertyGroup.ORANGE]:
                        prop.owner_owns_all_properties = False
            case PropertyGroup.RED:
                if len(self.owned_properties[PropertyGroup.RED]) != TOTAL_RED_PROPERTIES:
                    for prop in self.owned_properties[PropertyGroup.RED]:
                        prop.owner_owns_all_properties = False
            case PropertyGroup.YELLOW:
                if len(self.owned_properties[PropertyGroup.YELLOW]) != TOTAL_YELLOW_PROPERTIES:
                    for prop in self.owned_properties[PropertyGroup.YELLOW]:
                        prop.owner_owns_all_properties = False
            case PropertyGroup.GREEN:
                if len(self.owned_properties[PropertyGroup.GREEN]) != TOTAL_GREEN_PROPERTIES:
                    for prop in self.owned_properties[PropertyGroup.GREEN]:
                        prop.owner_owns_all_properties = False
            case PropertyGroup.DEEP_BLUE:
                if len(self.owned_properties[PropertyGroup.DEEP_BLUE]) != TOTAL_DEEP_BLUE_PROPERTIES:
                    for prop in self.owned_properties[PropertyGroup.DEEP_BLUE]:
                        prop.owner_owns_all_properties = False
            case PropertyGroup.STATION:
                property.num_of_stations_owned_by_owner -= 1
                if self.num_of_stations_owned != TOTAL_STATIONS:
                    for prop in self.owned_properties[PropertyGroup.STATION]:
                        prop.owner_owns_all_stations = False
            case PropertyGroup.UTILITY:
                property.num_of_utilities_owned_by_owner -= 1
                if self.num_of_utilities_owned != TOTAL_UTILITIES:
                    for prop in self.owned_properties[PropertyGroup.UTILITY]:
                        prop.owner_owns_all_utilities = False
            case _:
                pass

    def mortgage_property(self, property: Ownable, bank: Bank) -> None:
        if property.owned_by != self:
            raise errors.PropertyNotOwnedByPlayerError
        
        if property.is_mortgaged:
            raise errors.PropertyAlreadyMortgagedError
        
        property.is_mortgaged = True
        property.owned_by = bank
        self.add_cash_balance(property.value / 2)
        bank.sub_cash_balance(property.value / 2)

### CURRENTLY MOVING PLAYER METHODS DO NOT PAY PLAYER FOR PASSING GO ###
    # Updates current_position and is_first_circuit_complete and returns new position
    def move_player(self, steps: int) -> int:
        # Faciliate circular board
        if self.current_position + steps > 40:
            if not self.is_first_circuit_complete:
                self.is_first_circuit_complete = True
            self.current_position = (self.current_position + steps) % 40    
        else:
            self.current_position += steps
        return self.current_position

    # Updates current_position to a specified position
    def move_player_to_position(self, position: int) -> None:
        self.current_position = position
        
    def retire_player(self, bank) -> None:
        self.sub_cash_balance(self.get_cash_balance())
        bank.add_cash_balance(self.get_cash_balance())
        for property_group in self.owned_properties:
            for property in property_group:
                property.set_owner(bank)

    def get_player_net_worth(self) -> int:
        net_worth = self.cash_balance
        for property_group in self.owned_properties:
            for property in property_group:
                if property.is_mortgaged:
                    net_worth += property.value / 2
                else:
                    net_worth += property.value
        return net_worth
    