from typing import Tuple
from .backend.admin import Admin
from .backend.property_owners.player import Player
from .backend.enums.game_token import GameToken
from .backend.non_ownables.jail import Jail
from .backend.non_ownables.free_parking import FreeParking
from .backend.non_ownables.go import Go
from .backend.property_owners.bank import Bank
from .backend.non_ownables.game_card import GameCard
from .backend.ownables.ownable import Ownable
from .backend.ownables.property import Property
from .backend.enums.property_group import PropertyGroup
from .backend import errors
import time

# TEMP FUNCTION TO GET PLAYER INPUT
def get_player_input(prompt: str) -> str:
    res = input(prompt)
    if res == "y":
        return True
    elif res == "n":
        return False

# TODO: MUST ENSURE PLAYER OWNS PROPERTY BEFORE CALLING THIS FUNCTION
# Facilitate selling or mortgaging a property. 
def raise_capital(player: Player,
                bank: Bank, 
                property: Ownable,
                is_mortgaging_property: bool = False, 
                is_selling_property: bool = False,
                is_selling_house_or_hotel: bool = False) -> None:
    if is_mortgaging_property:
        player.mortgage_property(property, bank)
    elif is_selling_property:
        player.sell_property(property, bank)
    elif is_selling_house_or_hotel:
        if property.get_hotel():
            property.sell_hotel(bank)
        else:
            try:
                property.sell_house(bank)
            except errors.MaxDifferenceBetweenHousesOrHotelsError:
                print(f"Cannot sell house because max difference between number of houses owned on a property within a property group is 1")
    else:
        return
    
# Function to handle selling/mortgaging properties to raise funds for a specific action
def handle_insufficient_funds(current_player: Player, 
                            bank: Bank, 
                            action_description: str) -> bool:
    print(f"\n{current_player.get_name()} does not have enough funds for {action_description}\n")
    
    # TODO: front end needs to ask which property to sell/mortgage. MUST ONLY SHOW PROPERTIES THAT CAN BE SOLD/MORTGAGED. E.G. PROPERTIES THAT HAVE NO HOUSES/HOTELS ON THEM.
    property_to_use: Ownable = show_player_properties(current_player) # returns a tuple of (property, action_type), if action_type is then sell
    
    if property_to_use[0] == 0:
        raise_capital(current_player, bank, property_to_use, is_selling=True)
        print(f"{current_player.get_name()} sold a property and will try again")
        return True
    elif property_to_use[0] == 1:
        raise_capital(current_player, bank, property_to_use, is_mortgaging=True)
        print(f"{current_player.get_name()} mortgaged a property and will try again")
        return True
    elif property_to_use[0] == 2:
        raise_capital(current_player, bank, property_to_use, is_selling_house_or_hotel=True)
        print(f"{current_player.get_name()} sold a house or hotel and will try again")
        return True
    else:
        # Player doesn't want to sell or mortgage
        print(f"{current_player.get_name()} decided not to raise additional funds")
        return False
    
# temp function to show player what properties, house or hotel they can sell
def show_player_properties(player: Player) -> Tuple[Ownable, int]:
    props_to_sell = []
    props_to_downgrade = []
    for properties_in_group in player.get_owned_properties().values():
        for property in properties_in_group:
            if property.get_houses() > 0 or property.get_hotel() == 1:
                idx = len(props_to_downgrade)
                props_to_downgrade.append((idx, property))
            else:
                idx = len(props_to_sell)
                props_to_sell.append((idx, property))
    print(f"{player.get_name()} has the following properties, houses or hotels they can sell/mortgage:")
    for property in props_to_sell:
        print(f"{property[0]}: {property[1].get_name()} (cost: £{property[1].get_value()})")
    print(f"{player.get_name()} has the following properties they can downgrade:")
    for property in props_to_downgrade:
        print(f"{property[0]}: {property[1].get_name()} (cost: £)")
        
    print('Reply with "y" to only one of the following 3 questions...')
    wants_to_sell_property: bool = get_player_input("Do you want to sell a property? (y/n): ")
    wants_to_mortgage_property: bool = get_player_input("Do you want to mortgage a property? (y/n): ")
    wants_to_sell_house_or_hotel: bool = get_player_input("Do you want to sell a house or hotel? (y/n): ")
    
    if wants_to_sell_property:
        sell_choice = input('reply with the index of the property you want to sell or "n" if you don\'t want to sell any properties: ')
        if sell_choice == "n":
            return None
        else:
            return (0, props_to_sell[int(sell_choice)][1])
    elif wants_to_mortgage_property:
        sell_choice = input('reply with the index of the property you want to mortgage or "n" if you don\'t want to mortgage any properties: ')
        if sell_choice == "n":
            return None
        else:
            return (1, props_to_sell[int(sell_choice)][1])
    elif wants_to_sell_house_or_hotel:
        sell_choice = input('reply with the index of the property you want to downgrade or "n" if you don\'t want to downgrade any properties: ')
        if sell_choice == "n":
            return None
        else:
            return (2, props_to_downgrade[int(sell_choice)][1])
    else:
        return None
        
        
    
# Frontend must pass names and tokens for each player
player_names: list[(str, GameToken)] = [("Player 1", GameToken.BOOT),
                                        ("Player 2", GameToken.CAT),
                                        ("Player 3", GameToken.HATSTAND),
                                        ("Player 4", GameToken.IRON),
                                        ("Player 5", GameToken.SHIP)]

# TODO: get time limit from frontend
time_limit = int(input("Enter time limit for game (in minutes)(enter 0 for no time limit): "))

admin: Admin = Admin(player_names, time_limit)

players = [player for player in admin.get_players() if not player.get_is_bankrupt()]
bank: Bank = admin.get_bank()
game_board: list[Ownable | FreeParking | Jail | Go | GameCard] = admin.get_game_board()
game_space_helper: dict[Ownable | FreeParking | Jail | Go | GameCard, int] = admin.get_game_space_helper()
time_limit: int = admin.get_time_limit()
free_parking: FreeParking = admin.get_free_parking()
go: Go = admin.get_go()
jail: Jail = admin.get_jail() 
pot_luck_cards: GameCard = admin.get_pot_luck_cards()
opportunity_knocks: GameCard = admin.get_opportunity_knocks()


# TODO: frontend needs to display time limit somewhere?
if time_limit > 0:
    admin.start_timer()


# TODO: frontend needs to display current player somewhere

# Main game loop
while True:
###################################################
# Section: check if game is over
###################################################
    if len(players) <= 0:
        if admin.get_is_time_limit_reached():
            break
        else:
            print("\n\n----------NEXT ROUND----------\n\n")
            players = [player for player in admin.get_players() if not player.get_is_bankrupt()]
            if len(players) == 0:
                break
    
    # Get current player
    current_player = players[0]
    print("\nNEXT PLAYER IN ROUND\n")
    print(f"Current player: {current_player.name}")
    print(f"Current player's cash balance: {current_player.get_cash_balance()}\n")
    
###################################################
# Section: is current player in jail?
###################################################
    if current_player.get_is_in_jail():
        if current_player.get_rounds_in_jail() == 2:
            jail.release_from_jail(current_player)           
        elif current_player.get_get_out_of_jail_cards() > 0:
            # front end needs to ask if player wants to use an out of jail card
            use_get_out_of_jail_card: bool = get_player_input("Do you want to use an out of jail card? (y/n): ") # TODO: get from frontend 
            if use_get_out_of_jail_card:
                current_player.use_get_out_of_jail(jail)
        else:
            # TODO: front end needs to ask if player wants to pay $50 fine
            pay_fine: bool = get_player_input("Do you want to pay the fine to get out of jail? (y/n): ") # TODO: get from frontend        
            if pay_fine:
                print(f"{current_player.get_name()} chooses to pay the fine to get out of jail")
            # Try to pay jail fine, loop until successful or player chooses to stay in jail
                pay_fine_loop_flag = False
                while not pay_fine_loop_flag:
                    try:
                        jail.pay_fine_for_release(current_player, free_parking)
                        pay_fine_loop_flag = True
                        print(f"{current_player.get_name()} has paid the fine and is released from jail")
                    except errors.InsufficientFundsError:
                        if not handle_insufficient_funds(current_player, bank, "paying the jail fine"):
                            # Player can't pay fine and doesn't want to sell or mortgage a property
                            print(f"{current_player.get_name()} stays in jail")
                            current_player.set_rounds_in_jail(current_player.get_rounds_in_jail() + 1)
                            pay_fine_loop_flag = True  # Exit the loop
                            players.pop(0)
                            continue
            else:
                # Player stays in jail
                print(f"{current_player.get_name()} stays in jail")
                current_player.set_rounds_in_jail(current_player.get_rounds_in_jail() + 1)
                players.pop(0)
                continue
    
    
    
###################################################
# Section: Roll dice
###################################################
    move_result: list[list[int], int] | None = current_player.move_player() # return list of dice rolls and new position or None if player rolled 3 doubles
    if move_result is None:
        # Player rolls three doubles and goes to jail
        jail.put_in_jail(current_player)
        players.pop(0)
        continue
    
    dice_rolls, new_position = move_result
    print(f"{current_player.get_name()} rolled a {dice_rolls[0]} and a {dice_rolls[1]} and moved to {new_position}")
    
    space_on_board: Ownable | FreeParking | Jail | Go | GameCard = game_board[new_position]
    
    # Check if passed go (potentially move to backend logic?)
    if current_player.get_has_passed_go_flag():
        go.pay_player(current_player, bank)
        current_player.reset_has_passed_go_flag()
        print(f"{current_player.get_name()} passed go and collected £200!")
    
###################################################
# Section: Land on space and handle logic
###################################################
    match space_on_board:
        case Ownable():
            print(f"{current_player.get_name()} landed on {space_on_board.name}, which is an ownable property.")
            if space_on_board.get_owner() == current_player:
                print(f"{current_player.get_name()} landed on their own property, {space_on_board.name}. No action required.")
                continue
            elif space_on_board.get_owner() == bank:
                print(f"{current_player.get_name()} landed on a property that is owned by the bank, {space_on_board.name}. Offer to purchase the property.")
                
                if not current_player.get_is_first_circuit_complete():
                    print(f"{current_player.get_name()} is on the first circuit. They cannot make purchases until they have completed the first circuit.")
                    players.pop(0)
                    continue
                # TODO: front end needs to ask if player wants to buy the property
                wants_to_buy_property: bool = get_player_input("Do you want to buy this property? (y/n): ")
                if wants_to_buy_property:
                    # flag to check if purchase was successful or player decided to not purchase the property
                    property_purchase_loop_flag = False
                    while not property_purchase_loop_flag:
                        try:
                            current_player.purchase_property(space_on_board, bank)
                            property_purchase_loop_flag = True
                            print(f"{current_player.get_name()} purchased {space_on_board.name} for £{space_on_board.get_cost()}")
                        except errors.InsufficientFundsError:
                            if not handle_insufficient_funds(current_player, bank, f"purchasing {space_on_board.name}"):
                                # Player doesn't want to sell or mortgage, so they don't purchase
                                print(f"{current_player.get_name()} decided not to purchase {space_on_board.name}")
                                property_purchase_loop_flag = True  # Exit the loop
                else:
                    # AUCTION LOGIC HERE
                    None
            # Player landed on an ownable property that is owned by another player
            else:
                other_players = [player for player in admin.get_players() if player != current_player]
                for player in other_players:
                    if space_on_board.get_owner() == player:
                        print(f"{current_player.get_name()} landed on {space_on_board.name} and is being charged rent to {player.get_name()}")
                        pay_rent_loop_flag = False
                        current_player.cash_balance = 0
                        while not pay_rent_loop_flag:
                            try:
                                space_on_board.get_rent_due_from_player(current_player)
                                pay_rent_loop_flag = True
                            except errors.InsufficientFundsError:
                                if not handle_insufficient_funds(current_player, bank, f"paying rent to {player.get_name()}"):
                                    # Player can't sell or mortgage, so they are declared bankrupt
                                    print(f"{current_player.get_name()} is unable to pay rent and is therefore bankrupt")
                                    current_player.set_is_bankrupt(True)
                                    players.pop(0)
                                    continue
                        break
                else:
                    print(f"{current_player.get_name()} landed on {space_on_board.name} and is not being charged rent")
                    
        case FreeParking():
            print(f"{current_player.get_name()} landed on Free Parking. All previous fines that have been collected are now being paid out to the player.")
            free_parking.payout_fines(current_player)
            # Additional logic for Free Parking can be added here
        case Jail():
            print(f"{current_player.get_name()} is just visiting Jail.")
        case Go():
            print(f"{current_player.get_name()} landed on Go and collects $200!")
        case GameCard():
            print(f"{current_player.get_name()} landed on a Game Card space. Drawing a card...")
            pot_luck_card_positions = [0, 17, 33]
            opportunity_knocks_card_positions = [7, 22, 36]
            other_players = [player for player in admin.get_players() if player != current_player]
            if game_space_helper[space_on_board] in pot_luck_card_positions:
                card_info = pot_luck_cards.get_card()
                print(f'{current_player.get_name()} drew a pot luck card: {card_info[0]}')
                pot_luck_card_loop_flag = False
                while not pot_luck_card_loop_flag:
                    try:
                        pot_luck_cards.process_card(player=current_player, 
                                                bank=bank, 
                                                card_id=card_info[1], 
                                                free_parking=free_parking, 
                                                jail=jail, 
                                                other_players=other_players)
                        pot_luck_card_loop_flag = True
                    except errors.InsufficientFundsError:
                        if not handle_insufficient_funds(current_player, bank, f"paying rent to {player.get_name()}"):
                            # Player can't sell or mortgage, so they are declared bankrupt
                            print(f"{current_player.get_name()} is unable to pay rent and is therefore bankrupt")
                            current_player.set_is_bankrupt(True)
                            players.pop(0)
                            continue
            elif game_space_helper[space_on_board] in opportunity_knocks_card_positions:
                card_info = opportunity_knocks.get_card()
                print(f"{current_player.get_name()} drew an opportunity knocks card: {card_info[0]}")
                opportunity_knocks_card_loop_flag = False
                while not opportunity_knocks_card_loop_flag:
                    try:
                        opportunity_knocks.process_card(player=current_player, 
                                                    bank=bank, 
                                                    card_id=card_info[1], 
                                                    free_parking=free_parking, 
                                                    jail=jail, 
                                                    other_players=other_players)
                        opportunity_knocks_card_loop_flag = True
                    except errors.InsufficientFundsError:
                        if not handle_insufficient_funds(current_player, bank, f"paying rent to {player.get_name()}"):
                            # Player can't sell or mortgage, so they are declared bankrupt
                            print(f"{current_player.get_name()} is unable to pay rent and is therefore bankrupt")
                            current_player.set_is_bankrupt(True)
                            players.pop(0)
                            continue
        case _:
            print(f"{current_player.get_name()} landed on an unknown space.")
    
###################################################
# Section: Offer player chance to upgrade property
###################################################
    #TODO: front end needs to show the player the properties eligible for upgrade
    properties_eligible_for_upgrade = []
    for prop_group, props in current_player.get_owned_properties().items():
        for prop in props:
            if type(prop) == Property:
                if prop.get_is_eligible_for_upgrade():
                    properties_eligible_for_upgrade.append(prop)
    if len(properties_eligible_for_upgrade) > 0:
        upgrade_loop_flag = False
        while not upgrade_loop_flag:
            print(f"{current_player.get_name()} has the following properties eligible for upgrade:")
            
            prop_with_index = []
            for index, prop in enumerate(properties_eligible_for_upgrade):
                prop_with_index.append((index, prop))
                print(f"{index}: {prop.get_name()}")
            
            if len(properties_eligible_for_upgrade) == 0:
                #TODO: front end needs to tell player that they have no properties eligible for upgrade
                print(f"\n{current_player.get_name()} has no properties eligible for upgrade")
                upgrade_loop_flag = False
            else:
                #TODO: front end needs to ask player if they want to upgrade
                upgrade_choice = input("Would you like to upgrade any of your properties? (reply with the index of the property you want to upgrade or 'n' if you don't want to upgrade any properties): ")
                if int(upgrade_choice) in range(len(properties_eligible_for_upgrade)):
                    upgrade_loop_flag = False
                    while not upgrade_loop_flag:
                        try:
                            prop_to_upgrade = prop_with_index[int(upgrade_choice)][1]
                            prop_to_upgrade.upgrade_property()
                            upgrade_loop_flag = True
                            break
                        except errors.InsufficientFundsError:
                            if not handle_insufficient_funds(current_player, bank, f"upgrading {prop_to_upgrade.get_name()}"):
                                # Player can't sell or mortgage, so they are declared bankrupt
                                print(f"{current_player.get_name()} is unable to upgrade {prop_to_upgrade.get_name()} due to insufficient funds")
                                break
                        
                elif upgrade_choice == "n":
                    upgrade_loop_flag = False
                else:
                    print("Invalid input. Please enter 'y' or 'n'.")
                    
    # TODO: check if player rolled a double and should roll again
    if current_player.get_doubles_rolled() > 0:
        continue
    else:
        players.pop(0)
            
    
# Establish winner
winner = players[0]
for player in admin.get_players():
    if player.get_player_net_worth() > winner.get_player_net_worth():
        winner = player

print(f"{winner.get_name()} is the winner of the game!")# Start timer if time limit is passed



                

            
            





