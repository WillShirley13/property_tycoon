from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ..property_owners.bank import Bank
    from ..property_owners.player import Player


class Go:
    def __init__(self):
        self.pass_go_payout: int = 200

    def pay_player(self, player: "Player", bank: "Bank") -> None:
        player.add_cash_balance(self.pass_go_payout)
        bank.sub_cash_balance(self.pass_go_payout)

    def get_pass_go_payout(self) -> int:
        return self.pass_go_payout
