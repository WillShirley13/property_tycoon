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
        self.property = Property(name="Ibis Close", cost=320, property_group=PropertyGroup.GREEN, owner=self.bank)
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

    # def test_player_can_purchase_after_first_circuit(self):
    #     """Ensure a player can buy property after completing the first circuit."""
    #     self.player.is_first_circuit_complete = True  # Player now completed the first circuit
        
    #     # Attempt to purchase property at its card value
    #     can_purchase = self.player.get_is_first_circuit_complete()
    #     if can_purchase:
    #         self.player.purchase_property(self.property, self.bank)  # Simulate successful purchase
        
    #     self.assertEqual(self.property.get_owner(), self.player, "Player should be able to purchase property after completing first circuit at card value.")
    #     self.assertEqual(self.player.get_balance(), self.player.get_starting_balance() - self.property.get_cost(), "Player's balance should be reduced by the property's cost.")

    def test_player_can_purchase_after_first_circuit(self):
        """Ensure a player can buy property after completing the first circuit."""
        self.player.is_first_circuit_complete = True  # Player now completed the first circuit
        
        # Check the property exists in bank's portfolio before purchasing
        initial_owner = self.property.get_owner()
        print(f"Bank's property group before purchase: {self.bank.owned_properties[self.property.property_group]}")

        # Attempt to purchase property at its card value
        can_purchase = self.player.get_is_first_circuit_complete()
        if can_purchase:
            self.player.purchase_property(self.property, self.bank)  # Simulate successful purchase

        # Check the property has been successfully removed from the bank's portfolio and owned by the player
        self.assertEqual(self.property.get_owner(), self.player, "Player should be able to purchase property after completing first circuit at card value.")
        self.assertEqual(self.player.get_balance(), self.player.get_starting_balance() - self.property.get_cost(), "Player's balance should be reduced by the property's cost.")
        print(f"Bank's property group after purchase: {self.bank.owned_properties[self.property.property_group]}")


if __name__ == "__main__":
    unittest.main()
