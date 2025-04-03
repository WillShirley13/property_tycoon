from typing import TYPE_CHECKING, List, Tuple

from backend.non_ownables.go import Go
from backend.property_owners.bank import Bank

from .. import errors

if TYPE_CHECKING:
    from ..non_ownables.free_parking import FreeParking
    from ..property_owners.player import Player


class Jail:
    def __init__(self):
        self.currently_in_jail: List[Tuple["Player", int]] = []
        self.release_cost: int = 50

    def release_from_jail(self, player: "Player", go: Go, bank: Bank) -> None:
        for i, (p, _) in enumerate(self.currently_in_jail):
            if p == player:
                self.currently_in_jail.pop(i)
                player.set_is_in_jail(False)
                player.set_rounds_in_jail(0)
                player.move_player_to_position(10, go, bank)
                break

    def put_in_jail(self, player: "Player") -> None:
        self.currently_in_jail.append((player, 0))
        player.set_is_in_jail(True)

    def get_release_cost(self) -> int:
        return self.release_cost

    def get_currently_in_jail(self) -> List[Tuple["Player", int]]:
        return self.currently_in_jail

    def pay_fine_for_release(
            self, player: "Player", free_parking: "FreeParking", go: Go, bank: Bank) -> None:
        try:
            free_parking.add_fine(self.release_cost, player)
            self.release_from_jail(player, go, bank)
        except BaseException:
            raise errors.InsufficientFundsError

    def player_used_get_out_of_jail_card(self, player: "Player") -> None:
        self.release_from_jail(player)
        player.set_get_out_of_jail_card(player.get_get_out_of_jail_cards() - 1)
