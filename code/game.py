import pygame
import sys
import math
from spaceship import Spaceship
from asteroid import Asteroid
from laser import Laser
from asteroid_explosion import AsteroidExplosion
from ui import UI
import random
from item import Item
from coin import Coin, RedCoin, SilverCoin, GoldCoin
from heart import Heart
from game_over import GameOver
from pause_menu import PauseMenu
from upgrade import Upgrade
from title import Title
import json
from tkinter import filedialog
import datetime
from pathes import *
import pathlib

with open(SETTINGS_PATH) as fp:
    settings = json.load(fp)



random.seed()

class Game():
    """
    Eine Klasse, die das gesamte Spiel "Meteorhagel" darstellt
    ...

    Attribute
    ---------
    screen_width : int
        die Bildschirmbreite aus den settings
    screen_height : int
        die Bildschirmhoehe aus den settings
    screen : pygame.Surface
        der Bildschirm
    background : pygame.Surface
        das Hintergrundbild des Spiels
    clock : pygame.time.Clock
        stellt die Zeit des Spiels ein, wie viele ticks waehrend des Spiels vergehen etc.
    game_states : dict
        speichert welche Spielzustand gerade aktiv ist in Form eines Dictionary aus bools
    game_over_screen : GameOver
        der game_over_screen
    pause_menu : PauseMenu
        ein Pausenmenü
    spaceship : pygame.sprite.GroupSingle[Spaceship]
        eine Gruppe, die nur ein Spaceship enthaelt (das des Spielers)
    asteroids : pygame.sprite.Group[Asteroid]
        eine Gruppe, die die Asteroiden enthaelt
    asteroid_explosions : pygane.sprite.Group[AsteroidExplosion]
        eine Gruppe, die die Explosionen der Asteroiden speichert
    items : pygame.sprite.Group[Item]
        eine Gruppe, die die Items speichert
    ui : UI
        Benutzeroberflaeche
    current_frame : int
        der aktuelle Frame
    upgrade_menu : Upgrade
        das Upgrade-Menue
    difficulty_level : int
        der aktuelle Schwierigkeitsgrad
    asteroid_spawn_time : int
        nach wie vielen Frames ein neuer Asteroid erscheint
        in Abhaengigkeit von difficulty_level
        und den in settings definierten levels
    asteroid_speed : float
        die Geschwindigkeit der neuen Asteroiden
        in Abhaengigkeit von difficulty_level
        und den in settings definierten levels
    asteroid_size : tuple
        die Groesse neuer Asteroiden
        in Abhaengigkeit von difficulty_level
        und den in settings definierten levels
    start_menu : StartMenu
        der Titelbildschirm
    
    Methoden
    --------
    main()
        die Hauptschleife des Spiels, die abgebrochen wird, wenn der Benutzer das Fenster schliesst
        solange sie aktiv ist, wird run ausgefuehrt und der Bildschirm aktualisiert
        die FPS werden auf 60 gesetzt
    spawn_asteroid()
        laesst einen Asteroiden aus einem der vier Bildschirmraender erscheinen und
        laesst sie ungefaehr auf das Spaceship fliegen
        wenn die spawn_time erreicht wurde
    check_collision()
        ueberprueft die verschiedenen Kollisionen
        wenn ein Laser auf einen Asteroiden trifft, wird eine Explosion und ein Item erzeugt, Asteroid und Laser werden geloescht
        wenn das Spaceship einen Asteroiden trifft, werden ebenfalls Explosionen erzeugt und die Methode spaceship_hit() ausgefuehrt
        wenn das Spaceship mit einem Item kollidiert, wird das Item aktiviert und geloescht
    check_paused()
        ueberprueft, ob der Spieler ESC drueckt, um zu pausieren, wenn ja wird der Spielzustand auf paused gesetzt und alle anderen
        auf False
    check_upgrade()
        ueberprueft, ob der Spieler mit U das Upgrade-Menue oeffnen will, wenn ja wird der Zustand upgrade auf true und der Rest
        auf False gesetzt
    resume()
        ueberfuehrt in den running-Zustand
    spaceship_hit()
        wird ausgefuehrt, wenn das Spaceship getroffen wird und loescht daraufhin alle Asteroiden und setzt den Spieler in 
        die Mitte des Bildschirms zurueck und zieht ihm Leben ab
    spawn_item()
        laesst ein Item erscheinen, das durch eine gewichtete Liste aus den Wahrscheinlichkeiten der settings bestimmt wird
        oder keines
    check_death()
        ueberprueft, ob der Spieler tot ist und ueberfuehrt daraufhin hin den Game Over Zustand
    calculate_difficulty()
        berechnet difficulty_level aus dem Score und dem score_per_difficulty aus den settings und aktualisiert dann die 
        asteroid_size _spawn_time und _speed
    save_to_json()
        speichert alle Rueckgaben der save_to_json Methoden seiner eigenen Gruppen in einem Dictionary,
        welches in ein JSON-Objekt umgewandelt und in einer JSON-Datei der Wahl gespeichert wird
    load_from_json()
        laedt eine JSON-Datei, indem mit ihrer Informationen in Form eines Dictionariers die Gruppen
        und Objekte neu initialisiert werden
    run()
        ueberprueft, welcher state gerade aktiv ist und fuehrt die dementsprechenden Methoden der Klassen aus
        den verschiedenen Menues werden die Funktionen, die sie benoetigen, z.B. save_to_json uebergeben
    reset()
        setzt das Spiel so zurueck, als waere gerade neu begonnen worden

    """
    def __init__(self):
        """
        Attribute
        ---------
        keine
        """
        pygame.init()
        self.screen_width = settings["screen_width"]
        self.screen_height = settings["screen_height"]
        self.screen = pygame.display.set_mode((self.screen_width,self.screen_height))
        pygame.display.set_caption("Meteorhagel")
        self.background = pygame.image.load(IMAGE_PATH/"space.jpg")
        self.background = pygame.transform.scale(self.background, (self.screen_width, self.screen_height))
        self.clock = pygame.time.Clock()
        pygame.display.set_icon(pygame.image.load(IMAGE_PATH/"Main Ship - Base - Full health.png"))


        

        self.game_states = {"game_over": False, "paused": False, "running": False, "upgrade": False, "start": True}
        self.game_over_screen = GameOver(self.screen)
        self.pause_menu = PauseMenu(self.screen)
        spaceship = Spaceship((self.screen_width / 2, self.screen_height), (0, -1))
        self.spaceship: pygame.sprite.GroupSingle[Spaceship] = pygame.sprite.GroupSingle(spaceship)
        self.asteroids = pygame.sprite.Group()
        self.asteroid_explosions = pygame.sprite.Group()
        self.items = pygame.sprite.Group()
        self.ui = UI(self.screen)
        self.current_frame = 0
        self.upgrade_menu = Upgrade(self.screen, self.spaceship.sprite)

        self.difficulty_level = 0
        self.asteroid_spawn_time = settings["asteroid_spawn_time_levels"][self.difficulty_level]

        self.asteroid_speed = settings["asteroid_speed_levels"][self.difficulty_level]

        self.asteroid_size = tuple(settings["asteroid_size_levels"][self.difficulty_level])

        self.start_menu = Title(self.screen)

    def main(self):
        """die Hauptschleife des Spiels, die abgebrochen wird, wenn der Benutzer das Fenster schliesst
        solange sie aktiv ist, wird run ausgefuehrt und der Bildschirm aktualisiert
        die FPS werden auf 60 gesetzt
        
        Parameter
        ---------
        keine

        Rueckgabe
        ----------
        keine
        """
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
            self.run()
            pygame.display.flip()
            self.clock.tick(60)


    def spawn_asteroid(self):
        """laesst einen Asteroiden aus einem der vier Bildschirmraender erscheinen und
        laesst sie ungefaehr auf das Spaceship fliegen
        wenn die spawn_time erreicht wurde

        Parameter
        ---------
        keine

        Rueckgabe
        ----------
        keine
        """
        if self.current_frame == self.asteroid_spawn_time:
            border = random.randint(1, 4)
            if border == 1:
                x = random.randint(0, self.screen_width)
                y = 0
            elif border == 2:
                x = self.screen_width
                y = random.randint(0, self.screen_height)
            elif border == 3:
                x = random.randint(0, self.screen_width)
                y = self.screen_height
            else:
                x = 0
                y = random.randint(0, self.screen_height)

            direction = pygame.math.Vector2(self.spaceship.sprite.get_position() - pygame.math.Vector2(x, y))
            if direction.length != 0:
                direction.normalize_ip()
            self.asteroids.add(Asteroid((x, y), self.asteroid_speed, direction, self.asteroid_size))
            self.current_frame = 0

    def check_collision(self):
        """
        ueberprueft die verschiedenen Kollisionen
        wenn ein Laser auf einen Asteroiden trifft, wird eine Explosion und ein Item erzeugt, Asteroid und Laser werden geloescht
        wenn das Spaceship einen Asteroiden trifft, werden ebenfalls Explosionen erzeugt und die Methode spaceship_hit() ausgefuehrt
        wenn das Spaceship mit einem Item kollidiert, wird das Item aktiviert und geloescht

        Parameter
        ---------
        keine

        Rueckgabe
        ----------
        keine
        """
        if self.spaceship.sprite.lasers:
            for laser in self.spaceship.sprite.lasers:
                hit_asteroids = pygame.sprite.spritecollide(laser, self.asteroids, False, pygame.sprite.collide_mask)
                if hit_asteroids:
                    for asteroid in hit_asteroids:
                        self.asteroid_explosions.add(AsteroidExplosion(asteroid.get_position()))
                        self.spawn_item(asteroid.get_position())
                        asteroid.kill()
                        laser.kill()
                        self.spaceship.sprite.increase_score()
        if self.spaceship:
            hit_asteroids = pygame.sprite.spritecollide(self.spaceship.sprite, self.asteroids, False, pygame.sprite.collide_mask)
            if hit_asteroids:
                for asteroid in hit_asteroids:
                    self.asteroid_explosions.add(AsteroidExplosion(asteroid.get_position()))
                self.spaceship_hit()
            collected_items = pygame.sprite.spritecollide(self.spaceship.sprite, self.items, False, pygame.sprite.collide_mask)
            if collected_items:
                for item in collected_items:
                    item.activate(self.spaceship.sprite)
    
    def check_paused(self):
        """
        ueberprueft, ob der Spieler ESC drueckt, um zu pausieren, wenn ja wird der Spielzustand auf paused gesetzt und alle anderen
        auf False

        Parameter
        ---------
        keine

        Rueckgabe
        ----------
        keine
        """
        keys = pygame.key.get_pressed()
        if keys[pygame.K_ESCAPE]:
            self.game_states={"game_over": False, "paused": True, "running": False, "upgrade": False, "start": False}
    
    def check_upgrade(self):
        """
        ueberprueft, ob der Spieler mit U das Upgrade-Menue oeffnen will, wenn ja wird der Zustand upgrade auf true und der Rest
        auf False gesetzt

        Parameter
        ---------
        keine

        Rueckgabe
        ----------
        keine
        """
        keys = pygame.key.get_pressed()
        if keys[pygame.K_u]:
            self.game_states={"game_over": False, "paused": False, "running": False, "upgrade": True, "start": False}

    def resume(self):
        """
        ueberfuehrt in den running-Zustand

        Parameter
        ---------
        keine

        Rueckgabe
        ----------
        keine
        """
        self.game_states = {"game_over": False, "paused": False, "running": True, "upgrade": False, "start": False}
            
    def spaceship_hit(self):
        """
        wird ausgefuehrt, wenn das Spaceship getroffen wird und loescht daraufhin alle Asteroiden und setzt den Spieler in 
        die Mitte des Bildschirms zurueck und zieht ihm Leben ab

        Parameter
        ---------
        keine

        Rueckgabe
        ----------
        keine
        """
        self.spaceship.sprite.set_position((self.screen_height/2, self.screen_width/2))
        self.spaceship.sprite.hit(10)
        self.asteroids.empty()
    
    def spawn_item(self, position):
        """
        laesst ein Item erscheinen, das durch eine gewichtete Liste aus den Wahrscheinlichkeiten der settings bestimmt wird
        oder keines

        Parameter
        ---------
        keine

        Rueckgabe
        ----------
        keine
        """
        random.seed()
        chance_heart = settings["items"]["chances"]["life_chance"]
        chance_red_coin = settings["items"]["chances"]["red_coin_chance"]
        chance_silver_coin = settings["items"]["chances"]["silver_coin_chance"]
        chance_gold_coin = settings["items"]["chances"]["gold_coin_chance"]
        item = random.choices(["GC", "SC", "RC", "H", None], [chance_gold_coin, chance_silver_coin, chance_red_coin, chance_heart, (1 - chance_gold_coin - chance_heart - chance_silver_coin - chance_red_coin)])[0]
        dic = {"GC": GoldCoin(position), "SC": SilverCoin(position), "RC": RedCoin(position), "H": Heart(position)}
        if item:
           self.items.add(dic[item])
        
    
    def check_death(self):
        """
        ueberprueft, ob der Spieler tot ist und ueberfuehrt daraufhin hin den Game Over Zustand

        Parameter
        ---------
        keine

        Rueckgabe
        ----------
        keine
        """
        if self.spaceship.sprite.get_health() <= 0:
            self.game_states = {"game_over": True, "paused": False, "running": False, "upgrade": False, "start": False}
    
    def calculate_difficulty(self):
        """
        berechnet difficulty_level aus dem Score und dem score_per_difficulty aus den settings und aktualisiert dann die 
        asteroid_size _spawn_time und _speed

        Parameter
        ---------
        keine

        Rueckgabe
        ----------
        keine
        """
        if self.spaceship.sprite.get_score() // settings["score_per_difficulty_level"] != self.difficulty_level:
            self.difficulty_level = self.spaceship.sprite.get_score() // settings["score_per_difficulty_level"]
            if self.difficulty_level < len(settings["asteroid_spawn_time_levels"]):
                self.asteroid_spawn_time = settings["asteroid_spawn_time_levels"][self.difficulty_level]
            else:
                self.asteroid_spawn_time = settings["asteroid_spawn_time_levels"][-1]
            if self.difficulty_level < len(settings["asteroid_speed_levels"]):
                self.asteroid_speed = settings["asteroid_speed_levels"][self.difficulty_level]
            else:
                self.asteroid_speed = settings["asteroid_speed_levels"][-1]
            if self.difficulty_level < len(settings["asteroid_size_levels"]):
                self.asteroid_size = settings["asteroid_size_levels"][self.difficulty_level]
            else:
                self.asteroid_size= settings["asteroid_size_levels"][-1]
            self.current_frame = 0
    
    def save_to_json(self):
        """speichert alle Rueckgaben der save_to_json Methoden seiner eigenen Gruppen in einem Dictionary,
        welches in ein JSON-Objekt umgewandelt und in einer JSON-Datei der Wahl gespeichert wird

        Parameter
        ---------
        keine

        Rueckgabe
        ----------
        keine
        """
        asteroid_dic_list = []
        for asteroid in self.asteroids:
            asteroid_dic_list.append(asteroid.save_to_json())
        explosion_dic_list = []
        for explosion in self.asteroid_explosions:
            explosion_dic_list.append(explosion.save_to_json())
        items_dic_list = []
        for item in self.items:
            items_dic_list.append(item.save_to_json())
        dic = {"current_frame": self.current_frame, "asteroids": asteroid_dic_list, "spaceship": self.spaceship.sprite.save_to_json(), "asteroid_explosions": explosion_dic_list, "items": items_dic_list}
        time = datetime.datetime.now()
        time = time.strftime("%Y_%m_%d_%H_%M_%S")
        save_file = filedialog.asksaveasfile("w", defaultextension="*.json", filetypes=[("JSON Files", "*.json")], initialdir=SAVE_PATH, initialfile="save_{}".format(time))
        if save_file:
            json.dump(dic, save_file, indent="\t")

    def load_from_json(self):
        """laedt eine JSON-Datei, indem mit ihrer Informationen in Form eines Dictionariers die Gruppen
        und Objekte neu initialisiert werden

        Parameter
        ---------
        keine

        Rueckgabe
        ----------
        keine
        """
        load_file = filedialog.askopenfile("r", defaultextension="*.json", filetypes=[("JSON File", "*.json")], initialdir=SAVE_PATH)
        if load_file:
            dic = json.load(load_file)
            self.current_frame = dic["current_frame"]
            self.asteroids.empty()
            self.spaceship.empty()
            self.asteroid_explosions.empty()
            self.items.empty()
            spaceship_dic = dic["spaceship"]
            self.spaceship = pygame.sprite.GroupSingle(Spaceship(tuple(spaceship_dic["position"]), tuple(spaceship_dic["direction"]), spaceship_dic["coins"], spaceship_dic["score"], spaceship_dic["cooldown_level"], False, spaceship_dic["max_health_level"], spaceship_dic["speed_level"], health=spaceship_dic["health"]))
            laser_dic_list = spaceship_dic["lasers"]
            self.spaceship.sprite.load_from_json(laser_dic_list)
            asteroids_list = dic["asteroids"]
            for asteroid in asteroids_list:
                self.asteroids.add(Asteroid(tuple(asteroid["position"]), asteroid["velocity"], tuple(asteroid["direction"]), tuple(asteroid["size"])))
            asteroid_explosions_list = dic["asteroid_explosions"]
            for explosion in asteroid_explosions_list:
                self.asteroid_explosions.add(AsteroidExplosion(tuple(explosion["position"]), explosion["current_frame"]))
            items_list = dic["items"]
            for item in items_list:
                if item["type"] == "heart":
                    self.items.add(Heart(item["position"], item["current_frame"]))
                elif item["type"] == "red_coin":
                    self.items.add(RedCoin(item["position"], item["current_frame"]))
                elif item["type"] == "silver_coin":
                    self.items.add(SilverCoin(item["position"], item["current_frame"]))
                elif item["type"] == "gold_coin":
                    self.items.add(GoldCoin(item["position"], item["current_frame"]))
            self.ui = UI(self.screen)
            self.upgrade_menu = Upgrade(self.screen, self.spaceship.sprite)
            self.game_over_screen = GameOver(self.screen)
            self.calculate_difficulty()
            self.game_states = {"game_over": False, "paused": False, "running": True, "upgrade": False, "start": False}
            


    def run(self):
        """ueberprueft, welcher state gerade aktiv ist und fuehrt die dementsprechenden Methoden der Klassen aus
        den verschiedenen Menues werden die Funktionen, die sie benoetigen, z.B. save_to_json uebergeben

        Parameter
        ---------
        keine

        Rueckgabe
        ----------
        keine
        """
        if self.game_states["running"]:
            self.screen.blit(self.background, (0,0))
            self.spaceship.update()
            self.spaceship.draw(self.screen)
            self.asteroids.update()
            self.asteroids.draw(self.screen)
            self.spaceship.sprite.get_lasers().draw(self.screen)
            self.asteroid_explosions.update()
            self.asteroid_explosions.draw(self.screen)
            self.items.update()
            self.items.draw(self.screen)
            self.check_collision()
            self.ui.display(self.spaceship.sprite)
            self.spawn_asteroid()
            self.current_frame += 1
            self.check_death()
            self.check_paused()
            self.check_upgrade()
            self.calculate_difficulty()

        elif self.game_states["game_over"]:
            if self.spaceship:
                score = self.spaceship.sprite.get_score()
                self.game_over_screen.set_score(score)
                self.asteroids.empty()
                self.spaceship.empty()
                self.asteroid_explosions.empty()
                self.items.empty()
                self.game_over_screen.set_function(self.reset)
            self.game_over_screen.run()
        
        elif self.game_states["paused"]:
            self.pause_menu.set_resume(self.resume)
            self.pause_menu.set_save(self.save_to_json)
            self.pause_menu.set_load(self.load_from_json)
            self.pause_menu.run()
        
        elif self.game_states["upgrade"]:
            self.upgrade_menu.set_back(self.resume)
            self.upgrade_menu.run()
        
        elif self.game_states["start"]:
            self.start_menu.set_start_fun(self.resume)
            self.start_menu.set_load_fun(self.load_from_json)
            self.start_menu.run()
            
    
    def reset(self):
        """setzt das Spiel so zurueck, als waere gerade neu begonnen worden

        Parameter
        ---------
        keine

        Rueckgabe
        ----------
        keine
        """
        self.game_states = {"game_over": False, "paused": False, "running": True, "upgrade": False}
        self.game_over_screen = GameOver(self.screen)
        spaceship = Spaceship((self.screen_width / 2, self.screen_height), (0, -1))
        self.spaceship: pygame.sprite.GroupSingle[Spaceship] = pygame.sprite.GroupSingle(spaceship)
        self.asteroids = pygame.sprite.Group()
        self.asteroid_explosions = pygame.sprite.Group()
        self.items = pygame.sprite.Group()
        self.ui = UI(self.screen)
        self.upgrade_menu = Upgrade(self.screen, self.spaceship.sprite)
        self.calculate_difficulty()
        self.current_frame = 0 

g = Game()
g.main()


	





    