import pygame
from item import Item
from spaceship import Spaceship
import json
from pathes import *
import pathlib
with open(SETTINGS_PATH) as fp:
    settings = json.load(fp)

class Coin(Item):
    """
    Eine Klasse, die eine Muenze darstellen soll
    ...

    Superklasse
    -----------
    Item

    Attribute
    ---------
    value : int
        Wert der Muenze
    sprites : list[pygame.Surface]
        Bilder der Muenze
    animation_speed: int
        wie schnell die Animation abgespielt werden soll
    
    Methoden
    --------
    activate(spaceship: Spaceship)
        fuegt den Wert der Muenze den Muenzen des Spaceships hinzu
        und löscht sich dann aus der Gruppe
    animate()
        animiert die Drehung der Muenze
    update()
        aktualisiert die Muenze, indem sie immer weiter animiert wird und die update()-
        Methode von Item ausfuehrt
    """
    def __init__(self, current_frame = 0):
        """
        Parameter
        ---------
        current_frame : int, optional
            der aktuelle Frame der Animation (Standard ist 0)
        """
        super().__init__(current_frame)
        self.value = None
        self.sprites = []
        self.animation_speed = settings["animation_speed"]
        
    def activate(self, spaceship: Spaceship):
        """fuegt den Wert der Muenze den Muenzen des Spaceships hinzu
        und löscht sich dann aus der Gruppe

        Parameter
        ---------
        spaceship : Spaceship
            das Spieler-Spaceship
        
        Rueckgabe
        ---------
        keine
        """
        spaceship.add_coins(self.value)
        self.kill()

    def animate(self):
        """animate()
        animiert die Drehung der Muenze
        
        Parameter
        ----------
        keine

        Rueckgabe
        ---------
        keine
        """
        index = (self.current_frame // self.animation_speed) % len(self.sprites)
        self.image = self.sprites[index]
    
    def update(self):
        """aktualisiert die Muenze, indem sie immer weiter animiert wird, und die update()-Methode
        von Item ausfuehrt
        
        Parameter
        ---------
        keine

        Rueckgabe
        ---------
        keine
        """
        self.animate()
        super().update()
        


class RedCoin(Coin):
    """
    Eine Klasse, die eine rote Muenze darstellt
    ...

    Superklasse
    ------------
    Coin

    Attribute
    ---------
    sprites : list[pygame.Surface]
        Bilder der roten Muenze
    image : pygame.Surface
        das aktuelle Bild der Animation
    rect : pygame.Rect
        die Koordinaten der Muenze und Groesse
    value : int
        Wert der Muenze
    mask : pygame.Mask
        Maske aus dem Bild fuer Kollision, nur nicht-transparente Pixel
    
    Methoden
    --------
    save_to_json() -> dict
        speichert position, current_frame und im type, was fuer eine Muenze sie ist
        in Dictionary und gibt es zurueck
    """
    def __init__(self, position: tuple, current_frame = 0):
        """
        Parameter
        ----------
        position : tuple
            die Koordinaten der Muenzen-Mitte
        current_frame : int, optional
            der aktuelle frame der Animation (Standard ist 0)
        """
        super().__init__(current_frame)
        self.sprites.append(pygame.image.load(IMAGE_PATH/"red_coin000.png").convert_alpha())
        self.sprites.append(pygame.image.load(IMAGE_PATH/"red_coin001.png").convert_alpha())
        self.sprites.append(pygame.image.load(IMAGE_PATH/"red_coin002.png").convert_alpha())
        self.sprites.append(pygame.image.load(IMAGE_PATH/"red_coin003.png").convert_alpha())
        self.sprites.append(pygame.image.load(IMAGE_PATH/"red_coin004.png").convert_alpha())
        self.image: pygame.Surface = self.sprites[0]
        self.rect = self.image.get_rect(center = position)
        self.value = settings["items"]["coins"]["red_coin_value"]
        self.mask = pygame.mask.from_surface(self.image)
    
    def save_to_json(self):
        """speichert position, current_frame und im type, was fuer eine Muenze sie ist
        in Dictionary und gibt es zurueck
        
        Parameter
        ----------
        keine

        Rueckgabe
        ---------
        dic : dict
            das Dictionary aus position, current_frame und Art der Muenze(type)
        """
        dic = {"position": self.rect.center, "current_frame": self.current_frame, "type": "red_coin"}
        return dic

class SilverCoin(Coin):
    """
    Eine Klasse, die eine silberne Muenze darstellt
    ...

    Superklasse
    ------------
    Coin

    Attribute
    ---------
    sprites : list[pygame.Surface]
        Bilder der silbernen Muenze
    image : pygame.Surface
        das aktuelle Bild der Animation
    rect : pygame.Rect
        die Koordinaten der Muenze und Groesse
    value : int
        Wert der Muenze
    mask : pygame.Mask
        Maske aus dem Bild fuer Kollision, nur nicht-transparente Pixel
    
    Methoden
    --------
    save_to_json() -> dict
        speichert position, current_frame und im type, was fuer eine Muenze sie ist
        in Dictionary und gibt es zurueck
    """
    
    def __init__(self, position: tuple, current_frame = 0):
        """
        Parameter
        ----------
        position : tuple
            die Koordinaten der Muenzen-Mitte
        current_frame : int, optional
            der aktuelle frame der Animation (Standard ist 0)
        """
        super().__init__(current_frame)
        self.sprites.append(pygame.image.load(IMAGE_PATH/"silver_coin000.png").convert_alpha())
        self.sprites.append(pygame.image.load(IMAGE_PATH/"silver_coin001.png").convert_alpha())
        self.sprites.append(pygame.image.load(IMAGE_PATH/"silver_coin002.png").convert_alpha())
        self.sprites.append(pygame.image.load(IMAGE_PATH/"silver_coin003.png").convert_alpha())
        self.sprites.append(pygame.image.load(IMAGE_PATH/"silver_coin004.png").convert_alpha())
        self.image: pygame.Surface = self.sprites[0]
        self.rect = self.image.get_rect(center = position)
        self.value = settings["items"]["coins"]["silver_coin_value"]
        self.mask = pygame.mask.from_surface(self.image)
    
    def save_to_json(self):
        """speichert position, current_frame und im type, was fuer eine Muenze sie ist
        in Dictionary und gibt es zurueck
        
        Parameter
        ----------
        keine

        Rueckgabe
        ---------
        dic : dict
            das Dictionary aus position, current_frame und Art der Muenze(type)
        """
        dic = {"position": self.rect.center, "current_frame": self.current_frame, "type": "silver_coin"}
        return dic

class GoldCoin(Coin):
    """
    Eine Klasse, die eine goldene Muenze darstellt
    ...
    
    Superklasse
    ------------
    Coin

    Attribute
    ---------
    sprites : list[pygame.Surface]
        Bilder der goldene Muenze
    image : pygame.Surface
        das aktuelle Bild der Animation
    rect : pygame.Rect
        die Koordinaten der Muenze und Groesse
    value : int
        Wert der Muenze
    mask : pygame.Mask
        Maske aus dem Bild fuer Kollision, nur nicht-transparente Pixel
    
    Methoden
    --------
    save_to_json() -> dict
        speichert position, current_frame und im type, was fuer eine Muenze sie ist
        in Dictionary und gibt es zurueck
    """
    def __init__(self, position: tuple, current_frame = 0):
        """
        Parameter
        ----------
        position : tuple
            die Koordinaten der Muenzen-Mitte
        current_frame : int, optional
            der aktuelle frame der Animation (Standard ist 0)
        """
        super().__init__(current_frame)
        self.sprites.append(pygame.image.load(IMAGE_PATH/"gold_coin000.png").convert_alpha())
        self.sprites.append(pygame.image.load(IMAGE_PATH/"gold_coin001.png").convert_alpha())
        self.sprites.append(pygame.image.load(IMAGE_PATH/"gold_coin002.png").convert_alpha())
        self.sprites.append(pygame.image.load(IMAGE_PATH/"gold_coin003.png").convert_alpha())
        self.sprites.append(pygame.image.load(IMAGE_PATH/"gold_coin004.png").convert_alpha())
        self.image: pygame.Surface = self.sprites[0]
        self.rect = self.image.get_rect(center = position)
        self.value = settings["items"]["coins"]["gold_coin_value"]
        self.mask = pygame.mask.from_surface(self.image)
    
    def save_to_json(self):
        """speichert position, current_frame und im type, was fuer eine Muenze sie ist
        in Dictionary und gibt es zurueck
        
        Parameter
        ----------
        keine

        Rueckgabe
        ---------
        dic : dict
            das Dictionary aus position, current_frame und Art der Muenze(type)
        """
        dic = {"position": self.rect.center, "current_frame": self.current_frame, "type": "gold_coin"}
        return dic
        


