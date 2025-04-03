from ast import List
from typing import TYPE_CHECKING, Union

from .. import errors
from ..constants import PROPERTY_DATA
from ..enums.property_group import PropertyGroup

if TYPE_CHECKING:
    from ..property_owners.bank import Bank
    from ..property_owners.player import Player


class Ownable:
    def __init__(self, cost: int, property_group: PropertyGroup,
                 name: str, owner: "Bank" = None):
        self.name: str = name
        self.png_name: str = PROPERTY_DATA[self.name]["png_name"]
        self.owned_by: Player | Bank = owner  # Will be Player or Bank
        self.cost_to_buy: int = cost
        self.total_value: int = cost
        self.rent_cost: int = PROPERTY_DATA[self.name]["rents"][0]
        self.current_sell_value: List[int] = [self.cost_to_buy]
        self.is_mortgaged: bool = False
        self.property_group: PropertyGroup = property_group

    def get_name(self) -> str:
        return self.name

    def get_property_group(self) -> PropertyGroup:
        return self.property_group

    def get_cost(self) -> int:
        return self.cost_to_buy

    def get_total_value(self) -> int:
        return self.total_value

    def set_total_value(self, value_change: int,
                        increase: bool = False) -> None:
        if increase:
            self.total_value += value_change
        else:
            self.total_value -= value_change

    # Note: current_sell_value returns the cash the player would get if they
    # downgraded/sold. It is NOT the total value of the property.
    def get_current_sell_value(self) -> int:
        return self.current_sell_value[-1]

    def get_owner(self) -> Union["Player", "Bank"]:
        return self.owned_by

    def set_owner(self, new_owner: Union["Player", "Bank"]) -> None:
        self.owned_by = new_owner

    def get_rent_due_from_player(self, player: "Player") -> int:
        # If property is mortgaged or owner in jail, no rent is due
        if self.is_mortgaged or self.owned_by.is_in_jail:
            return 0
        try:
            player.sub_cash_balance(self.rent_cost)
            self.owned_by.add_cash_balance(self.rent_cost)
            return self.rent_cost
        except errors.InsufficientFundsError:
            raise errors.InsufficientFundsError

    def get_rent_cost(self) -> int:
        return self.rent_cost

    def get_is_mortgaged(self) -> bool:
        return self.is_mortgaged

    def set_is_mortgaged(self, is_mortgaged: bool) -> None:
        self.is_mortgaged = is_mortgaged
