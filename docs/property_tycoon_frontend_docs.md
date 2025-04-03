# Property Tycoon Frontend Documentation

This document provides an overview of the frontend architecture for Property Tycoon, including the main display components, utilities, and UI elements.

---

## Table of Contents

1. [Main Display Classes](#main-display-classes)
   - [MainGameDisplay](#maingamedisplay)
   - [StartScreenDisplay](#startscreendisplay)
   - [TimeLimitChoiceDisplay](#timelimitchoicedisplay)
2. [Game Components](#game-components)
   - [Board](#board)
   - [GameMenuDisplay](#gamemenudisplay) 
   - [DiceManager](#dicemanager)
   - [CurrentPlayerDisplay](#currentplayerdisplay)
   - [PlayerDisplay](#playerdisplay)
3. [Popup Components](#popup-components)
   - [AuctionPopup](#auctionpopup)
   - [BankruptPopup](#bankruptpopup)
   - [BuyPropertyPopup](#buypropertypopup)
   - [EndOfGamePopup](#endofgamepopup)
   - [FreeParkingPopup](#freeparkingpopup)
   - [GameCardPopup](#gamecardpopup)
   - [GoPopup](#gopopup)
   - [InsufficientFundsPopup](#insufficientfundspopup)
   - [JailPopup](#jailpopup)
   - [JailVisitPopup](#jailvisitpopup)
   - [RentPaidPopup](#rentpaidpopup)
   - [SellOrMortgagePopup](#sellormortgagepopup)
   - [UpgradePropertyPopup](#upgradepropertypopup)
4. [Helper Utilities](#helper-utilities)
   - [BoardTextUtils](#boardtextutils)
   - [SpaceData](#spacedata)
5. [Art Assets](#art-assets)

---

## Main Display Classes

### MainGameDisplay
**Description:**  
Central point for main game while running.

**Attributes:**
- **`screen: pygame.Surface`**  
  The main Pygame surface for rendering the game.
- **`screen_width: int`** and **`screen_height: int`**  
  Dimensions of the game window.
- **`player_data: List[Tuple[str, Any]]`**  
  Information about players including names and tokens.
- **`admin: Admin`**  
  Reference to the game's Admin object that manages game state.
- **`running: bool`**  
  Flag indicating if the game is running.
- **`background: pygame.Surface`**  
  Background image for the game.
- **`board: Board`**  
  The game board component.
- **`current_player: Optional[Player]`**  
  The player whose turn it is currently.
- **Various game state objects:**
  - `bank`, `game_board`, `free_parking`, `go`, `jail`, etc.
- **UI Components:**
  - `player_display`, `current_player_display`, `game_menu` and `dice_manager`.
- **Popup Components:**
  - `jail_popup`, `sell_or_mortgage_popup`, `upgrade_property_popup`, etc.

**Methods:**
- **`__init__(screen_width, screen_height, screen, player_data, admin)`**  
  Initialises the game display with all necessary components.
- **`load_player_tokens(players)`**  
  Loads token images for each player.
- **`draw()`**  
  Renders all game components to the screen.
- **`handle_dice_roll()`**  
  Processes dice roll actions and updates player positions.
- **`handle_is_in_jail()`**  
  Handles player interactions when in jail.
- **`handle_players_new_position()`**  
  Processes effects of a player landing on a board space.
- **`handle_events()`**  
  Processes user input events.
- **`next_players_turn()`**  
  Advances the game to the next player's turn.
- **`run()`**  
  Main game loop that drives the display updates.

---

### StartScreenDisplay
**Description:**  
The initial screen where players can set up a new game by entering names.

**Attributes:**
- **`screen: pygame.Surface`**  
  Reference to the main display surface.
- **`background: pygame.Surface`**  
  Background image for the start screen.
- **UI Elements:**
  - Text boxes for player names
  - Token selection buttons
  - Start game button
  - Time limit selection button

**Methods:**
- **`draw()`**  
  Renders the start screen.
- **`handle_events()`**  
  Processes user input on the start screen.
- **`start_game()`**  
  Initialises a new game with the selected players.

---

### TimeLimitChoiceDisplay
**Description:**  
A screen for selecting the game's time limit.

**Attributes:**
- **`screen: pygame.Surface`**  
  Reference to the main display surface.
- **`time_limit_options: List[int]`**  
  Available time limit options in minutes.
- **UI Elements:**
  - Time limit selection buttons
  - Back button

**Methods:**
- **`draw()`**  
  Renders the time limit selection screen.
- **`handle_events()`**  
  Processes user input for time limit selection.
- **`select_time_limit(time_limit)`**  
  Sets the selected time limit and returns to the start screen.

---
## Game Components

### Board
**Description:**  
Renders the game board with all spaces and handles visual positioning of game pieces.

**Attributes:**
- **`board_width: int`** and **`board_height: int`**  
  Dimensions of the game board.
- **`board_x: int`** and **`board_y: int`**  
  Coordinates of the board's top-left corner.
- **`spaces: List[pygame.Rect]`**  
  List of rectangles representing each board space.
- **`space_centers: Dict[int, Tuple[int, int]]`**  
  Lookup for centre coordinates of each space.

**Methods:**
- **`_create_spaces()`**  
  Creates the rectangles for all board spaces.
- **`get_space_centers()`**  
  Calculates centre points for all spaces.
- **`draw(game_board)`**  
  Renders the complete board with properties and special spaces.

---

### GameMenuDisplay
**Description:**  
Displays game controls and options during gameplay.

**Attributes:**
- **`buttons: Dict[str, pygame.Rect]`**  
  Interactive buttons for game actions.
- **`timer: int`**  
  Game timer countdown in seconds.

**Methods:**
- **`draw()`**  
  Renders the game menu.
- **`update_timer()`**  
  Updates the timer display.
- **`handle_click(pos)`**  
  Processes clicks on menu buttons.

---

### DiceManager
**Description:**  
Handles dice rolling animations.

**Attributes:**
- **`dice: List[pygame.Surface]`**  
  Images for each die face.
- **`current_values: List[int]`**  
  The current values shown on the dice.
- **`is_rolling: bool`**  
  Whether the dice are currently in a rolling animation.

**Methods:**
- **`roll_dice()`**  
  Initiates a dice rolling animation.
- **`update_roll()`**  
  Updates the dice during an animation.
- **`draw()`**  
  Renders the dice.
- **`get_total()`**  
  Returns the sum of the dice values.
- **`is_doubles()`**  
  Checks if the dice show matching values.

---

### CurrentPlayerDisplay
**Description:**  
Shows information about the active player.

**Attributes:**
- **`player: Player`**  
  The currently active player.
- **`token_image: pygame.Surface`**  
  The player's token image.

**Methods:**
- **`update_player(player, token_image)`**  
  Updates the display with a new current player.
- **`draw()`**  
  Renders the current player display.

---

### PlayerDisplay
**Description:**  
Shows a summary of all players and their tokens.

**Attributes:**
- **`players: List[Tuple[Player, pygame.Surface]]`**  
  List of all players and their token images.
- **`player_rects: List[pygame.Rect]`**  
  Rectangle areas for each player's display.

**Methods:**
- **`update_players(players)`**  
  Updates the player list.
- **`draw()`**  
  Renders the player list display.

---

## Popup Components

### AuctionPopup
**Description:**  
Handles property auctions when a player lands on an unowned property and chooses not to buy it.

**Attributes:**
- **`property: Ownable`**  
  The property being auctioned.
- **`current_bid: int`**  
  The highest current bid.
- **`bidding_players: List[Player]`**  
  Players participating in the auction.
- **`current_bidder_index: int`**  
  Index of the player currently bidding.
- **`input_fields: Dict[str, pygame.Rect]`**  
  Input fields for player bids.
- **`input_texts: Dict[str, str]`**  
  Stored text for each input field.
- **`input_active: Dict[str, bool]`**  
  Tracks which input field is active.
- **`submit_button: pygame.Rect`**  
  Button to submit bids.

**Methods:**
- **`draw(property_obj, players, current_player)`**  
  Renders the auction interface with bidding fields.
- **`handle_events(event, players)`**  
  Processes input events including bid submissions.
- **`show(current_player, players, property_obj, bank)`**  
  Displays the auction popup and manages the auction process.

---

### BankruptPopup
**Description:**  
Displays when a player goes bankrupt.

**Attributes:**
- **`continue_button: pygame.Rect`**  
  Button to continue after viewing bankruptcy notice.
- **`continue_hover: bool`**  
  Tracks hover state of continue button.

**Methods:**
- **`draw(player)`**  
  Renders the bankruptcy notification with player information.
- **`handle_events(event)`**  
  Processes input events for the popup.
- **`show(player)`**  
  Displays the bankruptcy notice for a player.

---

### BuyPropertyPopup
**Description:**  
Allows a player to buy a property they've landed on.

**Attributes:**
- **`property: Ownable`**  
  The property available for purchase.
- **`player: Player`**  
  The player who can purchase the property.
- **`buy_button_rect: pygame.Rect`**  
  Button to purchase the property.
- **`no_thanks_button_rect: pygame.Rect`**  
  Button to decline purchase.
- **`made_purchase: Optional[bool]`**  
  Records whether the player made the purchase.

**Methods:**
- **`draw(player, property_obj)`**  
  Renders the property purchase interface.
- **`handle_events(event, current_player, property_obj, bank)`**  
  Processes input events including purchase decisions.
- **`show(property_obj, player, bank)`**  
  Displays the property purchase options.
- **`draw_button(surface, button_rect, text, hover, color)`**  
  Helper method to draw interactive buttons.

---

### EndOfGamePopup
**Description:**  
Displayed when the game ends, showing the winner and final scores.

**Attributes:**
- **`winner: Player`**  
  The player who won the game.
- **`button_width: int`** and **`button_height: int`**  
  Dimensions of the close button.
- **`close_button: pygame.Rect`**  
  Button to exit the game.
- **`button_hover: bool`**  
  Tracks hover state of the close button.

**Methods:**
- **`draw()`**  
  Renders the end game display with winner details.
- **`handle_event(event)`**  
  Processes input events for the popup.

---

### FreeParkingPopup
**Description:**  
Shown when a player lands on the Free Parking space.

**Attributes:**
- **`continue_button: pygame.Rect`**  
  Button to continue after viewing free parking notification.
- **`continue_hover: bool`**  
  Tracks hover state of continue button.

**Methods:**
- **`draw(player, amount)`**  
  Displays the free parking notification with amount collected.
- **`handle_events(event)`**  
  Processes input events for the popup.
- **`show(player, amount)`**  
  Displays the free parking notification.

---

### GameCardPopup
**Description:**  
Displays game cards (Pot Luck or Opportunity Knocks) when drawn.

**Attributes:**
- **`card_text: str`**  
  The text on the card.
- **`card_id: int`**  
  The unique identifier for the card.
- **`continue_button: pygame.Rect`**  
  Button to continue after card display.
- **`continue_hover: bool`**  
  Tracks hover state of continue button.
- **`result: Optional[str]`**  
  Records the player's action.

**Methods:**
- **`show_insufficient_funds_notification(card_info)`**  
  Displays a notification if player lacks funds for card action.
- **`draw(player, card_info)`**  
  Renders the card display.
- **`draw_button(surface, button_rect, text, hover)`**  
  Helper method to draw interactive buttons.
- **`handle_events(event)`**  
  Processes input events for the popup.
- **`show(player, bank, free_parking, jail, other_players, card_info, card_pack, go)`**  
  Displays the card and processes its effects.

---

### GoPopup
**Description:**  
Displayed when a player passes or lands on GO.

**Attributes:**
- **`continue_button: pygame.Rect`**  
  Button to continue after viewing GO notification.
- **`continue_hover: bool`**  
  Tracks hover state of continue button.

**Methods:**
- **`draw(player)`**  
  Renders the GO notification.
- **`handle_events(event)`**  
  Processes input events for the popup.
- **`show(player)`**  
  Displays the GO notification.

---

### InsufficientFundsPopup
**Description:**  
Displayed when a player doesn't have enough money for a transaction.

**Attributes:**
- **`player_name: str`**  
  Name of the player with insufficient funds.

**Methods:**
- **`draw()`**  
  Renders the insufficient funds notification.
- **`show()`**  
  Displays the notification for a few seconds.

---

### JailPopup
**Description:**  
Handles player interactions when in jail.

**Attributes:**
- **`player: Player`**  
  The player in jail.
- **`stay_in_jail_button: pygame.Rect`**  
  Button to stay in jail.
- **`use_card_button: pygame.Rect`**  
  Button to use a Get Out of Jail Free card.
- **`pay_fine_button: pygame.Rect`**  
  Button to pay the fine.
- **`result: Optional[str]`**  
  Records the player's jail decision.

**Methods:**
- **`draw(player)`**  
  Renders the jail interface.
- **`draw_button(button_rect, text, hover, color)`**  
  Helper method to draw interactive buttons.
- **`show_insufficient_funds_notification()`**  
  Displays a notification if player lacks funds to pay fine.
- **`handle_events(event, player, jail, free_parking, bank, go)`**  
  Processes input events including jail decisions.
- **`show(player, jail, free_parking, bank, go)`**  
  Displays the jail options.

---

### JailVisitPopup
**Description:**  
Displayed when a player lands on the Jail space as a visitor.

**Attributes:**
- **`continue_button: pygame.Rect`**  
  Button to continue after viewing jail visit notification.
- **`continue_hover: bool`**  
  Tracks hover state of continue button.

**Methods:**
- **`draw(player)`**  
  Renders the jail visit notification.
- **`handle_events(event)`**  
  Processes input events for the popup.
- **`show(player)`**  
  Displays the jail visit notification.

---

### RentPaidPopup
**Description:**  
Shown when a player pays rent to another player.

**Attributes:**
- **`continue_button: pygame.Rect`**  
  Button to proceed with payment.
- **`continue_hover: bool`**  
  Tracks hover state of continue button.
- **`rent_paid: bool`**  
  Records whether rent has been paid.

**Methods:**
- **`draw(player, ownable)`**  
  Renders the rent payment interface.
- **`handle_events(event, player, ownable, bank, rent_amount)`**  
  Processes rent payment or shows options to sell assets if needed.
- **`show(player, ownable, bank)`**  
  Displays the rent payment interface.

---

### SellOrMortgagePopup
**Description:**  
Interface for selling or mortgaging properties.

**Attributes:**
- **`sell_hover: bool`** and **`mortgage_hover: bool`**  
  Track hover states for initial choice buttons.
- **`sell_or_mortgage_choice: Optional[str]`**  
  Records the player's choice to sell or mortgage.
- **`selected_property: Optional[Property]`**  
  The property selected for sale or mortgage.
- **`property_buttons: List[Tuple[pygame.Rect, Property]]`**  
  Buttons for each property the player can sell/mortgage.
- **`close_button_rect: pygame.Rect`**  
  Button to close the property selection popup.
- **`sell_button_rect: pygame.Rect`**  
  Button to confirm selling/mortgaging the selected property.
- **`current_player: Player`**  
  Reference to the player selling/mortgaging.
- **`bank: Bank`**  
  Reference to the game's bank.

**Methods:**
- **`draw_sell_or_mortgage_choice_popup()`**  
  Renders the initial popup for choosing to sell or mortgage.
- **`sell_or_mortgage_choice_handle_events(event)`**  
  Processes the player's choice between selling and mortgaging.
- **`draw_select_property_popup(player, sell, mortgage)`**  
  Renders the property selection interface based on first choice.
- **`select_property_handle_events(event, player)`**  
  Processes property selection events.
- **`draw_sell_or_mortgage_popup()`**  
  Renders details about the selected property and confirmation button.
- **`handle_sell_or_mortgage_property_events(event)`**  
  Processes the confirmation of sale/mortgage.
- **`show(player, bank)`**  
  Manages the complete flow of selling or mortgaging.
- **`draw_button(screen, button_rect, text, hover, color)`**  
  Helper method to draw interactive buttons.

---

### UpgradePropertyPopup
**Description:**  
Interface for upgrading properties with houses and hotels.

**Attributes:**
- **`player: Player`**  
  The player upgrading property.
- **`eligible_properties: List[Property]`**  
  Properties eligible for upgrades.
- **`selected_property: Optional[Property]`**  
  Property currently selected for upgrade.

**Methods:**
- **`draw_select_property_popup(player)`**  
  Renders the property selection interface.
- **`draw_upgrade_popup()`**  
  Renders the upgrade interface for the selected property.
- **`handle_upgrade_property_events(event)`**  
  Processes upgrade/downgrade actions.
- **`select_property_handle_events(event, player)`**  
  Processes property selection events.
- **`show(player, bank)`**  
  Displays the upgrade interface and manages the upgrade process.
- **`draw_button(screen, button_rect, text, hover, color)`**  
  Helper method to draw interactive buttons.

---

## Helper Utilities

### BoardTextUtils
**Description:**  
Utilities for rendering text on the game board.

**Methods:**
- **`render_text_for_space(screen, space, space_index, text, font_size, color)`**  
  Renders text on a board space with proper positioning and wrapping.
- **`wrap_text(text, font, max_width)`**  
  Wraps text to fit within a specified width.
- **`calculate_text_position(space, space_index, text_surface)`**  
  Calculates the optimal position for text on a board space.

---

### SpaceData
**Description:**  
Contains configuration data for board spaces.

**Constants:**
- **`BOARD_CONFIG`**  
  Board layout parameters like dimensions and spacing.
- **`SPACE_NAMES`**  
  Names of all board spaces.
- **`SPACE_PROPERTY_GROUPS`**  
  Property group for each board space.
- **`PROPERTY_COLORS`**  
  Colour codes for each property group.
- **`SPACE_COLORS`**  
  Colours for different types of board spaces.

---

## Art Assets
The frontend includes various graphical assets used to enhance the visual presentation of the game:

- Player tokens
- Dice faces
- Background images
- Property cards
- UI elements and buttons

These assets are stored in the `art_assets` directory.

--- 