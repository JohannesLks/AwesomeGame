#Main von "Krabs' Burger-Battle: Die Geldfischjagd!"

###

# Import: Alle Abhängigkeiten werden am Anfang eingebunden

import pygame   # die Spiele-Engine
import random   # Zufallszahlen
from settings import *
from sprites import *

###

# Initialisierung:    pygame wird gestartet
#                     und eine Bildschirm-Ausgabe wird generiert

pygame.init()           # pygame Initialisierung
pygame.mixer.init()     # Die Sound-Ausgabe wird initialisiert
pygame.display.set_caption("Krabs' Burger-Battle: Die Geldfischjagd!")   # Überschrift des Fensters

###

#Clock-Objekt:      Damit lassen sich Frames und Zeiten messen

clock = pygame.time.Clock()

###

#Screen-Objekt:     Auf dem screen werden alle Grafiken gerendert

screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.SCALED)

###

#Grafiken:     Das Einbinden von Grafiken wurde ausgelagert in einem Ordner im repository

