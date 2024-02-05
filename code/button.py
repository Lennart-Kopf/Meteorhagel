import pygame
import json
from pathes import *
import pathlib
with open(SETTINGS_PATH) as fp:
    settings = json.load(fp)


class Button():
    """
    Eine Klasse, die einen einfachen Button darstellt
    ...
    
    Attribute
    ---------
    text : str
        der Text, der auf dem Button angezeigt wird
    position : tuple
        die Position der Mitte des Buttons
    background_color : str
        die Farbe des Buttons
    activated_color : str
        die Farbe des Buttons, wenn der Mauszeiger ueber ihm ist
    font : pygame.Font
        die Schriftart und Groesse des Textes
    color : str
        die aktuelle Farbe des buttons
    text_surface : pygame.Surface
        das erzeugte Bild aus dem Text
    text_rect : pygame.Rect
        das Rect-Objekt aus dem Bild mit den Koordinaten und position als Mitte
    background_rect : pygame.Rect
        die Koordinaten des Buttons hinter dem Text
    disabled: bool
        zeigt an, ob der Knopf ausgeschaltet ist
    
    Methoden
    --------
    disable()
        schaltet den Button aus, wenn noch nicht ausgeschaltet
        und setzt die aktuelle Farbe auf die gedrueckte
    activate()
        schaltet den Button an, wenn noch nicht an und 
        setzt die Farbe auf die normale
    set_text(text: str)
        ersetzt den Text durch den neuen Text und aktualisiert die Koordinaten
        der Rects
    mouse_over()
        ueberprueft, ob die Maus ueber dem Button ist und setzt dementsprechend die Farben
    get_just_pressed()
        ueberprueft, ob der Knopf gerade einmalig gedrueckt wurde, wenn die Maus ueber dem Button ist
        und die linke Maustaste heruntergedrueckt wird (nur wenn der Button an ist)
    draw(screen: pygame.Surface)
        malt den Button auf den Bildschirm, und fuehrt dabei mouse_over() aus, wenn der Button aktiv ist
    
    """
    def __init__(self, position: tuple, text: str):
        """
        Parameter
        ---------
        position : tuple
            die Koordinaten der Mitte des Buttons
        text : str
            der Text, der angezeigt werden soll
        """
        self.text = text
        self.position = position
        self.background_color = settings["button"]["color"]
        self.activated_color = settings["button"]["activate_color"]
        self.font = pygame.font.SysFont("arial", settings["button"]["font_size"])
        self.font_color = settings["button"]["font_color"]
        self.color = self.background_color

        self.text_surface = self.font.render(self.text, True, self.font_color)
        self.text_rect = self.text_surface.get_rect(center = position)
        self.background_rect = pygame.Rect((self.text_rect.left - 20, self.text_rect.top - 20), (self.text_rect.width + 40, self.text_rect.height + 40))
    
        self.disabled = False

    def disable(self):
        """schaltet den Button aus, wenn noch nicht ausgeschaltet
        und setzt die aktuelle Farbe auf die gedrueckte
        
        Parameter
        ---------
        keine

        Rueckgabe
        ---------
        keine
        """
        if not self.disabled:
            self.disabled = True
        self.color = self.activated_color
    
    def activate(self):
        """schaltet den Button an, wenn noch nicht an und 
        setzt die Farbe auf die normale

        Paramter
        --------
        keine

        Rueckgabe
        ---------
        keine
        """
        if self.disabled:
            self.disabled = False
        self.color = self.background_color

    def set_text(self, text):
        """ersetzt den Text durch den neuen Text und aktualisiert die Koordinaten
        der Rects
        
        Paramter
        ---------
        keine

        Rueckgabe
        ----------
        keine
        """
        self.text = text
        self.text_surface = self.font.render(self.text, True, self.font_color)
        self.text_rect = self.text_surface.get_rect(center = self.position)
        self.background_rect = pygame.Rect((self.text_rect.left - 20, self.text_rect.top - 20), (self.text_rect.width + 40, self.text_rect.height + 40))

    def mouse_over(self):
        """ueberprueft, ob die Maus ueber dem Button ist und setzt dementsprechend die Farben
        
        Parameter
        ---------
        keine

        Rueckgabe
        ---------
        keine
        """
        mouse_position = pygame.mouse.get_pos()
        if self.background_rect.collidepoint(mouse_position):
            self.color = self.activated_color
        else:
            self.color = self.background_color

    
    def get_just_pressed(self):
        """ueberprueft, ob der Knopf gerade einmalig gedrueckt wurde, wenn die Maus ueber dem Button ist
        und die linke Maustaste heruntergedrueckt wird (nur wenn der Button an ist)
        
        Parameter
        --------
        keine

        Rueckgabe
        ---------
        keine
        """
        if self.background_rect.collidepoint(pygame.mouse.get_pos()) and not self.disabled:
            if pygame.event.wait().type == pygame.MOUSEBUTTONDOWN:
                return True
    
    def draw(self, screen: pygame.Surface):
        """ malt den Button auf den Bildschirm, und fuehrt dabei mouse_over() aus, wenn der Button aktiv ist
        
        Parameter
        ---------
        screen : pygame.Surface
            der Bildschirm, auf den der Button gemalt werden soll
        
        Rueckgabe
        ---------
        keine
        """
        if not self.disabled:
            self.mouse_over()
        pygame.draw.rect(screen, self.color, self.background_rect)
        screen.blit(self.text_surface, self.text_rect)
    

        
