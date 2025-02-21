from backend.property_owners.player import Player
from backend.property_owners.bank import Bank

class Go:
    def __init__(self):
        self.pass_go_payout: int = 200

    def pay_player(self, player: Player, bank: Bank) -> None:
        player.add_cash_balance(self.pass_go_payout)
        bank.sub_cash_balance(self.pass_go_payout)

    def get_pass_go_payout(self) -> int:
        return self.pass_go_payout
