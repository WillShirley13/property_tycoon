from .admin import Admin
from .property_owners.player import Player
from .enums.game_token import GameToken
from .non_ownables.jail import Jail
from .non_ownables.free_parking import FreeParking
from .non_ownables.go import Go
from .property_owners.bank import Bank
from .non_ownables.game_card import GameCard
from .ownables.ownable import Ownable
from . import errors
import time

# TEMP FUNCTION TO GET PLAYER INPUT
def get_player_input(prompt: str) -> str:
    res = input(prompt)
    if res == "y":
        return True
    elif res == "n":
        return False
    
    
    
# Frontend must pass names and tokens for each player
player_names: list[(str, GameToken)] = [("Player 1", GameToken.BOOT), ("Player 2", GameToken.CAT), ("Player 3", GameToken.HATSTAND), ("Player 4", GameToken.IRON), ("Player 5", GameToken.SHIP)]

# TODO: get time limit from frontend
time_limit = int(input("Enter time limit for game (in minutes)(enter 0 for no time limit): "))

admin: Admin = Admin(player_names, time_limit)

players: list[Player] = admin.get_players()
bank: Bank = admin.get_bank()
game_board: list[Ownable | FreeParking | Jail | Go | GameCard] = admin.get_game_board()
game_space_helper: dict[Ownable | FreeParking | Jail | Go | GameCard, int] = admin.get_game_space_helper()
time_limit: int = admin.get_time_limit()
free_parking: FreeParking = admin.get_free_parking()
go: Go = admin.get_go()
jail: Jail = admin.get_jail() 
player_1, player_2, player_3, player_4, player_5 = players
# Start timer if time limit is passed
# TODO: frontend needs to display time limit somewhere?
if time_limit > 0:
    admin.start_timer()


# TODO: frontend needs to display current player somewhere

# Main game loop
while True:
    if len(players) <= 0:
        if admin.is_game_over():
            break
        else:
            print("\n\n----------NEXT ROUND----------\n\n")
            players = [player_1, player_2, player_3, player_4, player_5]
    
    # Get current player
    current_player = players[0]
    print("\nNEXT PLAYER IN ROUND\n")
    print(f"Current player: {current_player.name}")
    
    # is current player in jail?
    if current_player.is_in_jail:
        if current_player.rounds_in_jail == 2:
            jail.release_from_jail(current_player)           
        elif current_player.get_get_out_of_jail_cards() > 0:
            # front end needs to ask if player wants to use an out of jail card
            use_get_out_of_jail_card: bool = get_player_input("Do you want to use an out of jail card? (y/n): ") # TODO: get from frontend 
            if use_get_out_of_jail_card:
                current_player.use_get_out_of_jail()
        else:
            # TODO: front end needs to ask if player wants to pay $50 fine
            pay_fine: bool = get_player_input("Do you want to pay the fine to get out of jail? (y/n): ") # TODO: get from frontend        
            if pay_fine:
                print(f"{current_player.name} chooses to pay the fine to get out of jail")
                try:
                    jail.pay_fine_for_release(current_player)
                except errors.InsufficientFundsError:
                    print(f"{current_player.name} does not have enough funds to pay the fine")
                    # TODO: front end needs to ask if player wants to sell a property or mortgage a property. If neither, player stays in jail.
                    wants_to_sell_property: bool = get_player_input("Do you want to sell a property? (y/n): ") # TODO: get from frontend
                    want_to_mortgage_property: bool = get_player_input("Do you want to mortgage a property? (y/n): ") # TODO: get from frontend
                    if wants_to_sell_property:
                        # TODO: front end needs to ask whibch property to sell
                        property_to_sell: Ownable = None #TODO: get from frontend
                        current_player.sell_property(property_to_sell, bank)
                    elif want_to_mortgage_property:
                        # TODO: front end needs to ask which property to mortgage
                        property_to_mortgage: Ownable = None #TODO: get from frontend
                        current_player.mortgage_property(property_to_mortgage, bank)
                    else:
                        # player can't pay fine and doesn't want to sell or mortgage a property, so they stay in jail
                        print(f"{current_player.name} stays in jail")
                        current_player.set_rounds_in_jail(current_player.rounds_in_jail + 1)
                        players.pop(0)
                        continue
            else:
                # Player stays in jail
                print(f"{current_player.name} stays in jail")
                current_player.set_rounds_in_jail(current_player.rounds_in_jail + 1)
                players.pop(0)
                continue
    
    # Roll dice
    move_result: list[list[int], int] | None = current_player.move_player() # return list of dice rolls and new position or None if player rolled 3 doubles
    if move_result is None:
        # Player rolls three doubles and goes to jail
        jail.put_in_jail(current_player)
        players.pop(0)
        continue
    
    dice_rolls, new_position = move_result
    print(f"{current_player.name} rolled a {dice_rolls[0]} and a {dice_rolls[1]} and moved to {new_position}")
    
    # Check if player rolled doubles as they roll again if they have. Checks for 3 doubles in a row performed on backend.
    double_roll_flag: bool = current_player.get_doubles_rolled() != 0
    
    
    space_on_board: Ownable | FreeParking | Jail | Go | GameCard = game_board[new_position]
    
    # Check if passed go
    if current_player.get_has_passed_go():
        go.pay_player(current_player, bank)
        current_player.reset_has_passed_go()
        print(f"{current_player.name} passed go and collected £200!")
    
    match space_on_board:
        case Ownable():
            print(f"{current_player.name} landed on {space_on_board.name}, which is an ownable property.")
            if space_on_board.get_owner() == current_player:
                print(f"{current_player.name} landed on their own property, {space_on_board.name}.")
                break
            elif space_on_board.get_owner() == bank:
                print(f"{current_player.name} landed on a property that is owned by the bank, {space_on_board.name}.")
                # TODO: front end needs to ask if player wants to buy the property
                wants_to_buy_property: bool = get_player_input("Do you want to buy this property? (y/n): ") # TODO: get from frontend
                if wants_to_buy_property:
                    current_player.purchase_property(space_on_board, bank)
            # Additional logic for landing on an ownable property can be added here
        case FreeParking():
            print(f"{current_player.name} landed on Free Parking. No action required.")
            # Additional logic for Free Parking can be added here
        case Jail():
            print(f"{current_player.name} landed in Jail. They must stay in jail.")
            # Additional logic for landing in Jail can be added here
        case Go():
            print(f"{current_player.name} landed on Go and collects $200!")
            current_player.add_cash_balance(200)
        case GameCard():
            print(f"{current_player.name} landed on a Game Card space. Drawing a card...")
            # Logic for drawing a game card can be added here
        case _:
            print(f"{current_player.name} landed on an unknown space.")
        
    input("Press Enter to continue...")
    players.pop(0)
                

            
            





