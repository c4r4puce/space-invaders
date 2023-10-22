
import logging

import pyxel

from spaceinvaders                import LOGGER_NAME
from spaceinvaders.invader        import Invader
from spaceinvaders.life_bar       import LifeBar
from spaceinvaders.rocket         import Rocket
from spaceinvaders.sprite_manager import SpriteManager
from spaceinvaders.star           import Star

logger = logging.getLogger(LOGGER_NAME)


class GameMode:

    def __init__(self):
        self.paused: bool = False

        manager = SpriteManager().reset()
        manager.spawn(Invader, 60)
        manager.spawn(Star,    0.5)
        manager.attach(Rocket())
        manager.attach(LifeBar())

        LifeBar().reset()

    def is_game_over(self):
        return LifeBar().is_dead()

    def next_mode(self):

        # Quit the game.
        if pyxel.btnp(pyxel.KEY_Q):
            from spaceinvaders.menu_mode import MenuMode
            return MenuMode()

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

        if not self.paused:
            SpriteManager().update()
        return self

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
