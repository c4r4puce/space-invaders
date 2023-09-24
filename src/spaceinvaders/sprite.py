
import pyxel

from spaceinvaders.sprite_manager import SpriteManager
from spaceinvaders.vector         import Vector


class Sprite:
    """A sprite is an animated object moving around on the screen. It can collide with other sprites.

    A sprite have a DEPTH to help decide which sprite to draw on top of the other.

    The position (POS) of a sprite is the (x, y) coordinates of its center.
    While it's TLC is the (x, y) coordinates of its top left corner. TLC is used to draw of its animation.

    Movement is described by its SPEED and is limited to vertical movements only.
    A positive speed means the sprite is moving from top to bottom. A negative one means moving from bottom to top.

    """

    def __init__(self, depth, pos: Vector, speed: Vector, animation):
        assert isinstance(pos,   Vector), "pos must be a Vector"
        assert isinstance(speed, Vector), "speed must be a Vector"

        self.animation = animation
        self.depth     = depth
        self.destroyed = False
        self.height    = animation.height
        self.img       = animation.img
        self.speed     = speed
        self.width     = animation.width

        self.pos         = pos
        (self.x, self.y) = self.pos.to_tuple() # Retro compatibility

    def tlc(self):
        """Top left corner's coordinates."""
        return (self.x - self.width / 2,
                self.y - self.height / 2)

    def update_frame(self):
        self.animation.next_frame()

    def teleport(self, v):
        """Teleport the sprite along vector V."""
        self.pos.add(v)
        (self.x, self.y) = self.pos.to_tuple() # Retro compatibility

    def update(self):
        """Update position"""
        assert isinstance(self.speed, Vector), "self.speed must be a Vector"
        self.update_frame()
        self.teleport(self.speed)

    def draw(self):
        self.animation.draw_at(self.tlc())

    def is_visible(self):
        """Tell if the sprite can be found somewhere on the screen."""
        hh = self.height / 2
        return self.y < pyxel.height + hh or self.y < -hh

    def is_done(self):
        """Tell if sprite's animation is still running."""
        return not self.animation.running

    def collide_with_point(self, p):
        (px, py) = p
        (x, y) = self.tlc()
        return x <= px and px <= x + self.width and y <= py and py <= y + self.height

    def collide_with_rect_1(self, tlc, width, height):
        return self.collide_with_point(tlc)

    def collide_with_rect_2(self, tlc, width, height):
        (x, y) = tlc
        return self.collide_with_point((x + width, y))

    def collide_with_rect_3(self, tlc, width, height):
        (x, y) = tlc
        return self.collide_with_point((x, y + height))

    def collide_with_rect_4(self, tlc, width, height):
        (x, y) = tlc
        return self.collide_with_point((x + width, y + height))

    def collide_with_rect(self, tlc, width, height):
        return self.collide_with_rect_1(tlc, width, height) \
            or self.collide_with_rect_2(tlc, width, height) \
            or self.collide_with_rect_3(tlc, width, height) \
            or self.collide_with_rect_4(tlc, width, height)

    def collide_with(self, other_sprite):
        """Tell if the current sprite collide with the other one.

        To detect all collision scenario, you should call this function on both
        sprites, i.e., foo.collide_with(bar) and bar.collide_with(foo).

        """
        if self.destroyed or other_sprite.destroyed:
            return False
        return self.collide_with_rect(other_sprite.tlc(),
                                      other_sprite.width, other_sprite.height)

    def draw_debug_overlay(self):
        """Draw sprite's debug overlay.

        It shows its collision box and its center.

        """
        color = 8

        # Collision box
        (x, y) = self.tlc()
        pyxel.rectb(x, y, self.width, self.height, color)

        # Center
        pyxel.pset(self.x, self.y - 1, color)
        pyxel.pset(self.x, self.y + 1, color)
        pyxel.pset(self.x - 1, self.y, color)
        pyxel.pset(self.x, self.y, color)
        pyxel.pset(self.x + 1, self.y, color)

    def destroy(self):
        assert not self.destroyed, "Already destroyed"
        SpriteManager().detach(self)
        self.destroyed = True

    def hit_by(self, sprite):
        """What to do when another sprite hit this one?"""
        self.destroy()
