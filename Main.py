# Based on the provided outline, here is the Python code for the game "Krabs' Burger-Battle: Die Geldfischjagd"

# Import necessary modules
import pygame
import random

# Initialize the pygame
pygame.init()

# Constants for the game
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 563
PLAYER_SPEED = 5
ENEMY_SPAWN_RATE = 60  # Lower number means more frequent spawns
POWER_UP_RATE = 500    # Lower number means more frequent power-ups
SCORE_MULTIPLIER = 2   # For X2-Boost power-up

# Define colors
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# Load game assets
player_img = pygame.image.load('mr_krabs.png')
enemy_img = pygame.image.load('blowfish.png')
burger_img = pygame.image.load('burger.png')
background_img = pygame.image.load('bikini_bottom.png')

# Background music and sound effects
pygame.mixer.music.load('background_music.mp3')
pygame.mixer.music.play(-1)  # Play the music indefinitely
money_sound = pygame.mixer.Sound('money_sound.mp3')

# Set up the screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Krabs' Burger-Battle: Die Geldfischjagd")

# Use pygame's event system to create a custom event for ammo regeneration
AMMO_REGEN_EVENT = pygame.USEREVENT + 1
pygame.time.set_timer(AMMO_REGEN_EVENT, 2000)  # Set a timer to trigger every 5 seconds

# Player class
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        # Inside the Player class __init__ method
        self.image = pygame.transform.scale(player_img, (100, 60))  # Resize to appropriate dimensions
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
        if self.type == 'score_boost':
            self.image = pygame.image.load('boost.png')
        elif self.type == 'speed_boost':
            self.image = pygame.image.load('boost.png')
        elif self.type == 'health_boost':
            self.image = pygame.image.load('boost.png')
        self.rect = self.image.get_rect(center=(x, y))

    def update(self):
        # Power-ups just float in the air, they don't move
        pass

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
        for burger in burgers:
            hit_enemies = pygame.sprite.spritecollide(burger, enemies, False, pygame.sprite.collide_mask)
            for enemy in hit_enemies:
                enemy.kill()
                burger.kill()
                player.score += 10
                money_sound.play()

        for event in pygame.event.get():
            if event.type == AMMO_REGEN_EVENT:
                regenerate_ammo(player)
        

        # Check for power-up collection
        for power_up in pygame.sprite.spritecollide(player, power_ups, True):
            if power_up.type == 'score_boost':
                player.score *= SCORE_MULTIPLIER
            elif power_up.type == 'speed_boost':
                player.speed += 2  # Increase speed temporarily
            elif power_up.type == 'health_boost':
                player.health += 20  # Increase health

        # Drawing everything on the screen
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


        # Spawn enemies and power-ups
        # Inside the main game loop
        spawn_enemies(enemies, player.rect)
        spawn_power_ups(power_ups)

        # Update the display
        pygame.display.flip()
except Exception as e:
    print(e)
    running = False

# Quit the game
pygame.quit()
