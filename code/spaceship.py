import pygame
from laser import Laser
import json
import pathlib
from pathes import *
with open(SETTINGS_PATH) as fp:
    settings = json.load(fp)


class Spaceship(pygame.sprite.Sprite):
    """
    Eine Klasse, die ein Spaceship und somit den Spieler darstellt

    ...

    Superklasse
    -----------
    pygame.sprite.Sprite

    Attribute
    ----------
    width : int
        Breite des Spaceships aus settings
    height : int
        Hoehe des Spaceships aus settings
    velocitiy_level : int
        das aktuelle Level der Geschwindigkeit
    velocity_levels : list[float]
        die Geschwindigkeit bei verschiedenen Levels aus settings
    velocity : float
        die aktuelle Geschwindigkeit
    direction : pygame.math.Vector2
        Richtung als 2D-Vektor
    border : pygame.math.Vector2
        Hoehe und Breite des Bildschirms aus settings (Ecke unten rechts)
    position : tuple
        Position
    lasers : pygame.sprite.Group
        Gruppe der Laser, die vom Spaceship geschossen wurden
    last_shot_ticks : int
        bei welchem tick zuletzt geschossen wurde
    cooldown_level : int
        das aktuelle Level des Cooldowns
    cooldown_levels : list[float]
        der Cooldown bei verschiedenen Levels aus settings
    cooldown_ticks : int
        Cooldown, Zeit nach der erst geschossen werden kann
    ready_to_shoot : bool
        ob Spaceship bereit zu schiessen
    score : int
        der aktuelle Score
    max_health_level : int
        das aktuelle Level der maximalen Leben
    max_health_levels : list[int]
        die maximalen Leben bei verschiedenen Levels aus settings
    max_health : int
        die aktuellen maximalen Leben
    health : int
        die aktuellen Leben
    damaged_image : pygame.Surface
        Bild des Raumschiffs, wenn beschaedigt
    slight_damage_image : pygame.Surface
        Bild des Raumschiffs, wenn leicht beschaedigt
    very_damaged_image : pygame.Surface
        Bild des Raumschiffs, wenn stark beschaedigt
    full_health_image : pygame.Surface
        Bild des Raumschiffs, wenn volle Leben
    image : pygame.Surface
        das aktuelle Bild
    old_image : pygame.Surface
        speichert das Bild vor der Rotation zwischen
    rect : pygame.Rect
        Koordinaten und Groesse des Raumschiffs
    mask : pygame.Masc
        Maske aus den nicht-transparenten Pixeln des Bildes fuer Kollision
    coins : int
        Wert der Muenzen, die der Spieler besitzt
    cannon_vector : pygame.math.Vector2
        Vektor von der Mitte des Bildes zur Kanone
    cannon_position : pygame.math.Vector2
        Position der Kanone
    
    Methoden
    ---------
    check_controls()
        ueberprueft die Mausposition und richtet das Raumschiff danach aus
        wenn Leertaste gedrueckt wird, wird geschossen, indem shoot() ausgefuehrt wird
        ready_to_shoot wird anschliessend auf false gesetzt
        wenn UP oder W gedrueckt wird, wird das rect um das Produkt aus velocity und direction bewegt
    check_cooldown()
        ueberprueft, ob der cooldown abgelaufen ist, wenn ja wird ready_to_shoot auf True gesetzt
    align()
        aktualisiert direction gemaess der Maus-Position und richtet die Position der Kanone
        danach aus
    rotate()
        rotiert das Bild nach der direction
    shoot()
        laesst das Raumschiff schiessen, indem der Lasergruppe ein Laser mit der Richtung und
        der Position der Kanone hinzugefuegt wird
    get_lasers() -> pygame.sprite.Group[Laser]
        gibt die Lasergruppe zurueck
    check_border()
        ueberprueft, ob das Raumschiff ausserhalb von Bildschirm, wenn ja wird die Position
        so gesetzt, dass der Spieler am Rand bleibt
    check_health()
        ueberprueft den Anteil der aktuellen Leben an den maximalen Leben und aktualisiert dementsprechend
        das aktuelle Bild (image) und speichert eine Kopie in old_image
    get_position() -> tuple
        gibt die Position der Raumschiff-Mitte zurueck
    hit(damage : int)
        zieht dem Raumschiff die Anzahl an Leben ab
    set_position(position : tuple)
        setzt die Position der Mitte des Raumschiffs
    add_coins(coins : int)
        fuegt den Muenzen des Spielers die Anzahl hinzu
    add_health(health : int)
        fuegt Spieler Anzahl an Leben hinzu, wenn das Maximum noch nicht erreicht wurde
    increase_score()
        erhoeht den Score um 1
    get_score() -> int
        gibt Score zurueck
    get_health() -> int
        gibt Leben zurueck
    get_max_health() -> int
        gibt maximale Leben zurueck
    get_coins() -> int
        gibt Wert der Muenzen zurueck
    get_ready_to_shoot() -> bool
        gibt ready_to_shoot zurueck
    decrease_coins(coins : int)
        zieht Anzahl von Muenzen ab
    increase_cooldown_level()
        erhoeht cooldown_level um 1 und aktualisiert cooldown_ticks
    increase_max_health_level()
        erhoeht max_health_level um 1 und aktualisiert max_health
    increase_engine_level()
        erhoeht velocity_level um 1 und aktualisiert velocity
    save_to_json() -> dict
        speichert position, direction, coins, score, die verschiedenen levels, last_shot_ticks und die Rueckgabe der Laser save_to_json()-
        Methoden in Dictionary und gibt es zurueck
    load_from_json(laser_dic_list)
        fuegt der Laser-Gruppe die gespeichterten Lasers in der laser_dic_list hinzu
    update()
        fuehrt die verschiedenen check-Methoden aus und die update-Methode der Laser aus
    """
    def __init__(self, position: tuple, direction: tuple, coins = 0, score = 0, cooldown_level = 0, ready_to_shoot = True, max_health_level = 0, velocity_level = 0, health = settings["spaceship"]["max_health_levels"][0]):
        """
        Parameter
        ----------
        position : tuple
            Position
        direction : tuple
            Richtung
        coins : int, optional
            Muenzen (Standard ist 0)
        score : int, optional
            Score (Standard ist 0)
        cooldown_level : int, optional
            Stufe des Cooldowns (Standard ist 0)
        ready_to_shoot : bool, optional
            bereit zu schiessen (Standard ist True)
        max_health_level : int, optional
            Stufe der maximalen Leben (Standard ist 0)
        velocity_level : int, optional
            Stufe der Geschwindigkeit (Standard ist 0)
        health : int, optional
            aktuelle Leben (Standard sind die maximalen Leben der ersten Stufe)
        """
        super().__init__()
        self.width = settings["spaceship"]["width"]
        self.height = settings["spaceship"]["height"]
        self.velocity_level = velocity_level
        self.velocity_levels = settings["spaceship"]["engine_levels"]
        self.velocity = self.velocity_levels[self.velocity_level]
        self.direction = pygame.math.Vector2(direction)
        self.border = pygame.math.Vector2(tuple((settings["screen_width"], settings["screen_height"])))
        self.position = position

        self.lasers = pygame.sprite.Group()
        self.last_shot_ticks = 0
        self.cooldown_levels = settings["spaceship"]["cooldown_levels"]
        self.cooldown_level = cooldown_level
        self.cooldown_ticks = self.cooldown_levels[self.cooldown_level]
        self.ready_to_shoot = ready_to_shoot

        self.score = score
        self.max_health_levels = settings["spaceship"]["max_health_levels"]
        self.max_health_level = max_health_level
        self.max_health = self.max_health_levels[self.max_health_level]
        self.health = health
        self.damaged_image = pygame.image.load(IMAGE_PATH/"Main Ship - Base - Damaged.png").convert_alpha()
        self.damaged_image = pygame.transform.scale(self.damaged_image, (self.width, self.height))
        self.slight_damage_image = pygame.image.load(IMAGE_PATH/"Main Ship - Base - Slight damage.png").convert_alpha()
        self.slight_damage_image = pygame.transform.scale(self.slight_damage_image, (self.width, self.height))
        self.very_damaged_image = pygame.image.load(IMAGE_PATH/"Main Ship - Base - Very damaged.png").convert_alpha()
        self.very_damaged_image = pygame.transform.scale(self.very_damaged_image, (self.width, self.height))
        self.full_health_image = pygame.image.load(IMAGE_PATH/"Main Ship - Base - Full health.png").convert_alpha()
        self.full_health_image = pygame.transform.scale(self.full_health_image, (self.width, self.height))
        self.image = self.full_health_image
        self.old_image = self.image
        self.rect = self.image.get_rect(midbottom = self.position)
        self.mask = pygame.mask.from_surface(self.image)
        self.coins: int = coins
        self.cannon_vector = pygame.math.Vector2(tuple(settings["spaceship"]["cannon_position"]))
        self.cannon_position = pygame.math.Vector2(self.rect.midbottom) + pygame.math.Vector2(self.cannon_vector)
        self.cannon_vector = self.cannon_position - pygame.math.Vector2(self.rect.center)


    def check_controls(self):
        """ueberprueft die Mausposition und richtet das Raumschiff danach aus
        wenn Leertaste gedrueckt wird, wird geschossen, indem shoot() ausgefuehrt wird
        ready_to_shoot wird anschliessend auf false gesetzt
        wenn UP oder W gedrueckt wird, wird das rect um das Produkt aus velocity und direction bewegt
        
        Paramter
        ---------
        keine

        Rueckgabe
        ---------
        keine
        """
        mouse_position = pygame.math.Vector2(pygame.mouse.get_pos())
        self.align(mouse_position)
        keys = pygame.key.get_pressed()
        if (keys[pygame.K_w] or keys[pygame.K_UP]) and pygame.math.Vector2(self.direction).length() != 0:
            move = pygame.math.Vector2(self.direction) * self.velocity
            self.rect.move_ip(move)
        if keys[pygame.K_SPACE] and self.ready_to_shoot:
            self.shoot()
            self.last_shot_ticks = pygame.time.get_ticks()
            self.ready_to_shoot = False

    def check_cooldown(self):
        """ueberprueft, ob der cooldown abgelaufen ist, wenn ja wird ready_to_shoot auf True gesetzt
        
        Paramter
        ---------
        keine

        Rueckgabe
        ---------
        keine
        """
        if self.ready_to_shoot == False:
            current_ticks = pygame.time.get_ticks()
            if current_ticks - self.last_shot_ticks >= self.cooldown_ticks:
                self.ready_to_shoot = True

    def align(self, mouse_position):
        """aktualisiert direction gemaess der Maus-Position und richtet die Position der Kanone
        danach aus
        
        Paramter
        ---------
        keine

        Rueckgabe
        ---------
        keine
        """
        self.direction = mouse_position - pygame.math.Vector2(self.rect.center)
        if self.direction.length() != 0:
            self.direction.normalize_ip()
        else:
            self.direction = pygame.math.Vector2((-1, 0))
        self.cannon_position = pygame.math.Vector2(self.rect.center) + self.direction * self.cannon_vector.length()

    def rotate(self):
        """rotiert das Bild nach der direction
        
        Paramter
        ---------
        keine

        Rueckgabe
        ---------
        keine
        """
        angle = self.direction.angle_to((0, -1))
        rotated_image = pygame.transform.rotate(self.old_image, angle)
        rotated_rect = rotated_image.get_rect(center = self.rect.center)
        self.rect = rotated_rect
        self.image = rotated_image
        
    def shoot(self):
        """laesst das Raumschiff schiessen, indem der Lasergruppe ein Laser mit der Richtung und
        der Position der Kanone hinzugefuegt wird
        
        Paramter
        ---------
        keine

        Rueckgabe
        ---------
        keine
        """
        self.lasers.add(Laser(self.cannon_position, self.direction, settings["spaceship"]["laser_speed"]))

    def get_lasers(self):
        """gibt die Lasergruppe zurueck
        
        Paramter
        ---------
        keine

        Rueckgabe
        ---------
        keine
        """
        return self.lasers
    
    def check_border(self):
        """ueberprueft, ob das Raumschiff ausserhalb von Bildschirm, wenn ja wird die Position
        so gesetzt, dass der Spieler am Rand bleibt
        
        Paramter
        ---------
        keine

        Rueckgabe
        ---------
        keine
        """
        if self.rect.midtop[0] <= 0:
            self.rect.midtop = (0, self.rect.midtop[1])
        elif self.rect.midtop[0] >= self.border.x:
            self.rect.midtop = (self.border.x, self.rect.midtop[1])
        if self.rect.midtop[1] <= 0:
            self.rect.midtop = (self.rect.midtop[0], 0)
        elif self.rect.midtop[1] >= self.border.y:
            self.rect.midtop = (self.rect.midtop[0], self.border.y)

    def check_health(self):
        """ueberprueft den Anteil der aktuellen Leben an den maximalen Leben und aktualisiert dementsprechend
        das aktuelle Bild (image) und speichert eine Kopie in old_image
        
        Paramter
        ---------
        keine

        Rueckgabe
        ---------
        keine
        """
        if self.health <= 0.25 * self.max_health:
            self.image = self.very_damaged_image
        elif self.health <= 0.5 * self.max_health:
            self.image = self.damaged_image
        elif self.health <= 0.75 * self.max_health:
            self.image = self.slight_damage_image
        elif self.health <= self.max_health:
            self.image = self.full_health_image
        self.old_image = self.image
    
    def get_position(self):
        """gibt die Position der Raumschiff-Mitte zurueck
        
        Paramter
        ---------
        keine

        Rueckgabe
        ---------
        keine
        """
        return self.rect.center
    
    def hit(self, damage):
        """zieht dem Raumschiff die Anzahl an Leben ab
        
        Paramter
        ---------
        keine

        Rueckgabe
        ---------
        keine
        """
        self.health -= damage
    
    def set_position(self, position: tuple):
        """setzt die Position der Mitte des Raumschiffs
        
        Paramter
        ---------
        keine

        Rueckgabe
        ---------
        keine
        """
        self.rect.center = position
    
    def add_coins(self, coins: int):
        """fuegt den Muenzen des Spielers die Anzahl hinzu
        
        Paramter
        ---------
        keine

        Rueckgabe
        ---------
        keine
        """
        self.coins += coins
    
    def add_health(self, health: int):
        """fuegt Spieler Anzahl an Leben hinzu, wenn das Maximum noch nicht erreicht wurde
        
        Paramter
        ---------
        keine

        Rueckgabe
        ---------
        keine
        """
        if self.health + health >= self.max_health:
            self.health = self.max_health
        else:
            self.health += health
    
    def increase_score(self):
        """erhoeht den Score um 1
        
        Paramter
        ---------
        keine

        Rueckgabe
        ---------
        keine
        """
        self.score += 1
    
    def get_score(self):
        """gibt Score zurueck
        
        Paramter
        ---------
        keine

        Rueckgabe
        ---------
        keine
        """
        return self.score

    def get_health(self):
        """gibt Leben zurueck
        
        Paramter
        ---------
        keine

        Rueckgabe
        ---------
        keine
        """
        return self.health
    
    def get_max_health(self):
        """gibt maximale Leben zurueck
        
        Paramter
        ---------
        keine

        Rueckgabe
        ---------
        keine
        """
        return self.max_health

    def get_coins(self):
        """gibt Wert der Muenzen zurueck
        
        Paramter
        ---------
        keine

        Rueckgabe
        ---------
        keine
        """
        return self.coins

    def get_ready_to_shoot(self):
        """gibt ready_to_shoot zurueck
        
        Paramter
        ---------
        keine

        Rueckgabe
        ---------
        keine
        """
        return self.ready_to_shoot

    def decrease_coins(self, coins: int):
        """zieht Anzahl von Muenzen ab
        
        Paramter
        ---------
        keine

        Rueckgabe
        ---------
        keine
        """
        self.coins -= coins
          

    def increase_cooldown_level(self):
        """erhoeht cooldown_level um 1 und aktualisiert cooldown_ticks
        
        Paramter
        ---------
        keine

        Rueckgabe
        ---------
        keine
        """
        self.cooldown_level += 1
        self.cooldown_ticks = self.cooldown_levels[self.cooldown_level]
    
    def increase_engine_level(self):
        """erhoeht velocity_level um 1 und aktualisiert velocity
        
        Paramter
        ---------
        keine

        Rueckgabe
        ---------
        keine
        """
        self.velocity_level += 1
        self.velocity = self.velocity_levels[self.velocity_level]

    def increase_max_health_level(self):
        """erhoeht max_health_level um 1 und aktualisiert max_health
        
        Paramter
        ---------
        keine

        Rueckgabe
        ---------
        keine
        """
        self.max_health_level += 1
        self.max_health = self.max_health_levels[self.max_health_level]
    
    def save_to_json(self):
        """speichert position, direction, coins, score, die verschiedenen levels, last_shot_ticks und die Rueckgabe der Laser save_to_json()-
        Methoden in Dictionary und gibt es zurueck
        
        Paramter
        ---------
        keine

        Rueckgabe
        ---------
        keine
        """
        laser_dic_list = []
        for laser in self.lasers:
            laser_dic_list.append(laser.save_to_json())
        dic = {"position": self.rect.center, "direction": tuple(self.direction), "score": self.score, "coins": self.coins, "cooldown_level": self.cooldown_level, "max_health_level": self.max_health_level, "speed_level": self.velocity_level, "last_shot_ticks": self.last_shot_ticks, "lasers": laser_dic_list, "health": self.health}
        return dic

    def load_from_json(self, laser_dic_list):
        """fuegt der Laser-Gruppe die gespeichterten Lasers in der laser_dic_list hinzu
        
        Paramter
        ---------
        keine

        Rueckgabe
        ---------
        keine
        """
        for laser in laser_dic_list:
            self.lasers.add(Laser(tuple(laser["position"]), tuple(laser["direction"]), laser["velocity"]))

    
    def update(self):
        """fuehrt die verschiedenen check-Methoden aus und die update-Methode der Laser aus
        
        Paramter
        ---------
        keine

        Rueckgabe
        ---------
        keine
        """
        self.check_health()
        self.check_controls()
        self.rotate()
        self.check_border()
        self.check_cooldown()
        self.lasers.update()
        
        
