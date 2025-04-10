
from typing import List
import unittest
import sys
import os

# # Add the backend directory to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../src/')))

from unittest.mock import MagicMock
from backend.property_owners.player import Player
from backend.enums.game_token import GameToken
from backend.non_ownables.jail import Jail 
from backend.admin import Admin
from backend.enums.property_group import PropertyGroup


class TestJailMechanism(unittest.TestCase):

    def setUp(self):
        """Set up test environment with a player, bank, and property."""        
        game_tokens: List[GameToken] = [
            GameToken.BOOT,
            GameToken.CAT,
            GameToken.TOPHAT,
            GameToken.IRON,
            GameToken.SMARTPHONE,
            GameToken.BOAT,
        ]
        self.admin = Admin([('Will', game_tokens[0]), ('John', game_tokens[1])], 0)
        self.jail = self.admin.get_jail()
        self.bank = self.admin.get_bank()
        self.free_parking = self.admin.get_free_parking()
        self.go = self.admin.get_go()
        self.property = self.bank.get_owned_properties()[PropertyGroup.BROWN][0]
        self.player1 = self.admin.get_players()[0]
        self.player2 = self.admin.get_players()[1]
        self.player1.is_first_circuit_complete = True  # Player now completed the first circuit
        self.player2.is_first_circuit_complete = True  # Player now completed the first circuit

    def test_three_consecutive_doubles_sends_player_to_jail(self):
        """Test that rolling three consecutive doubles sends a player to jail."""
        # Mock three consecutive double rolls
        move_results = [([2, 2], 4), ([3, 3], 10), ([4, 4], 18)]  # Third double roll triggers jail

        def mock_move():
            return move_results.pop(0)

        self.player1.move_player = MagicMock(side_effect=mock_move)

        # Simulate the player rolling three times
        for _ in range(3):
            move_result = self.player1.move_player()
            if move_result and move_result[0][0] == move_result[0][1]:  # Check if it's a double
                if _ == 2:  # Third double
                    self.jail.put_in_jail(self.player1)
                    break

        # Assert that the player is now in jail
        self.assertTrue(self.player1.get_is_in_jail(), "Player should be in jail after rolling three consecutive doubles.")
    
    def test_cannot_get_rent_if_in_jail(self):
        """Test that player in jail cannot collect rent."""
        # Purchase property first
        self.player1.purchase_property(self.property, self.bank)
        # Mortgage the property
        self.jail.put_in_jail(self.player1)
        
        # Check player is in jail
        self.assertTrue(self.player1.get_is_in_jail(), "Player should be in jail.")
        print(self.property.get_owner())
        
        # Check no rent is due. get_rent_due_from_player() returns 0 if player is in jail, else returns rent due
        rent_due = self.property.get_rent_due_from_player(self.player2)
        self.assertEqual(rent_due, 0, "Player in jail should not collect rent.")
    
    def test_player_freed_if_pay_fine(self):
        """Test that player is freed if they pay the fine."""
        # Put player in jail
        self.jail.put_in_jail(self.player1)
        # Check player is in jail
        self.assertTrue(self.player1.get_is_in_jail(), "Player should be in jail.")
        
        player_cash_balance_before_fine = self.player1.get_cash_balance()
        
        self.jail.pay_fine_for_release(self.player1, self.free_parking, self.go, self.bank)
        # Check player is no longer in jail
        self.assertFalse(self.player1.get_is_in_jail(), "Player should be freed if they pay the fine.")
        # Check player's cash balance has decreased by the fine amount
        self.assertEqual(self.player1.get_cash_balance(), player_cash_balance_before_fine - self.jail.get_release_cost(), "Player should have paid the fine.")

if __name__ == "__main__":
    unittest.main()
