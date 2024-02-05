import pygame
import json
from pathes import *
import pathlib
with open(SETTINGS_PATH) as fp:
    settings = json.load(fp)


class Asteroid(pygame.sprite.Sprite):
    """
    Eine Klasse, die einen Asteroiden darstellt
    ...
    
    Superklasse
    -----------
    pygame.sprite.Sprite

    Attribute
    ---------
    image : pygame.Surface
        das Bild des Asteroiden
    rect : pygame.Rect
        das Rect-Objekt des Bildes
    direction : pygame.math.Vector2
        die Richtung, in die der Asteroid fliegt als 2D-Vektor
    velocity : float
        die Geschwindigkeit des Asteroiden
    mask : pygame.Mask
        die Maske des Bildes, wichtig für die Kollision-Ueberpruefung
        besteht aus den nicht-transparenten Pixeln des Bildes
    size : tuple
        die Breite und Hoehe des Asteroiden
    border : tuple
        die Breite und Hoehe des Bildschirms
    
    Methoden
    --------
    move()
        bewegt die Mitte des Rect-Objekts um den Vektor aus der Multiplikation von direction und velocity
    get_position() -> tuple
        gibt die Mitte des Rect-Objekts zurueck
    save_to_json() -> dict
        speichert die Attribute position, velocity, size, direction in Dictionary
        und gibt es zurueck
    check_border()
        ueberprueft, ob der Asteroid ausserhalb des Bildschirms ist und loescht ihn
        dann aus der Gruppe, wenn dies der Fall ist
    update()
        fuert move() und check_border() bei jedem Durchlauf aus
    """
    def __init__(self, position, velocity, direction, size: tuple):
        """
        Parameter
        ---------
        position: tuple
            Koordinaten der Rect-Mitte
        velocity : float
            Geschwindigkeit
        direction : tuple
            Richtung
        size : tuple
            Groesse
        """
        super().__init__()
        self.image = pygame.image.load(IMAGE_PATH/"Asteroid 01 - Base.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, size)
        self.rect = self.image.get_rect(center = position)
        self.direction = pygame.math.Vector2(direction)
        self.velocity = velocity
        self.mask = pygame.mask.from_surface(self.image)
        self.size = size
        self.border = tuple((settings["screen_width"], settings["screen_height"]))

    def move(self):
        """bewegt die Mitte des Rect-Objekts um den Vektor aus der Multiplikation von direction und velocity

        Parameter
        ---------
        keine

        Rueckgabe
        ---------
        keine
        """
        move = self.direction * self.velocity
        self.rect.move_ip(move)
    
    def get_position(self):
        """gibt die Mitte des Rect-Objekts zurueck
        
        Parameter
        ---------
        keine

        Rueckgabe
        ---------
        rect.center : tuple
            die aktuellen Koordinaten der Mitte des Asteroiden
        """
        return self.rect.center

    def save_to_json(self):
        """speichert die Attribute position, velocity, size, direction in Dictionary
        und gibt es zurueck
        
        Parameter
        ----------
        keine

        Rueckgabe
        ---------
        dic : dict
            das Dictionary aus position, velocity, size und direction
        """
        dic = {"position": self.rect.center, "velocity": self.velocity, "size": self.size, "direction": tuple(self.direction)}
        return dic
    
    def check_border(self):
        """ueberprueft, ob der Asteroid ausserhalb des Bildschirms ist und loescht ihn
        dann aus der Gruppe, wenn dies der Fall ist
        
        Parameter
        ---------
        keine

        Rueckgabe
        ---------
        keine
        """
        if self.rect.centerx >= self.border[0] or self.rect.centerx <= 0 or self.rect.centery <= 0 or self.rect.centery >= self.border[1]:
            self.kill()
    
    def update(self):
        """fuert move() und check_border() bei jedem Durchlauf aus
        
        Parameter
        ---------
        keine

        Rueckgabe
        ---------
        keine
        """
        self.move()
        self.check_border()