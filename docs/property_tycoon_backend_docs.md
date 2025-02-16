# Game Documentation

NOTES:
 - This documentation is for the backend architecture of Property Tycoon.
 - This documentation is not complete and will be updated as the project progresses.

## Table of Contents
Enums:
  - GameToken
  - PropertyGroup
  
Classes:
  - Bank
  - GameCard
  - Player
  - Property
  - Ownable
  - Station
  - Utility
  - Jail
  - Go
  - FreeParking

## Enums

### GameToken:
Represents the different types of tokens a player can use in the game.
- `BOOT`
- `SMARTPHONE`
- `SHIP`
- `HATSTAND`
- `CAT`
- `IRON`

### PropertyGroup:
Defines groups of properties that can be owned in the game.
- `BROWN`
- `BLUE`
- `PURPLE`
- `ORANGE`
- `RED`
- `YELLOW`
- `GREEN`
- `DEEP_BLUE`
- `UTILITIES`
- `STATION`

## Classes

### Bank:
Handles monetary transactions within the game.

**Attributes:**
- `cash_balance`: `int` - the current cash balance of the bank.
- `owned_properties`: `dict<PropertyGroup, [Ownable]>` - properties owned by the bank, grouped by type.

**Methods:**
- `get_cash_balance() -> int`: Returns the current cash balance.
- `add_cash_balance(amount: int) -> void`: Adds the specified amount to the bank's cash balance.
- `sub_cash_balance(amount: int) -> void`: Subtracts the specified amount from the bank's cash balance.

### GameCard:
Represents the game card decks and their mechanics.

**Attributes:**
- `card_ids`: `dict<string, int>` - a dictionary mapping card descriptions to their identifiers.
- `card_pack`: `list<string>` - a list of card descriptions.

**Methods:**
- `getCard() -> (string, int)`: Returns a tuple containing a message from the card and an integer corresponding to an action.
- `process_card(player: Player, bank: Bank, card_id: int) -> void`: Processes the card's effect on the given player and bank.
- `shuffle_pack() -> void`: Shuffles the card pack.

### Player:
Represents a player in the game.

**Attributes:**
- `game_token`: `GameToken` - the token used by the player.
- `cash_balance`: `int` - the player's current cash balance.
- `has_get_out_of_jail`: `int` - indicates whether the player has a 'get out of jail free' card.
- `is_in_jail`: `bool` - indicates whether the player is currently in jail.
- `owned_properties`: `dict<PropertyGroup, [Ownable]>` - properties owned by the player, grouped by type.
- `is_first_circuit_complete`: `bool` - indicates if the player has completed one circuit of the board.
- `current_position`: `int` - the player's current position on the board.
- `stations_owned`: `int` - the number of stations owned by the player.
- `utilities_owned`: `int` - the number of utilities owned by the player.
- `owns_all_brown` to `owns_all_deep_blue`: `bool` - flags for ownership of all properties in each group.
- `owns_all_utilities`: `bool` - indicates if the player owns all utilities.
- `owns_all_stations`: `bool` - indicates if the player owns all stations.
- `isBankrupt`: `bool` - indicates if the player is bankrupt.

**Methods:**
- `get_cash_balance() -> int`: Returns the player's current cash balance.
- `add_cash_balance(amount: int) -> void`: Adds the specified amount to the player's cash balance.
- `sub_cash_balance(amount: int) -> void`: Subtracts the specified amount from the player's cash balance.
- `use_get_out_of_jail() -> void`: Uses the 'get out of jail free' card if available.
- `go_to_jail() -> void`: Moves the player to jail.
- `purchase_property(space: Space, bank: Bank) -> void`: Attempts to purchase a property.
- `move_player(steps: int) -> int`: Moves the player forward by the specified number of steps.
- `get_current_position() -> int`: Returns the current position of the player on the board.
- `get_stations_owned() -> int`: Returns the number of stations owned by the player.
- `get_utilities_owned() -> int`: Returns the number of utilities owned by the player.
- `retire_player(bank: Bank) -> void`: Retires the player from the game, transferring all assets to the bank.
- `get_player_net_worth() -> int`: Calculates and returns the net worth of the player.

### Ownable:
The base class for purchasable spaces on the game board.

**Attributes:**
- `owned_by`: `Player | Bank` - the current owner of the space
- `value`: `int` - the purchase cost of the space
- `is_mortgaged`: `bool` - indicates if the space is mortgaged
- `property_group`: `PropertyGroup` - the group to which the space belongs
- `name`: `string` - the name of the space

**Methods:**
- `get_cost() -> int`: Returns the cost of the space
- `get_owner() -> Player|Bank`: Returns the current owner of the space
- `set_owner(new_owner: Player) -> void`: Sets the owner of the space
- `get_rent_due(player: Player) -> void`: Calculates the rent due when a player lands on the space and deducts the  rent from the player's cash balance
- `sell_property(bank: Bank) -> void`: Sells the space back to the bank
- `mortgage_property(bank: Bank) -> void`: Mortgages the space

### Property:
Inherits from `Ownable`. Represents a property space on the game board.

**Attributes:**
- `houses`: `int` - the number of houses on the property
- `house_cost`: `int` - the cost of a house
- `hotel`: `int` - indicates whether a hotel is present (0 or 1)
- `hotel_cost`: `int` - the cost of a hotel
- `rent`: `int` - the current rent due for the property

**Methods:**
- `buy_house(bank: Bank) -> void`: Buys a house for the property, not exceeding four
- `buy_hotel(bank: Bank) -> void`: Buys a hotel for the property, replacing houses
- `sell_house(bank: Bank) -> void`: Sells one house from the property
- `sell_hotel(bank: Bank) -> void`: Sells the hotel on the property

### Station:
Inherits from `Ownable`. Represents a station space on the game board.

*No additional attributes or methods beyond those inherited from Ownable*

### Utility:
Inherits from `Ownable`. Represents a utility space on the game board.

*No additional attributes or methods beyond those inherited from Ownable*

### Jail:
Represents the 'jail' space on the game board and handles it's mechanics.

**Attributes:**
- `is_in_jail`: `list<(Player, int)>` - a list of tuples containing players and the number of turns they have been in jail.
- `release_cost`: `int` - the cost to release a player from jail.

**Methods:**
- `release_from_jail(player: Player) -> void`: Releases the specified player from jail upon payment or card use.
- `put_in_jail(player: Player) -> void`: Puts the specified player in jail.

### Go:
Represents the 'Go' space on the game board.

**Methods:**
- `pay_player(player: Player) -> void`: Pays the player for passing or landing on 'Go'.

### FreeParking:
Represents the 'free parking' space on the game board and handles it's mechanics.

**Attributes:**
- `fines_collected`: `int` - the total fines collected in the free parking space.

**Methods:**
- `get_fines_collected() -> int`: Returns the total fines collected.
- `add_fine(amount: int, player: Player) -> void`: Adds a fine to the total collected.
- `payout_fines(player: Player) -> void`: Pays out the collected fines to the player landing on the space. 