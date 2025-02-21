from backend.property_owners.player import Player
import errors
class FreeParking:
    def __init__(self):
        self.fines_collected: int = 0

    def get_fines_collected(self) -> int:
        return self.fines_collected

    def add_fine(self, amount: int, player: Player) -> None:
        try:
            player.sub_cash_balance(amount)
            self.fines_collected += amount
        except errors.InsufficientFundsError:
            raise errors.InsufficientFundsError


    def payout_fines(self, player: Player) -> None:
        player.add_cash_balance(self.fines_collected)
        self.fines_collected = 0
