from backend.property_owners.player import Player

class Jail:
    def __init__(self):
        self.currently_in_jail: list[tuple[Player, int]] = []
        self.release_cost: int = 50

    def release_from_jail(self, player) -> None:
        for player in self.currently_in_jail:
            if player[0] == player:
                self.currently_in_jail.remove(player)

    def put_in_jail(self, player) -> None:
        self.currently_in_jail.append((player, 0))
        
    def get_release_cost(self) -> int:
        return self.release_cost

    def get_is_in_jail(self) -> list[tuple[Player, int]]:
        return self.currently_in_jail
    
    def pay_fine_for_release(self, player) -> None:
        try:
            player.sub_cash_balance(self.release_cost)
            self.release_from_jail(player)
        except:
            raise errors.InsufficientFundsError
    
    # NEED TO IMPLEMENT 2 ROUNDS IN JAIL FOR RELEASING PLAYER

