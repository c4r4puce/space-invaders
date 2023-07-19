
import logging

import pyxel

from spaceinvaders import LOGGER_NAME
from spaceinvaders.meta_singleton import MetaSingleton

logger = logging.getLogger(LOGGER_NAME)


class SpriteManager(metaclass=MetaSingleton):
    """Help manage sprites.

    Once a sprite is attached to the manager, it starts being automatically updated
    and drawn. Its destruction is also automatically triggered when it leaves the
    screen or its animation is over.

    Sprites are sorted by depth and classes. Use get() to retrieve all the sprites
    from a given class.

    Sprites sorted by depth:
    [0] Star
    [1] Invader, InvaderExplosion, UFO, RocketProjectile
    [2] Rocket
    [3] LifeBar

    The manager also provide automatic sprite generation at a given frequency via
    spawn().

    """

    def __init__(self):
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
        """Tell the manager to spawn a new sprite with the CLS class every FREQ frames."""
        if freq in self.frequencies:
            self.frequencies[freq].append(cls)
        else:
            self.frequencies[freq] = [cls]

    def update(self):
        """Update the sprites under manager's control taking care to destroy them if necessary.

        Also spawn new sprites if necessary.

        """
        # Update sprites, destroying them when necessary.
        for plan in self.plans:
            for sprite in plan:
                sprite.update()

                # Destroy the sprite if:
                # - it left the screen
                # - or it's animation is done.
                if not sprite.is_visible() or sprite.is_done():
                    logger.debug("is_visible: %s", sprite.is_visible())
                    logger.debug("is_done:    %s", sprite.is_done())
                    sprite.destroy()

        # Auto-spawn sprites.
        for freq, classes in self.frequencies.items():
            if pyxel.frame_count % freq != 0:
                continue
            logger.debug("Will spawn: %s", classes)
            for cls in classes:
                self.attach(cls())

        if logger.isEnabledFor(logging.DEBUG):
            logger.debug("Sprite Plans:")
            for depth, plan in enumerate(self.plans):
                logger.debug("    [%s] %s", depth, len(plan))
            logger.debug("Sprite Classes:")
            for cls, sprites in self.classes.items():
                logger.debug("    %s: %s", cls, len(sprites))

    def draw(self):
        """Draw the sprites under manager's control taking into account their depth."""
        for sprites in self.plans:
            for sprite in sprites:
                sprite.draw()

        if logger.isEnabledFor(logging.DEBUG):
            for cls in ["Invader", "Rocket", "RocketProjectile"]:
                if cls not in self.classes:
                    continue
                for sprite in self.classes[cls]:
                    sprite.draw_debug_overlay()
