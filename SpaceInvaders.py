#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pyxel
from random import randrange

# Animation Directions:
LEFT_TO_RIGHT = 0
TOP_TO_BOTTOM = 1

# Singletons:
life_bar       = None
rocket         = None
root           = None
sprite_manager = None

class Animation:

    def __init__(self,
                 img, width, height, origx, origy, count,
                 loop=True, direction=LEFT_TO_RIGHT, fps=5):
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

    # Draw at the given top left corner.
    def draw_at(self, tlc):                 # FIXME life bar is not draw
        (x, y) = tlc
        pyxel.blt(x, y,                     # (x, y) destination
                  self.img,                 # numero image source
                  self.framex, self.framey, # (x, y) source
                  self.width, self.height,  # (largeur, hauteur) source et destination
                  0)                        # couleur transparente

class Sprite:

    def __init__(self, depth, pos, speed, animation):
        self.animation   = animation
        self.depth       = depth
        self.destroyed   = False
        self.height      = animation.height
        self.img         = animation.img
        self.speed       = speed
        self.width       = animation.width
        (self.x, self.y) = pos

    # Center's coordinates.
    def pos(self):
        return (self.x, self.y)

    # Top left corner's coordinates.
    def tlc(self):
        return (self.x - self.width  / 2,
                self.y - self.height / 2)

    def update_frame(self):
        self.animation.next_frame()

    def update(self):
        self.update_frame()
        self.y += self.speed # Update position

    def draw(self):
        self.animation.draw_at( self.tlc() )

    def is_visible(self):
        return self.y < pyxel.height + self.height/2 or self.y < 0 - self.height/2

    def is_done(self):
        return not self.animation.running

    def collide_with_point(self, p):
        (px, py) = p
        (x, y)   = self.tlc()
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
        return self.collide_with_rect(other_sprite.tlc(),
                                      other_sprite.width, other_sprite.height)

    def draw_debug_overlay(self):
        color = 8

        # Collision box
        (x, y) = self.tlc()
        pyxel.rectb(x, y, self.width, self.height, color)

        # Center
        pyxel.pset(self.x,     self.y - 1, color)
        pyxel.pset(self.x,     self.y + 1, color)
        pyxel.pset(self.x - 1, self.y,     color)
        pyxel.pset(self.x,     self.y,     color)
        pyxel.pset(self.x + 1, self.y,     color)

    def destroy(self):
        if not self.destroyed:
            SpriteManager.singleton().detach(self)
            self.destroyed = True

class SpriteManager:

    def singleton():
        global sprite_manager
        if sprite_manager is None:
            sprite_manager = SpriteManager()
        return sprite_manager

    def __init__(self):
        global sprite_manager
        assert sprite_manager is None, "Singleton pattern violation"

        # Sprites sorted by depth:
        # [0] Star
        # [1] Invader, InvaderExplosion, UFO, RocketProjectile
        # [2] Rocket
        # [3] LifeBar
        self.plans = [[], [], [], []]

        # Sprites sorted by class:
        self.classes = {}

        self.frequencies = {}

    def attach(self, sprite):
        self.plans[sprite.depth].append(sprite)

        cls = type(sprite).__name__
        if cls in self.classes:
            self.classes[cls].append(sprite)
        else:
            self.classes[cls] = [sprite]

    def detach(self, sprite):
        self.plans[sprite.depth].remove(sprite)
        cls = type(sprite).__name__
        self.classes[cls].remove(sprite)

    def get(self, cls):
        if cls in self.classes:
            sprites = self.classes[cls]
        else:
            sprites = []
        return sprites

    def spawn(self, cls, freq):
        if freq in self.frequencies:
            self.frequencies[freq].append(cls)
        else:
            self.frequencies[freq] = [cls]

    def update(self):

        # Update sprites, destroying them when necessary.
        for depth in range(0, len(self.plans)):
            for sprite in self.plans[depth]:
                sprite.update()

                # Destroy the sprite if:
                # - it left the screen
                # - or it's animation is done.
                if not sprite.is_visible() or sprite.is_done():
                    if Root.singleton().debug_mode:
                        print(f"is_visible: {sprite.is_visible()}")
                        print(f"is_done:    {sprite.is_done()}")
                    sprite.destroy()

        # Auto-spawn sprites.
        for freq, classes in self.frequencies.items():
            if pyxel.frame_count % freq != 0:
                continue
            if Root.singleton().debug_mode:
                print(f"Will spawn: {classes}")
            for cls in classes:
                self.attach( cls() )

        if Root.singleton().debug_mode:
            print(f"Sprite Plans:")
            for depth in range( len(self.plans) ):
                print(f"    [{depth}] {len(self.plans[depth])}")
            print(f"Sprite Classes:")
            for cls, sprites in self.classes.items():
                print(f"    {cls}: {len(sprites)}")

    def draw(self):
        for sprites in self.plans:
            for sprite in sprites:
                sprite.draw()

        if Root.singleton().debug_mode:
            for cls in ["Invader", "Rocket", "RocketProjectile"]:
                if cls not in self.classes:
                    continue
                for sprite in self.classes[cls]:
                    sprite.draw_debug_overlay()

class Projectile(Sprite):

    def __init__(self, depth, pos, speed, animation):
        Sprite.__init__(self,
                        1,    # depth
                        pos,
                        speed,
                        animation)
        
    def handle_collision(self):
        pass

    def update(self):
        Sprite.update(self)

        if self.destroyed:
            return

        self.handle_collision()

class RocketProjectile(Projectile):

    def __init__(self):
        animation = Animation(0,                          # img
                              8, 8,                       # width, height
                              0, 112,                     # origx, origy
                              1)                          # count
        Projectile.__init__(self, 1, Rocket.singleton().pos(), -3, animation)

    def handle_collision(self):
        for invader in SpriteManager.singleton().get("Invader"):
            if self.collide_with(invader) or invader.collide_with(self):
                self.destroy()
                invader.explode()

class InvaderProjectile(Projectile):

    def __init__(self, invader):
        animation = Animation(0,                          # img
                              8, 8,                       # width, height
                              8, 112,                     # origx, origy
                              1)                          # count
        Projectile.__init__(self, 1, invader.pos(), 3, animation)

    def handle_collision(self):
        rocket = Rocket.singleton()
        if self.collide_with(rocket) or rocket.collide_with(self):
            self.destroy()
            rocket.explode()
            #rocket.hit(self)

class Weapon:

    def __init__(self, cooldown):
        self.cooldown_reload  = cooldown
        self.cooldown_current = 0

    def update(self):
        if self.cooldown_current > 0:
            self.cooldown_current -= 1

    def reload(self):
        self.cooldown_current = self.cooldown_reload

    def ready(self):
        return self.cooldown_current == 0

    def projectile(self):
        raise NotImplementedError()

    # Try to fire. Return True if fired, False otherwise.
    def fire(self):
        if not self.ready():
            return False
        SpriteManager.singleton().attach( self.projectile() )
        self.reload()
        return True

class RocketWeapon(Weapon):
    
    def __init__(self):
        Weapon.__init__(self, 10)

    def projectile(self):
        return RocketProjectile()

class InvaderWeapon(Weapon):
    
    def __init__(self, invader):
        Weapon.__init__(self, 100)
        self.invader = invader

    def projectile(self):
        return InvaderProjectile(self.invader)

class Rocket(Sprite):

    def singleton():
        global rocket
        if rocket is None:
            rocket = Rocket()
        return rocket

    def __init__(self):
        global rocket
        assert rocket is None, "Singleton pattern violation"

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
                        ((pyxel.width / 2) - 8, pyxel.height - 16),  # pos
                        0,                                           # speed
                        self.normal_speed)
        self.rocket_speed = 1.5

        self.weapon = RocketWeapon()

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
            self.x -= self.rocket_speed
            self.animation = self.left_speed

    def right(self):
        if self.x + self.width/2 + self.rocket_speed <= pyxel.width:
            self.x += self.rocket_speed
            self.animation = self.right_speed

    def shoot(self):
        self.weapon.fire()

    def explode(self):
        LifeBar.singleton().dec()
        if LifeBar.singleton().is_dead():
            self.destroy()
            # FIXME Create a RocketExplosion here.

#    def hit(self):
#        pass

class Invader(Sprite):

    def __init__ (self):
        animation = Animation(0,                          # img
                              16, 16,                     # width, height
                              randrange(0, 6)*16, 128,    # origx, origy
                              8,                          # count
                              direction=TOP_TO_BOTTOM,
                              fps=6 )
        Sprite.__init__(self,
                        1,                                   # depth
                        (randrange(0, pyxel.width-16), -16), # pos
                        1,                                   # speed
                        animation)
        self.weapon = InvaderWeapon(self)

    def explode(self):
        assert not self.destroyed, "Already destroyed"
        self.destroy()
        SpriteManager.singleton().attach( InvaderExplosion(self) )

    def update(self):
        Sprite.update(self)
        self.weapon.update()
        if self.destroyed:
            return
        self.weapon.fire()

        # Do we collide with the rocket?
        rocket = Rocket.singleton()
        if self.collide_with(rocket) or rocket.collide_with(self):
            self.explode()
            LifeBar.singleton().dec()
            if LifeBar.singleton().is_dead():
                rocket.destroy()

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
                        invader.pos(),                 # pos
                        invader.speed,                 # speed
                        animation)

class RocketExplosion(Sprite):

    pass

class UFO(Sprite):

    def __init__ (self):
        UFO_animation = Animation(1,                          # img
                                  16, 16,                     # width, height
                                  0, 24,                      # origx, origy
                                  7,                          # count
                                  fps=6 )
        Sprite.__init__(self,
                          1,                                  # depth
                          (-16, 50),                          # pos
                          3,                                  # speed
                          UFO_animation)

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
                          (randrange(0, pyxel.width-8), -8), # pos
                          randrange(2, 4),                   # speed
                          star_animation)

class LifeBar(Sprite):

    def singleton():
        global life_bar
        if life_bar is None:
            life_bar = LifeBar()
        return life_bar

    def __init__(self):
        animation = Animation(1,           # img
                              24, 8,       # width, height
                              0, 0,        # origx, origy
                              1)           # count
        self.width = 24
        self.height = 8
        Sprite.__init__(self,
                          3,                  # depth
                         (0 + self.width/2,   # pos
                          0 + self.height/2), # pos
                          0,                  # speed
                          animation)
        self.hit_points = 18

    def draw(self):
        Sprite.draw(self)

        x = self.x -10
        y = self.y -2
        w = self.hit_points
        h = 4
        color = 2
        pyxel.rect(x, y, w, h, color)
        pyxel.rect(x+1, y+1, w-2, h-2, 8)
        pyxel.rect(x+3, y+1, 3, 1, 7)
        pyxel.rect(x+7, y+1, 1, 1, 7)

    def dec(self):
        self.hit_points = max(0, self.hit_points - 2)

    def inc(self):
        self.hit_points = min(18, self.hit_points + 2)

    def die_immediatly(self):
        self.hit_points = 0

    def is_dead(self):
        return self.hit_points == 0

class Root:

    def singleton():
        global root
        if root is None:
            root = Root()
        return root

    def __init__(self):
        global root
        assert root is None, "Singleton pattern violation"

        self.debug_mode = False
        self.fps        = 30
        self.paused     = False

    def init(self):
        pyxel.init(160, 120, fps=self.fps)
        pyxel.load("space-invaders.pyxres")

        manager = SpriteManager.singleton()
        manager.spawn(Invader, 60)
        manager.spawn(Star,    1)
        manager.attach( Rocket.singleton() )
        manager.attach( LifeBar.singleton() )

    def run(self):
        pyxel.run(self.update, self.draw)

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

        if self.paused:
            return

        SpriteManager.singleton().update()

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
        SpriteManager.singleton().draw()
        self.draw_game_over()
        self.draw_paused()

def main():
    root = Root.singleton()
    root.init()
    root.run()

def pause():
    Root.singleton().paused = True

if __name__ == "__main__":
    main()
