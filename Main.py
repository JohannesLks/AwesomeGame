import pygame
import random
import sys
import os
import csv
import time
from datetime import datetime
from settings import *
from sprites import *
from sprites import GameSpriteFactory

running = True
pygame.init()
size = (1000, 563)

screen = pygame.display.set_mode(size, pygame.NOFRAME)

start_image = pygame.image.load('media/loading_screen.png').convert()

screen.blit(start_image, (0, 0))
pygame.display.flip()
pygame.time.wait(3000)

pygame.display.set_mode(size)

pygame.font.init()
font = pygame.font.SysFont('arial', 32) 
custom_font = pygame.font.Font(adventure_font_path, 48)
FONT_SIZE = 32
FONT = pygame.font.Font(None, FONT_SIZE)
BUTTON_FONT = pygame.font.Font(None, 36)
BIG_FONT = pygame.font.SysFont(None, 80)
REGULAR_FONT = pygame.font.SysFont(None, 36)

BACKGROUND_MUSIC = 'media/background_music.mp3'
pygame.mixer.music.load(BACKGROUND_MUSIC)
pygame.mixer.music.play(-1)
throw_sound = pygame.mixer.Sound(THROW_SOUND)
bubble = pygame.mixer.Sound("media/bubble.mp3")
game_over = pygame.mixer.Sound(game_over_sound)
plankton_spawn_sound = pygame.mixer.Sound(PLANKTON_SPAWN_SOUND)

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Krabs' Burger-Battle: Die Geldfischjagd")

player_height = player_images[0].get_height()
buffer_zone = 10

shooting_area = {
    'left': 0,  
    'right': SCREEN_WIDTH,
    'top': 0,
    'bottom': SCREEN_HEIGHT - (player_height + buffer_zone)
}

AMMO_REGEN_EVENT = pygame.USEREVENT + 1
pygame.time.set_timer(AMMO_REGEN_EVENT, 2000)

def handle_input_events(event, input_text, input_box_active, input_box_rect):
    """
    Behandelt die Eingabeereignisse für das Texteingabefeld.

    Parameters:
        event (pygame.Event): Das pygame-Ereignis, das behandelt werden soll.
        input_text (str): Der aktuelle Text im Eingabefeld.
        input_box_active (bool): Gibt an, ob das Eingabefeld aktiv ist oder nicht.
        input_box_rect (pygame.Rect): Das Rechteck, das das Eingabefeld umgibt.

    Returns:
        input_text (str): Der aktualisierte Text im Eingabefeld.
        input_box_active (bool): Gibt an, ob das Eingabefeld aktiv ist oder nicht.
    """
    if event.type == pygame.MOUSEBUTTONDOWN:
        if input_box_rect.collidepoint(event.pos):
            input_box_active = not input_box_active
        else:
            input_box_active = False
    elif event.type == pygame.KEYDOWN:
        if input_box_active:
            if event.key == pygame.K_RETURN:
                print(input_text)
                input_text = ''
            elif event.key == pygame.K_BACKSPACE:
                input_text = input_text[:-1]
            else:
                input_text += event.unicode
    return input_text, input_box_active

def create_button(screen, image, image_hover, x, y, text='', text_color=BLACK, font_size=FONT_SIZE, font_path=None):
    """
    Erstellt einen Button auf dem Bildschirm mit einem Bild und optionalem Text.

    Args:
        screen (pygame.Surface): Die Oberfläche, auf der der Button angezeigt wird.
        image (pygame.Surface): Das Bild für den Button.
        image_hover (pygame.Surface): Das Bild für den Button, wenn die Maus darüber schwebt.
        x (int): Die x-Koordinate der Position des Buttons.
        y (int): Die y-Koordinate der Position des Buttons.
        text (str, optional): Der Text, der auf dem Button angezeigt wird. Standardmäßig ist der Text leer.
        text_color (tuple, optional): Die Farbe des Textes. Standardmäßig ist die Farbe schwarz.
        font_size (int, optional): Die Schriftgröße des Textes. Standardmäßig ist die Schriftgröße FONT_SIZE.
        font_path (str, optional): Der Pfad zur Schriftartdatei. Standardmäßig ist die Schriftart None.

    Returns:
        button_rect (pygame.Rect): Das Rechteck, das den Button umgibt.
        clicked (bool): Gibt an, ob der Button angeklickt wurde oder nicht.
    """
    button_rect = image.get_rect(topleft=(x, y))
    mouse = pygame.mouse.get_pos()
    clicked = pygame.mouse.get_pressed()[0]
    button_image = image_hover if button_rect.collidepoint(mouse) else image

    screen.blit(button_image, button_rect)

    if text:
        if font_path:
            text_font = pygame.font.Font(font_path, font_size)
        else:
            text_font = pygame.font.SysFont(None, font_size)
        text_surf = text_font.render(text, True, text_color)
        text_rect = text_surf.get_rect(center=button_rect.center)
        screen.blit(text_surf, text_rect)
    return button_rect, clicked

def text_objects(text, font):
    """
    Erstellt ein Textobjekt mit dem angegebenen Text und der Schriftart.

    Args:
        text (str): Der Text, der gerendert werden soll.
        font (pygame.font.Font): Die Schriftart, die für den Text verwendet werden soll.

    Returns:
        text_surface (pygame.Surface): Die Oberfläche, auf der der Text gerendert wird.
        text_surface.get_rect() (pygame.Rect): Das Rechteck, das den Text umgibt.
    """
    text_surface = font.render(text, True, BLACK)
    return text_surface, text_surface.get_rect()

def show_start_screen(screen):
    """
    Zeigt den Startbildschirm des Spiels an und ermöglicht es dem Benutzer, seinen Namen einzugeben, den Spielstart zu initiieren oder das Spiel zu beenden.

    Args:
        screen (pygame.Surface): Die Oberfläche, auf der der Startbildschirm angezeigt wird.

    Returns:
        input_text (str): Der Name des Spielers, der eingegeben wurde.
    """
    global running
    button_y = SCREEN_HEIGHT - BUTTON_HEIGHT - LOWER_OFFSET

    start_button_x = center_x - half_button_width - BUTTON_SPACING // 2

    quit_button_x = center_x + BUTTON_SPACING // 2

    start_button_x = center_x - BUTTON_WIDTH - BUTTON_SPACING // 2

    quit_button_x = center_x + BUTTON_SPACING // 2

    input_text = ''
    input_box_active = False
    input_box_x = SCREEN_WIDTH / 2 - INPUT_WIDTH / 2
    input_box_y = INPUT_BOX_Y_OFFSET
    input_box_rect = pygame.Rect(input_box_x, input_box_y, INPUT_WIDTH, INPUT_HEIGHT)

    while running:
        screen.blit(welcome_background_img, (0, 0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                start_button_rect, start_button_clicked = create_button(screen, start_button_img, start_button_hover_img, start_button_x, button_y, text='Start')
                if start_button_rect.collidepoint(event.pos):
                    main_game(input_text)
                quit_button_rect, quit_button_clicked = create_button(screen, quit_button_img, quit_button_hover_img, quit_button_x, button_y, text='Quit')
                if quit_button_rect.collidepoint(event.pos):
                    running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    main_game(input_text)
            input_text, input_box_active = handle_input_events(event, input_text, input_box_active, input_box_rect)

        start_button_rect, start_button_clicked = create_button(
            screen, start_button_img, start_button_hover_img, 
            start_button_x, button_y, text='Start'
        )
        quit_button_rect, quit_button_clicked = create_button(
            screen, quit_button_img, quit_button_hover_img, 
            quit_button_x, button_y, text='Quit'
        )

        input_text, input_box_active, input_box_rect = input_box(
            screen,
            input_box_x,
            input_box_y,
            INPUT_WIDTH,
            INPUT_HEIGHT,
            input_text,
            input_box_active,
            FONT,
            background_image=input_bg_image
        )
        pygame.display.flip()

    return input_text

def spawn_enemies(enemy_group, blocker_group, player_rect, shooting_area):
    """
    Spawnt Feinde und Blocker in einem Spiel.

    Args:
        enemy_group (pygame.sprite.Group): Die Gruppe, in der die Feinde gespeichert werden.
        blocker_group (pygame.sprite.Group): Die Gruppe, in der die Blocker gespeichert werden.
        player_rect (pygame.Rect): Das Rechteck, das den Spieler repräsentiert.
        shooting_area (dict): Ein Dictionary, das den Bereich definiert, in dem die Feinde und Blocker erscheinen können.

    Returns:
        enemy (pygame.sprite.Sprite): Der Feind, der gespawnt wurde.
    """
    global BLOCKER_COUNT, BLOCKER_MAXIMUM
    if random.randint(1, STANDARD_ENEMY_SPAWN_RATE) == 1:
        enemy = GameSpriteFactory.create_enemy("standard")

        enemy.rect.y = random.randint(0, shooting_area['bottom'] - enemy.rect.height)
        enemy_collides = pygame.sprite.spritecollideany(enemy, enemy_group) 
        if enemy_collides is None:
            enemy_group.add(enemy)
        else:
            pass

    if random.randint(1, ADVANCED_ENEMY_SPAWN_RATE) == 1:
        enemy = GameSpriteFactory.create_enemy("advanced")

        enemy.rect.y = random.randint(0, shooting_area['bottom'] - enemy.rect.height)
        enemy_collides = pygame.sprite.spritecollideany(enemy, enemy_group) 
        if enemy_collides is None:
            enemy_group.add(enemy)
        else:
            pass
    
    if random.randint(1, BLOCKER_SPAWN_RATE) == 1:                    
        if BLOCKER_COUNT < BLOCKER_MAXIMUM:
            blocker_height = blocker_img.get_rect().height
            blocker = GameSpriteFactory.create_blocker(player_rect.centerx, shooting_area['top'] + (blocker_height // 2), shooting_area['bottom'] - (blocker_height // 2))
            blocker_collides = pygame.sprite.spritecollideany(blocker, blocker_group) 
            if blocker_collides is None:
                blocker_group.add(blocker)
                BLOCKER_COUNT += 1
                plankton_spawn_sound.play()
            else:
                pass

def spawn_power_ups(power_up_group, player_rect, shooting_area):
    """
    Spawnt Power-Ups im Spiel.

    Args:
        power_up_group (pygame.sprite.Group): Die Gruppe, in der die Power-Ups gespeichert werden sollen.
        player_rect (pygame.Rect): Das Rechteck des Spielers.
        shooting_area (dict): Der Bereich, in dem die Power-Ups gespawnt werden können.

    Returns:
        power_up (pygame.sprite.Sprite): Das Power-Up, das gespawnt wurde.
    """
    global current_wave
    power_up_chance = max(1, POWER_UP_RATE - current_wave * 10)

    if random.randint(1, power_up_chance) == 1:
        power_up_type = random.choice(list(POWER_UPS_ATTRIBUTES.keys()))
        attributes = POWER_UPS_ATTRIBUTES[power_up_type]
        power_up_image = pygame.image.load(attributes['image'])
        
        half_width = power_up_image.get_width() // 2
        half_height = power_up_image.get_height() // 2
        
        x = random.randint(shooting_area['left'] + half_width, shooting_area['right'] - half_width)
        y = random.randint(shooting_area['top'] + half_height, shooting_area['bottom'] - half_height)

        while abs(y - player_rect.y) < 100:
            y = random.randint(shooting_area['top'] + half_height, shooting_area['bottom'] - half_height)

        power_up = GameSpriteFactory.create_power_up(power_up_type, x, y)
        power_up_group.add(power_up)

def regenerate_ammo(player):
    """
    Erhöht die Munition des Spielers basierend auf der aktuellen Welle und dem Boost-Status.

    Args:
        player (Player): Der Spieler, dessen Munition erhöht werden soll.

    Returns:
        player_increase (int): Die Anzahl der Munition, die dem Spieler hinzugefügt wird.
    """
    global current_wave
    if player.ammo_boost_active:
        ammo_increase_rate = 2
    else:
        ammo_increase_rate = 1
    ammo_increase = max(1, current_wave // 3) * ammo_increase_rate
    if player.ammo < 10 + ammo_increase:  
        player.ammo += ammo_increase

def load_highscores(filename='highscores.csv'):
    """
    Lädt die Highscores aus einer CSV-Datei und gibt sie als Liste zurück.
    
    Args:
        filename (str): Der Dateiname der CSV-Datei. Standardmäßig ist es 'highscores.csv'.
    
    Returns:
        highscores (list): Die Liste der Highscores.
    """
    highscores = []
    with open(filename, 'r', newline='') as file:
        reader = csv.reader(file)
        for row in reader:
            if len(row) == 3:  
                highscores.append(row)
        highscores.sort(key=lambda x: int(x[1]), reverse=True)
    return highscores

def save_highscore(name, score, filename='highscores.csv'):
    """
    Speichert den Highscore eines Spielers in einer CSV-Datei.

    :param name: Der Name des Spielers.
    :param score: Der erreichte Highscore.
    :param filename: Der Dateiname der CSV-Datei (Standardwert: 'highscores.csv').
    """
    date_str = datetime.now().strftime('%Y-%m-%d %H:%M')
    with open(filename, 'a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([name, score, date_str])
        
def input_box(screen, x, y, w, h, text, active, font, background_image):
    """
    Zeigt ein Eingabefeld auf dem Bildschirm an.

    Args:
        screen (pygame.Surface): Die Bildschirmoberfläche, auf der das Eingabefeld angezeigt wird.
        x (int): Die x-Koordinate des Eingabefelds.
        y (int): Die y-Koordinate des Eingabefelds.
        w (int): Die Breite des Eingabefelds.
        h (int): Die Höhe des Eingabefelds.
        text (str): Der aktuelle Text im Eingabefeld.
        active (bool): Gibt an, ob das Eingabefeld aktiv ist oder nicht.
        font (pygame.font.Font): Die Schriftart für den Text im Eingabefeld.
        background_image (pygame.Surface): Das Hintergrundbild für das Eingabefeld.

    Returns:
        tuple: Ein Tupel, das den aktualisierten Text, den Aktivitätsstatus und das Rechteck des Eingabefelds enthält.
    """
    color_active = pygame.Color('black')
    color_inactive = pygame.Color('grey')
    color = color_active if active else color_inactive

    input_box_rect = pygame.Rect(x, y, w, h)

    if background_image:
        input_bg_rect = background_image.get_rect(center=input_box_rect.center)
        screen.blit(background_image, input_bg_rect.topleft)

    if not active and not text:
        placeholder_text = "Name"
        txt_surface = font.render(placeholder_text, True, color_inactive)
    else:
        txt_surface = font.render(text, True, color)

    text_x = input_box_rect.x + (input_box_rect.w - txt_surface.get_width()) // 2
    text_y = input_box_rect.y + (input_box_rect.h - txt_surface.get_height()) // 2

    screen.blit(txt_surface, (text_x, text_y))

    return text, active, input_box_rect



def game_over_screen(screen, score, player_name):
    """
    Zeigt den Game Over-Bildschirm an und ermöglicht es dem Spieler, ein neues Spiel zu starten.

    Args:
        screen (pygame.Surface): Das Pygame-Surface-Objekt, auf dem der Bildschirm gerendert wird.
        score (int): Die Punktzahl des Spielers.
        player_name (str): Der Name des Spielers.
    """
    big_font = pygame.font.Font(adventure_font_path, 80)
    regular_font = pygame.font.Font(adventure_font_path, 36)
    save_highscore(player_name, score)
    highscores = load_highscores()

    start_button_x = SCREEN_WIDTH // 2 - start_button_img.get_width() // 2
    start_button_y = SCREEN_HEIGHT - start_button_img.get_height() - 50
    start_button_rect = pygame.Rect(start_button_x, start_button_y, start_button_img.get_width(), start_button_img.get_height())

    running = True
    pygame.mixer.music.stop()
    game_over.play()
    pygame.mixer.music.load(game_over_music)
    pygame.mixer.music.play(-1)
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if start_button_rect.collidepoint(event.pos):
                    pygame.mixer.music.stop()
                    pygame.mixer.music.load(BACKGROUND_MUSIC)
                    pygame.mixer.music.play(-1)
                    init_game()
                    main_game(player_name)
                    running = False

            screen.blit(game_over_img, (0, 0))
            mouse_pos = pygame.mouse.get_pos()
            if start_button_rect.collidepoint(mouse_pos):
                screen.blit(start_button_hover_img, start_button_rect.topleft)
            else:
                screen.blit(start_button_img, start_button_rect.topleft)

            text_surf = FONT.render('New Game', True, WHITE)
            text_rect = text_surf.get_rect(center=start_button_rect.center)
            screen.blit(text_surf, text_rect)

            title_surf = big_font.render('Game Over', True, WHITE)
            title_rect = title_surf.get_rect(center=(SCREEN_WIDTH // 2, 50))
            screen.blit(title_surf, title_rect)

            score_surf = regular_font.render(f'Money $: {score}', True, RED)
            score_rect = score_surf.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 150))
            screen.blit(score_surf, score_rect)


            for i, highscore in enumerate(highscores[:5]):
                highscore_text = f"{i + 1}. {highscore[0]} - {highscore[1]}"
                highscore_surf = regular_font.render(highscore_text, True, WHITE)
                highscore_rect = highscore_surf.get_rect(center=(SCREEN_WIDTH // 2, 150 + i * 50))
                screen.blit(highscore_surf, highscore_rect)
            pygame.display.flip()



def init_game():
    """
    Setzt die globalen Variablen auf die Standardwerte zurück und initialisiert das Spiel.

    Diese Funktion setzt die globalen Variablen BLOCKER_COUNT, STANDARD_ENEMY_SPAWN_RATE,
    ADVANCED_ENEMY_SPAWN_RATE, current_wave, in_between_waves und wave_start_time auf ihre
    Standardwerte zurück. Dadurch wird das Spiel in den Anfangszustand versetzt.

    Wird ausgelöst wenn im Game Over Bildschirm auf den "Neues Spiel" Button geklickt wird.
    """
    global BLOCKER_COUNT, STANDARD_ENEMY_SPAWN_RATE, ADVANCED_ENEMY_SPAWN_RATE, current_wave, in_between_waves, wave_start_time
    BLOCKER_COUNT = 0
    STANDARD_ENEMY_SPAWN_RATE = 200
    ADVANCED_ENEMY_SPAWN_RATE = 600
    current_wave = 1
    in_between_waves = False
    wave_start_time = 0

def main_game(player_name):
    """
    Führt das Hauptspiel aus.

    Args:
        player_name (str): Der Name des Spielers.
    """
def main_game(player_name):
    global current_wave, in_between_waves, wave_start_time, running

    clock = pygame.time.Clock()
    player = GameSpriteFactory.create_player()
    players = pygame.sprite.Group()
    players.add(player)
    enemies = pygame.sprite.Group()
    burgers = pygame.sprite.Group()
    power_ups = pygame.sprite.Group()
    wave_start_time = pygame.time.get_ticks()
    blocker_group = pygame.sprite.Group()

    while running:
        clock.tick(60)
        screen.fill(WHITE)
        screen.blit(background_img, (0, 0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    if player.ammo > 0:
                        player.start_animation()
                        burger = GameSpriteFactory.create_burger(player.rect.centerx, player.rect.top)
                        burgers.add(burger)
                        player.ammo -= 1
                        throw_sound.play()
            elif event.type == AMMO_REGEN_EVENT:
                regenerate_ammo(player)
            if in_between_waves:
                continue

        current_time = pygame.time.get_ticks()
        if not in_between_waves and current_time - wave_start_time > WAVE_DURATION:
            in_between_waves = True
            display_wave_message(screen, f"Wave {current_wave} completed!")
        elif in_between_waves and current_time - wave_start_time > WAVE_DURATION + BREAK_DURATION:
            next_wave(enemies, blocker_group)

        if not in_between_waves:
            spawn_enemies(enemies, blocker_group, player.rect, shooting_area)
            spawn_power_ups(power_ups, player.rect, shooting_area)

    
        for enemy in list(enemies):
            enemy_off_screen = enemy.update()
            if enemy_off_screen:
                if isinstance(enemy, AdvancedEnemy):
                    player.health -= 30
                elif isinstance(enemy, StandardEnemy):
                    player.health -= 10
                if player.health <= 0:
                    game_over_screen(screen, player.score, player_name)
                    running = False

        keys = pygame.key.get_pressed()
        keys = pygame.key.get_pressed()
        player.update(keys) 
        enemies.update()
        burgers.update()
        blocker_group.update()
        power_ups.update()

        for burger in list(burgers):
            hit_power_ups = pygame.sprite.spritecollide(burger, power_ups, True, pygame.sprite.collide_rect)
            for power_up in hit_power_ups:
                power_up.effect(player)
                bubble.play()
        for burger in burgers:
            hit_enemies = pygame.sprite.spritecollide(burger, enemies, False, pygame.sprite.collide_mask)
            for enemy in hit_enemies:
                if enemy.take_damage(BURGER_DAMAGE, player.rect.center):
                    player.score += enemy.score_value
                burger.kill()


            hit_blockers = pygame.sprite.spritecollide(burger, blocker_group, False, pygame.sprite.collide_mask)
            if hit_blockers:
                burger.kill()

        for event in pygame.event.get():
            if event.type == AMMO_REGEN_EVENT:
                regenerate_ammo(player)

            wave_text = font.render(f'Wave:  {current_wave}', True, BLACK)
            screen.blit(wave_text, (890, 10))

            pygame.display.flip()


        screen.blit(background_img, (0, 0))
        players.draw(screen)
        enemies.draw(screen)
        burgers.draw(screen)
        power_ups.draw(screen)

        for blocker in blocker_group:
            screen.blit(blocker.image, blocker.rect)                   

        font = pygame.font.SysFont(None, 36)
        score_text = font.render(f'Money $: {player.score}', True, GREEN)
        screen.blit(score_text, (10, 10))

        health_text = font.render(f'Health: {player.health}', True, RED)
        screen.blit(health_text, (10, 50))
    
        ammo_text = font.render(f'Burger: {player.ammo}', True, BLUE)
        screen.blit(ammo_text, (10, 80))

        wave_text = font.render(f'Wave:  {current_wave}', True, BLACK)
        screen.blit(wave_text, (890, 10))

        pygame.display.flip()

def game_intro():
    """
    Zeigt die Startbildschirm des Spiels an und ermöglicht es dem Spieler, seinen Namen einzugeben.
    Wenn der Spieler keinen Namen eingibt, wird das Spiel beendet. Ansonsten wird das Hauptspiel gestartet.
    """
    intro = True
    while intro:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        player_name = show_start_screen(screen)
        if player_name is None:
            intro = False
        else:
            main_game(player_name)
            intro = False

def next_wave(enemies, blocker_group):
    """
    Advances the game to the next wave by updating wave-related variables and resetting enemy and blocker groups.

    Args:
        enemies (pygame.sprite.Group): The group of enemies in the game.
        blocker_group (pygame.sprite.Group): The group of blockers in the game.
    """
    global current_wave, in_between_waves, wave_start_time, STANDARD_ENEMY_SPAWN_RATE, ADVANCED_ENEMY_SPAWN_RATE, BLOCKER_COUNT
    current_wave += 1
    if STANDARD_ENEMY_SPAWN_RATE > ENEMY_SPAWN_INCREMENT:
        STANDARD_ENEMY_SPAWN_RATE -= ENEMY_SPAWN_INCREMENT
        ADVANCED_ENEMY_SPAWN_RATE -= ENEMY_SPAWN_INCREMENT
    in_between_waves = False
    wave_start_time = pygame.time.get_ticks()
    enemies.empty()
    blocker_group.empty()
    BLOCKER_COUNT = 0

def display_wave_message(screen: pygame.Surface, message: str) -> None:
    """
    Zeigt eine Wellenmeldung auf dem Bildschirm an.

    Args:
        screen (pygame.Surface): Die Oberfläche (Surface) des Bildschirms, auf dem die Meldung angezeigt werden soll.
        message (str): Die Nachricht, die angezeigt werden soll.
    """
    
    overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 128))
    screen.blit(overlay, (0, 0))

    text_surface = custom_font.render(message, True, (255, 255, 255))
    text_rect = text_surface.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))

    screen.blit(text_surface, text_rect)
    pygame.display.flip()

    start_time = pygame.time.get_ticks()
    while pygame.time.get_ticks() - start_time < BREAK_DURATION:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        pygame.time.delay(100)


if __name__ == '__main__':
    try:
        game_intro()
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        pygame.quit()
        sys.exit()