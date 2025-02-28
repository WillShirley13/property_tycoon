from typing import TYPE_CHECKING, List
from .ownable import Ownable
from ..constants import *

if TYPE_CHECKING:
    from ..property_owners.player import Player

class Station(Ownable):
    def __init__(self, value: int, property_group, name: str):
        super().__init__(value, property_group, name)
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

    def get_rent_due_from_player(self, player: 'Player') -> int:
        # Get the rent due from a player based on the number of stations owned
        # ... implementation details ...
        return self.rent_values[0]  # Placeholder

