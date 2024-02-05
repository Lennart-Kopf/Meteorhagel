import pygame
import json
from spaceship import Spaceship
from pathes import *
import pathlib

with open(SETTINGS_PATH) as fp:
    settings = json.load(fp)


class UI():
    """
    Eine Klasse, die die Benutzeroberflaeche darstellt

    ...

    Attribute
    ----------
    font : pygame.Font
        Schriftart und Groesse fuer die Texte der UI
    screen : pygame.Surface
        Bildschirm
    highscore : int
        Highscore des Spielers
        muss bei jeder Initialisierung neu gelesen werden, falls sich Highscore aendert
    
    Methoden
    --------
    show_score(score : int)
        zeigt den aktuellen Score
    show_health_bar(max_health : int, health : int)
        zeigt die aktuellen Leben in Form eines Balken an, Farben aendern sich je nach Anteil
        der aktuellen Leben an den maximalen Leben
    show_coins(coins: int)
        zeigt die Coins
    show_ready_to_shoot()
        zeigt den Text "Ready to shoot!"
    show_high_score()
        zeigt den letzten High-Score aus der Highscore Datei
    show_controls()
        zeigt die Grundsteuerung
    display(spaceship : Spaceship)
        zeigt alle Komponenten der UI und fuehrt show_ready_to_shoot() aus, wenn 
        ready_to_shoot des Spaceships True ist
    """
    def __init__(self, screen: pygame.Surface):
        """
        Parameter
        ---------
        screen : pygame.Surface
            Bildschirm
        """
        with open(HIGHSCORE_PATH) as fp:
            highscore = json.load(fp)
        self.font = pygame.font.SysFont("arial", settings["ui"]["font_size"])
        self.screen = screen
        self.high_score = highscore["highscore"]

    
    def show_score(self, score):
        """zeigt den aktuellen Score
        
        Parameter
        ---------
        score : int
            der aktuelle Score
        
        Rueckgabe
        ---------
        keine
        """
        text = "SCORE: {}".format(score)
        text_surface = self.font.render(text, False, "white")
        text_rect = text_surface.get_rect(topleft = tuple(settings["ui"]["position"]))
        self.screen.blit(text_surface, text_rect)
    
    def show_health_bar(self, max_health, health):
        """zeigt die aktuellen Leben in Form eines Balken an, Farben aendern sich je nach Anteil
        der aktuellen Leben an den maximalen Leben
        
        Parameter
        ---------
        max_health : int
            die maximalen Leben des Spaceships
        health : int
            die aktuellen Leben des Spaceships
        
        Rueckgabe
        ---------
        keine
        """
        color = ""
        if health >= 0.75 * max_health:
            color = "green"
        elif health >= 0.25 * max_health:
            color = "yellow"
        else:
            color = "red"
        width = settings["ui"]["width_per_health"] * health
        height = 20
        bar_rect = pygame.Rect((settings["ui"]["position"][0], settings["ui"]["position"][1] + 30), (width, height))
        pygame.draw.rect(self.screen, color, bar_rect)
    
    def show_coins(self, coins: int):
        """zeigt die Coins
        
        Parameter
        --------
        coins : int
            aktuelle Muenzen
        
        Rueckgabe
        ----------
        keine
        """
        text = "x{}".format(coins)
        text_surface = self.font.render(text, False, "white")
        text_rect = text_surface.get_rect(topleft = (settings["ui"]["position"][0]+40, settings["ui"]["position"][1] + 60))
        self.screen.blit(text_surface, text_rect)
        coin_image = pygame.image.load(IMAGE_PATH/"gold_coin000.png").convert_alpha()
        coin_rect = coin_image.get_rect(topleft = (settings["ui"]["position"][0], settings["ui"]["position"][1] + 60))
        self.screen.blit(coin_image, coin_rect)
    
    def show_ready_to_shoot(self):
        """zeigt den Text "Ready to shoot!"
        
        Parameter
        ---------
        keine

        Rueckgabe
        ---------
        keine
        """
        text = "Ready to shoot!"
        text_surface = self.font.render(text, False, "white")
        text_rect = text_surface.get_rect(topleft = (settings["ui"]["position"][0], settings["ui"]["position"][1] + 90))
        self.screen.blit(text_surface, text_rect)
    
    def show_high_score(self):
        """zeigt den letzten High-Score aus der Highscore Datei
        
        Parameter
        ---------
        keine

        Rueckgabe
        ---------
        keine
        """
        text = "HI-SCORE: {}".format(self.high_score)
        text_surface = self.font.render(text, False, "white")
        text_rect = text_surface.get_rect(center = (self.screen.get_width() / 2, settings["ui"]["position"][1]))
        self.screen.blit(text_surface, text_rect)
    
    def show_controls(self):
        """zeigt die Grundsteuerung
        
        Parameter
        ---------
        keine

        Rueckgabe
        ---------
        keine
        """
        text_lines = ["(U) UPGRADE MENU","(ESC) PAUSE", "(SPACE) SHOOT", "(W / UP) MOVE", "(MOUVE MOUSE) AIM AND ROTATE"]
        for index, text in enumerate(text_lines):
            text_surface = self.font.render(text, False, "white")
            text_rect = text_surface.get_rect(topleft = (self.screen.get_width() * 0.7, settings["ui"]["position"][1] + text_surface.get_height() * index))
            self.screen.blit(text_surface, text_rect)
        
    
    def display(self, spaceship: Spaceship):
        """zeigt alle Komponenten der UI und fuehrt show_ready_to_shoot() aus, wenn 
        ready_to_shoot des Spaceships True ist
        
        Parameter
        ---------
        spaceship : Spaceship
            das Raumschiff

        Rueckgabe
        ---------
        keine
        """
        self.show_score(spaceship.get_score())
        self.show_health_bar(spaceship.get_max_health(), spaceship.get_health())
        self.show_coins(spaceship.get_coins())
        self.show_high_score()
        if spaceship.get_ready_to_shoot():
            self.show_ready_to_shoot()
        self.show_controls()
        