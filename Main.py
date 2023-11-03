# Import necessary modules
import pygame
import random
import sys
import os
import csv
from datetime import datetime
from settings import *
from sprites import *

# Initialize pygame
pygame.init()

# Centralized resources
FONT_SIZE = 32
FONT = pygame.font.Font(None, FONT_SIZE)
BUTTON_FONT = pygame.font.Font(None, 36)
BIG_FONT = pygame.font.SysFont(None, 80)
REGULAR_FONT = pygame.font.SysFont(None, 36)

# Sound effects
BACKGROUND_MUSIC = 'media/background_music.mp3'
MONEY_SOUND = 'media/money_sound.mp3'
pygame.mixer.music.load(BACKGROUND_MUSIC)
pygame.mixer.music.play(-1)
money_sound = pygame.mixer.Sound(MONEY_SOUND)

# Screen setup
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Krabs' Burger-Battle: Die Geldfischjagd")

# Custom events
AMMO_REGEN_EVENT = pygame.USEREVENT + 1
pygame.time.set_timer(AMMO_REGEN_EVENT, 2000)

def handle_input_events(event, input_text, input_box_active, input_box_rect):
    if event.type == pygame.MOUSEBUTTONDOWN:
        # If the user clicked on the input_box rect.
        if input_box_rect.collidepoint(event.pos):
            # Toggle the active variable.
            input_box_active = not input_box_active
        else:
            input_box_active = False
    elif event.type == pygame.KEYDOWN:
        if input_box_active:
            if event.key == pygame.K_RETURN:
                print(input_text)  # Do something with the input text here.
                input_text = ''  # Reset the input text.
            elif event.key == pygame.K_BACKSPACE:
                input_text = input_text[:-1]
            else:
                input_text += event.unicode
    return input_text, input_box_active
def create_button(screen, image, image_hover, x, y, text='', text_color=BLACK, font_size=FONT_SIZE):
    button_rect = image.get_rect(topleft=(x, y))
    mouse = pygame.mouse.get_pos()
    clicked = pygame.mouse.get_pressed()[0]
    button_image = image_hover if button_rect.collidepoint(mouse) else image

    # Draw button image
    screen.blit(button_image, button_rect)

    # Text on button
    if text:
        font = pygame.font.Font(None, font_size)
        text_surf = font.render(text, True, text_color)
        text_rect = text_surf.get_rect(center=button_rect.center)
        screen.blit(text_surf, text_rect)

    return button_rect, button_rect.collidepoint(mouse) and clicked


# Funktion zum Erstellen von Text
def text_objects(text, font):
    text_surface = font.render(text, True, BLACK)  # BLACK is a color constant
    return text_surface, text_surface.get_rect()

# Startbildschirm anzeigen
def show_start_screen(screen):
    try:
        # Define button positions and sizes once, outside of the loop.
        start_button_x = SCREEN_WIDTH / 2 - BUTTON_WIDTH / 2 - BUTTON_SPACING / 2 - BUTTON_WIDTH
        quit_button_x = SCREEN_WIDTH / 2 + BUTTON_SPACING / 2
        button_y = BUTTON_Y_OFFSET


        quit_button_rect = create_button(screen, quit_button_img, quit_button_hover_img, quit_button_x, button_y, text='Quit')
        start_button_rect, _ = create_button(screen, start_button_img, start_button_hover_img, start_button_x, button_y, text='Start')

        input_text = ''
        input_box_active = False
        input_box_x = SCREEN_WIDTH / 2 - INPUT_WIDTH / 2
        input_box_y = INPUT_BOX_Y_OFFSET
    
        # Main loop for the start screen.
        running = True
        while running:
            screen.blit(welcome_background_img, (0, 0))
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    # This should be the tuple unpacking the return of create_button
                    start_button_rect, start_button_clicked = create_button(screen, start_button_img, start_button_hover_img, start_button_x, button_y, text='Start')
                    if start_button_rect.collidepoint(event.pos):
                        main_game(input_text)  # Call the function or code to start the game
                    quit_button_rect, quit_button_clicked = create_button(screen, quit_button_img, quit_button_hover_img, quit_button_x, button_y, text='Quit')
                    if quit_button_rect.collidepoint(event.pos):
                        running = False
                        pygame.quit()
                        sys.exit()
                # Handle input events for the input box
                input_text, input_box_active = handle_input_events(event, input_text, input_box_active, input_box_rect)

            # Create the start and quit buttons
            start_button_rect = create_button(screen, start_button_img, start_button_hover_img, start_button_x, button_y, text='Start')
            quit_button_rect = create_button(screen, quit_button_img, quit_button_hover_img, quit_button_x, button_y, text='Quit')
            
            # Handle the input box drawing and interaction here
            input_text, input_box_active, input_box_rect = input_box(
                screen,
                input_box_x,
                input_box_y,
                INPUT_WIDTH,
                INPUT_HEIGHT,
                input_text,
                input_box_active,
                FONT,  # Pass the font object
                background_image=input_bg_image
            )
            pygame.display.flip()  # Update the screen

        return input_text  # Return the text entered by the user
    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        print(exc_type, fname, exc_tb.tb_lineno)
        running = False


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
def spawn_power_ups(power_up_group, player_rect):
    if random.randint(1, POWER_UP_RATE) == 1:
        safe_margin = 100
        power_up_x = random.randint(0, SCREEN_WIDTH)
        power_up_y = random.randint(0, SCREEN_HEIGHT)

        # Ensure the power-up does not spawn too close to the player
        while abs(power_up_y - player_rect.y) < safe_margin:
            power_up_y = random.randint(0, SCREEN_HEIGHT)

        power_up_type = random.choice(['score_boost', 'speed_boost', 'health_boost'])
        power_up = PowerUp(power_up_type, power_up_x, power_up_y)
        power_up_group.add(power_up)


def regenerate_ammo(player):
    if player.ammo < 10:
        player.ammo += 1  # Regenerate one ammo

def load_highscores(filename='highscores.csv'):
    highscores = []
    try:
        with open(filename, 'r', newline='') as file:
            reader = csv.reader(file)
            for row in reader:
                # Stellen Sie sicher, dass jede Zeile drei Elemente enthält: Name, Score, Datum
                if len(row) == 3:  
                    highscores.append(row)
            highscores.sort(key=lambda x: int(x[1]), reverse=True)
    except FileNotFoundError:
        with open(filename, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['Name', 'Score', 'Date'])
    return highscores


# Funktion zum Speichern der Highscores in der CSV-Datei
def save_highscore(name, score, filename='highscores.csv'):
    date_str = datetime.now().strftime('%Y-%m-%d %H:%M')
    with open(filename, 'a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([name, score, date_str])
        
def input_box(screen, x, y, w, h, text, active, font, background_image):
    # Define colors
    color_active = pygame.Color('black')
    color_inactive = pygame.Color('grey')
    color = color_active if active else color_inactive

    # Create the input box rectangle
    input_box_rect = pygame.Rect(x, y, w, h)

    # Draw the input box background image
    if background_image:
        input_bg_rect = background_image.get_rect(center=input_box_rect.center)
        screen.blit(background_image, input_bg_rect.topleft)

    # Check if the input box is active and the text is empty to display the placeholder
    if not active and not text:
        placeholder_text = "Name"
        txt_surface = font.render(placeholder_text, True, color_inactive)
    else:
        txt_surface = font.render(text, True, color)

    # Centralize the text inside the input box by calculating the position
    text_x = input_box_rect.x + (input_box_rect.w - txt_surface.get_width()) // 2
    text_y = input_box_rect.y + (input_box_rect.h - txt_surface.get_height()) // 2

    # Blit the text.
    screen.blit(txt_surface, (text_x, text_y))

    return text, active, input_box_rect




def handle_input_box_events(event, input_text, input_box_active):
    if event.type == pygame.MOUSEBUTTONDOWN:
        # If the user clicked on the input_box rect.
        if input_box.collidepoint(event.pos):
            # Toggle the active variable.
            input_box_active = not input_box_active
        else:
            input_box_active = False
    elif event.type == pygame.KEYDOWN:
        if input_box_active:
            if event.key == pygame.K_RETURN:
                print(input_text)  # Do something with the input text here.
                input_text = ''  # Reset the input text.
            elif event.key == pygame.K_BACKSPACE:
                input_text = input_text[:-1]
            else:
                input_text += event.unicode
    return input_text, input_box_active


# Funktion für den Startbildschirm
def start_screen(screen):
    running = True
    name = ''
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                return None  # Spiel wird nicht gestartet
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    running = False  # Starte das Spiel
                elif event.key == pygame.K_BACKSPACE:
                    name = name[:-1]
                else:
                    name += event.unicode
        screen.fill(WHITE)
        # Hier Code zum Anzeigen von Text, Highscores und Eingabefeld
        # ...
        pygame.display.flip()
    return name

# Funktion für den Game Over-Bildschirm
def game_over_screen(screen, score, player_name):
    try:
        screen.fill(WHITE)
        # Define the position for the start button on the game over screen
        start_button_x = SCREEN_WIDTH // 2 - start_button_img.get_width() // 2
        start_button_y = SCREEN_HEIGHT - start_button_img.get_height() - 100

        # Create a Rect for the start button
        start_button_rect = pygame.Rect(start_button_x, start_button_y, start_button_img.get_width(), start_button_img.get_height())
    # Define font for the button text
        button_font = pygame.font.Font(None, 36)  # Adjust the font size as needed
        text_color = (0, 0, 0)  # White color for the text
        button_text = "New Game"
        button_text = "New Game"
        text_surf = button_font.render(button_text, True, text_color)
        text_rect = text_surf.get_rect(center=start_button_rect.center)

        # Stop the current background music and play the game over music
        pygame.mixer.music.stop()
        pygame.mixer.music.load('media/background_music.mp3')  # Ensure you have this file in your media directory
        pygame.mixer.music.play(-1)  # Play the music indefinitely

        big_font = pygame.font.SysFont(None, 80)  # A larger font for "Game Over" title
        font = pygame.font.SysFont(None, 36)  # Regular font for scores
       

        # Load high scores and save the current score
        highscores = load_highscores()
        save_highscore(player_name, score)
        highscores = load_highscores()  # Reload highscores to include the latest one

        # Display the player's score
        your_score_surf = font.render(f'Your Score: {score}', True, RED)
        your_score_rect = your_score_surf.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 50))
        screen.blit(your_score_surf, your_score_rect)

        running = True
        while running:
            # Event handling loop
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:  # Left click
                    if start_button_rect.collidepoint(event.pos):
                        # The button was clicked, start the game
                        main_game(player_name)
                        running = False

            # Clear the screen
            screen.fill(WHITE)
            # Display "Game Over" text
            game_over_surf = big_font.render('Game Over', True, BLACK)
            game_over_rect = game_over_surf.get_rect(center=(SCREEN_WIDTH // 2, 50))
            screen.blit(game_over_surf, game_over_rect)

            # Display the title for highscores
            title_surf = font.render('High Scores', True, BLACK)
            title_rect = title_surf.get_rect(center=(SCREEN_WIDTH // 2, 120))
            screen.blit(title_surf, title_rect)

            # Display each high score
            for index, highscore in enumerate(highscores[:5]):  # Show top 5 high scores
                score_text = f"{index + 1}. {highscore[0]} - {highscore[1]} - {highscore[2]}"
                score_surf = font.render(score_text, True, BLACK)
                score_rect = score_surf.get_rect(center=(SCREEN_WIDTH // 2, 160 + index * 40))
                screen.blit(score_surf, score_rect)

                
            mouse_pos = pygame.mouse.get_pos()
            button_image = start_button_hover_img if start_button_rect.collidepoint(mouse_pos) else start_button_img
            screen.blit(button_image, start_button_rect.topleft)

            # Draw the button text
            button_text = "New Game"
            text_surf = button_font.render(button_text, True, text_color)
            text_rect = text_surf.get_rect(center=start_button_rect.center)
            screen.blit(text_surf, text_rect)


            # Update the display
            pygame.display.flip()
    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        print(exc_type, fname, exc_tb.tb_lineno)
        running = False


def main_game(player_name):
    try:
        # Main game loop
        running = True
        clock = pygame.time.Clock()
        player = Player()
        players = pygame.sprite.Group()
        players.add(player)
        enemies = pygame.sprite.Group()
        burgers = pygame.sprite.Group()
        power_ups = pygame.sprite.Group()


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
                        game_over_screen(screen, player.score, player_name)
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

            #Ammunation regeneration
            for event in pygame.event.get():
                if event.type == AMMO_REGEN_EVENT:
                    regenerate_ammo(player)
        

            # Spawn enemies and power-ups
            spawn_enemies(enemies, player.rect)
            spawn_power_ups(power_ups, player.rect)

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
# Spiel beenden
def quit_game():
    pygame.quit()
    quit()

# Hauptfunktion, die das Spiel startet
def game_intro():
    try:
        intro = True
        while intro:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
            player_name = show_start_screen(screen)
            if player_name is None:  # Überprüft, ob die input_box None zurückgibt
                intro = False  # Beendet die Schleife und damit das Intro
            else:
                main_game(player_name)  # Startet das Hauptspiel
                intro = False  # Beendet die Intro-Schleife, nachdem das Spiel beendet wurde

    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        print(exc_type, fname, exc_tb.tb_lineno)
        running = False


game_intro()       

import pygame
import random
import sys
import os
import csv
from datetime import datetime
from settings import *
from sprites import *

# Initialize pygame
pygame.init()

# Centralized resources
FONT_SIZE = 32
FONT = pygame.font.Font(None, FONT_SIZE)
BUTTON_FONT_SIZE = 36
BUTTON_FONT = pygame.font.Font(None, BUTTON_FONT_SIZE)
LARGE_FONT_SIZE = 80
LARGE_FONT = pygame.font.SysFont(None, LARGE_FONT_SIZE)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# Sound effects
pygame.mixer.music.load('media/background_music.mp3')
pygame.mixer.music.play(-1)  # Play the music indefinitely
money_sound = pygame.mixer.Sound('media/money_sound.mp3')

# Screen setup
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Krabs' Burger-Battle: Die Geldfischjagd")

# Custom events
AMMO_REGEN_EVENT = pygame.USEREVENT + 1
pygame.time.set_timer(AMMO_REGEN_EVENT, 2000)

# Centralize button and input box creation
def create_interactive_element(screen, element_type, image, image_hover, x, y, text='', text_color=BLACK, font=FONT, input_box_rect=None, input_bg_image=None):
    if element_type == 'button':
        button_rect = image.get_rect(topleft=(x, y))
        mouse = pygame.mouse.get_pos()
        clicked = pygame.mouse.get_pressed()[0]
        button_image = image_hover if button_rect.collidepoint(mouse) else image

        screen.blit(button_image, button_rect)

        if text:
            text_surf = font.render(text, True, text_color)
            text_rect = text_surf.get_rect(center=button_rect.center)
            screen.blit(text_surf, text_rect)

        return button_rect, button_rect.collidepoint(mouse) and clicked
    elif element_type == 'input_box':
        if input_bg_image:
            input_bg_rect = input_bg_image.get_rect(topleft=(input_box_rect.x, input_box_rect.y))
            screen.blit(input_bg_image, input_bg_rect)

        active_color = pygame.Color('dodgerblue2') if input_box_rect.active else pygame.Color('lightskyblue3')
        pygame.draw.rect(screen, active_color, input_box_rect, 2)
        text_surf = font.render(text, True, active_color)
        screen.blit(text_surf, (input_box_rect.x + 5, input_box_rect.y + 5))
        return text

# Event handling
def handle_events(event, input_text, input_box_active, input_box_rect):
    if event.type == pygame.MOUSEBUTTONDOWN:
        if input_box_rect.collidepoint(event.pos):
            input_box_active = not input_box_active
        else:
            input_box_active = False
    elif event.type == pygame.KEYDOWN:
        if input_box_active:
            if event.key == pygame.K_RETURN:
                print(input_text)  # Do something with the input text here.
                input_text = ''
            elif event.key == pygame.K_BACKSPACE:
                input_text = input_text[:-1]
            else:
                input_text += event.unicode
    return input_text, input_box_active

# Enemy and Power-Up Spawning
def spawn_entities(entity_group, entity_class, player_rect, spawn_chance, safe_margin=100):
    if random.randint(1, spawn_chance) == 1:
        entity = entity_class()
        entity.rect.x = random.randint(0, SCREEN_WIDTH - entity.rect.width)
        entity.rect.y = random.randint(0, SCREEN_HEIGHT - entity.rect.height)
        while abs(entity.rect.y - player_rect.y) < safe_margin:
            entity.rect.y = random.randint(0, SCREEN_HEIGHT - entity.rect.height)
        entity_group.add(entity)

# Highscore Management
def manage_highscores(action, score=None, name=None, filename='highscores.csv'):
    if action == 'load':
        highscores = []
        try:
            with open(filename, 'r', newline='') as file:
                reader = csv.reader(file)
                for row in reader:
                    if len(row) == 3:
                        highscores.append(row)
                highscores.sort(key=lambda x: int(x[1]), reverse=True)
        except FileNotFoundError:
            with open(filename, 'w', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(['Name', 'Score', 'Date'])
        return highscores
    elif action == 'save':
        date_str = datetime.now().strftime('%Y-%m-%d %H:%M')
        with open(filename, 'a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([name, score, date_str])

# Display Screens
def display_screen(screen, screen_type, player_name='', score=0):
    running = True
    while running:
        screen.fill(WHITE)
        if screen_type == 'start':
            start_button_rect, start_button_clicked = create_interactive_element(
                screen, 'button', start_button_img, start_button_hover_img,
                SCREEN_WIDTH // 2 - BUTTON_WIDTH // 2, SCREEN_HEIGHT // 2,
                text='Start', text_color=BLACK, font=BUTTON_FONT
            )
            if start_button_clicked:
                main_game(player_name)  # Start the main game with the given player name
                running = False

        elif screen_type == 'game_over':
            game_over_text = LARGE_FONT.render('Game Over', True, BLACK)
            game_over_rect = game_over_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 4))
            screen.blit(game_over_text, game_over_rect)

            score_text = FONT.render(f'Your Score: {score}', True, BLACK)
            score_rect = score_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
            screen.blit(score_text, score_rect)

            restart_button_rect, restart_button_clicked = create_interactive_element(
                screen, 'button', start_button_img, restart_button_hover_img,
                SCREEN_WIDTH // 2 - BUTTON_WIDTH // 2, SCREEN_HEIGHT // 2 + BUTTON_HEIGHT,
                text='Restart', text_color=BLACK, font=BUTTON_FONT
            )
            if restart_button_clicked:
                main_game(player_name)  # Restart the main game
                running = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                sys.exit()

        pygame.display.flip()


# Initialize the game loop
def main_game(player_name):
    running = True
    clock = pygame.time.Clock()
    player = Player()
    enemies = pygame.sprite.Group()
    bullets = pygame.sprite.Group()
    power_ups = pygame.sprite.Group()

    while running:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == AMMO_REGEN_EVENT:
                player.ammo += 1
            else:
                input_text, input_box_active = handle_events(event, player.name, False, pygame.Rect(0, 0, 0, 0))
                player.name = input_text

        spawn_entities(enemies, Enemy, player.rect, ENEMY_SPAWN_RATE)
        spawn_entities(power_ups, PowerUp, player.rect, POWER_UP_RATE)

        enemies.update()
        bullets.update()
        power_ups.update()

        screen.fill(WHITE)
        enemies.draw(screen)
        bullets.draw(screen)
        power_ups.draw(screen)

        pygame.display.flip()

    pygame.quit()
    sys.exit()

# Starting point of the game
def game_intro():
    intro = True
    player_name = ''
    while intro:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            else:
                player_name, _ = handle_events(event, player_name, False, pygame.Rect(0, 0, 0, 0))

        screen.fill(WHITE)
        BUTTON_FONT.render_to(screen, (100, 100), "Press any key to start", BLACK)
        pygame.display.flip()

        if player_name:  # Assuming player name is used as a start trigger
            intro = False
            main_game(player_name)

# Start the game
game_intro()
