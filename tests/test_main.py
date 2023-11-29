import unittest
from unittest.mock import Mock, patch
import pygame

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

    def test_handle_input_events(self):
        event_mouse = pygame.event.Event(pygame.MOUSEBUTTONDOWN, pos=(100, 100))
        event_key = pygame.event.Event(pygame.KEYDOWN, key=pygame.K_a, unicode='a')
        input_box_rect = pygame.Rect(50, 50, 100, 50)

        # Test mouse event
        input_text, input_box_active = Main.handle_input_events(event_mouse, "", False, input_box_rect)
        self.assertTrue(input_box_active)

        # Test key event
        input_text, input_box_active = Main.handle_input_events(event_key, "", True, input_box_rect)
        self.assertEqual(input_text, "a")

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
        mock_randint.return_value = 1  # Mock to always spawn an enemy

        enemy_group = pygame.sprite.Group()
        blocker_group = pygame.sprite.Group()
        player_rect = pygame.Rect(100, 100, 50, 50)
        shooting_area = {'top': 0, 'bottom': 500, 'left': 0, 'right': 800}

        Main.spawn_enemies(enemy_group, blocker_group, player_rect, shooting_area)
        self.assertEqual(len(enemy_group), 1)
if __name__ == '__main__':
    unittest.main()
