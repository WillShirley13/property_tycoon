import pytest
import unittest
import sys
import os

# # Add the backend directory to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))

from src.backend.property_owners.property_holder import PropertyHolder
from src.backend.property_owners.bank import Bank
from src.backend.enums.game_token import GameToken
from src.backend.property_owners.player import Player

class TestGame(unittest.TestCase):

    # Test if the initial cash is 1500
    def test_get_cash_balance(self):
        player = PropertyHolder(initial_cash=1500)  # Create an instance with 1500 cash
        assert player.get_cash_balance() == 1500, "get_cash_balance() should return 1500"

    # Test if initial bank account is 50, 000
    def test_bank_starting_cash(self):
        bank = Bank()  # Create a Bank instance
        # Verify the bank's cash balance is 50,000
        assert bank.get_cash_balance() == 50000, f"Expected 50000, but got {bank.get_cash_balance()}"
    
    def setUp(self):
        #Set up a Player instance for testing.
        self.player = Player(GameToken.BOOT, "Test Player")
    
    
    def test_initially_not_bankrupt(self):
        #Test that a new player is not bankrupt by default.
        self.assertFalse(self.player.get_is_bankrupt(), "Player should not be bankrupt initially.")
    
    
    def test_set_is_bankrupt(self):
        #Test that setting the player as bankrupt updates the status correctly.
        self.player.set_is_bankrupt()
        self.assertTrue(self.player.get_is_bankrupt(), 
                        "Player should be bankrupt after calling set_is_bankrupt().")
   


           
if __name__ == '__main__':
    unittest.main()