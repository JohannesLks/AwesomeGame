import pygame
import os
from settings import *
import random
from abc import ABC, abstractmethod




# Player class
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        # Load all the animation frames
        self.animation_frames = [player_img, player_throw_img1, player_throw_img2, player_throw_img3, player_throw_img4]
        self.current_frame = 0
        self.animating = False
        self.animation_speed = 100  # milliseconds per frame
        self.last_update = pygame.time.get_ticks()

        self.image = self.animation_frames[self.current_frame]
        self.rect = self.image.get_rect(midbottom=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 10))
        self.speed = PLAYER_SPEED
        self.health = 100
        self.score = 0
        self.ammo = 10  # Player starts with 10 ammunition
        self.ammo_boost_active = False
        self.ammo_boost_end_time = 0
        
    def start_animation(self):
        self.animating = True
        self.current_frame = 0  # Start from the first frame

    def update_animation(self):
        now = pygame.time.get_ticks()
        if self.animating and now - self.last_update > self.animation_speed:
            self.last_update = now
            self.current_frame += 1
            if self.current_frame == len(self.animation_frames):
                self.current_frame = 0  # Loop the animation
                self.animating = False  # Stop animating after one loop
            self.image = self.animation_frames[self.current_frame]

    def activate_ammo_boost(self):
        self.ammo_boost_active = True
        self.ammo_boost_end_time = pygame.time.get_ticks() + 10000  # 10 seconds from now

    def update(self, keys):
        self.update_animation()
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
        if self.ammo_boost_active and pygame.time.get_ticks() > self.ammo_boost_end_time:
            self.ammo_boost_active = False


# Enemy class

class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        # Decide the starting side (left or right)
        starting_side = random.choice(['left', 'right'])
        
        # Load the original image and flip it if necessary
        self.original_image = enemy_img
        self.image = pygame.transform.flip(self.original_image, True, False) if starting_side == 'left' else self.original_image
        self.rect = self.image.get_rect()

        # Set the initial x position and direction based on the starting side
        if starting_side == 'left':
            self.rect.x = -self.rect.width  # Start off-screen to the left
            self.direction = 1  # Move to the right
        else:
            self.rect.x = SCREEN_WIDTH  # Start off-screen to the right
            self.direction = -1  # Move to the left

        # Randomly choose the vertical position
        self.rect.y = random.randint(0, SCREEN_HEIGHT - self.rect.height)
        self.speed = ENEMY_SPEED

    def update(self):
        # Move horizontally at a constant speed
        self.rect.x += self.speed * self.direction
        
        # Remove the sprite when it moves off the screen
        if self.rect.right < 0 or self.rect.left > SCREEN_WIDTH:
            self.kill()  # Remove the enemy
            return True  # Indicate that an enemy has reached the edge
        return False

class Blocker(pygame.sprite.Sprite):
    def __init__(self, player_x, shooting_area):
        super().__init__()
        self.image = blocker_img
        self.rect = self.image.get_rect(center=(player_x, random.randint(shooting_area['top'], shooting_area['bottom'])))
        self.mask = pygame.mask.from_surface(self.image)  # Erstellen der Maske aus dem Bild
        self.spawn_time = pygame.time.get_ticks()  # Record the spawn time

    def update(self):
        current_time = pygame.time.get_ticks()
        if current_time - self.spawn_time > 10000:  # 10 seconds in milliseconds
            self.kill()  # Despawn the blocker



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
    def __init__(self, power_up_type, x, y):
        super().__init__()
        attributes = POWER_UPS_ATTRIBUTES[power_up_type]
        self.type = power_up_type
        self.image = pygame.image.load(attributes['image'])
        self.rect = self.image.get_rect(center=(x, y))
        self.effect = attributes['effect']
        self.half_width = self.image.get_width() // 2  # Half-width of the power-up image
        self.spawn_time = pygame.time.get_ticks()

        
    def update(self):
        current_time = pygame.time.get_ticks()
        if current_time - self.spawn_time > 4000:  # 4000 milliseconds = 4 seconds
            self.kill()  # Remove the power-up after 3 seconds
    

