
import logging

import pyxel

from spaceinvaders                import LOGGER_NAME
from spaceinvaders.game_mode      import GameMode
from spaceinvaders.quit_mode      import QuitMode

logger = logging.getLogger(LOGGER_NAME)


class MenuMode:

    def __init__(self):
        self.menu_entry      = 0
        self.last_menu_entry = 1

    def next_mode(self):
        if pyxel.btnp(pyxel.KEY_UP):
            self.menu_entry -= 1
            if self.menu_entry < 0:
                self.menu_entry = 0
        elif pyxel.btnp(pyxel.KEY_DOWN):
            self.menu_entry += 1
            if self.menu_entry > self.last_menu_entry:
                self.menu_entry = self.last_menu_entry
        elif pyxel.btnp(pyxel.KEY_RETURN):
            if self.menu_entry == 0:
                return GameMode()
            elif self.menu_entry == 1:
                return QuitMode()
        return self

    def draw(self):
        pyxel.blt(0, 0,                     # (x, y) destination
                  2,                        # numero image source
                  0, self.menu_entry * 120, # (x, y) source
                  160, 120,                 # (largeur, hauteur) source et destination
                  0)                        # couleur transparente
