# Import necessary modules
import pygame
import random
import sys
import os
import csv
import time
from datetime import datetime
from settings import *
from sprites import *

running = True
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

player_height = player_img.get_height()  # Assuming player_img is the player's sprite image
buffer_zone = 10  # Additional buffer zone where power-ups should not spawn

shooting_area = {
    'left': 0,  # You can add a WALL_WIDTH constant if you have walls
    'right': SCREEN_WIDTH,
    # The top and bottom will not change
    'top': 0,
    'bottom': SCREEN_HEIGHT - (player_height + buffer_zone)
}




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
        global running
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
        input_box_rect = pygame.Rect(input_box_x, input_box_y, INPUT_WIDTH, INPUT_HEIGHT)
    
        # Main loop for the start screen.
        while running:
            screen.blit(welcome_background_img, (0, 0))
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    # This should be the tuple unpacking the return of create_button
                    start_button_rect, start_button_clicked = create_button(screen, start_button_img, start_button_hover_img, start_button_x, button_y, text='Start')
                    if start_button_rect.collidepoint(event.pos):
                        main_game(input_text)  # Call the function or code to start the game
                    quit_button_rect, quit_button_clicked = create_button(screen, quit_button_img, quit_button_hover_img, quit_button_x, button_y, text='Quit')
                    if quit_button_rect.collidepoint(event.pos):
                        running = False
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
def spawn_enemies(enemy_group, blocker_group, player_rect, shooting_area):
    try:
        if random.randint(1, ENEMY_SPAWN_RATE) == 1:
            enemy = Enemy()
            # Adjust spawning position to be above the bottom buffer zone
            enemy.rect.y = random.randint(0, shooting_area['bottom'] - enemy.rect.height)
            enemy_group.add(enemy)
        
        # Add a chance to spawn a blocker instead of an enemy
        if random.randint(1, BLOCKER_SPAWN_RATE) == 1:
            # Spawn the blocker at the player's x position within the shooting area
            blocker = Blocker(player_rect.centerx, shooting_area)
            blocker_group.add(blocker)
    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        print(exc_type, fname, exc_tb.tb_lineno)
        running = False


# Function to handle spawning power-ups
def spawn_power_ups(power_up_group, player_rect, shooting_area):
    global current_wave
    # Adjust power-up rate based on the wave number
    power_up_chance = max(1, POWER_UP_RATE - current_wave * 10)

    if random.randint(1, power_up_chance) == 1:
        power_up_type = random.choice(list(POWER_UPS_ATTRIBUTES.keys()))
        attributes = POWER_UPS_ATTRIBUTES[power_up_type]
        power_up_image = pygame.image.load(attributes['image'])
        
        half_width = power_up_image.get_width() // 2
        half_height = power_up_image.get_height() // 2  # Half-height of the power-up image
        
        # Adjust the x and y coordinates to account for the half-width and half-height of the power-up
        x = random.randint(shooting_area['left'] + half_width, shooting_area['right'] - half_width)
        y = random.randint(shooting_area['top'] + half_height, shooting_area['bottom'] - half_height)

        # Ensure the power-up does not spawn too close to the player
        while abs(y - player_rect.y) < 100:
            y = random.randint(shooting_area['top'] + half_height, shooting_area['bottom'] - half_height)

        power_up = PowerUp(power_up_type, x, y)
        power_up_group.add(power_up)





def regenerate_ammo(player):
    global current_wave
    if player.ammo_boost_active:
        ammo_increase_rate = 2  # Double the rate
    else:
        ammo_increase_rate = 1  # Normal rate
    ammo_increase = max(1, current_wave // 3) * ammo_increase_rate
    if player.ammo < 10 + ammo_increase:  
        player.ammo += ammo_increase  # Regenerate ammo dynamically

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
        text_surf = button_font.render(button_text, True, text_color)
        text_rect = text_surf.get_rect(center=start_button_rect.center)

        # Stop the current background music
        pygame.mixer.music.stop()

        # Load and play the game over sound effect
        game_over_sound = pygame.mixer.Sound('media/game_over.wav')
        game_over_channel = pygame.mixer.find_channel()
        game_over_channel.play(game_over_sound)

        # Wait for the game over sound to finish before starting the background music
        while game_over_channel.get_busy():  # Wait until the sound is done playing
            pygame.time.delay(100)  # Check every 100 milliseconds

        # After the game over sound has finished playing, start the background music
        pygame.mixer.music.load('media/background_music.mp3')
        pygame.mixer.music.play(-1)


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
                    running = False
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
        global current_wave, in_between_waves, wave_start_time, running

        clock = pygame.time.Clock()
        player = Player()
        players = pygame.sprite.Group()
        players.add(player)
        enemies = pygame.sprite.Group()
        burgers = pygame.sprite.Group()
        power_ups = pygame.sprite.Group()
        wave_start_time = pygame.time.get_ticks()
        blocker_group = pygame.sprite.Group()

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
                            player.start_animation()
                            burger = Burger(player.rect.centerx, player.rect.top)
                            burgers.add(burger)
                            player.ammo -= 1
                elif event.type == AMMO_REGEN_EVENT:
                    regenerate_ammo(player)
                if in_between_waves:
                    continue  # Ignoriere alle Events, wenn wir uns zwischen den Wellen befinden

            # Aktualisiere die Zeit und überprüfe die Welle
            current_time = pygame.time.get_ticks()
            if not in_between_waves and current_time - wave_start_time > WAVE_DURATION:
                in_between_waves = True
                display_wave_message(screen, f"Wave {current_wave} completed!")
                # Hier sollten keine Gegner gespawnt werden
            elif in_between_waves and current_time - wave_start_time > WAVE_DURATION + BREAK_DURATION:
                next_wave(enemies)  # Starte die nächste Welle und leere die Gegnerliste

            if not in_between_waves:
                # Gegner und Power-Ups spawnen, wenn keine Pause ist
                spawn_enemies(enemies, blocker_group, player.rect, shooting_area)
                spawn_power_ups(power_ups, player.rect, shooting_area)
            # ...
                
            for enemy in list(enemies):  # Make a copy of the group list to iterate over
                enemy_off_screen = enemy.update()
                if enemy_off_screen:
                    player.health -= 10  # Decrease health when enemy reaches the edge
                    if player.health <= 0:
                        game_over_screen(screen, player.score, player_name)
                        running = False  # End the game if health is depleted

            # Update game states
            keys = pygame.key.get_pressed()
            keys = pygame.key.get_pressed()
            player.update(keys) 
            enemies.update()
            burgers.update()
            blocker_group.update()
            power_ups.update()

            # Collision detection with power-ups
            for burger in list(burgers):  # Iterate over a copy of the burgers again for power-up checks
                hit_power_ups = pygame.sprite.spritecollide(burger, power_ups, True, pygame.sprite.collide_mask)
                for power_up in hit_power_ups:
                    power_up.effect(player)  # Apply the effect of the power-up
# In the collision detection part of your game loop
            for burger in burgers:
                # Check for collision with enemies as usual
                hit_enemies = pygame.sprite.spritecollide(burger, enemies, True, pygame.sprite.collide_mask)
                for enemy in hit_enemies:
                    burger.kill()
                    player.score += 10  # Increase the score as usual

                # Check for collision with blockers, if you want the burgers to disappear
                hit_blockers = pygame.sprite.spritecollide(burger, blocker_group, False, pygame.sprite.collide_mask)
                if hit_blockers:
                    burger.kill()  # Optionally make the burger disappear when hitting a blocker


            #Ammunation regeneration
            for event in pygame.event.get():
                if event.type == AMMO_REGEN_EVENT:
                    regenerate_ammo(player)
        

            # Spawn enemies and power-ups
            spawn_enemies(enemies, blocker_group, player.rect, shooting_area)

            spawn_power_ups(power_ups, player.rect, shooting_area)


            # Drawing everything on the screen
            screen.blit(background_img, (0, 0))
            players.draw(screen)
            enemies.draw(screen)
            burgers.draw(screen)
            power_ups.draw(screen)

            for blocker in blocker_group:
                screen.blit(blocker.image, blocker.rect)


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

def next_wave(enemies):
    global current_wave, in_between_waves, wave_start_time, ENEMY_SPAWN_RATE
    current_wave += 1
    ENEMY_SPAWN_RATE += ENEMY_SPAWN_INCREMENT  # Increase linearly
    in_between_waves = False
    wave_start_time = pygame.time.get_ticks()
    enemies.empty()  # Clear all existing enemies at the start of the new wave

# Funktion zur Anzeige einer Nachricht zwischen den Wellen

def display_wave_message(screen, message):
    # Load the custom font
    custom_font = pygame.font.Font(adventure_font_path, 48)
    
    # Create a semi-transparent surface to darken the background
    overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 128))  # Black color with 50% opacity
    screen.blit(overlay, (0, 0))  # Blit this overlay onto the screen to "dim" it

    # Render the message text using the custom font
    text_surface = custom_font.render(message, True, (255, 255, 255))
    text_rect = text_surface.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))

    # Blit the text surface onto the screen
    screen.blit(text_surface, text_rect)
    pygame.display.flip()

    # Instead of waiting, loop for the duration of the break while still processing events
    start_time = pygame.time.get_ticks()
    while pygame.time.get_ticks() - start_time < BREAK_DURATION:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        pygame.time.delay(100)  # Wait for 100 milliseconds at a time



if __name__ == '__main__':
    try:
        game_intro()  # This will set the player_name and start the main game
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        pygame.quit()
        sys.exit()
