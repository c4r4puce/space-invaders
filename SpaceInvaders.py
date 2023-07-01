#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pyxel
from random import randrange

# Animation Directions:
LEFT_TO_RIGHT = 0
TOP_TO_BOTTOM = 1

# Singletons:
life_bar = None
rocket   = None
root     = None

class Animation:

    def __init__(self, img, width, height, origx, origy, count, loop=True, direction=LEFT_TO_RIGHT, fps=5):
        assert count >= 1, "Frame count must be greater than or equal to 1"

        # Config:
        self.img       = img
        self.width     = width
        self.height    = height
        self.origx     = origx
        self.origy     = origy
        self.count     = count
        self.loop      = loop
        self.direction = direction
        self.fps       = fps

        # State:
        self.framex  = origx
        self.framey  = origy
        self.frame   = 0
        self.running = True

    def start(self):
        self.running = True

    def stop(self):
        self.running = False

    def restart(self):
        self.frame   = 0
        self.running = True

    def next_frame(self):
        if not self.running:
            return

        if pyxel.frame_count % self.fps != 0:
            return

        self.frame += 1
        if self.frame == self.count:
            if self.loop:
                self.frame = 0
                if self.direction == LEFT_TO_RIGHT:
                    self.framex = self.origx
                else: # self.direction == TOP_TO_BOTTOM
                    self.framey = self.origy
            else:
                self.stop()
            return

        if self.direction == LEFT_TO_RIGHT:
            self.framex += self.width
        else: # self.direction == TOP_TO_BOTTOM
            self.framey += self.height

    def draw_at(self, x, y):
        pyxel.blt(x, y,                     # (x, y) destination
                  self.img,                 # numero image source
                  self.framex, self.framey, # (x, y) source
                  self.width, self.height,  # (largeur, hauteur) source et destination
                  0)                        # couleur transparente

class Sprite:

    def __init__(self, depth, x, y, speed, animation):
        self.animation = animation
        self.depth     = depth
        self.destroyed = False
        self.height    = animation.height
        self.img       = animation.img
        self.speed     = speed
        self.width     = animation.width
        self.x         = x
        self.y         = y

    def update_frame(self):
        self.animation.next_frame()

    def update(self):
        self.update_frame()
        self.y += self.speed # Update position

    def draw(self):
        self.animation.draw_at(self.x, self.y)

    def is_visible(self):
        return self.y < pyxel.height

    def is_done(self):
        return not self.animation.running

    def center(self):
        cx = self.x + self.width / 2
        cy = self.y + self.height / 2
        return (cx, cy)

    # Modify (self.x, self.y) to get:
    #     self.center() == other_centerable.center()
    def teleport(self, other_centerable):
        (ocx, ocy) = other_centerable.center()
        self.x = ocx - self.width  / 2
        self.y = ocy - self.height / 2
        assert self.center() == other_centerable.center(), "Teleportation failed"

    def collide_with_point(self, px, py):
        return self.x <= px and px <= self.x + self.width and self.y <= py and py <= self.y + self.height

    def collide_with_rect_1(self, rx, ry, rwidth, rheight):
        return self.collide_with_point(rx, ry)

    def collide_with_rect_2(self, rx, ry, rwidth, rheight):
        return self.collide_with_point(rx + rwidth, ry)

    def collide_with_rect_3(self, rx, ry, rwidth, rheight):
        return self.collide_with_point(rx, ry + rheight)

    def collide_with_rect_4(self, rx, ry, rwidth, rheight):
        return self.collide_with_point(rx + rwidth, ry + rheight)

    def collide_with_rect(self, rx, ry, rwidth, rheight):
        return self.collide_with_rect_1(rx, ry, rwidth, rheight) \
            or self.collide_with_rect_2(rx, ry, rwidth, rheight) \
            or self.collide_with_rect_3(rx, ry, rwidth, rheight) \
            or self.collide_with_rect_4(rx, ry, rwidth, rheight)

    def collide_with(self, oc):
        return self.collide_with_rect(oc.x, oc.y, oc.width, oc.height)

    def debug_draw_collision_data(self):
        pass

    def destroy(self):
        if not self.destroyed:
            Root.singleton().remove_sprite(self)
            self.destroyed = True

class Star(Sprite):

    def __init__(self):
        star_animation = Animation(1,                        # img
                                   8, 8,                     # width, height
                                   randrange(0, 9) * 8, 16,  # origx, origy
                                   1,                        # count
                                   direction=TOP_TO_BOTTOM,
                                   fps=10)
        Sprite.__init__(self,
                          0,                                 # depth
                          randrange(0, pyxel.width-8), -8,   # x, y
                          randrange(2, 4),                   # speed
                          star_animation)

class Invader(Sprite):

    def __init__ (self):
        invader_animation = Animation(0,                         # img
                                     16, 16,                     # width, height
                                     randrange(0, 6)*16, 128,    # origx, origy
                                     8,                          # count
                                     direction=TOP_TO_BOTTOM,
                                     fps=6 )
        Sprite.__init__(self,
                          1,                                     # depth
                          randrange(0, pyxel.width-16), -16,     # x, y
                          1,                                     # speed
                          invader_animation)

    def explode(self):
        if self.destroyed:
            return
        self.destroy()
        Root.singleton().add_sprite( InvaderExplosion(self) )

    def update(self):
        Sprite.update(self)

        if self.destroyed:
            return

        # Do we collide with the rocket?
        rocket = Rocket.singleton()
        if self.collide_with(rocket):
            self.explode()
            LifeBar.singleton().dec()
            if LifeBar.singleton().is_dead():
                rocket.destroy()

    def debug_draw_collision_data(self):
        pyxel.rectb(self.x, self.y, self.width, self.height, 7)

class InvaderExplosion(Sprite):

    def __init__(self, invader):
        animation = Animation(0,                       # img
                              16, 16,                  # width, height
                              0, randrange(3, 7)*16,   # origx, origy
                              10,                      # count
                              loop=False,
                              fps = 3)
        Sprite.__init__(self,
                        1,                             # depth
                        invader.x, invader.y,          # x, y
                        invader.speed,                 # speed
                        animation)


class UFO(Sprite):

    def __init__ (self):
        UFO_animation = Animation(1,                          # img
                                  16, 16,                     # width, height
                                  0, 24,                      # origx, origy
                                  7,                          # count
                                  fps=6 )
        Sprite.__init__(self,
                          1,                                     # depth
                          -16, 50,                               # x, y
                          3,                                     # speed
                          UFO_animation)

class LifeBar(Sprite):

    def singleton():
        global life_bar
        if life_bar is None:
            life_bar = LifeBar()
        return life_bar

    def __init__(self):
        animation = Animation(1,           # img
                              40, 16,      # width, height
                              0, 0,        # origx, origy
                              1)           # count
        Sprite.__init__(self,
                          3,               # depth
                          0, 0,            # x, y
                          0,               # speed
                          animation)
        self.hit_points = 18

    def draw(self):
        Sprite.draw(self)

        x = self.x + 2
        y = self.y + 2
        w = self.hit_points
        h = 4
        color = 2
        pyxel.rect(x, y, w, h, color)
        pyxel.rect(x+1, y+1, w-2, h-2, 8)
        pyxel.rect(self.x+5, self.y+3, 3, 1, 7)
        pyxel.rect(self.x+9, self.y+3, 1, 1, 7)

    def dec(self):
        self.hit_points = max(0, self.hit_points - 2)

    def inc(self):
        self.hit_points = min(18, self.hit_points + 2)

    def die_immediatly(self):
        self.hit_points = 0

    def is_dead(self):
        return self.hit_points == 0

class RocketProjectile(Sprite):

    def __init__ (self):
        animation = Animation(0,                          # img
                              8, 8,                       # width, height
                              0, 112,                     # origx, origy
                              1,                          # count
                              direction=TOP_TO_BOTTOM)
        (x, y) = Rocket.singleton().center()
        x -= 3 # FIXME Shouldn't be necessary!
        Sprite.__init__(self,
                        1,                                # depth
                        x, y,                             # x, y
                        -3,                               # speed
                        animation)

    def update(self):
        Sprite.update(self)

        if self.destroyed:
            return

        # Do we collide with an invader?
        for invader in Root.singleton().get_sprites("Invader"):
            if self.collide_with(invader):
                self.destroy()
                invader.explode()

    def debug_draw_collision_data(self):
        pyxel.rectb(self.x, self.y, self.width, self.height, 9)

class Rocket(Sprite):

    def singleton():
        global rocket
        if rocket is None:
            rocket = Rocket()
        return rocket

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
        Sprite.__init__(self,
                          2,                                           # depth
                          (pyxel.width / 2) - 8, pyxel.height - 16,    # x, y
                          0,                                           # speed
                          self.normal_speed)
        self.rocket_speed = 1.5

    def update(self):
        if pyxel.btn(pyxel.KEY_LEFT):
            self.left()
        elif pyxel.btn(pyxel.KEY_RIGHT):
            self.right()
        elif pyxel.btn(pyxel.KEY_UP):
            self.shoot()
        else:
            self.animation = self.normal_speed

        Sprite.update(self)

    def left(self):
        if self.x - self.rocket_speed >= 0:
            self.x -= self.rocket_speed
            self.animation = self.left_speed

    def right(self):
        if self.x + self.rocket_speed <= pyxel.width - self.width:
            self.x += self.rocket_speed
            self.animation = self.right_speed

    def shoot(self):
        Root.singleton().add_sprite( RocketProjectile() )

    def debug_draw_collision_data(self):
        pyxel.rectb(self.x, self.y, self.width, self.height, 6)

class SpriteGenerator:

    def __init__(self):
        self.frequencies = {}

    def add(self, sprite_class, freq):
        if freq in self.frequencies:
            self.frequencies[freq].append(sprite_class)
        else:
            self.frequencies[freq] = [sprite_class]

    def generate(self):
        for freq, sprite_classes in self.frequencies.items():
            if pyxel.frame_count % freq != 0:
                continue
            for sprite_class in sprite_classes:
                Root.singleton().add_sprite( sprite_class() )

class Root:

    def singleton():
        global root
        if root is None:
            root = Root()
        return root

    def __init__(self):
        global root
        if root is not None:
            raise AssertionError("singleton pattern violation")
        
        self.fps = 30
        pyxel.init(160, 120, fps=self.fps)
        pyxel.load("space-invaders.pyxres")

        self.ufos   = []
        self.paused = False

        self.generator = SpriteGenerator()
        self.generator.add(Invader, 60)
        self.generator.add(Star,    1)

        # Sprites sorted by depth:
        # [0] Stars
        # [1] Invader explosions
        # [2] Rocket
        # [3] HUD
        self.sprite_plans = [[], [], [], []]

        # Sprites sorted by class:
        self.sprite_classes = {}

        self.add_sprite( Rocket.singleton() )
        self.add_sprite( LifeBar.singleton() )

        self.debug_mode = False

    def run(self):
        pyxel.run(self.update, self.draw)

    def add_sprite(self, sprite):
        self.sprite_plans[sprite.depth].append(sprite)

        sprite_class = type(sprite).__name__
        if sprite_class in self.sprite_classes:
            self.sprite_classes[sprite_class].append(sprite)
        else:
            self.sprite_classes[sprite_class] = [sprite]

    def remove_sprite(self, sprite):
        self.sprite_plans[sprite.depth].remove(sprite)
        sprite_class = type(sprite).__name__
        self.sprite_classes[sprite_class].remove(sprite)

    def get_sprites(self, sprite_class):
        if sprite_class in self.sprite_classes:
            sprites = self.sprite_classes[sprite_class]
        else:
            sprites = []
        return sprites

    def add_ufo(self, ufo):
        self.add_drawable(ufo)
        self.ufos.append(ufo)

    def remove_ufo(self, ufo):
        self.remove_drawable(ufo)
        self.ufos.remove(ufo)

    def is_game_over(self):
        return LifeBar.singleton().is_dead()

    def update(self):
        if pyxel.btnp(pyxel.KEY_Q):
            pyxel.quit()

        if pyxel.btnp(pyxel.KEY_SPACE):
            self.paused = not self.paused

        if pyxel.btnp(pyxel.KEY_F1):
            self.debug_mode = not self.debug_mode
            if self.debug_mode:
                print("Debug Mode: enabled.")
            else:
                print("Debug Mode: disabled.")

        if self.debug_mode:
            print(f"Sprite Plans:")
            for depth in range( len(self.sprite_plans) ):
                print(f"    [{depth}] {len(self.sprite_plans[depth])}")
            print(f"Sprite Classes:")
            for cls, sprites in self.sprite_classes.items():
                print(f"    {cls}: {len(sprites)}")

        if self.paused:
            return

        for depth in range(0, len(self.sprite_plans)):
            for sprite in self.sprite_plans[depth]:
                sprite.update()

                # Destroy the sprite if:
                # - it left the screen
                # - or it's animation is done.
                if not sprite.is_visible() or sprite.is_done():
                    sprite.destroy()

        self.generator.generate()

        if self.is_game_over():
            return

    def draw_game_over(self):
        if self.is_game_over():
            pyxel.text(pyxel.width / 2 - 15, pyxel.height / 2, "GAME OVER", 7)

    def draw_paused(self):
        if self.paused:
            f = pyxel.frame_count % self.fps
            if (f // 8) % 2 == 0:
                pyxel.text(1, 1, "PAUSED", 7)

    def draw(self):
        pyxel.cls(0)
        for sprites in self.sprite_plans:
            for sprite in sprites:
                sprite.draw()

        if self.debug_mode:
            for depth in range(0, len(self.sprite_plans)):
                for sprite in self.sprite_plans[depth]:
                    sprite.debug_draw_collision_data()

        self.draw_game_over()
        self.draw_paused()

def main():
    Root.singleton().run()

def pause():
    Root.singleton().paused = True

if __name__ == "__main__":
    main()
