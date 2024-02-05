import pygame
import json
from button import Button
from spaceship import Spaceship
from pathes import *
import pathlib
with open(SETTINGS_PATH) as fp:
    settings = json.load(fp)

class Upgrade():
    """
    Eine Klasse, die ein Upgrade-Fenster darstellt

    ...

    Attribute
    ---------
    font : pygame.Font
        Schriftart und Groesse der Ueberschrift
    icon_font : pygame.Font
        Schriftart und Groesse der einzelnen Ueberschriften fuer die Verbesserungen
    screen : pygame.Surface
        Bildschirm
    font_color : str
        die Farbe der Texte
    engine_image : pygame.Surface
        das Bild fuer die Geschwindigkeitsverbesserung
    cooldown_image : pygame.Surface
        das Bild fuer die Cooldownverbesserung
    max_health_image : pygame.Surface
        das Bild fuer die maximale Leben-Verbesserung
    engine_button : Button
        Button mit dem Preis fuer die Verbesserung, der gedrueckt wird, um die Geschwindigkeit zu verbessern
    cooldown_button : Button
        Button mit dem Preis fuer die Verbesserung, der gedrueckt wird, um den Cooldown zu verbessern
    max_health_button : Button
        Button mit dem Preis fuer die Verbesserung, der gedrueckt wird, um die maximalen Leben zu verbessern
    back_button : Button
        Button mit der Beschriftung "BACK", der gedrueckt wird, wenn man zurueck zum Spiel gelangen will
    spaceship : Spaceship
        Raumschiff des Spielers
    back : func
        Funktion, die ausgefuehrt werden soll, wenn der back_button gedrueckt wird, um zurueck zum Spiel zu gelangen
    
    Methoden
    ---------
    draw_background()
        malt den Bildschirm mit dem Hintergrund (schwarz) aus
    draw_icon_background(rect : pygame.Rect)
        malt den Hintergrund fuer die einzelnen Symbole der Verbesserungen
    show_upgrade_titles()
        zeigt die Titel der einzelnen Verbesserungen und das aktuelle Level und das Limit
    show_title()
        zeigt den Titel "UPGRADE" des Upgrade-Fensters
    engine_upgrade()
        malt das Symbol, den Button und den Titel des Geschwindigkeit-Upgrades und fuehrt bei
        Druecken des Buttons die increase_engine_level()-Methode des Raumschiffes aus,
        um das Level zu erhoehen
        ueberprueft auch, ob der Spieler in der Lage ist, das Upgrade zu kaufen
        und ob das Limit an Upgrades schon erreicht ist
    cooldown_upgrade()
        malt das Symbol, den Button und den Titel des Cooldown-Upgrades und fuehrt bei
        Druecken des Buttons die increase_cooldown_level()-Methode des Raumschiffes aus,
        um das Level zu erhoehen
        ueberprueft auch, ob der Spieler in der Lage ist, das Upgrade zu kaufen
        und ob das Limit an Upgrades schon erreicht ist
    max_health_upgrade()
        malt das Symbol, den Button und den Titel des Maximale-Leben-Upgrades und fuehrt bei
        Druecken des Buttons die increase_max_health_level()-Methode des Raumschiffes aus,
        um das Level zu erhoehen
        ueberprueft auch, ob der Spieler in der Lage ist, das Upgrade zu kaufen
        und ob das Limit an Upgrades schon erreicht ist
    show_coins()
        zeigt die Muenzen, die der Spieler hat
    show_back_button()
        malt den back_button und ueberprueft, ob er gedrueckt wird, sodass die Funktion
        back ausgefuehrt werden kann, um ins Spiel zurueckzukehren
    set_back(back : func)
        ersetzt back durch die uebergebene Funktion
    run()
        zeigt alle Komponenten des Upgrade-Fensters
    """
    def __init__(self, screen: pygame.Surface, spaceship: Spaceship):
        """
        Parameter
        ---------
        screen : pygame.Surface
            Bildschirm
        spaceship : Spaceship
            Raumschiff
        """
        self.font = pygame.font.SysFont("arial", settings["upgrade"]["font_size"])
        self.icon_font = pygame.font.SysFont("arial", settings["upgrade"]["icon_font_size"])
        self.screen = screen
        self.font_color = settings["upgrade"]["font_color"]
        self.engine_image = pygame.image.load(IMAGE_PATH/"flame.png").convert_alpha()
        self.engine_image = pygame.transform.scale(self.engine_image, tuple(settings["upgrade"]["icon_size"]))
        self.cooldown_image = pygame.image.load(IMAGE_PATH/"laser000.png").convert_alpha()
        self.cooldown_image = pygame.transform.scale(self.cooldown_image, tuple(settings["upgrade"]["icon_size"]))
        self.max_health_image = pygame.image.load(IMAGE_PATH/"heart.png").convert_alpha()
        self.max_health_image = pygame.transform.scale(self.max_health_image, tuple(settings["upgrade"]["icon_size"]))
        self.engine_button = Button((self.screen.get_width()/2,self.screen.get_height()/2 + settings["upgrade"]["icon_size"][0]), "")
        self.cooldown_button = Button((self.screen.get_width()/4, self.screen.get_height()/2 + settings["upgrade"]["icon_size"][0]), "")
        self.max_health_button = Button((self.screen.get_width()*0.75,self.screen.get_height()/2 + settings["upgrade"]["icon_size"][0]), "")
        self.back_button = Button((self.screen.get_width() * 0.25, 40), "BACK")
        self.spaceship = spaceship
        self.back = None
    
    def draw_background(self):
        """malt den Bildschirm mit dem Hintergrund (schwarz) aus

        Parameter
        ---------
        keine

        Rueckgabe
        --------
        keine
        """
        background_rect = pygame.Rect((0, 0), (self.screen.get_width(), self.screen.get_height()))
        pygame.draw.rect(self.screen, "black", background_rect)
    
    def draw_icon_background(self, rect: pygame.Rect):
        """malt den Hintergrund fuer die einzelnen Symbole der Verbesserungen

        Parameter
        ---------
        rect : pygame.Rect
            Koordinaten und Breite und Laenge fuer den Hintergrund des Verbesserungsymbols

        Rueckgabe
        --------
        keine
        """
        pygame.draw.rect(self.screen, settings["upgrade"]["icon_background_color"], rect)
    
    def show_upgrade_titles(self, position: tuple, title: str, level, limit):
        """zeigt die Titel der einzelnen Verbesserungen und das aktuelle Level und das Limit

        Parameter
        ---------
        position : tuple
            Position der Verbesserungtitel
        title : str
            Titel der Verbesserung
        level : int
            aktuelles Level der Verbesserung
        limit : int
            das maximale Level der Verbesserung

        Rueckgabe
        --------
        keine
        """
        text = "{} Lvl. {}/{}".format(title, level, limit)
        text_surface = self.icon_font.render(text, False, self.font_color)
        text_rect = text_surface.get_rect(midbottom = position)
        self.screen.blit(text_surface, text_rect)

    def show_title(self):
        """zeigt den Titel "UPGRADE" des Upgrade-Fensters

        Parameter
        ---------
        keine

        Rueckgabe
        --------
        keine
        """
        text = "UPGRADE"
        text_surface = self.font.render(text, False, self.font_color)
        text_rect = text_surface.get_rect(center = (self.screen.get_width() / 2, 40))
        self.screen.blit(text_surface, text_rect)
    
    def engine_upgrade(self):
        """malt das Symbol, den Button und den Titel des Geschwindigkeit-Upgrades und fuehrt bei
        Druecken des Buttons die increase_engine_level()-Methode des Raumschiffes aus,
        um das Level zu erhoehen
        ueberprueft auch, ob der Spieler in der Lage ist, das Upgrade zu kaufen
        und ob das Limit an Upgrades schon erreicht ist

        Parameter
        ---------
        keine

        Rueckgabe
        --------
        keine
        """
        position = (self.screen.get_width()*0.5, self.screen.get_height()/2)
        rect = self.engine_image.get_rect(center=position)
        engine_level = self.spaceship.velocity_level
        engine_limit = len(self.spaceship.velocity_levels)
        price = settings["upgrade"]["level_prices"][engine_level]
        self.draw_icon_background(rect)
        self.show_upgrade_titles(rect.midtop, "SPEED", engine_level + 1, engine_limit)
        self.screen.blit(self.engine_image, rect)
        if self.spaceship.velocity_level >= engine_limit - 1:
            self.engine_button.set_text("MAX")
            self.engine_button.disable()
        else:
            self.engine_button.set_text("{} COINS".format(price))
            if price > self.spaceship.get_coins():
                self.engine_button.disable()
            else:
                self.engine_button.activate()
            if self.engine_button.get_just_pressed():
                self.spaceship.increase_engine_level()
                self.spaceship.decrease_coins(price)
        self.engine_button.draw(self.screen)


    def cooldown_upgrade(self):
        """malt das Symbol, den Button und den Titel des Cooldown-Upgrades und fuehrt bei
        Druecken des Buttons die increase_cooldown_level()-Methode des Raumschiffes aus,
        um das Level zu erhoehen
        ueberprueft auch, ob der Spieler in der Lage ist, das Upgrade zu kaufen
        und ob das Limit an Upgrades schon erreicht ist

        Parameter
        ---------
        keine

        Rueckgabe
        --------
        keine
        """
        position = (self.screen.get_width()*0.25, self.screen.get_height()/2)
        rect = self.cooldown_image.get_rect(center=position)
        cooldown_level = self.spaceship.cooldown_level
        cooldown_limit = len(self.spaceship.cooldown_levels)
        price = settings["upgrade"]["level_prices"][cooldown_level]
        self.draw_icon_background(rect)
        self.show_upgrade_titles(rect.midtop, "FIRE RATE", cooldown_level + 1, cooldown_limit)
        self.screen.blit(self.cooldown_image, rect)
        if self.spaceship.cooldown_level >= cooldown_limit - 1:
            self.cooldown_button.set_text("MAX")
            self.cooldown_button.disable()
        else:
            self.cooldown_button.set_text("{} COINS".format(price))
            if price > self.spaceship.get_coins():
                self.cooldown_button.disable()
            else:
                self.cooldown_button.activate()
            if self.cooldown_button.get_just_pressed():
                self.spaceship.increase_cooldown_level()
                self.spaceship.decrease_coins(price)
        self.cooldown_button.draw(self.screen)


    def max_health_upgrade(self):
        """malt das Symbol, den Button und den Titel des Maximale-Leben-Upgrades und fuehrt bei
        Druecken des Buttons die increase_max_health_level()-Methode des Raumschiffes aus,
        um das Level zu erhoehen
        ueberprueft auch, ob der Spieler in der Lage ist, das Upgrade zu kaufen
        und ob das Limit an Upgrades schon erreicht ist

        Parameter
        ---------
        keine

        Rueckgabe
        --------
        keine
        """
        position = (self.screen.get_width()*0.75, self.screen.get_height()/2)
        rect = self.max_health_image.get_rect(center=position)
        max_health_level = self.spaceship.max_health_level
        max_health_limit = len(self.spaceship.max_health_levels)
        price = settings["upgrade"]["level_prices"][max_health_level]
        self.draw_icon_background(rect)
        self.show_upgrade_titles(rect.midtop, "MAX. HEALTH", max_health_level + 1, max_health_limit)
        self.screen.blit(self.max_health_image, rect)
        if self.spaceship.max_health_level >= max_health_limit - 1:
            self.max_health_button.set_text("MAX")
            self.max_health_button.disable()
        else:
            self.max_health_button.set_text("{} COINS".format(price))
            if price > self.spaceship.get_coins():
                self.max_health_button.disable()
            else:
                self.max_health_button.activate()
            if self.max_health_button.get_just_pressed():
                self.spaceship.increase_max_health_level()
                self.spaceship.decrease_coins(price)
        self.max_health_button.draw(self.screen)


    
    def show_coins(self):
        """zeigt die Muenzen, die der Spieler hat

        Parameter
        ---------
        keine

        Rueckgabe
        --------
        keine
        """
        text = "YOU HAVE: {}x".format(self.spaceship.get_coins())
        text_surface = self.icon_font.render(text, False, "white")
        text_rect = text_surface.get_rect(center = (self.screen.get_width() * 0.8, 40))
        self.screen.blit(text_surface, text_rect)
        coin_image = pygame.image.load(IMAGE_PATH/"gold_coin000.png").convert_alpha()
        coin_rect = coin_image.get_rect(midleft = text_rect.midright)
        self.screen.blit(coin_image, coin_rect)
    
    def show_back_button(self):
        """malt den back_button und ueberprueft, ob er gedrueckt wird, sodass die Funktion
        back ausgefuehrt werden kann, um ins Spiel zurueckzukehren

        Parameter
        ---------
        keine

        Rueckgabe
        --------
        keine
        """
        self.back_button.draw(self.screen)
        if self.back_button.get_just_pressed():
            self.back()

    def set_back(self, back):
        """ersetzt back durch die uebergebene Funktion

        Parameter
        ---------
        keine

        Rueckgabe
        --------
        keine
        """
        self.back = back
    
    def run(self):
        """zeigt alle Komponenten des Upgrade-Fensters

        Parameter
        ---------
        keine

        Rueckgabe
        --------
        keine
        """
        self.draw_background()
        self.show_coins()
        self.show_title()
        self.engine_upgrade()
        self.cooldown_upgrade()
        self.max_health_upgrade()
        self.show_back_button()
        
