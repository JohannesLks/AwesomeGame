import pygame
import sys
import os
# Constants for the game
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 563
PLAYER_SPEED = 5
POWER_UP_RATE = 200    # Lower number means more frequent power-ups
SCORE_MULTIPLIER = 2   # For X2-Boost power-up
ENEMY_SPEED = 1
BLOCKER_SPAWN_RATE = 1000

# Define a constant for how much the enemy spawn rate should increase with each wave
ENEMY_SPAWN_INCREMENT = 10  # This means with each wave, the spawn rate will increase by 10
BUTTON_WIDTH = 200
BUTTON_HEIGHT = 50
INPUT_WIDTH = 200
INPUT_HEIGHT = 40
BUTTON_SPACING = 200  # Abstand zwischen den Knöpfen
LOWER_OFFSET = 70
INPUT_BOX_Y_OFFSET = 380 # Abstand des Eingabefeldes von der oberen Bildschirmkante
BUTTON_Y_OFFSET = INPUT_BOX_Y_OFFSET + INPUT_HEIGHT + 50  # Abstand der Knöpfe vom Eingabefeld
center_x = SCREEN_WIDTH // 2
half_button_width = BUTTON_WIDTH // 2

#Enemys
#Standard
STANDARD_HITPOINTS = 1
ENEMY_SPEED = 1
STANDARD_ENEMY_SCORE_VALUE = 10
STANDARD_ENEMY_SPAWN_RATE = 200  # Lower number means more frequent spawns
#Advanced
ADVANCED_ENEMY_SPEED = 0.5
ADVANCED_HITPOINTS = 5
ADVANCED_ENEMY_SCORE_VALUE = 100
ADVANCED_ENEMY_SPAWN_RATE = 600  # Lower number means more frequent spawns


#Burgers
BURGER_DAMAGE = 1

#Waves
current_wave = 1
WAVE_DURATION = 30000
BREAK_DURATION = 3000
in_between_waves = False
wave_start_time = 0


# Define colors
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)
LIGHT_BLUE = (173, 216, 230)  # An example color for the inactive state
DARK_BLUE = (0, 0, 139)  # An example color for the active state


# This dictionary maps power-up types to their images and attributes
POWER_UPS_ATTRIBUTES = {
    'score_boost': {
        'image': 'media/boost.png',
        'effect': lambda player: setattr(player, 'score', player.score + 50)
    },
    'ammo_boost': {
        'image': 'media/boost.png',
        'effect': lambda player: player.activate_ammo_boost()  # This will be a new method in the Player class
    },
    'health_boost': {
        'image': 'media/boost.png',
        'effect': lambda player: setattr(player, 'health', player.health + 20)
    },

}

# Load game assets
burger_img = pygame.image.load('media/burger.png')
background_img = pygame.image.load('media/bikini_bottom.png')
welcome_background_img = pygame.image.load('media/menu.png')
game_over_img = pygame.image.load('media/game_over_screen.png')
start_button_img = pygame.image.load('media/start_button.png')
start_button_hover_img = pygame.image.load('media/start_button_hover.png')
quit_button_img = pygame.image.load('media/quit_button.png')
quit_button_hover_img = pygame.image.load('media/quit_button_hover.png')
input_bg_image = pygame.image.load('media/text_input.png')
adventure_font_path = 'media/font_dungeon_quest.ttf'
blocker_img = pygame.image.load('media/Plankton.png')

THROW_SOUND = 'media/throw.mp3'
