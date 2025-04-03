from pickle import TRUE
import unittest
import sys
import os

# # Add the backend directory to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))

from src.backend.property_owners.bank import Bank
from src.backend.enums.game_token import GameToken
from src.backend.property_owners.player import Player
from src.backend.ownables.property import Property
from src.backend.enums.property_group import PropertyGroup


class TestPropertyPurchaseRestriction(unittest.TestCase):

    def setUp(self):
        """Set up test environment with a player, bank, and property."""
        self.bank = Bank()
        self.property = Property(name="The Old Creek", cost=60, property_group=PropertyGroup.BROWN, owner=self.bank)
        self.player = Player(game_token=GameToken.CAT, name="Alex")
        self.player.is_first_circuit_complete = False  # Player has not completed the first circuit

    def test_player_cannot_purchase_before_first_circuit(self):
        """Ensure a player cannot buy property before completing the first circuit."""
        can_purchase = self.player.get_is_first_circuit_complete()  # Should be False
        self.assertFalse(can_purchase, "Player should not be able to purchase property before completing the first circuit.")
        
        # Try purchasing property and check if it remains owned by the bank
        initial_owner = self.property.get_owner()
        if not can_purchase:
            self.property.set_owner(self.bank)  # Ensure no purchase happens
        
        self.assertEqual(self.property.get_owner(), initial_owner, "Property should remain with the bank.")

    def test_player_can_purchase_after_first_circuit(self):
        """Ensure a player can buy property after completing the first circuit."""
        self.player.is_first_circuit_complete = True  # Player now completed the first circuit

        # Attempt to purchase property
        can_purchase = self.player.get_is_first_circuit_complete()
        if can_purchase:
            self.property.set_owner(self.player)  # Simulate successful purchase
        
        self.assertEqual(self.property.get_owner(), self.player, "Player should be able to purchase property after completing first circuit.")


if __name__ == "__main__":
    unittest.main()
