from backend.ownables.ownable import Ownable
from constants import *

class Station(Ownable):
    def __init__(self, value: int, property_group, name: str):
        super().__init__(value, property_group, name)
        self.owner_owns_all_stations: bool = False
        self.num_of_stations_owned_by_owner: int = 0
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

