
from random import randrange

import pyxel

from spaceinvaders.animation         import Animation, TOP_TO_BOTTOM
from spaceinvaders.invader_explosion import InvaderExplosion
from spaceinvaders.invader_weapon    import InvaderWeapon
from spaceinvaders.path              import Path
from spaceinvaders.rocket            import Rocket
from spaceinvaders.sprite            import Sprite
from spaceinvaders.sprite_manager    import SpriteManager
from spaceinvaders.vector            import Vector
from spaceinvaders.vertical_speed    import VerticalSpeed
from spaceinvaders.horizontal_speed  import HorizontalSpeed


class Invader(Sprite):
    """An invader is a sprite that can collide with the rocket."""

    def __init__(self):
        animation = Animation(0,                          # img
                              16, 16,                     # width, height
                              randrange(0, 3)*16, 128,    # origx, origy
                              8,                          # count
                              direction=TOP_TO_BOTTOM,
                              fps=6)
        hw = int(animation.width / 2)

        v = VerticalSpeed(1.0)
        r = HorizontalSpeed(1.0)
        l = HorizontalSpeed(-1.0)
        moves = 32*[v] + 128*[r] + 32*[v] + 128*[l]

        super().__init__(1,                                   # depth
                        #Vector(randrange(hw, pyxel.width - hw), -animation.height),
                         Vector(16, -animation.height),
                         Path(moves, loop=True),
                         animation)
        self.weapon = InvaderWeapon(self)

    def destroy(self):
        Sprite.destroy(self)
        SpriteManager().attach(InvaderExplosion(self))

    def update(self):
        super().update()
        self.weapon.update()
        if self.destroyed:
            return

        self.weapon.fire()

        # Do we collide with the rocket?
        rocket = Rocket()
        if self.collide_with(rocket) or rocket.collide_with(self):
            self.hit_by(rocket)
            rocket.hit_by(self)
