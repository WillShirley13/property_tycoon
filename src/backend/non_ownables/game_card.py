import random
from typing import TYPE_CHECKING, Dict, List, Tuple
from ..enums.property_group import PropertyGroup
from ..constants import POT_LUCK_CARDS, OPPORTUNITY_KNOCKS_CARDS
from .. import errors

if TYPE_CHECKING:
    from ..non_ownables.free_parking import FreeParking
    from ..non_ownables.jail import Jail
    from ..ownables.property import Property
    from ..property_owners.player import Player
    from ..property_owners.bank import Bank


class GameCard:
    def __init__(self, card_ids: Dict[str, int], card_pack: List[str]):
        self.card_ids: Dict[str, int] = card_ids
        self.card_pack: List[str] = card_pack
        self.shuffle_pack()

    # Returns a tuple of the card and the card id
    def get_card(self) -> Tuple[str, int]:
        card = self.card_pack[0]
        self.card_pack.append(self.card_pack.pop(0))
        return (card, self.card_ids[card])

    # Facilitates actions of card id passed. Function may raise errror if player does not have enough funds
    def process_card(
        self,
        player: "Player",
        bank: "Bank",
        card_id: int,
        free_parking: "FreeParking",
        jail: "Jail",
        other_players: List["Player"],
    ) -> None:
        match card_id:
            # Pot Luck Cards (1-17)
            case 1:  # "You inherit £200"
                player.add_cash_balance(200)
                bank.sub_cash_balance(200)

            case 2:  # "You have won 2nd prize in a beauty contest"
                player.add_cash_balance(50)
                bank.sub_cash_balance(50)

            case 3:  # "Go back to the Old Creek"
                player.move_player_to_position(2)

            case 4:  # "Student loan refund"
                player.add_cash_balance(20)
                bank.sub_cash_balance(20)

            case 5:  # "Bank error in your favour"
                player.add_cash_balance(200)
                bank.sub_cash_balance(200)

            case 6:  # "Pay bill for text books"
                try:
                    player.sub_cash_balance(100)
                    bank.add_cash_balance(100)
                except errors.InsufficientFundsError:
                    raise errors.InsufficientFundsError

            case 7:  # "Mega late night taxi bill"
                try:
                    player.sub_cash_balance(50)
                    bank.add_cash_balance(50)
                except errors.InsufficientFundsError:
                    raise errors.InsufficientFundsError

            case 8:  # "Advance to go"
                player.move_player_to_position(0)

            case 9:  # "From sale of Bitcoin"
                player.add_cash_balance(50)
                bank.sub_cash_balance(50)

            case 10:  # "Bitcoin assets fall"
                try:
                    player.sub_cash_balance(50)
                    bank.add_cash_balance(50)
                except errors.InsufficientFundsError:
                    raise errors.InsufficientFundsError

            case 11:  # "Pay £10 fine or take opportunity knocks"
                # This will need player choice implementation
                pass

            case 12:  # "Pay insurance fee"
                try:
                    free_parking.add_fine(50, player)
                except errors.InsufficientFundsError:
                    raise errors.InsufficientFundsError

            case 13:  # "Savings bond matures"
                player.add_cash_balance(100)
                bank.sub_cash_balance(100)

            case 14:  # "Go to jail"
                jail.put_in_jail(player)

            case 15:  # "Received interest on shares"
                player.add_cash_balance(25)
                bank.sub_cash_balance(25)
            case 16:  # "It's your birthday"
                for other_player in other_players:
                    try:
                        other_player.sub_cash_balance(10)
                        player.add_cash_balance(10)
                    except errors.InsufficientFundsError:
                        # HOW TO RETURN PLAYER WHO DOES NOT HAVE ENOUGH FUNDS?
                        raise errors.InsufficientFundsError

            case 17:  # "Get out of jail free"
                player.add_get_out_of_jail_card()

            # Opportunity Knocks Cards (18-33)
            case 18:  # "Bank pays you dividend"
                player.add_cash_balance(50)
                bank.sub_cash_balance(50)

            case 19:  # "Won lip sync battle"
                player.add_cash_balance(100)
                bank.sub_cash_balance(100)

            case 20:  # "Advance to Turing Heights"
                player.move_player_to_position(40)

            case 21:  # "Advance to Han Xin Gardens"
                player.move_player_to_position(25)

            case 22:  # "Fined for speeding"
                try:
                    free_parking.add_fine(15, player)
                except errors.InsufficientFundsError:
                    raise errors.InsufficientFundsError

            case 23:  # "Pay university fees"
                try:
                    player.sub_cash_balance(150)
                    bank.add_cash_balance(150)
                except errors.InsufficientFundsError:
                    raise errors.InsufficientFundsError

            case 24:  # "Take a trip to Hove station"
                player.move_player_to_position(16)

            case 25:  # "Loan matures"
                player.add_cash_balance(150)
                bank.sub_cash_balance(150)

            case 26:  # "Repairs £40/house, £115/hotel"
                total = 0
                for property_group in player.get_owned_properties().values():
                    for property in property_group:
                        if isinstance(property, Property):
                            total += (property.houses * 40) + (property.hotels * 115)
                player.sub_cash_balance(total)
                bank.add_cash_balance(total)

            case 27:  # "Advance to GO"
                player.move_player_to_position(0)

            case 28:  # "Repairs £25/house, £100/hotel"
                total = 0
                for property_group in player.get_owned_properties().values():
                    for property in property_group:
                        if isinstance(property, Property):
                            total += (property.houses * 25) + (property.hotels * 100)
                player.sub_cash_balance(total)
                bank.add_cash_balance(total)

            case 29:  # "Go back 3 spaces"
                player.move_player_to_position(player.current_position - 3)

            case 30:  # "Advance to Skywalker Drive"
                player.move_player_to_position(12)

            case 31:  # "Go to jail"
                jail.put_in_jail(player)

            case 32:  # "Drunk in charge of hoverboard"
                free_parking.add_fine(30, player)

            case 33:  # "Get out of jail free"
                player.add_get_out_of_jail_card()

    def shuffle_pack(self) -> None:
        random.shuffle(self.card_pack)
