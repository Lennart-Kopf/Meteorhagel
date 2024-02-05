import pygame
import json
import pathlib
from pathes import *
with open(SETTINGS_PATH) as fp:
    settings = json.load(fp)


class Laser(pygame.sprite.Sprite):
    """
    Eine Klasse, die ein Laser darstellt
    ...
    
    Superklasse
    -----------
    pygame.sprite.Sprite

    Attribute
    ---------
    sprites : list[pygame.Surface]
        die Bilder der Laser-Animation
    current_sprite_index : int
        der Index des aktuellen Bildes
    direction : pygame.math.Vector2
        Richtung als 2D-Vektor
    velocity : float
        Geschwindigkeit
    position : tuple
        Position
    border : tuple
        Hoehe und Breite des Bildschirms
    mask : pygame.Mask
        Maske aus den nicht-transparenten Pixeln des Bildes fuer Kollision
    
    Methoden
    ---------
    rotate_sprites(position : tuple)
        rotiert alle Sprites der Sprite liste entsprechend
        der direction und setzt das aktuelle Bild (image)
        und erzeugt das Rect daraus, bei dem mitte unten
        die Position ist
    move()
        bewegt das rect, um das Produkt aus direction und velocity
    check_border()
        loescht den Laser, wenn er ausserhalb des Bildschirms ist
    save_to_json() -> dict
        speichert position, direction, velocity in Dictionary
        und gibt es zurueck
    update()
        aktualisiert, indem es das naechste Bild als aktuelles setzt
        und bewegt und ueberprueft, ob es ausserhalb ist
    
    """
    def __init__(self, position, direction: tuple, velocity: float):
        """
        Parameter
        ----------
        position : tuple
            Position
        direction : tuple
            Richtung
        velocity : float
            Geschwindigkeit
        """
        super().__init__()
        self.sprites: list[pygame.Surface] = []
        self.sprites.append(pygame.image.load(IMAGE_PATH/"laser000.png").convert_alpha())
        self.sprites.append(pygame.image.load(IMAGE_PATH/"laser001.png").convert_alpha())
        self.sprites.append(pygame.image.load(IMAGE_PATH/"laser002.png").convert_alpha())
        self.sprites.append(pygame.image.load(IMAGE_PATH/"laser003.png").convert_alpha())
        self.sprites.append(pygame.image.load(IMAGE_PATH/"laser004.png").convert_alpha())
        self.sprites.append(pygame.image.load(IMAGE_PATH/"laser005.png").convert_alpha())
        self.sprites.append(pygame.image.load(IMAGE_PATH/"laser006.png").convert_alpha())
        self.sprites.append(pygame.image.load(IMAGE_PATH/"laser007.png").convert_alpha())
        self.current_sprite_index = 0
        self.direction = pygame.math.Vector2(direction)
        self.velocity = velocity
        self.position = position
        self.rotate_sprites(self.position)
        self.border = tuple((settings["screen_width"], settings["screen_height"]))
        self.mask = pygame.mask.from_surface(self.image)

    def rotate_sprites(self, position):
        """rotiert alle Sprites der Sprite liste entsprechend
        der direction und setzt das aktuelle Bild (image)
        und erzeugt das Rect daraus, bei dem mitte unten
        die Position ist
        
        Parameter
        ---------
        position : tuple
            Position
        
        Rueckgabe
        ----------
        keine
        """
        angle = self.direction.angle_to((0, -1)) 
        for index, sprite in enumerate(self.sprites):
           rotated_sprite = pygame.transform.rotate(sprite, angle)
           self.sprites[index] = rotated_sprite
        self.image = self.sprites[self.current_sprite_index]
        self.rect = self.image.get_rect(midbottom = position)
            
    def move(self):
        """bewegt das rect, um das Produkt aus direction und velocity
        
        Parameter
        --------
        keine

        Rueckgabe
        ---------
        keine
        """
        move = self.direction * self.velocity
        self.rect.move_ip(move)
    
    def check_border(self):
        """loescht den Laser, wenn er ausserhalb des Bildschirms ist
        
        Parameter
        ---------
        keine
        
        Rueckgabe
        ---------
        keine
        """
        if self.rect.centerx >= self.border[0] or self.rect.centerx <= 0 or self.rect.centery <= 0 or self.rect.centery >= self.border[1]:
            self.kill()
    
    def save_to_json(self):
        """speichert position, direction, velocity in Dictionary
        und gibt es zurueck
        
        Parameter
        ----------
        keine

        Rueckgabe
        ----------
        dic : dict
            Dictionary aus position, direction und velocity
        """
        dic = {"position": self.rect.center, "direction": tuple(self.direction), "velocity": self.velocity}
        return dic


    def update(self):
        """aktualisiert, indem es das naechste Bild als aktuelles setzt
        und bewegt und ueberprueft, ob es ausserhalb ist
        
        Parameter
        ----------
        keine

        Rueckgabe
        ---------
        keine
        """
        self.current_sprite_index += 1
        if self.current_sprite_index >= len(self.sprites):
            self.current_sprite_index = 0
        self.image = self.sprites[self.current_sprite_index]
        self.move()
        self.check_border()