import pytest
import unittest
import sys
import os

# # Add the backend directory to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))

from src.backend.property_owners.bank import Bank
from src.backend.enums.game_token import GameToken
from src.backend.property_owners.player import Player
from src.backend.non_ownables.go import Go


class TestGame(unittest.TestCase):
    
    def setUp(self):
        #Set up a Player instance for testing.
        self.player = Player(GameToken.BOOT, "Will")
        self.player1 = Player(GameToken.CAT, "Nathan")
        self.player2 = Player(GameToken.CAT, "Nathan")
        self.bank = Bank()
        self.go = Go()

    def test_players_have_different_tokens(self):
        """Test that the players have different tokens despite the same name."""
        self.assertNotEqual(self.player1.get_game_token(), self.player2.get_game_token(), "Players should have different game tokens.")
    
    def test_players_have_same_name(self):
        """Test that two players with the same name are allowed."""
        self.assertEqual(self.player1.get_name(), self.player2.get_name(), "Players should not have the same name.")

    def test_player_receives_200_when_passing_go(self):
        """Test that the player gets £200 when passing GO."""
        initial_player_balance = self.player.get_cash_balance()
        initial_bank_balance = self.bank.get_cash_balance()

        self.go.pay_player(self.player, self.bank)

        self.assertEqual(self.player.get_cash_balance(), initial_player_balance + 200, 
                         "Player should receive £200 when passing GO.")
        self.assertEqual(self.bank.get_cash_balance(), initial_bank_balance - 200, 
                         "Bank should deduct £200 when player passes GO.")
        
        print(f"Player balance is {self.player.get_cash_balance()}") 
        """Tests that the players balance is 1700 after getting the GO money"""

            
if __name__ == '__main__':
    unittest.main()