import unittest
from unittest.mock import Mock, patch, ANY
import pygame
import random
import sys
import os

# Custom subclass of pygame.Rect with a mock collidepoint method
class MockRect(pygame.Rect):
    def collidepoint(self, point):
        return True  # Mocked collidepoint method always returns True

# Mock necessary Pygame functionalities
@patch('pygame.display.set_mode', Mock())
@patch('pygame.image.load', Mock(return_value=Mock(convert=Mock(return_value=Mock()))))
@patch('pygame.display.flip', Mock())
@patch('pygame.mixer.init', Mock())
@patch('pygame.mixer.music.load', Mock())
@patch('pygame.mixer.music.play', Mock())
@patch('pygame.mixer.Sound', Mock())
@patch('pygame.time.set_timer', Mock())
@patch('pygame.event.get', Mock())

def setUpModule():
    # Import Main after mocks are set up
    global Main
    import Main


class TestMainGame(unittest.TestCase):

    def setUp(self):
        pygame.init()

    @patch('pygame.mouse.get_pos')
    @patch('pygame.mouse.get_pressed')
    def test_create_button(self, mock_get_pressed, mock_get_pos):
        mock_get_pos.return_value = (150, 150)  # Mock mouse position
        mock_get_pressed.return_value = (1, 0, 0)  # Mock mouse click

        screen = pygame.display.set_mode((800, 600))
        button_image = pygame.Surface((100, 50))
        button_rect, clicked = Main.create_button(screen, button_image, button_image, 100, 100)

        self.assertTrue(clicked)
        self.assertEqual(button_rect.topleft, (100, 100))



    @patch('random.randint')
    def test_spawn_enemies(self, mock_randint):
        # Mocks and test setup
        enemy_group = Mock()
        blocker_group = Mock()
        player_rect = Mock()
        shooting_area = {'top': 0, 'bottom': 500}
        
        # Mock the random.randint to simulate the spawning of a standard enemy
        mock_randint.side_effect = [1, Main.ADVANCED_ENEMY_SPAWN_RATE + 1, Main.BLOCKER_SPAWN_RATE + 1]

        # Call the function
        Main.spawn_enemies(enemy_group, blocker_group, player_rect, shooting_area)

        # Assert that a standard enemy was added
        self.assertEqual(enemy_group.add.call_count, 1)

        # Reset mocks for next test scenario
        enemy_group.reset_mock()
        blocker_group.reset_mock()
        mock_randint.reset_mock()

        # Similarly, test for advanced enemy and blocker spawning...
        # For advanced enemy, make randint return a value to spawn an advanced enemy
        # For blocker, make randint return a value to spawn a blocker
        # Assert accordingly

    @patch('random.randint')
    def test_spawn_enemies_no_spawn(self, mock_randint):
        mock_randint.side_effect = [2, 2, 2]  # Mock to not spawn any enemy or blocker

        enemy_group = Mock()
        blocker_group = Mock()
        player_rect = Mock()
        shooting_area = {'top': 0, 'bottom': 500}

        Main.spawn_enemies(enemy_group, blocker_group, player_rect, shooting_area)

        enemy_group.add.assert_not_called()
        blocker_group.add.assert_not_called()

if __name__ == '__main__':
    unittest.main()

