
import pyxel

from spaceinvaders.animation         import Animation
from spaceinvaders.invader_explosion import InvaderExplosion
from spaceinvaders.life_bar          import LifeBar
from spaceinvaders.meta_singleton    import MetaSingleton
from spaceinvaders.path              import Path
from spaceinvaders.rocket_weapon     import RocketWeapon
from spaceinvaders.sprite            import Sprite
from spaceinvaders.sprite_manager    import SpriteManager
from spaceinvaders.vector            import Vector
from spaceinvaders.vertical_speed    import VerticalSpeed


class Rocket(Sprite, metaclass=MetaSingleton):

    def __init__(self):
        self.normal_speed = Animation(0,         # img
                                      16, 16,    # width, height
                                      0, 0,      # origx, origy
                                      4)         # count
        self.left_speed = Animation(0,           # img
                                      16, 16,    # width, height
                                      0, 16,     # origx, origy
                                      4)         # count
        self.right_speed = Animation(0,          # img
                                      16, 16,    # width, height
                                      0, 32,     # origx, origy
                                      4)         # count
        super().__init__(2,                                                 # depth
                         Vector((pyxel.width / 2) - 8, pyxel.height - 16),
                         Path([VerticalSpeed(0.0)], loop=True),
                         self.normal_speed)
        self.rocket_speed = 1.5

        self.weapon = RocketWeapon(10)

    def update(self):
        if pyxel.btn(pyxel.KEY_LEFT):
            self.left()
        elif pyxel.btn(pyxel.KEY_RIGHT):
            self.right()
        else:
            self.animation = self.normal_speed

        if pyxel.btn(pyxel.KEY_UP):
            self.shoot()

        self.weapon.update()

        Sprite.update(self)

    def left(self):
        if self.x - self.width/2 - self.rocket_speed >= 0:
            self.teleport( Vector(-self.rocket_speed, 0) )
            self.animation = self.left_speed

    def right(self):
        if self.x + self.width/2 + self.rocket_speed <= pyxel.width:
            self.teleport( Vector(self.rocket_speed, 0) )
            self.animation = self.right_speed

    def shoot(self):
        self.weapon.fire()

    def hit_by(self, sprite):
        LifeBar().dec()
        if LifeBar().is_dead():
            self.destroy()
            SpriteManager().attach(InvaderExplosion(self))
