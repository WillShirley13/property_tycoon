# Total number of properties in each group
TOTAL_BROWN_PROPERTIES = 2
TOTAL_BLUE_PROPERTIES = 3
TOTAL_PURPLE_PROPERTIES = 3
TOTAL_ORANGE_PROPERTIES = 3
TOTAL_RED_PROPERTIES = 3
TOTAL_YELLOW_PROPERTIES = 3
TOTAL_GREEN_PROPERTIES = 3
TOTAL_DEEP_BLUE_PROPERTIES = 2
TOTAL_STATIONS = 4
TOTAL_UTILITIES = 2

# Station rents
ONE_STATION_RENT = 25
TWO_STATION_RENT = 50
THREE_STATION_RENT = 100
FOUR_STATION_RENT = 200

# Utility rents
ONE_UTILITY_RENT_DICE_MULTIPLIER = 4
TWO_UTILITY_RENT_DICE_MULTIPLIER = 10

# House and hotel costs by colour group
PROPERTY_BUILD_COSTS = {
    "brown": {"house": 50, "hotel": 50},
    "blue": {"house": 50, "hotel": 50},
    "purple": {"house": 100, "hotel": 100},
    "orange": {"house": 100, "hotel": 100},
    "red": {"house": 150, "hotel": 150},
    "yellow": {"house": 150, "hotel": 150},
    "green": {"house": 200, "hotel": 200},
    "deep_blue": {"house": 200, "hotel": 200},
}

# Property data structure
# Format: {property_name: {"cost": purchase_cost, "rents": [base_rent, 1_house, 2_houses, 3_houses, 4_houses, hotel]}}
PROPERTY_DATA = {
    # Brown Properties
    "The Old Creek": {"cost": 60, "rents": [2, 10, 30, 90, 160, 250]},
    "Gangsters Paradise": {"cost": 60, "rents": [4, 20, 60, 180, 320, 450]},
    
    # Blue Properties
    "The Angels Delight": {"cost": 100, "rents": [6, 30, 90, 270, 400, 550]},
    "Potter Avenue": {"cost": 100, "rents": [6, 30, 90, 270, 400, 550]},
    "Granger Drive": {"cost": 120, "rents": [8, 40, 100, 300, 450, 600]},
    
    # Purple Properties
    "Skywalker Drive": {"cost": 140, "rents": [10, 50, 150, 450, 625, 750]},
    "Wookie Hole": {"cost": 140, "rents": [10, 50, 150, 450, 625, 750]},
    "Rey Lane": {"cost": 160, "rents": [12, 60, 180, 500, 700, 900]},
    
    # Orange Properties
    "Bishop Drive": {"cost": 180, "rents": [14, 70, 200, 550, 750, 950]},
    "Dunham Street": {"cost": 180, "rents": [14, 70, 200, 550, 750, 950]},
    "Broyles Lane": {"cost": 200, "rents": [16, 80, 220, 600, 800, 1000]},
    
    # Red Properties
    "Yue Fei Square": {"cost": 220, "rents": [18, 90, 250, 700, 875, 1050]},
    "Mulan Rouge": {"cost": 220, "rents": [18, 90, 250, 700, 875, 1050]},
    "Han Xin Gardens": {"cost": 240, "rents": [20, 100, 300, 750, 925, 1100]},
    
    # Yellow Properties
    "Shatner Close": {"cost": 260, "rents": [22, 110, 330, 800, 975, 1150]},
    "Picard Avenue": {"cost": 260, "rents": [22, 110, 330, 800, 975, 1150]},
    "Crusher Creek": {"cost": 280, "rents": [22, 120, 360, 850, 1025, 1200]},
    
    # Green Properties
    "Sirat Mews": {"cost": 300, "rents": [26, 130, 390, 900, 1100, 1275]},
    "Ghengis Crescent": {"cost": 300, "rents": [26, 130, 390, 900, 1100, 1275]},
    "Ibis Close": {"cost": 320, "rents": [28, 150, 450, 1000, 1200, 1400]},
    
    # Deep Blue Properties
    "James Webb Way": {"cost": 350, "rents": [35, 175, 500, 1100, 1300, 1500]},
    "Turing Heights": {"cost": 400, "rents": [50, 200, 600, 1400, 1700, 2000]},
    
    # Stations
    "Brighton Station": {"cost": 200, "rents": [25, 50, 100, 200]},  # rents based on number of stations owned
    "Hove Station": {"cost": 200, "rents": [25, 50, 100, 200]},
    "Falmer Station": {"cost": 200, "rents": [25, 50, 100, 200]},
    "Portslade Station": {"cost": 200, "rents": [25, 50, 100, 200]},
    
    # Utilities
    "Tesla Power Co": {"cost": 150, "rents": [4, 10]},  # multipliers for 1 or 2 utilities owned
    "Edison Water": {"cost": 150, "rents": [4, 10]},
}

POT_LUCK_CARDS = {
    "You inherit £200": 1,
    "You have won 2nd prize in a beauty contest, collect £50": 2,
    "You are up the creek with no paddle - go back to the Old Creek": 3,
    "Student loan refund. Collect £20": 4,
    "Bank error in your favour. Collect £200": 5,
    "Pay bill for text books of £100": 6,
    "Mega late night taxi bill pay £50": 7,
    "Advance to go": 8,
    "From sale of Bitcoin you get £50": 9,
    "Bitcoin assets fall - pay off Bitcoin short fall": 10,
    "Pay a £10 fine or take opportunity knocks": 11,
    "Pay insurance fee of £50": 12,
    "Savings bond matures, collect £100": 13,
    "Go to jail. Do not pass GO, do not collect £200": 14,
    "Received interest on shares of £25": 15,
    "It's your birthday. Collect £10 from each player": 16,
    "Get out of jail free": 17
}

OPPORTUNITY_KNOCKS_CARDS = {
    "Bank pays you divided of £50": 18,
    "You have won a lip sync battle. Collect £100": 19,
    "Advance to Turing Heights": 20,
    "Advance to Han Xin Gardens. If you pass GO, collect £200": 21,
    "Fined £15 for speeding": 22,
    "Pay university fees of £150": 23,
    "Take a trip to Hove station. If you pass GO collect £200": 24,
    "Loan matures, collect £150": 25,
    "You are assessed for repairs, £40/house, £115/hotel": 26,
    "Advance to GO": 27,
    "You are assessed for repairs, £25/house, £100/hotel": 28,
    "Go back 3 spaces": 29,
    "Advance to Skywalker Drive. If you pass GO collect £200": 30,
    "Go to jail. Do not pass GO, do not collect £200": 31,
    "Drunk in charge of a hoverboard. Fine £30": 32,
    "Get out of jail free": 33
}

# Bank constants
BANK_STARTING_CASH = 500_000

# Station constants
STATION_RENT_VALUES = [25, 50, 100, 200]  # Rent for 1, 2, 3, 4 stations

# Player constants
PLAYER_STARTING_CASH = 1_500
GO_PAYOUT = 200

# Game board constants
NUM_SPACES = 40


