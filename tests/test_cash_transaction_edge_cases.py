from typing import List
import unittest
import sys
import os
current_dir = os.path.dirname(os.path.abspath(__file__))
# Get parent directory (property_tycoon-Will)
parent_dir = os.path.dirname(current_dir)
sys.path.append(f'{parent_dir}/src')

from backend.admin import Admin
from backend.enums.game_token import GameToken
from backend.enums.property_group import PropertyGroup
from backend.property_owners.player import Player
from backend.property_owners.bank import Bank
from backend.ownables.property import Property
from backend import errors

class TestCashTransactionEdgeCases(unittest.TestCase):
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
        self.player1.cash_balance = 0
        self.initial_cash = 1000

    def test_cash_balance_exactly_zero(self):
        """Test that a player's cash balance can reach exactly zero without errors"""
        # Set initial cash
        self.player1.add_cash_balance(self.initial_cash)
        
        # Subtract exactly the initial cash amount
        self.player1.sub_cash_balance(self.initial_cash)
        
        # Verify balance is exactly zero
        self.assertEqual(self.player1.get_cash_balance(), 0)
        
        # Verify no unexpected errors occurred
        self.assertFalse(self.player1.is_bankrupt)

    def test_cash_balance_exactly_zero_after_property_purchase(self):
        """Test that a player's cash balance can reach exactly zero after property purchase"""
        # Set initial cash equal to property cost
        self.player1.add_cash_balance(self.property.get_cost())
        
        # Purchase property
        self.player1.purchase_property(self.property, self.bank)
        
        # Verify balance is exactly zero
        self.assertEqual(self.player1.get_cash_balance(), 0)
        
        # Verify property ownership
        self.assertEqual(self.property.get_owner(), self.player1)

    def test_purchase_property_with_insufficient_funds(self):
        """Test that attempting to purchase property with insufficient funds raises correct exception"""
        
        # Attempt to purchase property
        with self.assertRaises(errors.InsufficientFundsError):
            self.player1.purchase_property(self.property, self.bank)
        
        # Verify property remains with bank
        self.assertEqual(self.property.get_owner(), self.bank)
        
        # Verify player's cash wasn't changed
        self.assertEqual(self.player1.get_cash_balance(), 0)

    def test_purchase_property_with_exact_funds(self):
        """Test that purchasing property with exact required funds works correctly"""
        # Set initial cash exactly equal to property cost
        self.player1.add_cash_balance(self.property.get_cost())
        
        # Purchase property
        self.player1.purchase_property(self.property, self.bank)
        
        # Verify property ownership
        self.assertEqual(self.property.get_owner(), self.player1)
        
        # Verify cash balance is exactly zero
        self.assertEqual(self.player1.get_cash_balance(), 0)

    def test_multiple_transactions_to_zero(self):
        """Test that multiple transactions can reduce cash to exactly zero"""
        self.initial_cash = 1000
        # Set initial cash
        self.player1.add_cash_balance(self.initial_cash)
        
        # Perform multiple transactions that sum to initial cash
        self.player1.sub_cash_balance(self.initial_cash // 2)
        self.player1.sub_cash_balance(self.initial_cash // 2)
        
        # Verify balance is exactly zero
        self.assertEqual(self.player1.get_cash_balance(), 0)
        
        # Verify no unexpected errors occurred
        self.assertFalse(self.player1.is_bankrupt)

    def test_purchase_property_with_almost_enough_funds(self):
        """Test that attempting to purchase property with almost enough funds fails gracefully"""
        # Set initial cash just below property cost
        self.player1.add_cash_balance(self.property.get_cost() - 1)
        
        # Attempt to purchase property
        with self.assertRaises(errors.InsufficientFundsError):
            self.player1.purchase_property(self.property, self.bank)
        
        # Verify property remains with bank
        self.assertEqual(self.property.get_owner(), self.bank)
        
        # Verify player's cash wasn't changed
        self.assertEqual(self.player1.get_cash_balance(), self.property.get_cost() - 1)

if __name__ == '__main__':
    unittest.main()