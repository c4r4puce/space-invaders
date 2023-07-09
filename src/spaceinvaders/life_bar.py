
import pyxel

from spaceinvaders.animation import Animation
from spaceinvaders.meta_singleton import MetaSingleton
from spaceinvaders.sprite import Sprite


class LifeBar(Sprite, metaclass=MetaSingleton):
    """Draw rocket's remaining hit points."""

    def __init__(self):
        animation = Animation(1,           # img
                              40, 16,      # width, height
                              0, 0,        # origx, origy
                              1)           # count
        pos = (2 + animation.width / 2, 2 + animation.height / 2)
        super().__init__(3,               # depth
                          pos,
                          0,               # speed
                          animation)
        self.hit_points = 18

    def draw(self):
        Sprite.draw(self)

        (x, y) = self.tlc()
        (x, y) = (x + 2, y + 2)
        w = self.hit_points
        h = 4
        pyxel.rect(x,     y,     w,     h,     2)
        pyxel.rect(x + 1, y + 1, w - 2, h - 2, 8)
        pyxel.rect(x + 3, y + 1, 3,     1,     7)
        pyxel.rect(x + 7, y + 1, 1,     1,     7)

    def dec(self):
        self.hit_points = max(0, self.hit_points - 2)

    def inc(self):
        self.hit_points = min(18, self.hit_points + 2)

    def die_immediatly(self):
        self.hit_points = 0

    def is_dead(self):
        return self.hit_points == 0
