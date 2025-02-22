from backend.constants import OPPORTUNITY_KNOCKS_CARDS, POT_LUCK_CARDS
from backend.enums.game_token import GameToken
from backend.enums.property_group import PropertyGroup
from backend.ownables.ownable import Ownable
from backend.non_ownables.free_parking import FreeParking
from backend.non_ownables.jail import Jail
from backend.non_ownables.go import Go
from backend.non_ownables.game_card import GameCard
from backend.ownables.property import Property
from backend.ownables.station import Station
from backend.ownables.utility import Utility
from backend.property_owners.player import Player
from backend.property_owners.bank import Bank

class Admin:
    def __init__(self, player_names: list[(str, GameToken)]):
        # game board - each index corresponds to a space on the board (in order provided in docs from company)
        self.game_board: list[Ownable | FreeParking | Jail | Go | GameCard] = []
        # helper dictionary to quickly look up the index of a space on the board
        self.game_space_helper: dict[Ownable | FreeParking | Jail | Go | GameCard, int] = {}
        self.players: list[Player] = []
        self.bank: Bank = Bank()
        
        # Initialize players
        self.create_players()
        
        # Initialize game board
        self.create_game_board()

    def create_game_board(self):
        # Initialize game board list
        self.game_board = []
        
        # Create Pot Luck and Opportunity Knocks card packs
        pot_luck_cards = GameCard(POT_LUCK_CARDS, list(POT_LUCK_CARDS.keys()))
        opportunity_knocks = GameCard(OPPORTUNITY_KNOCKS_CARDS, list(OPPORTUNITY_KNOCKS_CARDS.keys()))
        
        # Create board spaces in sequential order
        self.game_board = [
            Go(),  # Position 1
            Property(60, PropertyGroup.BROWN, "The Old Creek", 50, 50, 2),  # Position 2
            pot_luck_cards,  # Position 3
            Property(60, PropertyGroup.BROWN, "Gangsters Paradise", 50, 50, 4),  # Position 4
            FreeParking(),  # Position 5 (Income Tax - using FreeParking to collect £200)
            Station(200, PropertyGroup.STATION, "Brighton Station"),  # Position 6
            Property(100, PropertyGroup.BLUE, "The Angels Delight", 50, 50, 6),  # Position 7
            opportunity_knocks,  # Position 8
            Property(100, PropertyGroup.BLUE, "Potter Avenue", 50, 50, 6),  # Position 9
            Property(120, PropertyGroup.BLUE, "Granger Drive", 50, 50, 8),  # Position 10
            Jail(),  # Position 11
            Property(140, PropertyGroup.PURPLE, "Skywalker Drive", 100, 100, 10),  # Position 12
            Utility(150, PropertyGroup.UTILITIES, "Tesla Power Co"),  # Position 13
            Property(140, PropertyGroup.PURPLE, "Wookie Hole", 100, 100, 10),  # Position 14
            Property(160, PropertyGroup.PURPLE, "Rey Lane", 100, 100, 12),  # Position 15
            Station(200, PropertyGroup.STATION, "Hove Station"),  # Position 16
            Property(180, PropertyGroup.ORANGE, "Bishop Drive", 100, 100, 14),  # Position 17
            pot_luck_cards,  # Position 18
            Property(180, PropertyGroup.ORANGE, "Dunham Street", 100, 100, 14),  # Position 19
            Property(200, PropertyGroup.ORANGE, "Broyles Lane", 100, 100, 16),  # Position 20
            FreeParking(),  # Position 21
            Property(220, PropertyGroup.RED, "Yue Fei Square", 150, 150, 18),  # Position 22
            opportunity_knocks,  # Position 23
            Property(220, PropertyGroup.RED, "Mulan Rouge", 150, 150, 18),  # Position 24
            Property(240, PropertyGroup.RED, "Han Xin Gardens", 150, 150, 20),  # Position 25
            Station(200, PropertyGroup.STATION, "Falmer Station"),  # Position 26
            Property(260, PropertyGroup.YELLOW, "Shatner Close", 150, 150, 22),  # Position 27
            Property(260, PropertyGroup.YELLOW, "Picard Avenue", 150, 150, 22),  # Position 28
            Utility(150, PropertyGroup.UTILITIES, "Edison Water"),  # Position 29
            Property(280, PropertyGroup.YELLOW, "Crusher Creek", 150, 150, 22),  # Position 30
            Jail(),  # Position 31 (Go to Jail)
            Property(300, PropertyGroup.GREEN, "Sirat Mews", 200, 200, 26),  # Position 32
            Property(300, PropertyGroup.GREEN, "Ghengis Crescent", 200, 200, 26),  # Position 33
            pot_luck_cards,  # Position 34
            Property(320, PropertyGroup.GREEN, "Ibis Close", 200, 200, 28),  # Position 35
            Station(200, PropertyGroup.STATION, "Portslade Station"),  # Position 36
            opportunity_knocks,  # Position 37
            Property(350, PropertyGroup.DEEP_BLUE, "James Webb Way", 200, 200, 35),  # Position 38
            FreeParking(),  # Position 39 (Super Tax - using FreeParking to collect £100)
            Property(400, PropertyGroup.DEEP_BLUE, "Turing Heights", 200, 200, 50)  # Position 40
        ]
        
        # Create helper dictionary for quick position lookup
        for i, space in enumerate(self.game_board):
            self.game_space_helper[space] = i

    def create_players(self):
        for name, token in self.player_names:
            self.players.append(Player(token, name))

