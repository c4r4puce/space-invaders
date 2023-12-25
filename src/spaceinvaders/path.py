from spaceinvaders.vector import Vector


class Path:

    def __init__(self, moves=[], loop=True):
        self.moves   = moves
        self.current = 0
        self.loop    = loop

    def next_move(self):
        assert self.loop or self.current < len(self.moves), "Missing next move"

        move = self.moves[self.current]
        assert isinstance(move, Vector)
        self.current += 1
        if self.current == len(self.moves) and self.loop:
            self.current = 0
        return move

    def end(self):
        return not self.loop and self.current == len(self.moves)

    def copy(self):
        moves = []
        for m in self.moves:
            moves.append(m.copy())
        return Path(moves, loop=self.loop)
