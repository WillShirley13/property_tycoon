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
    "GREEN": (0, 255, 0),         # Green
    "DEEP_BLUE": (0, 0, 139),     # Deep Blue
    "STATION": (128, 128, 128),   # Gray for stations
    "UTILITY": (192, 192, 192)    # Light gray for utilities
}

# Space property groups (maps each space to its property group)
SPACE_PROPERTY_GROUPS = [
    "SPECIAL",      # GO
    "BROWN",        # The Old Creek
    "SPECIAL",      # Pot Luck
    "BROWN",        # Gangsters Paradise
    "SPECIAL",      # Free Parking
    "STATION",      # Brighton Station
    "BLUE",         # The Angels Delight
    "SPECIAL",      # Opportunity Knocks
    "BLUE",         # Potter Avenue
    "BLUE",         # Granger Drive
    "SPECIAL",      # JAIL
    "PURPLE",       # Skywalker Drive
    "UTILITY",      # Tesla Power Co
    "PURPLE",       # Wookie Hole
    "PURPLE",       # Rey Lane
    "STATION",      # Hove Station
    "ORANGE",       # Bishop Drive
    "SPECIAL",      # Pot Luck
    "ORANGE",       # Dunham Street
    "ORANGE",       # Broyles Lane
    "SPECIAL",      # FREE PARKING
    "RED",          # Yue Fei Square
    "SPECIAL",      # Opportunity Knocks
    "RED",          # Mulan Rouge
    "RED",          # Han Xin Gardens
    "STATION",      # Falmer Station
    "YELLOW",       # Shatner Close
    "YELLOW",       # Picard Avenue
    "UTILITY",      # Edison Water
    "YELLOW",       # Crusher Creek
    "SPECIAL",      # GO TO JAIL
    "GREEN",        # Sirat Mews
    "GREEN",        # Ghengis Crescent
    "SPECIAL",      # Pot Luck
    "GREEN",        # Ibis Close
    "STATION",      # Portslade Station
    "SPECIAL",      # Opportunity Knocks
    "DEEP_BLUE",    # James Webb Way
    "SPECIAL",      # Free Parking
    "DEEP_BLUE"     # Turing Heights
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