#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pyxel
from random import randrange

# Debug Parameters:
DEBUG_COLLISION      = False

# Animation Directions:
LEFT_TO_RIGHT = 0
TOP_TO_BOTTOM = 1

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
        self.depth     = depth
        self.x         = x
        self.y         = y
        self.width     = animation.width
        self.height    = animation.height
        self.img       = animation.img
        self.speed     = speed
        self.animation = animation

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

class Centerable:

    def center(self):
        cx = self.x + self.width / 2
        cy = self.y + self.height / 2
        return (cx, cy)

    # Modifie (self.x, self.y) pour que:
    #     self.center() == other_centerable.center()
    def teleport(self, other_centerable):
        (ocx, ocy) = other_centerable.center()
        self.x = ocx - self.width  / 2
        self.y = ocy - self.height / 2
        assert self.center() == other_centerable.center(), "Teleportation failed"

class Collidable:

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

    def debug_draw_collision_data(self, obj, col):
        pyxel.rectb(self.x, self.y, self.width, self.height, col)
        pyxel.line(self.x, self.y, obj.x, obj.y, col)
        pyxel.rectb(obj.x, obj.y, obj.width, obj.height, col)

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

class Invader(Sprite, Collidable):

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


class Shot(Sprite, Collidable, Centerable):

    def __init__ (self, rocket):
        shot_animation = Animation(0,                          # img
                                   8, 8,                       # width, height
                                   0, 112,                     # origx, origy
                                   1,                          # count
                                   direction=TOP_TO_BOTTOM)
        Sprite.__init__(self,
                          1,                                     # depth
                          rocket.x + rocket.x/2, rocket.y,       # x, y
                          3,                                     # speed
                          shot_animation)

class InvaderExplosion(Sprite):

    def __init__(self, invader):
        invader_explosion_animation = Animation(0,                      # img
                                               16, 16,                  # width, height
                                               0, randrange(3, 6) * 16, # origx, origy
                                               10,                      # count
                                               loop=False)
        Sprite.__init__(self,
                          1,                                             # depth
                          invader.x, invader.y,                          # x, y
                          invader.speed,                                 # speed
                          invader_explosion_animation)

class Life(Sprite):

    def __init__(self):
        life_animation = Animation(1,           # img
                                   40, 16,      # width, height
                                   0, 0,        # origx, origy
                                   1)           # count
        Sprite.__init__(self,
                          3,                    # depth
                          0, 0, # x, y
                          0,                    # speed
                          life_animation)
        self.life   = 18

    def draw(self):
        Sprite.draw(self)

        x = self.x + 2
        y = self.y + 2
        w = self.life
        h = 4
        color = 2
        pyxel.rect(x, y, w, h, color)
        pyxel.rect(x+1, y+1, w-2, h-2, 8)
        pyxel.rect(self.x+5, self.y+3, 3, 1, 7)
        pyxel.rect(self.x+9, self.y+3, 1, 1, 7)

    def dec(self):
        self.life = max(0, self.life - 2)

    def inc(self):
        self.life = min(18, self.life + 2)

    def die_immediatly(self):
        self.life = 0

    def is_dead(self):
        return self.life == 0

class Rocket(Sprite, Centerable, Collidable):

    def __init__(self):
        self.normal_speed = Animation(0,         # img
                                      16, 16,    # width, height
                                      0, 0,     # origx, origy
                                      4)         # count
        self.left_speed = Animation(0,         # img
                                      16, 16,    # width, height
                                      0, 16,     # origx, origy
                                      4)         # count
        self.right_speed = Animation(0,         # img
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
            if self.x - self.rocket_speed >= 0:
                self.x -= self.rocket_speed
                self.animation = self.left_speed
        elif pyxel.btn(pyxel.KEY_RIGHT):
            if self.x + self.rocket_speed <= pyxel.width - self.width:
                self.x += self.rocket_speed
                self.animation = self.right_speed
        elif pyxel.btn(pyxel.KEY_UP):
            pass
        else:
            self.animation = self.normal_speed

        Sprite.update(self)

class Root:

    def __init__(self):
        self.fps = 30
        pyxel.init(160, 120, fps=self.fps)
        pyxel.load("space-invaders.pyxres")

        self.stars              = []
        self.invaders           = []
        self.rocket             = Rocket()
        self.shots              = []
        self.life               = Life()
        self.invader_explosions = []
        self.paused             = False

        # Sprites sorted by depth:
        # [0] Stars
        # [1] Blackholes, planets, planet explosions
        # [2] Rocket, implosion
        # [3] HUD
        #
        # FIXME Find a better name for this tree of sprites.
        self.sprites = [[], [], [], []]
        self.add_sprite(self.rocket)
        self.add_sprite(self.life)

        self.debug_objects = []

    def run(self):
        pyxel.run(self.update, self.draw)

    def add_sprite(self, sprite):
        self.sprites[sprite.depth].append(sprite)

    def remove_sprite(self, sprite):
        self.sprites[sprite.depth].remove(sprite)

    def remove_rocket(self):
        self.remove_sprite(self.rocket)
        self.rocket = None

    def rocket_destroyed_by_invader(self, invader):
        self.remove_rocket()
        self.add_invader_explosion( InvaderExplosion(invader) )

    def add_star(self, star):
        self.add_sprite(star)
        self.stars.append(star)

    def remove_star(self, star):
        self.remove_sprite(star)
        self.stars.remove(star)

    def update_stars(self):
        for star in self.stars:
            if not star.is_visible():
                self.remove_star(star)
        if pyxel.frame_count % 1 == 0:
            star = Star()
            self.add_star(star)

    def add_shot(self, shot):
        self.add_sprite(shot)
        self.shots.append(shot)

    def remove_shot(self, shot):
        self.remove_sprite(shot)
        self.shots.remove(shot)

    def update_shots(self):
        for shot in self.shots:
            if not shot.is_visible():
                self.remove_shot(shot)
                continue

            if self.rocket is not None and shot.collide_with(self.invader):
                    self.remove_shot(shot)
                    self.add_invader_explosion(InvaderExplosion(invader))

        for invader_explosion in self.invader_explosions:
            if invader_explosion.is_done():
                self.remove_invader_explosion(invader_explosion)

    def add_invader(self, invader):
        self.add_sprite(invader)
        self.invaders.append(invader)

    def remove_invader(self, invader):
        self.remove_sprite(invader)
        self.invaders.remove(invader)

    def add_invader_explosion(self, invader_explosion):
        self.add_sprite(invader_explosion)
        self.invader_explosions.append(invader_explosion)

    def remove_invader_explosion(self, invader_explosion):
        self.remove_sprite(invader_explosion)
        self.invader_explosions.remove(invader_explosion)

    def update_invaders(self):
        for invader in self.invaders:
            if not invader.is_visible():
                self.remove_invader(invader)
                continue

            if self.rocket is not None and invader.collide_with(self.rocket):
                    self.remove_invader(invader)
                    self.life.dec()
                    self.add_invader_explosion(InvaderExplosion(invader))
                    if self.life.is_dead():
                        self.rocket_destroyed_by_invader(invader)

        if pyxel.frame_count % 60 == 0:
            invader = Invader()
            self.add_invader(invader)

        for invader_explosion in self.invader_explosions:
            if invader_explosion.is_done():
                self.remove_invader_explosion(invader_explosion)

    def is_game_over(self):
        return self.life.is_dead()

    def update(self):
        if pyxel.btnp(pyxel.KEY_Q):
            pyxel.quit()

        if pyxel.btnp(pyxel.KEY_SPACE):
            self.paused = not self.paused

        if pyxel.btnp(pyxel.KEY_F1):
            global DEBUG_COLLISION
            DEBUG_COLLISION = not DEBUG_COLLISION

        if self.paused:
            return

        for depth in range(0, len(self.sprites)):
            sprites = self.sprites[depth]
            for sprite in sprites:
                sprite.update()
        self.update_shots()
        self.update_stars()
        self.update_invaders()
        if self.is_game_over():
            return

    def debug_draw_collision_data(self, collidables):
        if self.rocket is None:
            return

        col = 0
        for c in collidables:
            c.debug_draw_collision_data(self.rocket, 2+col)
            col += 1

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
        for sprites in self.sprites:
            for sprite in sprites:
                sprite.draw()

        if DEBUG_COLLISION:
            for cl in [self.invaders]:
                self.debug_draw_collision_data(cl)

        self.draw_game_over()
        self.draw_paused()

        f = pyxel.frame_count % self.fps
        if (f // 8) % 2 == 0:
            color = 1
            for o in self.debug_objects:
                pyxel.rectb(o.x, o.y, o.width, o.height, color)
                color += 1

def main():
    global root
    root = Root()
    root.run()

def pause():
    global root
    root.paused = True

if __name__ == "__main__":
    main()
