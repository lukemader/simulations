import random

class Random_Walk():
    def __init__(self, start = [0,0], n=100, moves = None, p = None):
        self.starting_position = start
        self.number_of_steps = n

        self.moves = moves
        if self.moves == None:
            self.moves = [[0] * len(self.starting_position) for i in range(2 * len(self.starting_position))]
            for i in range(0, len(self.starting_position)):
                self.moves[2 * i][i] = 1
                self.moves[2 * i + 1][i] = -1

        self.p_distro = p
        if self.p_distro == None:
            self.p_distro = [1 / len(self.moves)] * len(self.moves)

        self.path = self.walk(self.p_distro)

    def step(self, p = None):
        if p == None: p = self.p_distro

        current_position = [coord for coord in self.starting_position]
        moves = random.choices(self.moves, weights = p, k = self.number_of_steps)
        for move in moves:
            current_position = [current_position[i] + move[i] for i in range(len(self.starting_position))]
            yield (current_position)

    def walk(self, p = None):
        if p == None: p = self.p_distro

        step = self.step(p)
        path = [next(step) for i in range(self.number_of_steps)]
        return (path)