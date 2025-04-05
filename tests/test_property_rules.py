from pickle import TRUE
import unittest
import sys
import os

# # # Add the backend directory to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../src/')))

from backend.admin import Admin
from backend.ownables.property import Property
from backend.enums.property_group import PropertyGroup


class TestPropertyPurchaseRestriction(unittest.TestCase):

    def setUp(self):
        """Set up test environment with a player, bank, and property."""
        self.admin = Admin(['Will'], 0)
        self.bank = self.admin.get_bank()
        self.property = Property(name="The Old Creek", cost=60, property_group=PropertyGroup.BROWN, owner=self.bank)
        self.player = self.admin.get_players()[0]
        self.player.is_first_circuit_complete = False  # Player has not completed the first circuit

    def test_player_cannot_purchase_before_first_circuit(self):
        """Ensure a player cannot buy property before completing the first circuit."""
        player_purchase = self.player.purchase_property(self.property, self.bank)
        self.assertFalse(player_purchase, "Player should not be able to purchase property before completing the first circuit.")

    def test_player_can_purchase_after_first_circuit(self):
        """Ensure a player can buy property after completing the first circuit."""
        self.player.is_first_circuit_complete = True  # Player now completed the first circuit

        # Attempt to purchase property
        player_purchase = self.player.purchase_property(self.property, self.bank)
        self.assertTrue(player_purchase, "Player should be able to purchase property after completing first circuit.")


if __name__ == "__main__":
    unittest.main()
