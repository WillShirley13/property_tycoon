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
    "Tesla Power Co": {"cost": 150, "multipliers": [4, 10]},  # multipliers for 1 or 2 utilities owned
    "Edison Water": {"cost": 150, "multipliers": [4, 10]},
}






