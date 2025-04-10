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
- **`rounds_in_jail: int`**  
  Number of rounds the player has been in jail.
- **`is_first_circuit_complete: bool`**  
  Set to true if the player has completed a full circuit of the board.
- **`has_passed_go_flag: bool`**  
  Flag indicating if the player has passed GO.
- **`current_position: int`**  
  The player's current position on the board.
- **`doubles_rolled: int`**  
  Number of consecutive doubles rolled.
- **`is_bankrupt: bool`**  
  Indicates if the player is bankrupt.
- **`recent_dice_rolls: list[int]`**  
  List of recent dice roll values.
- **Inherited Attributes (from PropertyHolder):**
  - `cash_balance` (starts at 1,500)
  - `owned_properties`

**Methods:**
- **Name and Token Methods:**
  - **`get_name() -> str`**  
    Returns the player's name.
  - **`get_game_token() -> GameToken`**  
    Returns the player's game token.

- **Jail Card Methods:**
  - **`get_get_out_of_jail_cards() -> int`**  
    Returns the number of "Get Out of Jail Free" cards held.
  - **`add_get_out_of_jail_card() -> None`**  
    Increases the count of "Get Out of Jail Free" cards.
  - **`use_get_out_of_jail(jail: Jail) -> None`**  
    Uses a "Get Out of Jail Free" card; if none are available, raises `NoGetOutOfJailCardsError`.

- **Jail Status Methods:**
  - **`get_is_in_jail() -> bool`**  
    Returns whether the player is in jail.
  - **`get_rounds_in_jail() -> int`**  
    Returns the number of rounds the player has been in jail.
  - **`set_rounds_in_jail(rounds: int) -> None`**  
    Sets the number of rounds the player has been in jail.

- **Position and Movement Methods:**
  - **`get_current_position() -> int`**  
    Returns the player's current position on the board.
  - **`get_is_first_circuit_complete() -> bool`**  
    Returns whether the player has completed a full circuit.
  - **`set_is_first_circuit_complete() -> None`**  
    Sets the player's first circuit completion status to true.
  - **`get_has_passed_go_flag() -> bool`**  
    Returns and resets the flag indicating if the player has passed GO.
  - **`set_has_passed_go_flag(has_passed_go_flag: bool) -> None`**  
    Sets the flag indicating if the player has passed GO.
  - **`move_player() -> list[list[int], int] | None`**  
    Moves the player based on dice rolls, handling circular movement.
  - **`move_player_to_position(position: int) -> None`**  
    Sets the player's board position directly.

- **Dice Roll Methods:**
  - **`get_recent_dice_rolls() -> list[int]`**  
    Returns the list of recent dice roll values.
  - **`set_recent_dice_rolls(recent_dice_rolls: list[int]) -> None`**  
    Sets the list of recent dice roll values.
  - **`get_doubles_rolled() -> int`**  
    Returns the number of consecutive doubles rolled.
  - **`set_doubles_rolled(doubles_rolled: int) -> None`**  
    Sets the number of consecutive doubles rolled.
  - **`reset_doubles_rolled() -> None`**  
    Resets the doubles rolled counter to zero.

- **Property Transaction Methods:**
  - **`purchase_property(property: Ownable, bank: Bank) -> None`**  
    Purchases a property from the bank by verifying ownership, checking funds, updating cash balances, updating portfolios, and transferring property ownership.
  - **`sell_property(property: Ownable, bank: Bank) -> None`**  
    Sells a property back to the bank. Mortgaged properties are exchanged for half the property's cost.
  - **`mortgage_property(property: Ownable, bank: Bank) -> None`**  
    Mortgages a property, receiving half its cost from the bank.
  - **`pay_off_mortgage(property: Ownable, bank: Bank) -> None`**  
    Pays off a mortgaged property.
  - **`_add_property_to_portfolio(property: Ownable) -> None`**  
    Adds a property to the player's portfolio.
  - **`_remove_property_from_portfolio(property: Ownable) -> None`**  
    Removes a property from the player's portfolio.

- **Player Status Methods:**
  - **`get_is_bankrupt() -> bool`**  
    Returns whether the player is bankrupt.
  - **`set_is_bankrupt() -> None`**  
    Sets the player's bankrupt status to true.
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
- **`get_name() -> str`**  
  Returns the name of the property.
- **`get_property_group() -> PropertyGroup`**  
  Returns the property group.
- **`get_cost() -> int`**  
  Returns the purchase cost.
- **`get_value() -> int`**  
  Returns the current value.
- **`set_value(value: int) -> None`**  
  Sets the current value.
- **`get_owner() -> Player | Bank`**  
  Returns the current owner.
- **`set_owner(new_owner: Player | Bank) -> None`**  
  Updates the owner.
- **`get_rent_due_from_player(player: Player) -> int`**  
  Processes rent collection from a player landing on this ownable space. If the property is mortgaged, no rent is charged.
- **`get_rent_cost() -> int`**  
  Returns the current rent cost.
- **`get_is_mortgaged() -> bool`**  
  Returns whether the property is mortgaged.
- **`set_is_mortgaged(is_mortgaged: bool) -> None`**  
  Sets whether the property is mortgaged.

---

### Property
**Description:**  
A developable property that may have houses and/or a hotel.

**Inheritance:**  
Extends `Ownable`.

**Attributes:**
- **`houses: int`**  
  Number of houses built.
- **`hotel: int`**  
  Indicates if a hotel is built (0 or 1).
- **`next_upgrade_cost: int`**  
  Cost for the next upgrade (house or hotel).
- **`owner_owns_all_properties_in_group: bool`**  
  Set to true if the owner holds all properties in this property group (monopoly).
- **`is_eligible_for_upgrade: bool`**  
  Indicates if the property is eligible for an upgrade.
- **`is_eligible_for_downgrade: bool`**  
  Indicates if the property is eligible for a downgrade.

**Methods:**
- **Getters and Setters:**
  - **`get_property_group() -> PropertyGroup`**  
    Returns the property group.
  - **`get_houses() -> int`**  
    Returns the number of houses.
  - **`set_houses(houses: int) -> None`**  
    Sets the number of houses.
  - **`get_hotel() -> int`**  
    Returns whether a hotel is present (0 or 1).
  - **`set_hotel(hotel: int) -> None`**  
    Sets whether a hotel is present.
  - **`get_is_eligible_for_upgrade() -> bool`**  
    Returns whether the property is eligible for an upgrade.
  - **`set_is_eligible_for_upgrade(is_eligible_for_upgrade: bool) -> None`**  
    Sets whether the property is eligible for an upgrade.
  - **`get_is_eligible_for_downgrade() -> bool`**  
    Returns whether the property is eligible for a downgrade.
  - **`set_is_eligible_for_downgrade(is_eligible_for_downgrade: bool) -> None`**  
    Sets whether the property is eligible for a downgrade.
  - **`get_owner_owns_all_properties_in_group() -> bool`**  
    Returns whether the owner owns all properties in the group.
  - **`set_owner_owns_all_properties_in_group(owner_owns_all_properties_in_group: bool) -> None`**  
    Sets whether the owner owns all properties in the group.

- **Property Management:**
  - **`upgrade_property(bank: Bank) -> None`**  
    Upgrades a property by adding a house or hotel. Checks for eligibility, funds, and property group balance.
  - **`downgrade_property(bank: Bank) -> None`**  
    Downgrades a property by removing a house or hotel. Checks for eligibility and property group balance.

- **Utility Methods:**
  - **`set_rent_cost() -> None`**  
    Updates the rent based on current development and monopoly status.
  - **`check_max_difference_between_houses_owned_is_1_within_property_group(this_props_houses_after_change: int) -> bool`**  
    Verifies that the difference in house counts between this property (after a change) and others in the same group does not exceed one.

---

### Station
**Description:**  
A station (e.g., train station) that charges rent based on the number of stations owned.

**Inheritance:**  
Extends `Ownable`.

**Attributes:**
- **`owner_owns_all_stations: bool`**  
  True if the owner holds all stations.
- **`num_of_stations_owned_by_owner: int`**  
  The number of stations owned by the property owner.
- **`rent_values: List[int]`**  
  List of rent values based on number of stations owned.

**Methods:**
- **`set_rent_cost() -> None`**  
  Adjusts the rent based on the number of stations the owner holds.
- **`get_rent_due_from_player(player: Player) -> int`**  
  Calculates and returns the rent due from a player.
- **`get_owner_owns_all_stations() -> bool`**  
  Returns whether the owner owns all stations.
- **`set_owner_owns_all_stations(owner_owns_all_stations: bool) -> None`**  
  Sets whether the owner owns all stations.
- **`get_num_of_stations_owned_by_owner() -> int`**  
  Returns the number of stations owned by the owner.
- **`set_num_of_stations_owned_by_owner(num_of_stations_owned_by_owner: int) -> None`**  
  Sets the number of stations owned by the owner.
- **`get_rent_values() -> List[int]`**  
  Returns the list of rent values.

---

### Utility
**Description:**  
Represents a utility property where rent is determined by the dice roll multiplied by a specified factor.

**Inheritance:**  
Extends `Ownable`.

**Attributes:**
- **`owner_owns_all_utilities: bool`**  
  True if the same player owns both utilities.
- **`num_of_utilities_owned_by_owner: int`**  
  The count of utilities held by the owner.

**Methods:**
- **`get_rent_due_from_player(player: Player) -> int`**  
  Applies the appropriate multiplier to the dice roll to calculate and collect rent; no rent is collected if the utility is mortgaged.
- **`get_owner_owns_all_utilities() -> bool`**  
  Returns whether the owner owns all utilities.
- **`set_owner_owns_all_utilities(owner_owns_all_utilities: bool) -> None`**  
  Sets whether the owner owns all utilities.
- **`get_num_of_utilities_owned_by_owner() -> int`**  
  Returns the number of utilities owned by the owner.
- **`set_num_of_utilities_owned_by_owner(num_of_utilities_owned_by_owner: int) -> None`**  
  Sets the number of utilities owned by the owner.

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
- **`get_currently_in_jail() -> list[tuple[Player, int]]`**  
  Returns the list of players currently in jail.
- **`pay_fine_for_release(player: Player, free_parking: FreeParking) -> None`**  
  Player pays a fine to be released from jail, with the fine going to Free Parking.

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
- **`player_names: list[(str, GameToken)]`**  
  List of player names and their chosen tokens.
- **`bank: Bank`**  
  The game's bank instance.
- **`free_parking: FreeParking`**  
  The Free Parking instance.
- **`go: Go`**  
  The Go instance.
- **`jail: Jail`**  
  The Jail instance.
- **`pot_luck_cards: GameCard`**  
  The Pot Luck card deck.
- **`opportunity_knocks: GameCard`**  
  The Opportunity Knocks card deck.
- **`time_limit: int`**  
  The time limit for the game (default is 0, indicating no limit).
- **`is_time_limit_reached: bool`**  
  Flag indicating if the time limit has been reached.

**Methods:**
- **`start_timer() -> None`**  
  Starts the game timer in a separate thread.
- **`countdown() -> None`**  
  Counts down the time limit and sets the flag when time is up.
- **`get_is_time_limit_reached() -> bool`**  
  Returns whether the time limit has been reached.
- **`get_time_limit() -> int`**  
  Returns the time limit for the game.
- **`get_players() -> list[Player]`**  
  Returns the list of players in the game.
- **`get_bank() -> Bank`**  
  Returns the bank instance for the game.
- **`assign_all_properties_to_bank() -> None`**  
  Assigns all properties to the bank at the start of the game.
- **`get_free_parking() -> FreeParking`**  
  Returns the Free Parking instance.
- **`get_go() -> Go`**  
  Returns the Go instance.
- **`get_jail() -> Jail`**  
  Returns the Jail instance.
- **`get_pot_luck_cards() -> GameCard`**  
  Returns the Pot Luck card deck.
- **`get_opportunity_knocks() -> GameCard`**  
  Returns the Opportunity Knocks card deck.
- **`get_game_board() -> list[Ownable | FreeParking | Jail | Go | GameCard]`**  
  Returns the current game board.
- **`get_game_space_helper() -> dict[Ownable | FreeParking | Jail | Go | GameCard, int]`**  
  Returns the helper dictionary for quick position lookup of game spaces.
- **`create_game_board() -> None`**  
  Initializes the game board with all spaces in the correct order.
- **`create_players() -> None`**  
  Creates player instances based on the provided player names and tokens.

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
  - `STATION_RENT_VALUES = [25, 50, 100, 200]`

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
