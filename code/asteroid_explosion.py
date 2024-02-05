import pygame
import pathlib
from pathes import *

class AsteroidExplosion(pygame.sprite.Sprite):
    """
    Eine Klasse, die eine Explosion eines Asteroiden darstellen soll
    ...

    Super-Klasse
    ------------
    pygame.sprite.Sprite

    Attribute
    ---------
    sprites : list[pygame.Surface]
        speichert, die verschieden Bilder während der Animation
    current_frame : int
        der aktuelle Frame der Animation
    frames_per_animation : int
        wie viele Frames, das Bild gleich bleibt
    image : pygame.Surface
        das aktuelle Bild
    rect : pygame.Rect
        das Rect-Objekt des Bildes, die Mitte ist die uebergebene Position
    rect.center : tuple
        die Mitte des Rect-Objekts
    
    Methoden
    --------
    animate()
        animiert die Explosion, indem das aktuelle Bild dem Frame angepasst wird
    check_kill()
        ueberprueft, ob die Explosion zu Ende ist (das letzte Bild gezeigt wurde)
        und loescht sie dann anschliessend aus ihrer Gruppe
    save_to_json() -> dict
        speichert current_frame und position in Dictionary und gibt es zurueck
    update()
        wird bei jedem Durchlauf der Mainloop ausgefuehrt, um die Explosion zu animieren
        und zu ueberpruefen, ob sie bereits fertig ist
    """
    def __init__(self, position: tuple, current_frame = 0):
        """
        Parameter
        ---------
        position : tuple
            die Position der Explosion
        current_frame : int, optional
            der aktuelle Frame (Standard ist 0)
        """
        super().__init__()
        self.sprites: list[pygame.Surface] = []
        self.sprites.append(pygame.image.load(IMAGE_PATH/"asteroid_explosion000.png").convert_alpha())
        self.sprites.append(pygame.image.load(IMAGE_PATH/"asteroid_explosion001.png").convert_alpha())
        self.sprites.append(pygame.image.load(IMAGE_PATH/"asteroid_explosion002.png").convert_alpha())
        self.sprites.append(pygame.image.load(IMAGE_PATH/"asteroid_explosion003.png").convert_alpha())
        self.sprites.append(pygame.image.load(IMAGE_PATH/"asteroid_explosion004.png").convert_alpha())
        self.sprites.append(pygame.image.load(IMAGE_PATH/"asteroid_explosion005.png").convert_alpha())
        self.sprites.append(pygame.image.load(IMAGE_PATH/"asteroid_explosion006.png").convert_alpha())
        self.sprites.append(pygame.image.load(IMAGE_PATH/"asteroid_explosion007.png").convert_alpha())
        self.current_frame = current_frame
        self.frames_per_animation = 2
        index = self.current_frame // self.frames_per_animation
        self.image = self.sprites[index]
        self.rect = self.image.get_rect(center = position)
        self.rect.center = position
    
    def animate(self):
        """animiert die Explosion, indem das aktuelle Bild dem Frame angepasst wird

        Parameter
        ----------
        keine

        Rueckgabe
        ---------
        keine
        """
        index = self.current_frame // self.frames_per_animation
        if index < len(self.sprites):
            self.image = self.sprites[index]
        self.current_frame += 1

    def check_kill(self):
        """ueberprueft, ob die Explosion zu Ende ist (das letzte Bild gezeigt wurde)
        und loescht sie dann anschliessend aus ihrer Gruppe

        Parameter
        ---------
        keine

        Rueckgabe
        ---------
        keine
        """
        if self.current_frame // self.frames_per_animation >= len(self.sprites):
            self.kill()
    
    def save_to_json(self):
        """speichert current_frame und position in Dictionary und gibt es zurueck
        
        Parameter
        ---------
        keine

        Rueckgabe
        ----------
        dic : dict
            current_frame und position als Dictionary
        """
        dic = {"current_frame": self.current_frame, "position": self.rect.center}
        return dic
    
    def update(self):
        """wird bei jedem Durchlauf der Mainloop ausgefuehrt, um die Explosion zu animieren
        und zu ueberpruefen, ob sie bereits fertig ist

        Parameter
        ---------
        keine

        Rueckgabe
        ---------
        keine
        """
        self.check_kill()
        self.animate()
        
        

