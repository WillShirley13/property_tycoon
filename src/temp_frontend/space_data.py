# Space names for the Monopoly board
SPACE_NAMES = [
    "GO",                      # 0
    "The Old Creek",           # 1
    "Pot Luck",                # 2
    "Gangsters Paradise",      # 3
    "Free Parking",            # 4
    "Brighton Station",        # 5
    "The Angels Delight",      # 6
    "Opportunity Knocks",      # 7
    "Potter Avenue",           # 8
    "Granger Drive",           # 9
    "JAIL",                    # 10
    "Skywalker Drive",         # 11
    "Tesla Power Co",          # 12
    "Wookie Hole",             # 13
    "Rey Lane",                # 14
    "Hove Station",            # 15
    "Bishop Drive",            # 16
    "Pot Luck",                # 17
    "Dunham Street",           # 18
    "Broyles Lane",            # 19
    "FREE PARKING",            # 20
    "Yue Fei Square",          # 21
    "Opportunity Knocks",      # 22
    "Mulan Rouge",             # 23
    "Han Xin Gardens",         # 24
    "Falmer Station",          # 25
    "Shatner Close",           # 26
    "Picard Avenue",           # 27
    "Edison Water",            # 28
    "Crusher Creek",           # 29
    "GO TO JAIL",              # 30
    "Sirat Mews",              # 31
    "Ghengis Crescent",        # 32
    "Pot Luck",                # 33
    "Ibis Close",              # 34
    "Portslade Station",       # 35
    "Opportunity Knocks",      # 36
    "James Webb Way",          # 37
    "Free Parking",            # 38
    "Turing Heights"           # 39
]

# Property group colors
PROPERTY_COLORS = {
    "BROWN": (150, 75, 0),        # Brown
    "BLUE": (135, 206, 235),      # Light Blue
    "PURPLE": (221, 160, 221),    # Purple
    "ORANGE": (255, 165, 0),      # Orange
    "RED": (255, 0, 0),           # Red
    "YELLOW": (255, 255, 0),      # Yellow
    "GREEN": (0, 128, 0),         # Green
    "DEEP_BLUE": (0, 0, 139),     # Dark Blue
    "STATION": (120, 120, 120),   # Gray for stations
    "UTILITY": (200, 200, 255),   # Light blue-gray for utilities
    "SPECIAL": (240, 240, 240)    # Light gray for special spaces (GO, JAIL, etc.)
}

# Space property groups
SPACE_PROPERTY_GROUPS = [
    "SPECIAL",      # 0 - GO
    "BROWN",        # 1 - The Old Creek
    "SPECIAL",      # 2 - Pot Luck
    "BROWN",        # 3 - Gangsters Paradise
    "SPECIAL",      # 4 - Free Parking (Income Tax)
    "STATION",      # 5 - Brighton Station
    "BLUE",         # 6 - The Angels Delight
    "SPECIAL",      # 7 - Opportunity Knocks
    "BLUE",         # 8 - Potter Avenue
    "BLUE",         # 9 - Granger Drive
    "SPECIAL",      # 10 - JAIL
    "PURPLE",       # 11 - Skywalker Drive
    "UTILITY",      # 12 - Tesla Power Co
    "PURPLE",       # 13 - Wookie Hole
    "PURPLE",       # 14 - Rey Lane
    "STATION",      # 15 - Hove Station
    "ORANGE",       # 16 - Bishop Drive
    "SPECIAL",      # 17 - Pot Luck
    "ORANGE",       # 18 - Dunham Street
    "ORANGE",       # 19 - Broyles Lane
    "SPECIAL",      # 20 - FREE PARKING
    "RED",          # 21 - Yue Fei Square
    "SPECIAL",      # 22 - Opportunity Knocks
    "RED",          # 23 - Mulan Rouge
    "RED",          # 24 - Han Xin Gardens
    "STATION",      # 25 - Falmer Station
    "YELLOW",       # 26 - Shatner Close
    "YELLOW",       # 27 - Picard Avenue
    "UTILITY",      # 28 - Edison Water
    "YELLOW",       # 29 - Crusher Creek
    "SPECIAL",      # 30 - GO TO JAIL
    "GREEN",        # 31 - Sirat Mews
    "GREEN",        # 32 - Ghengis Crescent
    "SPECIAL",      # 33 - Pot Luck
    "GREEN",        # 34 - Ibis Close
    "STATION",      # 35 - Portslade Station
    "SPECIAL",      # 36 - Opportunity Knocks
    "DEEP_BLUE",    # 37 - James Webb Way
    "SPECIAL",      # 38 - Free Parking (Super Tax)
    "DEEP_BLUE"     # 39 - Turing Heights
]

# Space colors for different board elements
SPACE_COLORS = {
    "default": [(200, 200, 200), (180, 180, 180)],  # Alternating light gray colors
    "corner": (220, 220, 220),                      # Slightly lighter gray for corners
    "board_bg": (240, 240, 240),                    # Background color for the center of the board
    "screen_bg": (255, 255, 255),                   # Background color for the screen
    "border": (0, 0, 0)                             # Border color
}

# Board configuration constants
BOARD_CONFIG = {
    "screen_size_percentage": 0.9,     # Percentage of screen size to use for the window
    "board_width_percentage": 0.75,    # Percentage of window width to use for the board
    "max_height_percentage": 0.95,     # Maximum percentage of window height for the board
    "corner_size_divisor": 6,          # Divisor to determine corner size from board width
    "spaces_per_side": 9,              # Number of non-corner spaces per side
    "regular_font_size": 20,           # Font size for regular spaces (increased from 16)
    "corner_font_size": 28,            # Font size for corner spaces (increased from 22)
    "color_strip_height": 0.25         # Height of the color strip as a percentage of space height
} 