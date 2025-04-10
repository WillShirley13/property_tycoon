import pytest
import unittest
import sys
import os

# Add the backend directory to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))

from src.backend.property_owners.property_holder import PropertyHolder
from src.backend.property_owners.bank import Bank
from src.backend.enums.game_token import GameToken
from src.backend.property_owners.player import Player
from src.backend.ownables.property import Property
from src.backend.enums.property_group import PropertyGroup
from src.backend import errors
from src.backend.constants import PROPERTY_DATA



class TestGame(unittest.TestCase):
    def setUp(self):
        """Set up instances for testing."""
        self.bank = Bank()  # Create bank instance with default 50,000 cash balance
        self.player = Player(GameToken.BOOT, "Test Player")  # Create a player
        self.other_player = Player(GameToken.CAT, "Opponent")  # Create another player
        self.player.sub_cash_balance(400) #Player starts with 1100
        self.player.is_bankrupt = False

        # Mock a property that the opponent owns
        self.property = Property(name="Ibis Close", cost=320, property_group=PropertyGroup.GREEN, owner=self.bank)
        self.property.set_owner(self.other_player)  # Set property owner to the opponent
        self.property.set_owner_owns_all_properties_in_group(True)
        self.property.set_houses(4)  # Set 4 houses to get the rent higher
        self.property.set_rent_cost() #Sets the cost of the rent
        
        
        # Add the property to the player's portfolio before selling it
        self.mock_property_to_sell = Property(name="The Old Creek", cost=60, property_group=PropertyGroup.BROWN, owner=self.player)
        
        # Add property to player's portfolio
        self.player.add_property_to_portfolio(self.mock_property_to_sell )
        print(f"Player's starting cash balance: {self.player.get_cash_balance()}")
        # Get the rent cost of the property owned by the other player
        other_player_rent_cost = self.property.get_rent_cost()

        print(f"The rent cost for the property owned by the other player is: {other_player_rent_cost}")
        


    # def test_player_sells_assets_if_unable_to_pay_rent(self):
    #     """Test that the player sells assets to pay rent when they do not have enough cash."""
    #     other_player_rent_cost = self.property.get_rent_cost()

    #     # The player does not have enough cash to cover the rent
    #     #self.assertTrue(self.player.get_cash_balance() < other_player_rent_cost, "Player should not have enough cash to pay rent.")
       
    #     # The player needs to sell properties to cover the rent
    #     if self.player.get_cash_balance() < other_player_rent_cost and not self.player.get_is_bankrupt():
    #         # Sell properties to raise cash
    #         for group in self.player.owned_properties:
    #             for owned_property in self.player.owned_properties[group]:
    #                 self.player.sell_property(owned_property, self.bank)
    #                 if self.player.get_cash_balance() >= other_player_rent_cost:
    #                    break

    #     print(f"Player's cash balance after selling: {self.player.get_cash_balance()}")               
    #     # The player's bankruptcy status should be false if they could sell enough assets
    #     self.assertFalse(self.player.get_is_bankrupt(), "Player should not go bankrupt after selling assets to pay rent.")

    #     # Check if the property was successfully sold, so it is no longer in players possession
    #     # self.assertNotIn(self.mock_property_to_sell, self.player.owned_properties[PropertyGroup.BROWN], "Player should no longer own the sold property.")

    #     # If player cannot pay rent even after selling all assets, declare bankruptcy
    #     if self.player.get_cash_balance() < other_player_rent_cost:
    #         self.player.set_is_bankrupt()
    #         self.assertTrue(self.player.get_is_bankrupt(), "Player should be bankrupt after selling all assets and still unable to pay rent.")

    def test_player_is_removed_when_bankrupt(self):
        """Test that a bankrupt player and their token are removed from the game display."""

        # Simulate game state before bankruptcy
        self.players_objects = [(self.player, "boot_token.png"), (self.other_player, "cat_token.png")]
        
        # Ensure both players are initially in the game
        self.assertEqual(len(self.players_objects), 2, "There should be two players at the start.")

        # Simulate the player becoming bankrupt
        self.player.set_is_bankrupt()

        # Update player data for display (this mimics the actual game logic)
        self.player_data = []
        for player, _ in self.players_objects:
            if not player.get_is_bankrupt():
                self.player_data.append((player.get_name(), player.get_game_token()))
            else:
                self.player_data.append((f"{player.get_name()} (Bankrupt)", player.get_game_token()))

        # Ensure the player's name is updated to show "Bankrupt"
        expected_name = f"{self.player.get_name()} (Bankrupt)"
        self.assertIn((expected_name, self.player.get_game_token()), self.player_data, "Bankrupt player's name should be updated.")

        # Simulate the game logic that removes bankrupt players from the active list
        players_objects = [player for player, _ in self.players_objects if not player.get_is_bankrupt()]

        # Ensure the bankrupt player is removed from active players
        self.assertNotIn(self.player, players_objects, "Bankrupt player should be removed from active players list.")

        # Ensure only the remaining player is still active
        self.assertEqual(len(players_objects), 1, "Only one player should remain after bankruptcy.")

        # Ensure the correct player remains in the game
        self.assertEqual(players_objects[0], self.other_player, "Opponent should be the only remaining player.")


if __name__ == '__main__':
    unittest.main()
