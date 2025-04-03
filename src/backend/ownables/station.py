from typing import TYPE_CHECKING, List

from ..constants import *
from ..enums.property_group import PropertyGroup
from .ownable import Ownable

if TYPE_CHECKING:
    from ..property_owners.bank import Bank
    from ..property_owners.player import Player


class Station(Ownable):
    def __init__(self, cost: int, property_group: PropertyGroup,
                 name: str, owner: "Bank" = None):
        super().__init__(cost=cost, property_group=property_group, name=name, owner=owner)
        self.owner_owns_all_stations: bool = False
        self.num_of_stations_owned_by_owner: int = 0
        self.rent_values: List[int] = STATION_RENT_VALUES
        # No additional attributes or methods beyond Ownable

    def set_rent_cost(self) -> None:
        if self.num_of_stations_owned_by_owner == 1:
            self.rent_cost = ONE_STATION_RENT
        elif self.num_of_stations_owned_by_owner == 2:
            self.rent_cost = TWO_STATION_RENT
        elif self.num_of_stations_owned_by_owner == 3:
            self.rent_cost = THREE_STATION_RENT
        elif self.num_of_stations_owned_by_owner == 4:
            self.rent_cost = FOUR_STATION_RENT

    def get_rent_due_from_player(self, player: "Player") -> int:
        # Get the rent due from a player based on the number of stations owned
        # ... implementation details ...
        return self.rent_cost

    def get_owner_owns_all_stations(self) -> bool:
        return self.owner_owns_all_stations

    def set_owner_owns_all_stations(
            self, owner_owns_all_stations: bool) -> None:
        self.owner_owns_all_stations = owner_owns_all_stations

    def get_num_of_stations_owned_by_owner(self) -> int:
        return self.num_of_stations_owned_by_owner

    def set_num_of_stations_owned_by_owner(
            self, num_of_stations_owned_by_owner: int) -> None:
        self.num_of_stations_owned_by_owner = num_of_stations_owned_by_owner

    def get_rent_values(self) -> List[int]:
        return self.rent_values
