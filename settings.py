import pygame
# Constants for the game
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 563
PLAYER_SPEED = 5
ENEMY_SPAWN_RATE = 60  # Lower number means more frequent spawns
POWER_UP_RATE = 500    # Lower number means more frequent power-ups
SCORE_MULTIPLIER = 2   # For X2-Boost power-up


BUTTON_WIDTH = 200
BUTTON_HEIGHT = 50
INPUT_WIDTH = 200
INPUT_HEIGHT = 40
BUTTON_SPACING = 20  # Abstand zwischen den Knöpfen
INPUT_BOX_Y_OFFSET = 150  # Abstand des Eingabefeldes von der oberen Bildschirmkante
BUTTON_Y_OFFSET = INPUT_BOX_Y_OFFSET + INPUT_HEIGHT + 50  # Abstand der Knöpfe vom Eingabefeld

# Define colors
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)
LIGHT_BLUE = (173, 216, 230)  # An example color for the inactive state
DARK_BLUE = (0, 0, 139)  # An example color for the active state

# Initialize the font
pygame.font.init()  # Only needed if not already called
font = pygame.font.SysFont('arial', 32)  # You can replace 'arial' with any other font

# Load game assets
player_img = pygame.image.load('media/mr_krabs.png')
enemy_img = pygame.image.load('media/blowfish.png')
burger_img = pygame.image.load('media/burger.png')
background_img = pygame.image.load('media/bikini_bottom.png')
welcome_background_img = pygame.image.load('media/bikini_bottom.png')
start_button_img = pygame.image.load('media/start_button.png')
start_button_hover_img = pygame.image.load('media/start_button_hover.png')
quit_button_img = pygame.image.load('media/quit_button.png')
quit_button_hover_img = pygame.image.load('media/quit_button_hover.png')
input_bg_image = pygame.image.load('media/text_input.png')
adventure_font_path = 'media/font_dungeon_quest.ttf'  # Replace with the correct path
