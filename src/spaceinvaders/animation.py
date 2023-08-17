
import pyxel

# Animation Directions:
LEFT_TO_RIGHT = 0
TOP_TO_BOTTOM = 1


class Animation:
    """An animation is a list of COUNT frames of WIDTH x HEIGHT pixels each taken
     from the image IMG starting at (ORIGX, ORIGY) following the given DIRECTION.

    A loop animation (LOOP set to True) is an animation that keeps repeating itself, i.e., that won't stop by itself.

    The animation speed is described by its FPS, i.e., frames per seconds.

    """

    def __init__(self,
                 img, width, height, origx, origy, count,
                 loop=True, direction=LEFT_TO_RIGHT, fps=5):
        assert count >= 1, "Frame count must be greater than or equal to 1"

        # Config:
        self.img = img
        self.width = width
        self.height = height
        self.origx = origx
        self.origy = origy
        self.count = count
        self.loop = loop
        self.direction = direction
        self.fps = fps

        # State:
        self.framex = origx
        self.framey = origy
        self.frame = 0
        self.running = True

    def start(self):
        self.running = True

    def stop(self):
        self.running = False

    def restart(self):
        self.frame = 0
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
        else:  # self.direction == TOP_TO_BOTTOM
            self.framey += self.height

    # Draw at the given top left corner's coordinates.
    def draw_at(self, tlc):
        (x, y) = tlc
        pyxel.blt(x, y,                     # (x, y) destination
                  self.img,                 # numero image source
                  self.framex, self.framey, # (x, y) source
                  self.width, self.height,  # (largeur, hauteur) source et destination
                  0)                        # couleur transparente