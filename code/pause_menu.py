import pygame
from button import Button
import json
from pathes import *
with open(SETTINGS_PATH) as fp:
    settings = json.load(fp)

class PauseMenu():
    """
    Eine Klasse, die ein Pausen-Menue darstellt

    ...

    Attribute
    ----------
    font : pygame.Font
        Schriftart und Groesse der Ueberschrift
    screeen : pygame.Surface
        Bildschirm, auf den das Pausen-Menue gemalt wird
    continue_button : Button
        Button, mit der Bezeichnung "CONTINUE", mit dem man zum Spiel zurueckkehren kann
    save_button : Button
        Button, mit der Bezeichnung "SAVE", mit dem man das aktuelle Spiel in einer
        JSON Datei speichern kann
    load_button : Button
        Button, mit der Bezeichnung "LOAD", mit dem man ein Spielstand laden kann
    resume : func
        Funktion, die beim Druecken des continue_buttons ausgefuehrt werden soll,
        um zum Spiel zurueckzukehren
    save_to_json : func
        Funktion, die beim Druecken des save_buttons ausgefuehrt werden soll,
        um das Spiel zu speichern
    load_from_json : func
        Funktion, die beim Druecken des load_buttons ausgefuehrt werden soll,
        um ein Spielstand zu laden
    
    Methoden
    ---------
    show_title()
        zeigt den Titel "PAUSED"
    set_resume(resume : func)
        setzt die resume-Funktion
    set_save(save : func)
        setzt die save-Funktion
    set_load(load : func)
        setzt die load-Funktion
    draw_background()
        malt den Hintergrund des Pausenmenues (schwarz)
    check_buttons()
        ueberprueft, ob die Buttons gedrueckt wurden und fuehrt die entsprechende Funktion aus
    run()
        malt die Komponenten und ueberprueft mit check_buttons() die Buttons
    """
    def __init__(self, screen: pygame.Surface):
        """
        Parameter
        ---------
        screen : pygame.Surface
            Bildschirm, auf den das Menue gemalt wird
        """
        self.font = pygame.font.SysFont("arial", settings["pause_menu"]["font_size"])
        self.screen = screen
        self.continue_button = Button((self.screen.get_width() / 2, 300), "CONTINUE")
        self.save_button = Button((self.screen.get_width() / 2, 400), "SAVE")
        self.load_button = Button((self.screen.get_width() / 2, 500), "LOAD")
        self.resume = None
        self.save_to_json = None
        self.load_from_json = None

    def show_title(self):
        """zeigt den Titel "PAUSED"
        
        Parameter
        ----------
        keine

        Rueckgabe
        ----------
        keine
        """
        text = "PAUSED"
        text_surface = self.font.render(text, False, settings["pause_menu"]["font_color"])
        text_rect = text_surface.get_rect(center = (self.screen.get_width() / 2, 20))
        self.screen.blit(text_surface, text_rect)
    
    def set_resume(self, resume):
        """setzt die resume-Funktion
        
        Parameter
        ----------
        resume : func
            Funktion, mit der man zum Spiel beim Druecken des continue_buttons zurueckkehren soll

        Rueckgabe
        ----------
        keine
        """
        self.resume = resume
    
    def set_save(self, save):
        """setzt die save-Funktion
        
        Parameter
        ----------
        save : func
            Funktion, mit der man das aktuelle Spiel beim Druecken des save_buttons
            speichern soll

        Rueckgabe
        ----------
        keine
        """
        self.save_to_json = save
    
    def set_load(self, load):
        """setzt die load-Funktion
        
        Parameter
        ----------
        load : func
            Funktion, mit der man ein Spielstand beim Druecken des load_buttons
            laden soll

        Rueckgabe
        ----------
        keine
        """
        self.load_from_json = load
    
    def draw_background(self):
        """malt den Hintergrund des Pausenmenues (schwarz)
        
        Parameter
        ----------
        keine

        Rueckgabe
        ----------
        keine
        """
        background_rect = pygame.Rect((0, 0), (self.screen.get_width(), self.screen.get_height()))
        pygame.draw.rect(self.screen, "black", background_rect)

    def check_buttons(self):
        """ueberprueft, ob die Buttons gedrueckt wurden und fuehrt die entsprechende Funktion aus
        
        Parameter
        ----------
        keine

        Rueckgabe
        ----------
        keine
        """
        if self.continue_button.get_just_pressed():
            self.resume()
        elif self.save_button.get_just_pressed():
            self.save_to_json()
        elif self.load_button.get_just_pressed():
            self.load_from_json()
    
    def run(self):
        """malt die Komponenten und ueberprueft mit check_buttons() die Buttons
        
        Parameter
        ----------
        keine

        Rueckgabe
        ----------
        keine
        """
        self.draw_background()
        self.continue_button.draw(self.screen)
        self.save_button.draw(self.screen)
        self.load_button.draw(self.screen)
        self.show_title()
        self.check_buttons()

        
