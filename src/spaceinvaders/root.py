
import logging

import pyxel

from spaceinvaders import LOGGER_NAME
from spaceinvaders.invader import Invader
from spaceinvaders.life_bar import LifeBar
from spaceinvaders.meta_singleton import MetaSingleton
from spaceinvaders.rocket import Rocket
from spaceinvaders.sprite_manager import SpriteManager
from spaceinvaders.star import Star

logger = logging.getLogger(LOGGER_NAME)


class Root(metaclass=MetaSingleton):

    def __init__(self):
        self.fps: int = 30
        self.paused: bool = False

    def init(self):
        pyxel.init(160, 120, fps=self.fps)
        pyxel.load("graphics/space-invaders.pyxres")

        manager = SpriteManager()
        manager.spawn(Invader, 60)
        manager.spawn(Star, 1)
        manager.attach(Rocket())
        manager.attach(LifeBar())

    def run(self):
        pyxel.run(self.update, self.draw)

    def is_game_over(self):
        return LifeBar().is_dead()

    def update(self):

        # Quit the game.
        if pyxel.btnp(pyxel.KEY_Q):
            pyxel.quit()

        # Toggle debug mode.
        if pyxel.btnp(pyxel.KEY_F1):
            if logger.isEnabledFor(logging.DEBUG):
                logger.setLevel(logging.INFO)
                logger.info("Debug Mode: disabled.")
            else:
                logger.setLevel(logging.DEBUG)
                logger.info("Debug Mode: enabled.")

        # Toggle pause mode.
        if pyxel.btnp(pyxel.KEY_F2):
            self.paused = not self.paused

        if self.paused:
            return

        SpriteManager().update()

    def draw_game_over(self):
        if self.is_game_over():
            pyxel.text(pyxel.width / 2 - 15, pyxel.height / 2, "GAME OVER", 7)

    def draw_paused(self):
        if self.paused:
            f = pyxel.frame_count % self.fps
            if (f // 8) % 2 == 0:
                pyxel.text(1, pyxel.height - 7, "HIT F2 TO RESUME", 7)

    def draw(self):
        pyxel.cls(0)
        SpriteManager().draw()
        self.draw_game_over()
        self.draw_paused()
