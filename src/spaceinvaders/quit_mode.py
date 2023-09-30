
import logging

import pyxel

from spaceinvaders import LOGGER_NAME

logger = logging.getLogger(LOGGER_NAME)


class QuitMode:

    def __init__(self):
        pass

    def init(self):
        pass

    def next_mode(self):
        return self

    def draw(self):
        pyxel.quit()
