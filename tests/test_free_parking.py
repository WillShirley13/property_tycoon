import unittest
import sys
import os

# # Add the backend directory to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))

from src.backend.non_ownables.free_parking import FreeParking
from src.backend.property_owners.player import Player
from src.backend.enums.game_token import GameToken
from src.backend import errors


class TestFreeParking(unittest.TestCase):

    def setUp(self):
        """Set up FreeParking and a test player before each test."""
        self.free_parking = FreeParking()
        self.player = Player(GameToken.BOOT, "Test Player")
        self.player.add_cash_balance(500)  # Give player some initial money, player now has 2000.

    def test_payout_fines(self):
        """Test if fines are correctly paid out to a player."""
        self.free_parking.add_fine(50, self.player)
        self.free_parking.add_fine(30, self.player)

        initial_balance = self.player.get_cash_balance() 
        self.free_parking.payout_fines(self.player) #Balance is at 1920 after the fine of 80 has been taken
        
        self.assertEqual(self.player.get_cash_balance(), initial_balance + 80, "Player should receive 80 in fines payout.")
        self.assertEqual(self.free_parking.get_fines_collected(), 0, "Fines collected should reset to 0 after payout.")

    def test_add_fine(self):
        """Test if fines are correctly added to FreeParking."""
        self.free_parking.add_fine(50, self.player)
        self.assertEqual(self.free_parking.get_fines_collected(), 50, "Fines collected should be 50.")

    def test_multiple_fines_accumulate(self):
        """Test if multiple fines accumulate correctly in FreeParking."""
        self.free_parking.add_fine(50, self.player)
        self.free_parking.add_fine(30, self.player)
        self.assertEqual(self.free_parking.get_fines_collected(), 80, "Total fines collected should be 80.")

if __name__ == "__main__":
    unittest.main()


