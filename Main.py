#Main von "Krabs' Burger-Battle: Die Geldfischjagd!"

###

# Import: Alle Abhängigkeiten werden am Anfang eingebunden

import pygame   # die Spiele-Engine
import random   # Zufallszahlen
import os       # Das Dateisystem
from settings import *
from sprites import *

###

# Initialisierung:    pygame wird gestartet
#                     und eine Bildschirm-Ausgabe wird generiert

pygame.init()           # pygame Initialisierung
pygame.mixer.init()     # Die Sound-Ausgabe wird initialisiert
pygame.display.set_caption("Krabs' Burger-Battle: Die Geldfischjagd!")   # Überschrift des Fensters
programmIcon = pygame.image.load('images\icon.png')     #Icon des Fensters
pygame.display.set_icon(programmIcon)

###

#Clock-Objekt:      Damit lassen sich Frames und Zeiten messen

clock = pygame.time.Clock()

###

#Screen-Objekt:     Auf dem screen werden alle Grafiken gerendert

screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.SCALED)

###

#Grafiken:     

game_folder = os.path.dirname(__file__)

###

# Wir binden eine Grafik ein


image_dict = {}


###

#Wir binden Sprites ein

sprites = []

#Game Loop

running = True

while running:

    # 1. Wait-Phase:
    dt = clock.tick(FPS) / 1000

###

    # 2. Input-Phase:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:   # Windows Close Button?
            running = False             # dann raus aus dem Game Loop

###

    # 3. Update-Phase: Hier ist die komplette Game Logik untergebracht.

    for sprite in sprites:
        sprite.update()

###

    # 4. Render-Phase: Zeichne alles auf den Bildschirm

    # Hintergrund
    hintergrund = pygame.image.load("images\bikini_bottom.png").convert()    # Hintergrund von Bikini bottom

    pygame.display.flip()

    screen.fill([255, 255, 255])
    
    gameDisplay.blit(hintergrund)
    
    
    


    # Zeichne Objekte an Position auf den Screen
    for sprite in sprites:
        screen.blit(sprite.image, sprite.imageRect)

###
    
    # 5. Double Buffering

    pygame.display.flip()

####
# Spiel verlassen: quit

