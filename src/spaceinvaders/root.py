
import logging

import pyxel

from spaceinvaders                import LOGGER_NAME
from spaceinvaders.menu_mode      import MenuMode
from spaceinvaders.meta_singleton import MetaSingleton

logger = logging.getLogger(LOGGER_NAME)


class Root(metaclass=MetaSingleton):

    def __init__(self):
        self.fps: int = 30
        self.mode = MenuMode()

        pyxel.init(160, 120, fps=self.fps)
        pyxel.load("graphics/space-invaders.pyxres")

    def run(self):
        pyxel.run(self.update, self.draw)

    def update(self):
        self.mode = self.mode.next_mode()

    def draw(self):
        self.mode.draw()
