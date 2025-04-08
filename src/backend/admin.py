import threading
import time

from . import errors
from .constants import OPPORTUNITY_KNOCKS_CARDS, POT_LUCK_CARDS
from .enums.game_token import GameToken
from .enums.property_group import PropertyGroup
from .non_ownables.free_parking import FreeParking
from .non_ownables.game_card import GameCard
from .non_ownables.go import Go
from .non_ownables.jail import Jail
from .ownables.ownable import Ownable
from .ownables.property import Property
from .ownables.station import Station
from .ownables.utility import Utility
from .property_owners.bank import Bank
from .property_owners.player import Player


class Admin:
    def __init__(self, player_names: list[(
            str, GameToken)], time_limit: int = 0):
        # game board - each index corresponds to a space on the board (in order
        # provided in docs from company)
        self.game_board: list[Ownable | FreeParking | Jail | Go | GameCard] = []
        # helper dictionary to quickly look up the index of a space on the
        # board
        self.game_space_helper: dict[Ownable | FreeParking | Jail | Go | GameCard, int] = {}
        self.players: list[Player] = []
        self.player_names: list[(str, GameToken)] = player_names
        self.bank: Bank = Bank()
        self.free_parking: FreeParking = FreeParking()
        self.go: Go = Go()
        self.jail: Jail = Jail()
        self.pot_luck_cards: GameCard = GameCard(
            card_ids=POT_LUCK_CARDS, card_pack=list(
                POT_LUCK_CARDS.keys()))
        self.opportunity_knocks: GameCard = GameCard(
            card_ids=OPPORTUNITY_KNOCKS_CARDS,
            card_pack=list(OPPORTUNITY_KNOCKS_CARDS.keys()),
        )
        self.time_limit: int = time_limit
        self.is_time_limit_reached: bool = False

        # Initialize players
        self.create_players()

        # Initialize game board
        self.create_game_board()

        # Assign all properties to bank
        self.assign_all_properties_to_bank()
        

    def start_timer(self):
        self.timer_thread = threading.Thread(target=self.countdown)
        self.timer_thread.start()

    def countdown(self):
        print(f"Game will end in {self.time_limit} minutes.")
        time.sleep(self.time_limit * 60)
        self.is_time_limit_reached = True

    def get_is_time_limit_reached(self) -> bool:
        return self.is_time_limit_reached

    def get_time_limit(self) -> int:
        return self.time_limit

    def get_players(self) -> list[Player]:
        return self.players

    def get_bank(self) -> Bank:
        return self.bank

    def assign_all_properties_to_bank(self):
        for prop in self.game_board:
            if isinstance(prop, Ownable):
                prop.set_owner(self.bank)
                self.bank.add_property_to_portfolio(prop)

    def get_free_parking(self) -> FreeParking:
        return self.free_parking

    def get_go(self) -> Go:
        return self.go

    def get_jail(self) -> Jail:
        return self.jail

    def get_pot_luck_cards(self) -> GameCard:
        return self.pot_luck_cards

    def get_opportunity_knocks(self) -> GameCard:
        return self.opportunity_knocks

    def get_game_board(self) -> list[Ownable | FreeParking | Jail | Go | GameCard]:
        return self.game_board

    def get_game_space_helper(
        self,
    ) -> dict[Ownable | FreeParking | Jail | Go | GameCard, int]:
        return self.game_space_helper

    def create_game_board(self):
        # Initialize game board list
        self.game_board = []

        # Create Pot Luck and Opportunity Knocks card packs
        pot_luck_cards = GameCard(
            card_ids=POT_LUCK_CARDS, card_pack=list(
                POT_LUCK_CARDS.keys()))
        opportunity_knocks = GameCard(
            card_ids=OPPORTUNITY_KNOCKS_CARDS,
            card_pack=list(OPPORTUNITY_KNOCKS_CARDS.keys()),
        )

        # Create board spaces in sequential order
        self.game_board = [
            Go(),  # Position 1
            Property(
                cost=60,
                property_group=PropertyGroup.BROWN,
                name="The Old Creek"),
            # Position 2
            pot_luck_cards,  # Position 3
            Property(
                cost=60,
                property_group=PropertyGroup.BROWN,
                name="Gangsters Paradise"),
            # Position 4
            FreeParking(),  # Position 5 (Income Tax - using FreeParking to collect £200)
            Station(
                cost=200,
                property_group=PropertyGroup.STATION,
                name="Brighton Station"),
            # Position 6
            Property(
                cost=100,
                property_group=PropertyGroup.BLUE,
                name="The Angels Delight"),
            # Position 7
            opportunity_knocks,  # Position 8
            Property(
                cost=100,
                property_group=PropertyGroup.BLUE,
                name="Potter Avenue"),
            # Position 9
            Property(
                cost=120,
                property_group=PropertyGroup.BLUE,
                name="Granger Drive"),
            # Position 10
            Jail(),  # Position 11
            Property(
                cost=140,
                property_group=PropertyGroup.PURPLE,
                name="Skywalker Drive"),
            # Position 12
            Utility(
                cost=150,
                property_group=PropertyGroup.UTILITY,
                name="Tesla Power Co"),
            # Position 13
            Property(
                cost=140,
                property_group=PropertyGroup.PURPLE,
                name="Wookie Hole"),
            # Position 14
            Property(
                cost=160,
                property_group=PropertyGroup.PURPLE,
                name="Rey Lane"),
            Station(
                cost=200,
                property_group=PropertyGroup.STATION,
                name="Hove Station"),
            # Position 16
            Property(
                cost=180,
                property_group=PropertyGroup.ORANGE,
                name="Bishop Drive"),
            # Position 17
            pot_luck_cards,  # Position 18
            Property(
                cost=180,
                property_group=PropertyGroup.ORANGE,
                name="Dunham Street"),
            # Position 19
            Property(
                cost=200,
                property_group=PropertyGroup.ORANGE,
                name="Broyles Lane"),
            # Position 20
            FreeParking(),  # Position 21
            Property(
                cost=220,
                property_group=PropertyGroup.RED,
                name="Yue Fei Square"),
            # Position 22
            opportunity_knocks,  # Position 23
            Property(
                cost=220,
                property_group=PropertyGroup.RED,
                name="Mulan Rouge"),
            # Position 24
            Property(
                cost=240,
                property_group=PropertyGroup.RED,
                name="Han Xin Gardens"),
            # Position 25
            Station(
                cost=200,
                property_group=PropertyGroup.STATION,
                name="Falmer Station"),
            # Position 26
            Property(
                cost=260,
                property_group=PropertyGroup.YELLOW,
                name="Shatner Close"),
            # Position 27
            Property(
                cost=260,
                property_group=PropertyGroup.YELLOW,
                name="Picard Avenue"),
            # Position 28
            Utility(
                cost=150,
                property_group=PropertyGroup.UTILITY,
                name="Edison Water"),
            # Position 29
            Property(
                cost=280,
                property_group=PropertyGroup.YELLOW,
                name="Crusher Creek"),
            # Position 30
            Jail(),  # Position 31 (Go to Jail)
            Property(
                cost=300,
                property_group=PropertyGroup.GREEN,
                name="Sirat Mews"),
            # Position 32
            Property(
                cost=300,
                property_group=PropertyGroup.GREEN,
                name="Ghengis Crescent"),
            # Position 33
            pot_luck_cards,
            Property(
                cost=320,
                property_group=PropertyGroup.GREEN,
                name="Ibis Close"),
            # Position 35
            Station(
                cost=200,
                property_group=PropertyGroup.STATION,
                name="Portslade Station"),
            # Position 36
            opportunity_knocks,  # Position 37
            Property(
                cost=350,
                property_group=PropertyGroup.DEEP_BLUE,
                name="James Webb Way"),
            # Position 38
            FreeParking(),  # Position 39 (Super Tax - using FreeParking to collect £100)
            Property(
                cost=400,
                property_group=PropertyGroup.DEEP_BLUE,
                name="Turing Heights"),
            # Position 40
        ]

        # Create helper dictionary for quick position lookup
        for i, space in enumerate(self.game_board):
            self.game_space_helper[space] = i

    def create_players(self):
        if len(self.player_names) > 5:
            raise errors.ExceededMaxPlayersError
        for name, token in self.player_names:
            self.players.append(Player(token, name))
