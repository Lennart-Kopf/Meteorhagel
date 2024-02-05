import pygame
from button import Button
import os
from pathes import *
import pathlib

class Title():
    """
    Eine Klasse, die einen Titelbildschirm darstellt

    ...

    Attribute
    ----------
    screen : pygame.Surface
        Bildschirm
    title_image : pygame.Surface
        Bild des Titels
    start_button : Button
        Button mit der Bezeichnung "START", der gedrueckt wird, wenn man das Spiel starten will
    load_button : Button
        Button mit der Bezeichnung "LOAD", der gedrueckt wird, wenn man einen Spielstand laden will
    instructions_button : Button
        Button mit der Bezeichnung "INSTRUCTIONS", der gedrueckt wird, wenn man die Spielanleitung ansehen will
    start_fun : func
        Funktion, die ausgefuehrt werden soll, wenn der start_button gedrueckt wird
    load_fun : func
        Funktion, die ausgefuehrt werden soll, wenn load_button gedrueckt wird
    
    Methoden
    ---------
    draw_background()
        malt den Bildschirm mit dem Hintergrund (schwarz) aus
    set_start_fun(start_fun : func)
        setzt die start_fun 
    set_load_fun(load_fun : func)
        setzt die load_fun
    start()
        malt den start_button und ueberprueft, ob er gedrueckt wird, wenn ja wird die start_fun ausgefuehrt
    instructions()
        malt den instructions_button und ueberprueft, ob er gedrueckt wird, wenn ja wird die Instructions Text Datei geoeffnet
    load()
        malt den load_button und ueberprueft, ob er gedrueckt wird, wenn ja wird die load_fun ausgefuehrt
    show_title()
        malt den Titel
    run()
        malt die Komponenten und ueberprueft, ob einer der Buttons gedrueckt wird
    """
    def __init__(self, screen: pygame.Surface):
        """
        Parameter
        ---------
        screen : pygame.Surface
            Bildschirm
        """
        self.screen = screen
        self.title_image = pygame.image.load(IMAGE_PATH/"title.png").convert_alpha()
        self.title_image = pygame.transform.scale(self.title_image, ((self.screen.get_height()/5) * 4.6, self.screen.get_height() / 5))
        self.title_rect = self.title_image.get_rect(center = (self.screen.get_width() / 2, self.screen.get_height()/3))
        self.start_button = Button((self.screen.get_width() / 2, self.title_rect.bottom + 40), "START")
        self.load_button = Button((self.screen.get_width() / 2, self.title_rect.bottom + 120), "LOAD")
        self.instructions_button = Button((self.screen.get_width() / 2, self.title_rect.bottom + 200), "INSTRUCTIONS")
        self.start_fun = None
        self.load_fun = None
        
    
    def draw_background(self):
        """malt den Bildschirm mit dem Hintergrund (schwarz) aus
        
        Parameter
        ---------
        keine

        Rueckgabe
        ----------
        keine
        """
        background_rect = pygame.Rect((0, 0), (self.screen.get_width(), self.screen.get_height()))
        pygame.draw.rect(self.screen, "black", background_rect)
    
    def set_start_fun(self, start_fun):
        """setzt die start_fun 
        
        Parameter
        ---------
        start_fun : func
            Funktion, mit der start_fun ersetzt werden soll
        
        Rueckgabe
        ----------
        keine
        """
        self.start_fun = start_fun
    
    def set_load_fun(self, load_fun):
        """setzt die load_fun 
        
        Parameter
        ---------
        load_fun : func
            Funktion, mit der load_fun ersetzt werden soll
        
        Rueckgabe
        ----------
        keine
        """
        self.load_fun = load_fun
    
    def start(self):
        """malt den start_button und ueberprueft, ob er gedrueckt wird, wenn ja wird die start_fun ausgefuehrt
        
        Parameter
        ---------
        keine

        Rueckgabe
        ----------
        keine
        """
        self.start_button.draw(self.screen)
        if self.start_button.get_just_pressed():
            self.start_fun()
    
    def instructions(self):
        """malt den instructions_button und ueberprueft, ob er gedrueckt wird, wenn ja wird die Instructions Text Datei geoeffnet

        Parameter
        ---------
        keine

        Rueckgabe
        ----------
        keine
        """
        self.instructions_button.draw(self.screen)
        if self.instructions_button.get_just_pressed():
            os.startfile(INSTRUCTIONS_PATH)
    
    def load(self):
        """malt den load_button und ueberprueft, ob er gedrueckt wird, wenn ja wird die load_fun ausgefuehrt
        
        Parameter
        ---------
        keine

        Rueckgabe
        ----------
        keine
        """
        self.load_button.draw(self.screen)
        if self.load_button.get_just_pressed():
            self.load_fun()

    def show_title(self):
        """malt den Titel
        
        Parameter
        ---------
        keine

        Methoden
        --------
        keine
        """
        self.screen.blit(self.title_image, self.title_rect)

    
    def run(self):
        """malt die Komponenten und ueberprueft, ob einer der Buttons gedrueckt wird
        
        Parameter
        ----------
        keine

        Methoden
        ---------
        keine
        """
        self.draw_background()
        self.show_title()
        self.start()
        self.load()
        self.instructions()
