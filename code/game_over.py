import pygame
import json
from spaceship import Spaceship
from button import Button
from pathes import *
with open(SETTINGS_PATH) as fp:
    settings = json.load(fp)
with open(HIGHSCORE_PATH) as fp:
    highscore = json.load(fp)


class GameOver():
    """
    Eine Klasse, die einen Game-Over-Screen darstellt
    ...
    
    Attribute
    ---------
    screen : pygame.Surface
        Bildschirm, auf dem Game-Over angezeigt wird
    font : pygame.Font
        die Schriftart und Groesse, in der Game Over geschrieben wird
    again-button : Button
        Button, der gedrueckt wird, um nochmal zu spielen
    score : int
        der Score, den der Spieler erreicht hat
    reset : func
        Fuction, die ausgefuehrt wird, wenn der again_button gedrueckt
        wird

    Methoden
    --------
    set_score(score: int)
        setzt den Score
    set_function(reset : func)
        setzt die reset-Funktion, die bei again ausgefuehrt wird
    draw_background()
        malt den Bildschirm mit Hintergrund (schwarz) aus
    show_game_over()
        zeigt den Schriftzug Game Over in Schriftfarbe (rot) auf Bildschirm
    show_score()
        zeigt den Score des Spielers auf Bildschirm
    new_highscore()
        ueberprueft, ob der erreichte Score der neue High-Score sein muss
        und speichert daraufhin den neuen High-Score in der JSON-Datei highscore
        und gibt NEW HIGHSCORE aus
    run()
        malt alle Komponenten und ueberprueft, ob again_button gedrueckt wurde,
        sodass dann die reset-Funktion ausgefuehrt werden kann
    """
    def __init__(self, screen: pygame.Surface):
        """
        Parameter
        ---------
        screen : pygame.Surface
            der Bildschirm, auf den das Game-Over Fenster gemalt wird
        """
        self.screen = screen
        self.font = pygame.font.SysFont("arial", settings["game_over"]["font_size"])
        self.again_button = Button((self.screen.get_width() / 2, self.screen.get_height() / 2 + 70), "AGAIN")
        self.score = 0
        self.reset = None

    def set_score(self, score: int):
        """setzt den Score
        
        Parameter
        ---------
        score : int
            der Score des Spielers
        
        Rueckgabe
        ---------
        keine
        """
        self.score = score
    
    def set_function(self, reset):
        """setzt die reset-Funktion, die bei again ausgefuehrt wird
        
        Parameter
        ---------
        reset : func
            die reset-Funktion
        
        Rueckgabe
        ---------
        keine
        """
        self.reset = reset

    def draw_background(self):
        """malt den Bildschirm mit Hintergrund (schwarz) aus
        
        Parameter
        ---------
        keine

        Rueckgabe
        ---------
        keine
        """
        background_rect = pygame.Rect((0, 0), (self.screen.get_width(), self.screen.get_height()))
        pygame.draw.rect(self.screen, "black", background_rect)

    def show_game_over(self):
        """zeigt den Schriftzug Game Over in Schriftfarbe (rot) auf Bildschirm
        
        Parameter
        ---------
        keine

        Rueckgabe
        ----------
        keine
        """
        text = "GAME OVER"
        text_surface = self.font.render(text, False, "red")
        text_rect = text_surface.get_rect(center = (self.screen.get_width() / 2, self.screen.get_height() / 2))
        self.screen.blit(text_surface, text_rect)
    
    def show_score(self):
        """zeigt den Score des Spielers auf Bildschirm
        
        Parameter
        ----------
        keine

        Rueckgabe
        ----------
        keine
        """
        text = "YOUR SCORE WAS: {}".format(self.score)
        text_surface = self.font.render(text, False, "white")
        text_rect = text_surface.get_rect(topleft = (15, 15))
        self.screen.blit(text_surface, text_rect)

    def new_high_score(self):
        """ueberprueft, ob der erreichte Score der neue High-Score sein muss
        und speichert daraufhin den neuen High-Score in der JSON-Datei highscore
        und gibt NEW HIGHSCORE aus
        
        Parameter
        ---------
        keine

        Rueckgabe
        ----------
        keine
        """
        old_high_score = highscore["highscore"]
        if self.score >= old_high_score:
            dic = {"highscore": self.score}
            with open(HIGHSCORE_PATH, "w") as fp:
                json.dump(dic, fp, indent="\t")
            text = "NEW HI-SCORE !!!"
            text_surface = self.font.render(text, False, "white")
            text_rect = text_surface.get_rect(topleft = (15, 50))
            self.screen.blit(text_surface, text_rect)
        
    def run(self):
        """malt alle Komponenten und ueberprueft, ob again_button gedrueckt wurde,
        sodass dann die reset-Funktion ausgefuehrt werden kann
        
        Parameter
        ---------
        keine

        Methoden
        --------
        keine
        """
        self.draw_background()
        self.show_game_over()
        self.again_button.draw(self.screen)
        self.show_score()
        self.new_high_score()
        if self.again_button.get_just_pressed():
            self.reset()

