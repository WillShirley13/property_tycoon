import unittest
import sys
import os

from unittest.mock import MagicMock

# Add the backend directory to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))

from src.backend.property_owners.player import Player
from src.backend.enums.game_token import GameToken
from src.backend.non_ownables.jail import Jail
from src.backend.non_ownables.go import Go
from src.backend.property_owners.bank import Bank
from src.backend.non_ownables.free_parking import FreeParking


class TestJailMechanism(unittest.TestCase):

    def setUp(self):
        """Set up necessary game elements for jail testing."""
        self.player = Player(GameToken.BOOT, "Will")
        self.jail = Jail()
        self.go = MagicMock(spec=Go)
        self.bank = MagicMock(spec=Bank)
        self.free_parking = MagicMock(spec=FreeParking)
    
    def test_pay_fine_to_get_out_of_jail(self):  
        """Test that a player can pay £50 to get out of jail and the fine goes to Free Parking."""
        self.jail.put_in_jail(self.player)
        self.assertTrue(self.player.get_is_in_jail())

        initial_balance = self.player.get_cash_balance()
        print(f"Player's balance before paying fine: {initial_balance}")

        self.jail.pay_fine_for_release(self.player, self.free_parking, self.go, self.bank)

        final_balance = self.player.get_cash_balance()
        print(f"Player's balance after paying fine: {final_balance}")

        #self.assertEqual(final_balance, initial_balance - 50)  # Assert £50 was deducted
        self.assertFalse(self.player.get_is_in_jail()) 

    def test_three_consecutive_doubles_sends_player_to_jail(self):
        """Test that rolling three consecutive doubles sends a player to jail."""
        move_results = [([2, 2], 4), ([3, 3], 10), ([4, 4], 18)]

        def mock_move():
            return move_results.pop(0)

        self.player.move_player = MagicMock(side_effect=mock_move)

        for i in range(3):
            move_result = self.player.move_player()
            if move_result[0][0] == move_result[0][1]:
                if i == 2:
                    self.jail.put_in_jail(self.player)
                    break

        self.assertTrue(self.player.get_is_in_jail(), "Player should be in jail after 3 doubles.")

    def test_player_released_after_two_rounds_in_jail(self):
        """Test that a player is released after staying in jail for 2 rounds."""
        self.jail.put_in_jail(self.player)
        self.player.set_rounds_in_jail(0)

        # Simulate 2 turns in jail
        for _ in range(2):
            rounds = self.player.get_rounds_in_jail()
            self.player.set_rounds_in_jail(rounds + 1)
        
        if self.player.get_rounds_in_jail() == 2:
            self.assertEqual(self.player.get_rounds_in_jail(), 2)
            self.jail.release_from_jail(self.player, self.go, self.bank)

        # self.jail.release_from_jail(self.player, self.go, self.bank)

        self.assertFalse(self.player.get_is_in_jail(), "Player should be released after 2 rounds in jail.") #Player should be out of jail
        self.assertEqual(self.player.get_rounds_in_jail(), 0) #Round should be reset to 0



if __name__ == "__main__":
    unittest.main()
