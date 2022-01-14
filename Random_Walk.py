import random

class Random_Walk():
    """class Random_Walk
    Class to model a simple random walk.
    Features:
        - Simulate random walk based on position, possible moves, and probability distribution of moves.
    """
    def __init__(self, start = [0,0], n=100, moves = None, p = None):
        """class method Random_Walk.__init__
        PARAMETERS:
                - starting position:            float array start
                    - if none: assume 2D walk starting at [0,0]
                - number of moves:              int n
                    - if none: assume 100 steps
                - possible moves:               float array moves
                    - if none: assume possible step in each direction
                - probability distribution:     float array p
                    - if none: assume each step has equal weighting
            RETURN:
                None
            DESCRIPTION:
                - sets up starting position, number of moves, possible moves, the probability of each move, and does
                    a random walk
                - if no moves inputted, determined by number of dimensions of starting position
                - if no probabilities inputted, assumed to be equally weighted
                - does a random walk and saves it to self.path
        """
        # init starting position and number of steps
        self.starting_position = start
        self.number_of_steps = n

        # init possible moves
        self.moves = moves
        # if no possible moves inputted, assume that moves in each direction possible
        # so store an array which moves 1 or -1 in each dimension of the starting position
        if self.moves == None:
            self.moves = [[0] * len(self.starting_position) for i in range(2 * len(self.starting_position))]
            for i in range(0, len(self.starting_position)):
                self.moves[2 * i][i] = 1
                self.moves[2 * i + 1][i] = -1

        # init probability distribution of chance of each move
        self.p_distro = p
        # if move no probability distribution given, assume uniform modelling
        if self.p_distro == None:
            self.p_distro = [1 / len(self.moves)] * len(self.moves)

        # create a default random path of the walk, save to self.path
        self.path = self.walk(self.p_distro)

    def step(self, p = None):
        """class method Random_Walk.step
        Generator method to create sequence of random walks.
        Usese random.choices() to choose the random moves based on some inputted possibility distro p
        PARAMETERS:
            - probability distribution:     float array p
                - if none: assume initiated probability distribution (default is uniform)
        RETURN:
            - current position:             float array current_position
        """
        if p == None: p = self.p_distro

        # copy over starting position and generate full set of random moves
        current_position = [coord for coord in self.starting_position]
        moves = random.choices(self.moves, weights = p, k = self.number_of_steps)
        # for each move: update current_position based on the move, then yield cururent_possition
        for move in moves:
            current_position = [current_position[i] + move[i] for i in range(len(self.starting_position))]
            yield (current_position)

    def walk(self, p = None):
        """class method Random_Walk.walk
        Method to call generator function Random_Walk.step and get the path of the random walk
        PARAMETERS:
            - probability distribution:     float array p
                - if none: assume initiated probability distribution (default is uniform)
        RETURN:
            - path that random walk takes:  float 2D array path
        """
        if p == None: p = self.p_distro
        # call generator function,
        # store each step in 2D array path
        # return path
        step = self.step(p)
        path = [next(step) for i in range(self.number_of_steps)]
        return (path)
