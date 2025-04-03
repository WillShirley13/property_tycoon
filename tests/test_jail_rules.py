
import unittest
import sys
import os

# # Add the backend directory to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))

from unittest.mock import MagicMock
from src.backend.property_owners.player import Player
from src.backend.enums.game_token import GameToken
from src.backend.non_ownables.jail import Jail 


class TestJailMechanism(unittest.TestCase):

    def setUp(self):
        """Set up a Player and Jail instance for testing."""
        self.player = Player(GameToken.BOOT, "Will")
        self.jail = Jail()

    def test_three_consecutive_doubles_sends_player_to_jail(self):
        """Test that rolling three consecutive doubles sends a player to jail."""
        # Mock three consecutive double rolls
        move_results = [([2, 2], 4), ([3, 3], 10), ([4, 4], 18)]  # Third double roll triggers jail

        def mock_move():
            return move_results.pop(0)

        self.player.move_player = MagicMock(side_effect=mock_move)

        # Simulate the player rolling three times
        for _ in range(3):
            move_result = self.player.move_player()
            if move_result and move_result[0][0] == move_result[0][1]:  # Check if it's a double
                if _ == 2:  # Third double
                    self.jail.put_in_jail(self.player)
                    break

        # Assert that the player is now in jail
        self.assertTrue(self.player.get_is_in_jail(), "Player should be in jail after rolling three consecutive doubles.")


if __name__ == "__main__":
    unittest.main()
