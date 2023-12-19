import pygame
import random
from settings import *
import sys
import os
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

class GameSpriteFactory(SpriteFactory):
    """
    Eine Klasse, die ein Factory-Pattern für Spiel-Sprites implementiert.
    """

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


class Player(pygame.sprite.Sprite):
    def __init__(self, player_images, speed, *args, **kwargs):
        """
        Initialisiert ein Player-Objekt.

        :param player_images: Eine Liste von Bildern für die Animation des Spielers. (list)
        :type player_images: list
        :param speed: Die Geschwindigkeit des Spielers. (int)
        :type speed: int
        :param args: Positionale Argumente für die übergeordnete Klasse. (*args)
        :param kwargs: Schlüsselwortargumente für die übergeordnete Klasse. (**kwargs)
        """
        super().__init__(*args, **kwargs)
        self.animation_frames = player_images
        self.current_frame = 0
        self.animating = False
        self.animation_speed = 100
        self.last_update = pygame.time.get_ticks()
        self.image = self.animation_frames[self.current_frame]
        self.rect = self.image.get_rect(midbottom=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 10))
        self.speed = speed
        self.health = 100
        self.score = 0
        self.ammo = 10
        self.ammo_boost_active = False
        self.ammo_boost_end_time = 0

    def start_animation(self):
        """
        Startet die Animation des Spielers.
        """
        self.animating = True
        self.current_frame = 0

    def update_animation(self):
        """
        Aktualisiert die Animation des Spielers.
        """
        now = pygame.time.get_ticks()
        if self.animating and now - self.last_update > self.animation_speed:
            self.last_update = now
            self.current_frame += 1
            if self.current_frame == len(self.animation_frames):
                self.current_frame = 0
                self.animating = False
            self.image = self.animation_frames[self.current_frame]

    def activate_ammo_boost(self):
        """
        Aktiviert den Munitionsboost des Spielers für eine bestimmte Zeit.
        """
        self.ammo_boost_active = True
        self.ammo_boost_end_time = pygame.time.get_ticks() + 10000

    def update(self, keys):
        """
        Aktualisiert den Spieler basierend auf den gedrückten Tasten.

        :param keys: Ein Dictionary, das die Zustände der Tasten enthält.
        """
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

class BaseEnemy(pygame.sprite.Sprite):
    def __init__(self, enemy_image, speed, *args, **kwargs):
        """
        Initialisiert eine BaseEnemy-Instanz.

        :param enemy_image: Das Bild des Gegners.
        :param speed: Die Geschwindigkeit des Gegners.
        :param args: Zusätzliche argumente.
        :param kwargs: Zusätzliche Schlüsselwortargumente.
        """
        self.hitpoints = kwargs.pop('hitpoints', 1)
        self.destroy_sound = kwargs.pop('destroy_sound', None)
        self.score_value = kwargs.pop('score_value', 10)
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
        self.sine_wave_amplitude = kwargs.pop('amplitude', 10)
        self.sine_wave_frequency = kwargs.pop('frequency', 0.01)
        self.angle = 0
        self.initial_y = random.randint(0, SCREEN_HEIGHT - (self.rect.height + player_images[0].get_height() + self.sine_wave_amplitude))       

    def update(self):
        """
        Aktualisiert den Zustand des Gegners.
        """
        self.rect.x += self.speed
        self.rect.y = self.initial_y + self.sine_wave_amplitude * math.sin(self.sine_wave_frequency * self.rect.x)

        self.angle = math.degrees(math.atan(self.sine_wave_amplitude * self.sine_wave_frequency * math.cos(self.sine_wave_frequency * self.rect.x)))

        if self.starting_side == 'left':
            self.image = pygame.transform.flip(self.original_image, True, False)
            self.image = pygame.transform.rotate(self.image, -self.angle)
        else:
            self.image = pygame.transform.rotate(self.original_image, self.angle)

        if self.rect.right < 0 or self.rect.left > SCREEN_WIDTH:
            self.kill()
            return True

    def take_damage(self, damage, player_position):
        """
        Fügt dem Gegner Schaden zu.

        :param damage: Der Schaden, der dem Gegner zugefügt wird.
        :param player_position: Die Position des Spielers.
        :return: True, wenn der Gegner besiegt wurde, sonst False.
        """
        self.hitpoints -= damage
        if self.hitpoints <= 0:
            if self.destroy_sound:
                pygame.mixer.Sound(self.destroy_sound).play()
            if self.hitpoints <= 0 and not self.defeated:
                self.change_to_defeated_state(player_position)
                return True

    def change_to_defeated_state(self, player_position):
        """
        Ändert den Zustand des Gegners in den besiegt-Zustand.

        :param player_position: Die Position des Spielers.
        """
        self.defeated = True
        self.image = pygame.image.load('media/coin.png')
        self.target_position = player_position
        self.update = self.update_defeated_state

    def update_defeated_state(self):
        """
        Aktualisiert den Zustand des Gegners im besiegt-Zustand.
        """
        target_vector = pygame.math.Vector2(self.target_position[0] - self.rect.x, self.target_position[1] - self.rect.y)
        distance = target_vector.length()
        target_vector.normalize_ip()

        if distance < 100:
            self.defeated_speed = max(1, self.speed * 0.95)

        curve_strength = 2
        direction = pygame.math.Vector2(target_vector.y, -target_vector.x) * curve_strength
        movement = target_vector * self.defeated_speed + direction
        self.rect.x += movement.x
        self.rect.y += movement.y

        if distance < 10:
            self.kill()
    
class StandardEnemy(BaseEnemy):
    """
    Eine Klasse, die einen Standard-Gegner im Spiel repräsentiert.

    Args:
        enemy_image (str): Der Pfad zum Bild des Gegners.
        speed (int): Die Geschwindigkeit des Gegners.
        *args: Variable Argumente.
        **kwargs: Schlüsselwortargumente.

    Attributes:
        enemy_image (str): Der Pfad zum Bild des Gegners.
        speed (int): Die Geschwindigkeit des Gegners.
        hitpoints (int): Die Trefferpunkte des Gegners.
        amplitude (int): Die Amplitude der Bewegung des Gegners.
        frequency (float): Die Frequenz der Bewegung des Gegners.
    """

    def __init__(self, enemy_image, speed, *args, **kwargs):
        super().__init__(enemy_image=enemy_image, speed=STANDARD_ENEMY_SPEED, hitpoints=STANDARD_HITPOINTS, amplitude=1, frequency=0.07, *args, **kwargs)

class AdvancedEnemy(BaseEnemy):
    """
    Fortgeschrittener Gegner-Klasse.

    Diese Klasse repräsentiert einen fortgeschrittenen Gegner im Spiel.
    Er erbt von der BaseEnemy-Klasse und hat zusätzliche Eigenschaften wie Geschwindigkeit, Trefferpunkte, Zerstörungssound und Punktwert.

    Args:
        enemy_image (str): Der Pfad zum Bild des Gegners.
        speed (int): Die Geschwindigkeit des Gegners.
        *args: Variable Argumente für die BaseEnemy-Klasse.
        **kwargs: Variable Schlüsselwortargumente für die BaseEnemy-Klasse.

    Attributes:
        enemy_image (str): Der Pfad zum Bild des Gegners.
        speed (int): Die Geschwindigkeit des Gegners.
        hitpoints (int): Die Trefferpunkte des Gegners.
        destroy_sound (str): Der Soundeffekt beim Zerstören des Gegners.
        score_value (int): Der Punktwert des Gegners.
    """

    def __init__(self, enemy_image, speed, *args, **kwargs):
        super().__init__(enemy_image=advanced_enemy_image, speed=ADVANCED_ENEMY_SPEED, hitpoints=ADVANCED_HITPOINTS, destroy_sound=ADVANCED_DESTROY_SOUND, score_value=ADVANCED_ENEMY_SCORE_VALUE, *args, **kwargs)

class Burger(pygame.sprite.Sprite):
    def __init__(self, x, y, burger_image, *args, **kwargs):
        """
        Initialisiert ein Burger-Objekt.

        :param x: Die x-Koordinate der Position des Burgers.
        :param y: Die y-Koordinate der Position des Burgers.
        :param burger_image: Das Bild des Burgers.
        :param args: Zusätzliche nicht benannte Argumente.
        :param kwargs: Zusätzliche benannte Argumente.
        """
        super().__init__(*args, **kwargs)
        self.image = burger_image
        self.rect = self.image.get_rect(center=(x, y))

    def update(self):
        """
        Aktualisiert die Position des Burgers.

        Der Burger bewegt sich nach oben und wird entfernt, wenn er den oberen Bildschirmrand erreicht.

        :return: None
        """
        self.rect.y -= 5
        if self.rect.bottom < 0:
            self.kill()

class PowerUp(pygame.sprite.Sprite):
    def __init__(self, power_up_type, x, y, power_up_images, *args, **kwargs):
        """
        Erstellt eine PowerUp-Instanz.

        :param power_up_type: Der Typ des Power-Ups.
        :param x: Die x-Koordinate der Position des Power-Ups.
        :param y: Die y-Koordinate der Position des Power-Ups.
        :param power_up_images: Eine Sammlung von Bildern für verschiedene Power-Up-Typen.
        :param args: Zusätzliche Positional Arguments.
        :param kwargs: Zusätzliche Keyword Arguments.
        """
        super().__init__(*args, **kwargs)
        self.type = power_up_type
        self.image = power_up_images[power_up_type]
        self.rect = self.image.get_rect(center=(x, y))
        self.effect = POWER_UPS_ATTRIBUTES[power_up_type]['effect']
        self.spawn_time = pygame.time.get_ticks()
        self.destroy_sound = kwargs.pop('destroy_sound', None)

    def update(self):
        """
        Aktualisiert den Zustand des Power-Ups.
        Überprüft, ob das Power-Up seit mehr als 4 Sekunden existiert und entfernt es dann.
        """
        current_time = pygame.time.get_ticks()
        if current_time - self.spawn_time > 4000:
            self.kill()

class Blocker(pygame.sprite.Sprite):
    def __init__(self, player_x, top, bottom, *args, **kwargs):
        """
        Erstellt ein Blocker-Objekt.

        Args:
            player_x (int): Die x-Koordinate des Spielers.
            top (int): Die obere Grenze für die zufällige y-Koordinate.
            bottom (int): Die untere Grenze für die zufällige y-Koordinate.
            *args: Variable Argumente.
            **kwargs: Variable Schlüsselwortargumente.

        Attributes:
            image (pygame.Surface): Das Bild des Blockers.
            rect (pygame.Rect): Das Rechteck, das den Blocker umgibt.
            mask (pygame.Mask): Die Maske des Blockers für Kollisionserkennung.
            spawn_time (int): Die Zeit, zu der der Blocker erstellt wurde.
        """
        super().__init__()
        self.image = kwargs.pop('blocker_image')
        self.rect = self.image.get_rect(center=(player_x, random.randint(top, bottom)))
        self.mask = pygame.mask.from_surface(self.image)
        self.spawn_time = pygame.time.get_ticks()