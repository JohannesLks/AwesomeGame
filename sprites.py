import pygame
import os
from settings import *
import random
from abc import ABC, abstractmethod




# Player class
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        # Inside the Player class __init__ method
        self.image = pygame.transform.scale(player_img, (200, 185))  # Resize to appropriate dimensions
        self.rect = self.image.get_rect(midbottom=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 10))
        self.speed = PLAYER_SPEED
        self.health = 100
        self.score = 0
        self.ammo = 10  # Player starts with 10 ammunition

    def update(self, keys):
        if keys[pygame.K_a]:
            self.rect.x -= self.speed
        if keys[pygame.K_d]:
            self.rect.x += self.speed
        if keys is None:
            keys = pygame.key.get_pressed()
        # Keep the player on the screen
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH


# Enemy class
class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = enemy_img
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)  # Erstellen der Maske aus dem Bild
        
        # Set a constant speed for all enemies
        self.speed = 1
        
        # Decide the starting side (left or right)
        if random.choice([True, False]):
            self.rect.x = -self.rect.width  # Start from the left side
            self.direction = 1  # Move to the right
        else:
            self.rect.x = SCREEN_WIDTH  # Start from the right side
            self.direction = -1  # Move to the left

        # Randomly choose the vertical position
        self.rect.y = random.randint(0, SCREEN_HEIGHT - self.rect.height)

    def update(self):
        # Move horizontally at a constant speed
        self.rect.x += self.speed * self.direction
        
        # Remove the sprite when it moves off the screen
        if self.rect.right < 0 or self.rect.left > SCREEN_WIDTH:
            self.kill()  # Remove the enemy
            return True  # Indicate that an enemy has reached the edge
        return False




# Make sure the burger's update method moves it upwards
class Burger(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = burger_img
        self.rect = self.image.get_rect(center=(x, y))
        self.mask = pygame.mask.from_surface(self.image)  # Erstellen der Maske aus dem Bild
    def update(self):
        # Move the burger upwards
        self.rect.y -= 5
        # Remove the burger if it moves off the top of the screen
        if self.rect.bottom < 0:
            self.kill()

# Power-up class
class PowerUp(pygame.sprite.Sprite):
    def __init__(self, type, x, y):
        super().__init__()
        self.type = type
        self.image = pygame.image.load('media/boost.png')  # Placeholder for actual power-up image
        self.rect = self.image.get_rect(center=(x, y))
        self.spawn_time = pygame.time.get_ticks()
    def update(self):
        current_time = pygame.time.get_ticks()
        if current_time - self.spawn_time > 3000:  # 3000 milliseconds = 3 seconds
            self.kill()  # Remove the power-up after 3 seconds

