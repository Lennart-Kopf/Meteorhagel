from typing import Any
import pygame
import json
from pathes import *
with open(SETTINGS_PATH) as fp:
    settings = json.load(fp)

class Item(pygame.sprite.Sprite):
    """
    Eine Klasse, die ein Item darstellt
    ...
    
    Superklasse
    ------------
    pygame.sprite.Sprite

    Attribute
    ---------
    life_time : int
        wie viele Ticks ein Item lebt, definiert in settings
    current_frame : int
        der aktuelle Frame
    
    Methoden
    ---------
    check_kill()
        wenn der aktuelle Frame hoeher als die life_time ist, wird das Item
        geloescht
    update()
        aktualisiert das Item, indem check_kill geprueft wird
        und der aktuelle Frame erhoeht wird
    """
    def __init__(self, current_frame = 0):
        """
        Parameter
        ----------
        current_frame : int, optional
            der aktuelle Frame (Standard ist 0)
        """
        super().__init__()
        self.life_time = settings["items"]["life_time"]
        self.current_frame = current_frame
    
    def check_kill(self):
        """wenn der aktuelle Frame hoeher als die life_time ist, wird das Item
        geloescht
        
        Parameter
        ---------
        keine

        Rueckgabe
        ----------
        keine
        """
        if self.current_frame >= self.life_time:
            self.kill()
    
    def update(self):
        """aktualisiert das Item, indem check_kill geprueft wird
        und der aktuelle Frame erhoeht wird
        
        Parameter
        --------
        keine
        
        Rueckgabe
        ---------
        keine
        """
        self.check_kill()
        self.current_frame += 1
