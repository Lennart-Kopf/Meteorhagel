import pygame
from item import Item
from spaceship import Spaceship
import json
from pathes import *
import pathlib
with open(SETTINGS_PATH) as fp:
    settings = json.load(fp)

class Heart(Item):
    """
    Eine Klasse, die ein Herz darstellt
    ...
    
    Superklasse
    ------------
    Item

    Attribute
    ---------
    hp : int
        die Leben die ein Herz gibt (in settings)
    image : pygame.Surface
        das Bild des Herz
    rect : pygame.Rect
        Koordinaten und Groesse des Herz
    mask : pygame.Mask
        Maske des Herz, aus den nicht-transparenten Pixeln
    
    Methoden
    --------
    activate(spaceship : Spaceship)
        fuegt dem Spaceship die Leben hinzu und loescht das Herz aus Gruppe
    save_to_json() -> dict
        speichert position, current_frame und type(Herz) in Dictionary und gibt es zurueck
    """
    def __init__(self, position, current_frame = 0):
        """
        Parameter
        ---------
        position : tuple
            die Position des Herz
        current_frame : int, optional
            der aktuelle Frame (Standard ist 0)
        """
        super().__init__(current_frame)
        self.hp = settings["items"]["heart"]["hp_value"]
        self.image = pygame.image.load(IMAGE_PATH/"heart.png")
        self.rect = self.image.get_rect(center = position)
        self.mask = pygame.mask.from_surface(self.image)

    def activate(self, spaceship: Spaceship):
        """fuegt dem Spaceship die Leben hinzu und loescht das Herz aus Gruppe
        
        Parameter
        ---------
        spaceship : Spaceship
            das Raumschiff
        
        Rueckgabe
        ---------
        keine
        """
        spaceship.add_health(self.hp)
        self.kill()

    def save_to_json(self):
        """speichert position, current_frame und type(Herz) in Dictionary und gibt es zurueck
        
        Parameter
        ---------
        keine

        Rueckgabe
        ---------
        dic : dict
            Dictionary aus position, current_frame und type
        """
        dic = {"position": self.rect.center, "current_frame": self.current_frame, "type": "heart"}
        return dic   
        