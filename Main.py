# Based on the provided outline, here is the Python code for the game "Krabs' Burger-Battle: Die Geldfischjagd"

# Import necessary modules
import pygame
import random
from settings import *
from sprites import *


import sys, os

# Initialize the pygame
pygame.init()

# Define colors
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# Background music and sound effects
pygame.mixer.music.load('media/background_music.mp3')
pygame.mixer.music.play(-1)  # Play the music indefinitely
money_sound = pygame.mixer.Sound('media/money_sound.mp3')

# Set up the screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Krabs' Burger-Battle: Die Geldfischjagd")

# Use pygame's event system to create a custom event for ammo regeneration
AMMO_REGEN_EVENT = pygame.USEREVENT + 1
pygame.time.set_timer(AMMO_REGEN_EVENT, 2000)  # Set a timer to trigger every 5 seconds

# Function to handle spawning enemies
def spawn_enemies(enemy_group, player_rect):
    if random.randint(1, ENEMY_SPAWN_RATE) == 1:
        enemy = Enemy()
        # Adjust the spawning position so it doesn't overlap with the player's area
        safe_margin = 100  # Set a safe margin distance
        # Make sure the enemy doesn't spawn within the safe margin around the player
        while abs(enemy.rect.y - player_rect.y) < safe_margin:
            enemy.rect.y = random.randint(0, SCREEN_HEIGHT - enemy.rect.height)
        enemy_group.add(enemy)


# Function to handle spawning power-ups
def spawn_power_ups(power_up_group):
    if random.randint(1, POWER_UP_RATE) == 1:
        # Randomly choose a power-up type
        power_up_type = random.choice(['score_boost', 'speed_boost', 'health_boost'])
        power_up = PowerUp(power_up_type, random.randint(0, SCREEN_WIDTH), random.randint(0, SCREEN_HEIGHT))
        power_up_group.add(power_up)

def regenerate_ammo(player):
    if player.ammo < 10:
        player.ammo += 1  # Regenerate one ammo

# Main game loop
running = True
clock = pygame.time.Clock()
player = Player()
players = pygame.sprite.Group()
players.add(player)
enemies = pygame.sprite.Group()
burgers = pygame.sprite.Group()
power_ups = pygame.sprite.Group()
try:
    # Your main game loop code here
    while running:
        clock.tick(60)  # Run at 60 frames per second
        screen.fill(WHITE)  # Fill the background with white color
        screen.blit(background_img, (0, 0))  # Draw the background image

        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    if player.ammo > 0:
                        burger = Burger(player.rect.centerx, player.rect.top)
                        burgers.add(burger)
                        player.ammo -= 1
            elif event.type == AMMO_REGEN_EVENT:
                regenerate_ammo(player)

        for enemy in list(enemies):  # Make a copy of the group list to iterate over
            enemy_off_screen = enemy.update()
            if enemy_off_screen:
                player.health -= 10  # Decrease health when enemy reaches the edge
                if player.health <= 0:
                    running = False  # End the game if health is depleted

        # Update game states
        keys = pygame.key.get_pressed()
        player.update(keys)
        enemies.update()
        burgers.update()
        power_ups.update()

        # Collision detection
        # Collision detection with enemies
        for burger in list(burgers):  # Iterate over a copy of the burgers
            hit_enemies = pygame.sprite.spritecollide(burger, enemies, True, pygame.sprite.collide_mask)
            for enemy in hit_enemies:
                burger.kill()  # Remove the burger
                player.score += 10  # Increase the score
                money_sound.play()  # Play the money sound effect

        # Collision detection with power-ups
        for burger in list(burgers):  # Iterate over a copy of the burgers again for power-up checks
            hit_power_ups = pygame.sprite.spritecollide(burger, power_ups, True, pygame.sprite.collide_mask)
            for power_up in hit_power_ups:
                if power_up.type == 'score_boost':
                    player.score *= SCORE_MULTIPLIER  # Apply score boost
                elif power_up.type == 'speed_boost':
                    player.speed += 2  # Apply speed boost
                elif power_up.type == 'health_boost':
                    player.health += 20  # Apply health boost


        for event in pygame.event.get():
            if event.type == AMMO_REGEN_EVENT:
                regenerate_ammo(player)
    

        # Spawn enemies and power-ups
        spawn_enemies(enemies, player.rect)
        spawn_power_ups(power_ups)

        # Drawing everything on the screen
        screen.blit(background_img, (0, 0))
        players.draw(screen)
        enemies.draw(screen)
        burgers.draw(screen)
        power_ups.draw(screen)


        # Display the score
        font = pygame.font.SysFont(None, 36)
        score_text = font.render(f'Score: {player.score}', True, BLUE)
        screen.blit(score_text, (10, 10))

        # Display the health
        health_text = font.render(f'Health: {player.health}', True, RED)
        screen.blit(health_text, (10, 50))
    
        # Display the ammunation
        ammo_text = font.render(f'Ammo: {player.ammo}', True, GREEN)
        screen.blit(ammo_text, (10, 80))

        # Update the display
        pygame.display.flip()
except Exception as e:
    exc_type, exc_obj, exc_tb = sys.exc_info()
    fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
    print(exc_type, fname, exc_tb.tb_lineno)
    running = False

# Quit the game
pygame.quit()