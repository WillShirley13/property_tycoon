from typing import TYPE_CHECKING, List, Tuple
from .. import errors

if TYPE_CHECKING:
    from ..property_owners.player import Player

class Jail:
    def __init__(self):
        self.currently_in_jail: List[Tuple['Player', int]] = []
        self.release_cost: int = 50

    def release_from_jail(self, player: 'Player') -> None:
        for i, (p, _) in enumerate(self.currently_in_jail):
            if p == player:
                self.currently_in_jail.pop(i)
                player.is_in_jail = False
                player.set_rounds_in_jail(0)
                break

    def put_in_jail(self, player: 'Player') -> None:
        self.currently_in_jail.append((player, 0))
        player.is_in_jail = True

    def get_release_cost(self) -> int:
        return self.release_cost

    def get_is_in_jail(self) -> List[Tuple['Player', int]]:
        return self.currently_in_jail
    
    def pay_fine_for_release(self, player) -> None:
        try:
            player.sub_cash_balance(self.release_cost)
            self.release_from_jail(player)
        except:
            raise errors.InsufficientFundsError
    
    # NEED TO IMPLEMENT 2 ROUNDS IN JAIL FOR RELEASING PLAYER

