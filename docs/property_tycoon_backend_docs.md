# Property Tycoon Backend Documentation

This document provides an overview of the backend architecture for Property Tycoon, including enums, classes, constants, and errors.

---

## Table of Contents

1. [Enums](#enums)
2. [Classes](#classes)
   - [PropertyHolder](#propertyholder)
   - [Bank](#bank)
   - [Player](#player)
   - [GameCard](#gamecard)
   - [Ownable](#ownable)
   - [Property](#property)
   - [Station](#station)
   - [Utility](#utility)
   - [Jail](#jail)
   - [Go](#go)
   - [FreeParking](#freeparking)
   - [Admin](#admin)
3. [Constants](#constants)
4. [Errors](#errors)

---

## Enums

### GameToken
Represents the tokens available for players.

- `BOOT`
- `SMARTPHONE`
- `SHIP`
- `HATSTAND`
- `CAT`
- `IRON`

### PropertyGroup
Classifies the groups/types of ownable properties:

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

---

## Classes

### PropertyHolder
**Description:**  
Base class for all entities that can own properties (e.g., `Player` and `Bank`).

**Attributes:**
- **`cash_balance: int`**  
  The current cash balance.
- **`owned_properties: dict<PropertyGroup, list[Ownable]>`**  
  A dictionary mapping each property group to the list of properties owned.

**Methods:**
- **`get_cash_balance() -> int`**  
  Returns the current cash balance.
- **`add_cash_balance(amount: int) -> None`**  
  Adds the specified amount to the cash balance.
- **`sub_cash_balance(amount: int) -> None`**  
  Deducts the specified amount; raises `InsufficientFundsError` if the balance is insufficient.
- **`get_owned_properties() -> dict<PropertyGroup, list[Ownable]>`**  
  Retrieves the owned properties.
- **`add_property_to_portfolio(property: Ownable) -> None`**  
  Adds an ownable property to the portfolio; raises `PropertyAlreadyInPortfolioError` if already present.
- **`remove_property_from_portfolio(property: Ownable) -> None`**  
  Removes an ownable property from the portfolio; raises `PropertyNotInPortfolioError` if not found.

---

### Bank
**Description:**  
Represents the bank in the game, handling transactions and owning properties that have not yet been purchased by a player.

**Inheritance:**  
Inherits from `PropertyHolder`.

**Attributes:**
- **`cash_balance`** is initialized to 500,000.
- Inherited **`owned_properties`**.

**Methods:**
- **`get_cash_balance() -> int`**  
  Returns the current cash balance.
- **`add_cash_balance(amount: int) -> None`**  
  Adds the specified amount to the bank's cash balance.
- **`sub_cash_balance(amount: int) -> None`**  
  Subtracts the specified amount from the bank's cash balance.

---

### Player
**Description:**  
Represents a game player.

**Inheritance:**  
Inherits from `PropertyHolder`.

**Attributes:**
- **`name: str`**  
  The player's name.
- **`game_token: GameToken`**  
  The token representing the player.
- **`get_out_of_jail_cards: int`**  
  Number of "Get Out of Jail Free" cards held.
- **`is_in_jail: bool`**  
  Indicates whether the player is currently in jail.
- **`is_first_circuit_complete: bool`**  
  Set to true if the player has completed a full circuit of the board.
- **`current_position: int`**  
  The player's current position on the board.
- **`is_bankrupt: bool`**  
  Indicates if the player is bankrupt.
- **Inherited Attributes (from PropertyHolder):**
  - `cash_balance` (starts at 1,500)
  - `owned_properties`

**Methods:**
- **`use_get_out_of_jail(jail: Jail) -> None`**  
  Uses a "Get Out of Jail Free" card; if none are available, raises `NoGetOutOfJailCardsError`.
- **`go_to_jail(jail: Jail) -> None`**  
  Sends the player to jail; raises `PlayerAlreadyInJailError` if already incarcerated.
- **`add_get_out_of_jail() -> None`**  
  Increases the count of "Get Out of Jail Free" cards.
- **`purchase_property(property: Ownable, bank: Bank) -> None`**  
  Purchases a property from the bank by verifying ownership, checking funds, updating cash balances, updating portfolios, and transferring property ownership.
- **`sell_property(property: Ownable, bank: Bank) -> None`**  
  Sells a property back to the bank. Mortgaged properties are exchanged for half the property's cost.
- **`move_player(steps: int) -> int`**  
  Moves the player a specified number of steps along the board, handling circular movement; does not award a GO payout.
- **`move_player_to_position(position: int) -> None`**  
  Sets the player's board position directly.
- **`retire_player(bank: Bank) -> None`**  
  Processes player retirement by transferring all cash and properties to the bank.
- **`get_player_net_worth() -> int`**  
  Calculates the player's net worth combining cash and property values (mortgaged properties contribute half their value).

---

### GameCard
**Description:**  
Models the game card decks (both Pot Luck and Opportunity Knocks) and implements their associated actions.

**Attributes:**
- **`card_ids: dict[str, int]`**  
  Maps card descriptions to their corresponding identifier numbers.
- **`card_pack: list[str]`**  
  A list representing the deck; cards are cycled to achieve a continuous rotation.

**Methods:**
- **`get_card() -> tuple[str, int]`**  
  Retrieves and returns the next card from the deck as a tuple `(card text, card id)`, using a cyclic rotation.
- **`process_card(player: Player, bank: Bank, card_id: int, free_parking: FreeParking, jail: Jail, players: list[Player]) -> None`**  
  Executes actions associated with a given card id. May involve cash transactions, movement, jail operations, or repair fee payments. If funds are insufficient in any case, it raises an `InsufficientFundsError`.
- **`shuffle_pack() -> None`**  
  Shuffles the card pack in place using Python's built-in random shuffle.

---

### Ownable
**Description:**  
Abstract class for all board spaces that may be owned, including properties, stations, and utilities.

**Attributes:**
- **`name: str`**
- **`owned_by: Player | Bank`**
- **`cost_to_buy: int`**
- **`value: int`**
- **`rent_cost: int`**
- **`is_mortgaged: bool`**
- **`property_group: PropertyGroup`**

**Methods:**
- **`get_cost() -> int`**  
  Returns the purchase cost.
- **`get_owner() -> Player | Bank`**  
  Returns the current owner.
- **`set_owner(new_owner: Player | Bank) -> None`**  
  Updates the owner.
- **`get_rent_due_from_player(player: Player) -> int`**  
  Processes rent collection from a player landing on this ownable space. If the property is mortgaged, no rent is charged.

---

### Property
**Description:**  
A developable property that may have houses and/or a hotel.

**Inheritance:**  
Extends `Ownable`.

**Additional Attributes:**
- **`houses: int`**  
  Number of houses built.
- **`house_cost: int`**  
  Cost to build a house.
- **`hotel: int`**  
  Indicates if a hotel is built (0 or 1).
- **`hotel_cost: int`**  
  Cost to build a hotel.
- **`rent: int`**  
  The current rent, updated as the property is developed.
- **`owner_owns_all_properties: bool`**  
  Set to true if the owner holds all properties in this property group (monopoly).

**Methods:**
- **`buy_house(bank: Bank) -> None`**  
  Purchases a house after verifying group balance (maximum difference of 1 among properties) and checking funds. May raise `MaxDifferenceBetweenHousesOrHotelsError` or `MaxHousesOrHotelsError`.
- **`buy_hotel(bank: Bank) -> None`**  
  Buys a hotel if exactly 4 houses exist and no hotel is yet built. May raise `MaxHousesOrHotelsError`.
- **`sell_house(bank: Bank) -> None`**  
  Sells a house while maintaining group balance. Raises `NoHousesOrHotelsToSellError` if no houses exist.
- **`sell_hotel(bank: Bank) -> None`**  
  Sells the hotel if present.
- **`set_rent_cost(new_rent_cost: int) -> None`**  
  Updates the rent based on current development and monopoly status.
- **`check_max_difference_between_houses_owned_is_1_within_property_group(this_props_houses_after_change: int) -> bool`**  
  Verifies that the difference in house counts between this property (after a change) and others in the same group does not exceed one.

---

### Station
**Description:**  
A station (e.g., train station) that charges rent based on the number of stations owned.

**Inheritance:**  
Extends `Ownable`.

**Additional Attributes:**
- **`owner_owns_all_stations: bool`**  
  True if the owner holds all stations.
- **`num_of_stations_owned_by_owner: int`**  
  The number of stations owned by the property owner.

**Methods:**
- **`set_rent_cost() -> None`**  
  Adjusts the rent based on the number of stations the owner holds:
  - 1 Station: 25
  - 2 Stations: 50
  - 3 Stations: 100
  - 4 Stations: 200

---

### Utility
**Description:**  
Represents a utility property where rent is determined by the dice roll multiplied by a specified factor.

**Inheritance:**  
Extends `Ownable`.

**Additional Attributes:**
- **`owner_owns_all_utilities: bool`**  
  True if the same player owns both utilities.
- **`num_of_utilities_owned_by_owner: int`**  
  The count of utilities held by the owner.

**Methods:**
- **`set_rent_cost() -> None`**  
  Sets the rent cost based on the number of utilities owned.
- **`get_rent_due_from_player(player: Player, dice_roll: int) -> int`**  
  Applies the appropriate multiplier to the dice roll to calculate and collect rent; no rent is collected if the utility is mortgaged.

---

### Jail
**Description:**  
Manages jail mechanics within the game.

**Attributes:**
- **`currently_in_jail: list[tuple[Player, int]]`**  
  A list of tuples tracking players in jail along with their turn counts.
- **`release_cost: int`** (default: 50)  
  The cost required to be released from jail.

**Methods:**
- **`release_from_jail(player: Player) -> None`**  
  Releases the specified player from jail.
- **`put_in_jail(player: Player) -> None`**  
  Puts a player in jail.
- **`get_release_cost() -> int`**  
  Returns the cost for jail release.
- **`get_is_in_jail() -> list[tuple[Player, int]]`**  
  Returns the list of players currently in jail.

---

### Go
**Description:**  
Represents the "Go" space on the board.

**Methods:**
- **`pay_player(player: Player, bank: Bank) -> None`**  
  Awards a fixed amount (typically 200) to the player.
- **`get_pass_go_payout() -> int`**  
  Retrieves the payout amount for landing on or passing Go.

---

### FreeParking
**Description:**  
Handles the collection of fines in the Free Parking area and manages payouts to players.

**Attributes:**
- **`fines_collected: int`**  
  Total fines that have been accumulated.

**Methods:**
- **`get_fines_collected() -> int`**  
  Returns the total accumulated fines.
- **`add_fine(amount: int, player: Player) -> None`**  
  Deducts the specified fine amount from the player and adds it to the Free Parking pool (raises `InsufficientFundsError` if funds are insufficient).
- **`payout_fines(player: Player) -> None`**  
  Awards the total collected fines to the specified player and resets the fines to zero.

---

### Admin
**Description:**  
Manages the game board, players, and overall game state.

**Attributes:**
- **`game_board: list[Ownable | FreeParking | Jail | Go | GameCard]`**  
  A list representing the game board, where each index corresponds to a space on the board.
- **`game_space_helper: dict[Ownable | FreeParking | Jail | Go | GameCard, int]`**  
  A helper dictionary to quickly look up the index of a space on the board.
- **`players: list[Player]`**  
  A list of all players in the game.
- **`bank: Bank`**  
  The game's bank instance.
- **`time_limit: int`**  
  The time limit for the game (default is 0, indicating no limit).

**Methods:**
- **`create_game_board() -> None`**  
  Initializes the game board with all spaces in the correct order, including properties, stations, utilities, and special spaces like Go, Jail, and Free Parking. Also creates card decks for Pot Luck and Opportunity Knocks.
- **`create_players() -> None`**  
  Creates player instances based on the provided player names and tokens.
- **`get_time_limit() -> int`**  
  Returns the time limit for the game. Default set to 0 for full game.
- **`get_players() -> list[Player]`**  
  Returns the list of players in the game.
- **`get_bank() -> Bank`**  
  Returns the bank instance for the game.
- **`get_game_board() -> list[Ownable | FreeParking | Jail | Go | GameCard]`**  
  Returns the current game board.
- **`get_game_space_helper() -> dict[Ownable | FreeParking | Jail | Go | GameCard, int]`**  
  Returns the helper dictionary for quick position lookup of game spaces.

---

## Constants

Defined in `constants.py`:

- **Total Number of Properties per Group:**
  - `TOTAL_BROWN_PROPERTIES = 2`
  - `TOTAL_BLUE_PROPERTIES = 3`
  - `TOTAL_PURPLE_PROPERTIES = 3`
  - `TOTAL_ORANGE_PROPERTIES = 3`
  - `TOTAL_RED_PROPERTIES = 3`
  - `TOTAL_YELLOW_PROPERTIES = 3`
  - `TOTAL_GREEN_PROPERTIES = 3`
  - `TOTAL_DEEP_BLUE_PROPERTIES = 2`
  - `TOTAL_STATIONS = 4`
  - `TOTAL_UTILITIES = 2`

- **Station Rents:**
  - `ONE_STATION_RENT = 25`
  - `TWO_STATION_RENT = 50`
  - `THREE_STATION_RENT = 100`
  - `FOUR_STATION_RENT = 200`

- **Utility Rent Multipliers:**
  - `ONE_UTILITY_RENT_DICE_MULTIPLIER = 4`
  - `TWO_UTILITY_RENT_DICE_MULTIPLIER = 10`

- **Property Build Costs and Rent Data:**  
  Managed via `PROPERTY_BUILD_COSTS` and `PROPERTY_DATA`.

- **Card Decks:**
  - `OPPORTUNITY_KNOCKS_CARDS`: Dictionary mapping card text to card IDs for Opportunity Knocks cards.
  - `POT_LUCK_CARDS`: Dictionary mapping card text to card IDs for Pot Luck cards.

---

## Errors

Custom exceptions defined in `errors.py`:

- **`InsufficientFundsError`**  
  Raised when a player does not have enough funds.
- **`BankCannotSellPropertyError`**  
  Raised when attempting to sell a property owned by the bank.
- **`CannotSellPropertyError`**  
  Raised when a property cannot be sold (e.g., if houses or hotels are present).
- **`PropertyAlreadyMortgagedError`**  
  Raised when attempting to mortgage a property that is already mortgaged.
- **`PropertyNotInPortfolioError`**  
  Raised when trying to perform an operation on a property not in the portfolio.
- **`NoGetOutOfJailCardsError`**  
  Raised when a player attempts to use a "Get Out of Jail Free" card with none available.
- **`PlayerAlreadyInJailError`**  
  Raised if a player already in jail is sent to jail again.
- **`PropertyAlreadyInPortfolioError`**  
  Raised when a property is already present in the portfolio.
- **`PropertyNotOwnedByBankError`**  
  Raised when attempting to purchase a property not owned by the bank.
- **`NoHousesOrHotelsToSellError`**  
  Raised when there are no houses or hotels to sell.
- **`MaxHousesOrHotelsError`**  
  Raised when an attempt is made to exceed the allowed number of houses or hotels.
- **`MaxDifferenceBetweenHousesOrHotelsError`**  
  Raised when building or selling would result in a house count imbalance (exceeding a difference of 1) within a property group.

---
