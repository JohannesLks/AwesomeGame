#Import der benötigten Module1
import pygame
import sys
import os

# Spiel Konstanten
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 563
PLAYER_SPEED = 5

POWER_UP_RATE = 200    # Eine niedrigere Zahl bedeutet häufigere Power-ups
SCORE_MULTIPLIER = 2   # Für X2-Boost Power-up
BLOCKER_SPAWN_RATE = 400 # Niedrigere Zahl bedeutet häufigeres spawnen
BLOCKER_COUNT = 0
BLOCKER_MAXIMUM = 5 # Anzahl der Blocker auf die Zahl limitiert

# Definieren einer Konstante, um die die Spawnrate der Gegner in jeder Welle erhöht wird
ENEMY_SPAWN_INCREMENT = 20  # Wert um den die Spawnrate jede Wave verringert wird - je weniger, desto mehr Spawns

#Knopf Einstellungen
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

#Gegner Attribute
#Standard-Gegner
STANDARD_ENEMY_SPEED = 2 # Speed sollte immer int sein, sonst kommt es zu Problemen, da rect.x float nicht benutzen kann -> Rundungsfehler; komische Geschwindigkeiten
STANDARD_HITPOINTS = 1
STANDARD_ENEMY_SCORE_VALUE = 10
STANDARD_ENEMY_SPAWN_RATE = 200  # Niedrigere Zahl bedeutet häufigeres spawnen
#Advanced-Gegner
ADVANCED_ENEMY_SPEED = 1 # Speed sollte immer int sein, sonst kommt es zu Problemen, da rect.x float nicht benutzen kann -> Rundungsfehler; komische Geschwindigkeiten
ADVANCED_HITPOINTS = 3
ADVANCED_ENEMY_SCORE_VALUE = 100
ADVANCED_ENEMY_SPAWN_RATE = 600  # Niedrigere Zahl bedeutet häufigeres spawnen

#Burger schaden
BURGER_DAMAGE = 1

#Einstellungen der Wellen
current_wave = 1
WAVE_DURATION = 30000
BREAK_DURATION = 3000
in_between_waves = False
wave_start_time = 0

# Farben bestimmen
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)

# Dieses Dictionary bestimmt die PowerUp Attribute und Bilder
POWER_UPS_ATTRIBUTES = {
    'score_boost': {
        'image': 'media/moneyboost.png',
        'effect': lambda player: setattr(player, 'score', player.score + 50)
    },
    'ammo_boost': {
        'image': 'media/ammoboost.png',
        'effect': lambda player: player.activate_ammo_boost()  
    },
    'health_boost': {
        'image': 'media/healthboost.png',
        'effect': lambda player: setattr(player, 'health', player.health + 20)
    },

}

# Laden der Medien
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

#Sounds
THROW_SOUND = 'media/throw.mp3'
game_over_sound = 'media/game_over.wav'
game_over_music = 'media/game_over_music.mp3'
PLANKTON_SPAWN_SOUND = 'media/evil_laugh.wav'
