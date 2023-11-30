import pygame
import random
from settings import *

player_images = [pygame.image.load(f'media/mr_krabs{i}.png') for i in range(4)]
enemy_images = {'enemy_type_1': pygame.image.load('media/fish.png'),
                'enemy_type_2': pygame.image.load('media/fish2.png'),
                #'enemy_type_3': pygame.image.load('media/fish4.png'),
                #'enemy_type_4': pygame.image.load('media/fish5.png')
}
burger_image = pygame.image.load('media/burger.png')
blocker_image = pygame.image.load('media/plankton.png')
power_up_images = {
    'score_boost': pygame.image.load('media/boost.png'),
    'ammo_boost': pygame.image.load('media/boost.png'),
    'health_boost': pygame.image.load('media/boost.png'),
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
    def create_enemy(*args, **kwargs):
        return Enemy(enemy_images=enemy_images, speed=ENEMY_SPEED, *args, **kwargs)

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
class Enemy(pygame.sprite.Sprite):
    def __init__(self, enemy_images, speed, *args, **kwargs):
        super().__init__(*args, **kwargs)
        starting_side = random.choice(['left', 'right'])
        enemy_type = random.choice(['enemy_type_1', 'enemy_type_2'])
        self.original_image = enemy_images[enemy_type]
        self.image = pygame.transform.flip(self.original_image, True, False) if starting_side == 'left' else self.original_image
        self.rect = self.image.get_rect()
        if starting_side == 'left':
            self.rect.x = -self.rect.width
            self.direction = 1
        else:
            self.rect.x = SCREEN_WIDTH
            self.direction = -1
        self.rect.y = random.randint(0, SCREEN_HEIGHT - self.rect.height)
        self.speed = ENEMY_SPEED

    def update(self):
        self.rect.x += self.speed * self.direction
        if self.rect.right < 0 or self.rect.left > SCREEN_WIDTH:
            self.kill()
            return True
        return False

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

    def update(self):
        current_time = pygame.time.get_ticks()
        if current_time - self.spawn_time > 4000:  # 4000 milliseconds = 4 seconds
            self.kill()

class Blocker(pygame.sprite.Sprite):
    def __init__(self, player_x, top, bottom, blocker_image, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.image = blocker_image
        self.rect = self.image.get_rect(center=(player_x, random.randint(top, bottom)))
        self.mask = pygame.mask.from_surface(self.image)
        self.spawn_time = pygame.time.get_ticks()