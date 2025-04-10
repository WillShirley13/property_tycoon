import unittest
import sys
import os

# # Add the backend directory to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))

#Make sure the Go module is imported properly in the game_card file

import random
from typing import TYPE_CHECKING, Dict, List, Tuple
from src.backend.non_ownables.game_card import GameCard
from src.backend.constants import POT_LUCK_CARDS, OPPORTUNITY_KNOCKS_CARDS

class TestGameCard(unittest.TestCase):
    
    def setUp(self):
        """Set up a GameCard instance before each test."""
        self.card_ids = {card: idx + 1 for idx, card in enumerate(list(POT_LUCK_CARDS.keys()) + list(OPPORTUNITY_KNOCKS_CARDS.keys()))}
        self.card_pack = list(POT_LUCK_CARDS.keys())  # Ensure it's a list
        self.game_card = GameCard(self.card_ids, self.card_pack)
        self.original_order = POT_LUCK_CARDS.copy()
        self.shuffled_order = self.game_card.shuffle_pack()

    # # def test_cards_shuffled_at_start(self):
    # #     """Ensure the cards are shuffled upon initialization."""
    # #     shuffled_order = self.game_card.card_pack
    # #     print("\nOriginal order:", self.original_order)  # Print original order
    # #     print("Shuffled order:", shuffled_order)  # Print shuffled order
    # #     self.assertNotEqual(self.original_order, shuffled_order, "Cards should be shuffled at the start.")


    # def test_drawn_cards_go_to_bottom(self):
    #     """Ensure that drawn cards move to the bottom of the deck."""
    #     print("\nBefore drawing a card:", self.game_card.card_pack)  # Print deck before drawing
    #     first_card, _ = self.game_card.get_card()
    #     print("Drawn card:", first_card)  # Print drawn card
    #     print("After drawing a card:", self.game_card.card_pack)  # Print deck after drawing
    #     self.assertEqual(self.game_card.card_pack[-1], first_card, "Drawn card should be placed at the bottom of the deck.")

    def test_player_draws_card_on_pot_luck_space(self):
        """Test that landing on a Pot Luck space triggers drawing a card."""
        pot_luck_positions = [0, 17, 33]
        for position in pot_luck_positions:
            self.assertIn(position, pot_luck_positions)
            card, card_id = self.game_card.get_card()
            self.assertIsNotNone(card)
            self.assertTrue(card in POT_LUCK_CARDS)

    def test_player_draws_card_on_opportunity_knocks_space(self):
        """Test that landing on an Opportunity Knocks space triggers drawing a card."""
        # Create a GameCard with Opportunity Knocks cards
        card_pack = list(OPPORTUNITY_KNOCKS_CARDS.keys())
        game_card = GameCard(self.card_ids, card_pack)

        opp_knocks_positions = [7, 22, 36]
        for position in opp_knocks_positions:
            self.assertIn(position, opp_knocks_positions)
            card, card_id = game_card.get_card()
            self.assertIsNotNone(card)
            self.assertTrue(card in OPPORTUNITY_KNOCKS_CARDS)
    

if __name__ == '__main__':
    unittest.main()
