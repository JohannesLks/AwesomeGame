import pygame
import random
from settings import *
import math
pygame.mixer.init()
STANDARD_DESTROY_SOUND = 'media/money.mp3'
ADVANCED_DESTROY_SOUND = 'media/money.mp3'

player_images = [pygame.image.load(f'media/mr_krabs{i}.png') for i in range(4)]
enemy_image = pygame.image.load('media/fish.png')
advanced_enemy_image = pygame.image.load('media/fish2.png')
burger_image = pygame.image.load('media/burger.png')
blocker_image = pygame.image.load('media/Plankton.png')
power_up_images = {
    'score_boost': pygame.image.load('media/moneyboost.png'),
    'ammo_boost': pygame.image.load('media/ammoboost.png'),
    'health_boost': pygame.image.load('media/healthboost.png'),
}

# Abstract Factory Interface
class SpriteFactory:
    @staticmethod
    def create_player():
        raise NotImplementedError

    @staticmethod
    def create_enemy():
        raise NotImplementedError

    @staticmethod
    def create_burger(x, y):
        raise NotImplementedError

    @staticmethod
    def create_power_up(power_up_type, x, y):
        raise NotImplementedError

# Concrete Factory
class GameSpriteFactory(SpriteFactory):
    @staticmethod
    def create_player(*args, **kwargs):
        return Player(player_images=player_images, speed=PLAYER_SPEED, *args, **kwargs)

    @staticmethod
    def create_enemy(enemy_type, *args, **kwargs):
        if enemy_type == "standard":
            return StandardEnemy(enemy_image=enemy_image, speed=STANDARD_ENEMY_SPEED, *args, **kwargs)
        elif enemy_type == "advanced":
            return AdvancedEnemy(enemy_image=advanced_enemy_image, speed=ADVANCED_ENEMY_SPEED, *args, **kwargs)
        else:
            raise ValueError("Unknown enemy type")

    @staticmethod
    def create_burger(x, y, *args, **kwargs):
        return Burger(x, y, burger_image=burger_image, *args, **kwargs)

    @staticmethod
    def create_power_up(power_up_type, x, y, *args, **kwargs):
        return PowerUp(power_up_type, x, y, power_up_images=power_up_images, *args, **kwargs)

    @staticmethod
    def create_blocker(player_x, top, bottom, *args, **kwargs):
        return Blocker(player_x, top, bottom, blocker_image=blocker_image, *args, **kwargs)

# Player class

class Player(pygame.sprite.Sprite):
    def __init__(self, player_images, speed, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.animation_frames = player_images
        self.current_frame = 0
        self.animating = False
        self.animation_speed = 100  # milliseconds per frame
        self.last_update = pygame.time.get_ticks()
        self.image = self.animation_frames[self.current_frame]
        self.rect = self.image.get_rect(midbottom=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 10))
        self.speed = speed
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
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH
        if self.ammo_boost_active and pygame.time.get_ticks() > self.ammo_boost_end_time:
            self.ammo_boost_active = False

# Enemy class
class BaseEnemy(pygame.sprite.Sprite):
    def __init__(self, enemy_image, speed, *args, **kwargs):
        self.hitpoints = kwargs.pop('hitpoints', 1)  # Extract hitpoints and remove it from kwargs
        self.destroy_sound = kwargs.pop('destroy_sound', None)  # Extract destroy_sound and remove it from kwargs
        self.score_value = kwargs.pop('score_value', 10)  # Extract score_value
        super().__init__()
        self.starting_side = random.choice(['left', 'right'])
        self.original_image = enemy_image
        self.image = pygame.transform.flip(self.original_image, True, False) if self.starting_side == 'left' else self.original_image
        self.rect = self.image.get_rect()
        self.speed = speed
        self.defeated_speed = 5 
        self.defeated = False
        if self.starting_side == 'left':
            self.rect.x = -self.rect.width
            self.speed = abs(self.speed)
        else:
            self.rect.x = SCREEN_WIDTH
            self.speed = -abs(self.speed)
        # Additional attributes for sine wave movement
        self.sine_wave_amplitude = kwargs.pop('amplitude', 10) # Adjust this value to control the height of the wave
        self.sine_wave_frequency = kwargs.pop('frequency', 0.01)  # Adjust this value to control the frequency
        self.angle = 0
        self.initial_y = random.randint(0, SCREEN_HEIGHT - (self.rect.height + player_images[0].get_height() + self.sine_wave_amplitude))

    def update(self):
        # Update x-coordinate as before
        self.rect.x += self.speed

        # Update y-coordinate based on a sine wave
        self.rect.y = self.initial_y + self.sine_wave_amplitude * math.sin(self.sine_wave_frequency * self.rect.x)

        # Berechne den Neigungswinkel basierend auf der Ableitung der Sinusfunktion
        self.angle = math.degrees(math.atan(self.sine_wave_amplitude * self.sine_wave_frequency * math.cos(self.sine_wave_frequency * self.rect.x)))

        # Spiegle und neige das Bild basierend auf der Bewegungsrichtung
        if self.starting_side == 'left':
            self.image = pygame.transform.flip(self.original_image, True, False)
            self.image = pygame.transform.rotate(self.image, -self.angle)
        else:
            self.image = pygame.transform.rotate(self.original_image, self.angle)

        # Check if the enemy is out of screen
        if self.rect.right < 0 or self.rect.left > SCREEN_WIDTH:
            self.kill()
            return True

    def take_damage(self, damage, player_position):
            self.hitpoints -= damage
            if self.hitpoints <= 0:
                if self.destroy_sound:
                    pygame.mixer.Sound(self.destroy_sound).play()
                if self.hitpoints <= 0 and not self.defeated:
                    self.change_to_defeated_state(player_position)
                    return True

    def change_to_defeated_state(self, player_position):
        # Mark the enemy as defeated
        self.defeated = True

        # Change the image to a defeated state image
        self.image = pygame.image.load('media/coin.png')

        # Store player position for curved movement
        self.target_position = player_position

        # Override the update method to move towards the player
        self.update = self.update_defeated_state

    def update_defeated_state(self):
        # Calculate the direction towards the target position
        target_vector = pygame.math.Vector2(self.target_position[0] - self.rect.x, self.target_position[1] - self.rect.y)
        distance = target_vector.length()
        target_vector.normalize_ip()

        # If close to the player, reduce speed for a smooth stop
        if distance < 100:
            self.defeated_speed = max(1, self.speed * 0.95)

        # Move in a curve by adjusting the direction vector
        curve_strength = 2  # Adjust this value for more or less curvature
        direction = pygame.math.Vector2(target_vector.y, -target_vector.x) * curve_strength
        movement = target_vector * self.defeated_speed + direction
        self.rect.x += movement.x
        self.rect.y += movement.y

        # Check if the enemy has reached near the player position
        if distance < 10:  # Adjust this threshold as needed
            self.kill()
    
class StandardEnemy(BaseEnemy):
    def __init__(self, enemy_image, speed, *args, **kwargs):
        super().__init__(enemy_image=enemy_image, speed=STANDARD_ENEMY_SPEED, hitpoints=STANDARD_HITPOINTS, amplitude = 1, frequency = 0.07, *args, **kwargs)

class AdvancedEnemy(BaseEnemy):
    def __init__(self, enemy_image, speed, *args, **kwargs):
        super().__init__(enemy_image=advanced_enemy_image, speed=ADVANCED_ENEMY_SPEED, hitpoints=ADVANCED_HITPOINTS, destroy_sound=ADVANCED_DESTROY_SOUND, score_value=ADVANCED_ENEMY_SCORE_VALUE, *args, **kwargs)


# Burger class
class Burger(pygame.sprite.Sprite):
    def __init__(self, x, y, burger_image, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.image = burger_image
        self.rect = self.image.get_rect(center=(x, y))

    def update(self):
        self.rect.y -= 5
        if self.rect.bottom < 0:
            self.kill()

# PowerUp class
class PowerUp(pygame.sprite.Sprite):
    def __init__(self, power_up_type, x, y, power_up_images, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.type = power_up_type
        self.image = power_up_images[power_up_type]
        self.rect = self.image.get_rect(center=(x, y))
        self.effect = POWER_UPS_ATTRIBUTES[power_up_type]['effect']
        self.spawn_time = pygame.time.get_ticks()
        self.destroy_sound = kwargs.pop('destroy_sound', None)

    def update(self):
        current_time = pygame.time.get_ticks()
        if current_time - self.spawn_time > 4000:  # 4000 milliseconds = 4 seconds
            self.kill()


class Blocker(pygame.sprite.Sprite):
    def __init__(self, player_x, top, bottom, *args, **kwargs):
        super().__init__()
        self.image =  kwargs.pop('blocker_image')
        self.rect = self.image.get_rect(center=(player_x, random.randint(top, bottom)))
        self.mask = pygame.mask.from_surface(self.image)
        self.spawn_time = pygame.time.get_ticks()