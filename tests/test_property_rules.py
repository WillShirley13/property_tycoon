from pickle import TRUE
from typing import List
import unittest
import sys
import os

# # # Add the backend directory to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../src/')))

from backend.admin import Admin
from backend.ownables.property import Property
from backend.enums.property_group import PropertyGroup
from backend.enums.game_token import GameToken
from backend.property_owners.player import Player
from backend.property_owners.bank import Bank
from backend.ownables.property import Property
class TestPropertyPurchaseRestriction(unittest.TestCase):

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
        self.admin = Admin([('Will', game_tokens[0])], 0)
        self.bank = self.admin.get_bank()
        self.property = self.bank.get_owned_properties()[PropertyGroup.BROWN][0]
        self.player = self.admin.get_players()[0]
        self.player.is_first_circuit_complete = True  # Player now completed the first circuit

    def test_player_cannot_purchase_before_first_circuit(self):
        """Ensure a player cannot buy property before completing the first circuit."""
        self.player.is_first_circuit_complete = False  # Player has not completed the first circuit
        # Attempt to purchase property
        player_purchase = self.player.purchase_property(self.property, self.bank)
        self.assertFalse(player_purchase, "Player should not be able to purchase property before completing the first circuit.")

    def test_player_can_purchase_after_first_circuit(self):
        """Ensure a player can buy property after completing the first circuit."""
        # Attempt to purchase property
        player_purchase = self.player.purchase_property(self.property, self.bank)
        self.assertTrue(player_purchase, "Player should be able to purchase property after completing first circuit.")
        self.assertEqual(self.property.get_owner(), self.player, "Property should be owned by the player.")
        
    def test_player_cannot_upgrade_property_without_all_properties_in_group(self):
        """Ensure a player cannot upgrade property without all properties in group."""
        # Attempt to upgrade property, should return False
        player_upgrade = self.player.purchase_property(self.property, self.bank)
        upgrade_result = self.property.upgrade_property(self.bank)
        self.assertFalse(upgrade_result, "Player should not be able to upgrade property without all properties in group.")
        


if __name__ == "__main__":
    unittest.main()
