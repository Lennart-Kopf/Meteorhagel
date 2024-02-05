"""
Ein Modul, das die verschiedenen Pfade fuer das Projekt unabhaengig vom Betriebssystem konfiguriert
...

Variablen
    RELATIVE_PATH : pathlib.Path
        Pfad des Projekt-Ordners
        falls die Datei in Form der exe-Datei ausgefuehrt wird, muss der Pfad neu ermittelt werden
    IMAGE_PATH : pathlib.Path
        Bilder-Pfad
    SETTINGS_PATH : pathlib.Path
        Pfad der settings Datei
    HIGHSCORE_PATH : pathlib.Path
        Pfad der highscore Datei
    SAVE_PATH : pathlib.Path
        Pfad der gespeicherten Spielstaende
    INSTRUCTIONS_PATH : pathlib.Path
        Pfad der Spielanleitung Datei
"""

import pathlib
import sys

if getattr(sys, 'frozen', False):
    RELATIVE_PATH = pathlib.Path(sys.executable).parent.resolve()
else:
    RELATIVE_PATH = pathlib.Path(__file__).parent.parent.resolve()
IMAGE_PATH = pathlib.Path(RELATIVE_PATH / "images")
SETTINGS_PATH = pathlib.Path(RELATIVE_PATH / "code/settings.json")
HIGHSCORE_PATH = pathlib.Path(RELATIVE_PATH / "highscore.json")
SAVE_PATH = pathlib.Path(RELATIVE_PATH / "saves")
INSTRUCTIONS_PATH = pathlib.Path(RELATIVE_PATH / "instructions.txt")