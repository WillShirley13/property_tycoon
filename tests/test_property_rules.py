from pickle import TRUE
from typing import List
import unittest
import sys
import os

# # # Add the backend directory to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../src/')))
from backend.errors import PropertyNotInPortfolioError
from backend.admin import Admin
from backend.ownables.property import Property
from backend.enums.property_group import PropertyGroup
from backend.enums.game_token import GameToken
from backend.property_owners.player import Player
from backend.property_owners.bank import Bank
from backend.ownables.property import Property
from backend.constants import PROPERTY_BUILD_COSTS
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
        self.admin = Admin([('Will', game_tokens[0]), ('John', game_tokens[1])], 0)
        self.bank = self.admin.get_bank()
        self.property = self.bank.get_owned_properties()[PropertyGroup.BROWN][0]
        self.player1 = self.admin.get_players()[0]
        self.player2 = self.admin.get_players()[1]
        self.player1.is_first_circuit_complete = True  # Player now completed the first circuit
        self.player2.is_first_circuit_complete = True  # Player now completed the first circuit

    def test_player_cannot_purchase_before_first_circuit(self):
        """Ensure a player cannot buy property before completing the first circuit."""
        self.player1.is_first_circuit_complete = False  # Player has not completed the first circuit
        # Attempt to purchase property
        player_purchase = self.player1.purchase_property(self.property, self.bank)
        self.assertFalse(player_purchase, "Player should not be able to purchase property before completing the first circuit.")

    def test_player_can_purchase_after_first_circuit(self):
        """Ensure a player can buy property after completing the first circuit."""
        # Attempt to purchase property
        player_purchase = self.player1.purchase_property(self.property, self.bank)
        self.assertTrue(player_purchase, "Player should be able to purchase property after completing first circuit.")
        self.assertEqual(self.property.get_owner(), self.player1, "Property should be owned by the player.")
        
    def test_player_cannot_upgrade_property_without_all_properties_in_group(self):
        """Ensure a player cannot upgrade property without all properties in group."""
        # Attempt to upgrade property, should return False
        purchase_result = self.player1.purchase_property(self.property, self.bank)
        
        # attempt to upgrade property, should return False
        upgrade_result = self.property.upgrade_property(self.bank)
        self.assertFalse(upgrade_result, "Player should not be able to upgrade property without all properties in group.")
        
    def test_player_can_upgrade_property_with_all_properties_in_group(self):
        """Ensure a player can upgrade property with all properties in group."""
        # Purchase all properties in the same group
        purchase_result = self.player1.purchase_property(self.property, self.bank)
        other_property_in_group = self.bank.get_owned_properties()[PropertyGroup.BROWN][0]
        purchase_result2 = self.player1.purchase_property(other_property_in_group, self.bank)
        
        # Attempt to upgrade first property, should return True
        upgrade_result = self.property.upgrade_property(self.bank)
        self.assertTrue(upgrade_result, "Player should be able to upgrade property with all properties in group.")
        
    def test_max_dif_between_houses_is_1_in_group(self):
        """Ensure the maximum difference between houses in a group is 1."""
        # Purchase all properties in the same group
        purchase_result = self.player1.purchase_property(self.property, self.bank)
        other_property_in_group = self.bank.get_owned_properties()[PropertyGroup.BROWN][0]
        purchase_result2 = self.player1.purchase_property(other_property_in_group, self.bank)
        
        # Attempt to upgrade first property, should return True
        upgrade_result = self.property.upgrade_property(self.bank)
        # First property should be upgraded to 1 house
        self.assertTrue(upgrade_result, "Player should be able to purchase first house.")
        
        # Attempt to upgrade first property again, should return False
        upgrade_result2 = self.property.upgrade_property(self.bank)
        self.assertFalse(upgrade_result2, "Player should not be able to purchase second house.")
        
    def test_various_upgrading_scenarios(self):
        """Ensure various upgrading scenarios work correctly."""
        # Purchase all properties in the same group
        purchase_result = self.player1.purchase_property(self.property, self.bank)
        other_property_in_group = self.bank.get_owned_properties()[PropertyGroup.BROWN][0]
        purchase_result2 = self.player1.purchase_property(other_property_in_group, self.bank)
        
        # Attempt to upgrade first property, should return True
        upgrade_result = self.property.upgrade_property(self.bank)
        self.assertTrue(upgrade_result, "Player should be able to upgrade property.")
        
        # Attempt to upgrade first property again, should return False    
        upgrade_result2 = self.property.upgrade_property(self.bank)
        self.assertFalse(upgrade_result2, "Player should not be able to purchase second house.")
        
        # Attempt to upgrade second property with all properties in group, should return True
        upgrade_result3 = other_property_in_group.upgrade_property(self.bank)
        self.assertTrue(upgrade_result3, "Player should be able to upgrade property with all properties in group.")
        
        # Attempt to upgrade first property again, should return True. Now has 2 houses
        upgrade_result4 = self.property.upgrade_property(self.bank)
        self.assertTrue(upgrade_result4, "Player should be able to upgrade property again.")
        
        # Attempt to upgrade second property again, should return True. Now has 2 houses
        upgrade_result5 = other_property_in_group.upgrade_property(self.bank)
        self.assertTrue(upgrade_result5, "Player should be able to upgrade property again.")
        
    def test_transfer_of_ownership_when_property_is_purchased_and_sold(self):
        """Ensure the ownership is transferred correctly when a property is purchased and sold."""
        # Purchase property, property owner should now be player
        purchase_result = self.player1.purchase_property(self.property, self.bank)
        self.assertEqual(self.property.get_owner(), self.player1, "Property should be owned by the player.")
        
        # Sell property, property owner should now be bank
        sell_result = self.player1.sell_property(self.property, self.bank)
        self.assertTrue(sell_result, "Player should be able to sell property.")
        self.assertEqual(self.property.get_owner(), self.bank, "Property should be owned by the bank.")
        
    def test_cannot_sell_property_if_not_owned(self):
        """Ensure a player cannot sell a property if they don't own it."""
        # Attempt to sell property 
        try:
            sell_result = self.player1.sell_property(self.property, self.bank)
            self.fail("Player should not be able to sell property if they don't own it.")
        except PropertyNotInPortfolioError as e:
            # Check that the error was raised
            self.assertTrue(True, "Attempt to sell property that is not in portfolio successfully raised an error.")
        
    def test_property_mortgage_and_pay_off(self):
        """Test mortgaging a property and paying off the mortgage."""
        # Purchase property first
        purchase_result = self.player1.purchase_property(self.property, self.bank)
        self.assertTrue(purchase_result, "Player should be able to purchase property.")
        
        # Get player's cash balance before mortgaging
        cash_before_mortgage = self.player1.get_cash_balance()
        property_value = self.property.get_cost()
        
        # Mortgage the property
        self.player1.mortgage_property(self.property, self.bank)
        
        # Check that property is now mortgaged
        self.assertTrue(self.property.get_is_mortgaged(), "Property should be mortgaged.")
        
        # Check player received half the property value
        self.assertEqual(self.player1.get_cash_balance(), cash_before_mortgage + property_value/2, 
                        "Player should receive half the property value when mortgaging.")
        
        # Check that the owner is bank
        self.assertEqual(self.property.get_owner(), self.bank, "Property owner should be bank when mortgaged.")
        
        # Get cash balance before paying off mortgage
        cash_before_payoff = self.player1.get_cash_balance()
        
        # Pay off the mortgage (same amount as received, no interest)
        mortgage_value = property_value / 2
        self.player1.pay_off_mortgage(self.property, self.bank)
        
        # Check mortgage is cleared
        self.assertFalse(self.property.get_is_mortgaged(), "Property should no longer be mortgaged.")
        
        # Check that the owner is player
        self.assertEqual(self.property.get_owner(), self.player1, "Property owner should be player when mortgage is paid off.")
        
        # Check correct amount was deducted
        self.assertEqual(self.player1.get_cash_balance(), cash_before_payoff - mortgage_value, 
                        "Player should pay the same mortgage value to clear mortgage.")
    
    def test_property_downgrade(self):
        """Test downgrading properties with houses/hotels."""
        # Purchase all properties in the same group
        purchase_result = self.player1.purchase_property(self.property, self.bank)
        other_property_in_group = self.bank.get_owned_properties()[PropertyGroup.BROWN][0]
        purchase_result2 = self.player1.purchase_property(other_property_in_group, self.bank)
        
        # Upgrade both properties to 2 houses each
        self.property.upgrade_property(self.bank)
        other_property_in_group.upgrade_property(self.bank)
        self.property.upgrade_property(self.bank)
        other_property_in_group.upgrade_property(self.bank)
        
        # Check houses before downgrade
        self.assertEqual(self.property.get_houses(), 2, "Property should have 2 houses before downgrade.")
        
        # Get cash balance before downgrade
        cash_before_downgrade = self.player1.get_cash_balance()
        house_cost = PROPERTY_BUILD_COSTS[self.property.get_property_group().value]["house"]
        
        # Downgrade property
        downgrade_result = self.property.downgrade_property(self.bank)
        
        # Check result and house count
        self.assertTrue(downgrade_result, "Downgrade should succeed.")
        self.assertEqual(self.property.get_houses(), 1, "Property should have 1 house after downgrade.")
        
        # Check player received correct refund
        self.assertEqual(self.player1.get_cash_balance(), cash_before_downgrade + house_cost, 
                        "Player should receive house value when downgrading.")
    
    def test_hotel_upgrade_and_downgrade(self):
        """Test upgrading to a hotel and then downgrading back to houses."""
        # Purchase all properties in the same group
        purchase_result = self.player1.purchase_property(self.property, self.bank)
        other_property_in_group = self.bank.get_owned_properties()[PropertyGroup.BROWN][0]
        purchase_result2 = self.player1.purchase_property(other_property_in_group, self.bank)
        
        # Upgrade both properties to 4 houses
        for _ in range(4):
            self.property.upgrade_property(self.bank)
            other_property_in_group.upgrade_property(self.bank)
        
        # Check houses before hotel upgrade
        self.assertEqual(self.property.get_houses(), 4, "Property should have 4 houses before hotel upgrade.")
        self.assertEqual(self.property.get_hotel(), 0, "Property should have no hotel before upgrade.")
        
        # Upgrade to hotel
        hotel_upgrade_result = self.property.upgrade_property(self.bank)
        
        # Check hotel status
        self.assertTrue(hotel_upgrade_result, "Hotel upgrade should succeed.")
        self.assertEqual(self.property.get_houses(), 0, "Property should have 0 houses after hotel upgrade.")
        self.assertEqual(self.property.get_hotel(), 1, "Property should have 1 hotel after upgrade.")
        
        # Downgrade from hotel back to houses
        hotel_downgrade_result = self.property.downgrade_property(self.bank)
        
        # Check house/hotel status after downgrade
        self.assertTrue(hotel_downgrade_result, "Hotel downgrade should succeed.")
        self.assertEqual(self.property.get_houses(), 4, "Property should have 4 houses after hotel downgrade.")
        self.assertEqual(self.property.get_hotel(), 0, "Property should have 0 hotels after downgrade.")
    
    def test_rent_increases_with_houses(self):
        """Test that rent increases correctly with house upgrades."""
        # Purchase property
        purchase_result = self.player1.purchase_property(self.property, self.bank)
        
        # Record base rent for property 1
        base_rent = self.property.get_rent_cost()
        
        # Purchase all properties in group to enable upgrades
        other_property_in_group = self.bank.get_owned_properties()[PropertyGroup.BROWN][0]
        purchase_result2 = self.player1.purchase_property(other_property_in_group, self.bank)
        
        # Add a house to property 1
        self.property.upgrade_property(self.bank)
        
        # Check rent increased for property 1
        self.assertGreater(self.property.get_rent_cost(), base_rent, 
                        "Rent should increase after adding a house.")
        
        # Record rent with one house for property 1
        one_house_rent = self.property.get_rent_cost()
        
        # Add another house to property 1, so now has 2 houses
        other_property_in_group.upgrade_property(self.bank)
        self.property.upgrade_property(self.bank)
        
        # Check rent increased again
        self.assertGreater(self.property.get_rent_cost(), one_house_rent, 
                        "Rent should increase after adding a second house.")
    
    def test_mortgaged_property_collects_no_rent(self):
        """Test that mortgaged properties do not collect rent."""
        # Purchase property first
        self.player1.purchase_property(self.property, self.bank)
        # Mortgage the property
        self.player1.mortgage_property(self.property, self.bank)
        
        # Check property is mortgaged but still owned by player
        self.assertTrue(self.property.get_is_mortgaged(), "Property should be mortgaged.")
        
        # Check no rent is due. get_rent_due_from_player() returns 0 if property is mortgaged, else returns rent due
        rent_due = self.property.get_rent_due_from_player(self.player2)
        self.assertEqual(rent_due, 0, "Mortgaged property should not collect rent.")

if __name__ == "__main__":
    unittest.main()
