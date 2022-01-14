import random
import re
import pickle
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

class Random_Walk():
    """class Random_Walk
    Class to model a discrete random walk.
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

    def graph(self, path = None, name = "random_walk.jpg", save_pickle = False):
        """class method Random_Walk.graph
        Method to call correct graphing function
        PARAMETERS:
            - path:                 float 2D array path
                - if none: assume that user wants default path self.path
            - file name:            string name
                - if none, call "random_walk.jpg"
            - create pickle file?:  bool save_pickle
                - if none, assume False
            RETURN:
                - None
                - Calls correct graphing function, which will return True and save image file of graph
        """
        # input handling:
        # acceptable name extensions: jpg. jpeg, png
        # if name has wrong extension type, get rid of extension type
        # if name has no extension type, no issue as matplotlib will default to png
        # if no path specified, set to default path
        if not name.endswith(('jpg', 'jpeg', 'png')):
            if "." in name:
                name = name.split('.', 1)[0]
        if path == None: path = self.path

        # call graphing function based on if 1D, 2D or 3D starting position
        if len(self.starting_position) == 1:
            # 1D is actually just 2D with x axis set to discrete time stamps
            # so create time stamps and plot
            x = [i for i in range(0, self.number_of_steps)]
            path = [[x[i], path[i]] for i in range(self.number_of_steps)]
            self.graph_2D(path, name, save_pickle)
        elif len(self.starting_position) == 2:
            self.graph_2D(path, name, save_pickle)
        elif len(self.starting_position) == 3:
            self.graph_3D(path, name, save_pickle)
        else:
            raise ValueError('Starting position must be 1-dimensional, 2-dimensional or '
                             '3-dimensional for a graph of the walk to be generated.')

    def graph_2D(self, path, name, save_pickle):
        """class method Random_Walk.graph_2D
        Used by: Random_Walk.graph
        Method to create image file of graph of 2D walk
        PARAMETERS:
            - path:         float 2D array path
            - name:         string name
            - save_pickle:  bool
        RETURN:
            - True
            - Saves 2D plot of path and potentially saves pickle of plot
        """
        # extract x and y values from each position in path
        x = [position[0] for position in path]
        y = [position[1] for position in path]

        #plot and save plot
        plt.plot(x, y)
        plt.savefig(name)

        if save_pickle == True:
            # if user wants to save pickle of plot,
            # get rid of extension from name,
            # add correct pickle extension
            # extract the figure and save
            if "." in name:
                name = name.split('.', 1)[0]
            name += '.fig.pickle'
            fig = plt.figure()
            pickle.dump(fig, open(name, 'wb'))

        return True
    def graph_3D(self, path, name, save_pickle):
        """class method Random_Walk.graph_3D
            Used by: Random_Walk.graph
            Method to create image file of graph of 3D walk
            PARAMETERS:
                - path:         float 2D array path
                - name:         string name
                - save_pickle:  bool
            RETURN:
                - True
                - Saves 3D plot of path and potentially saves pickle of plot
        """
        # extract x,y, and z values from each position in plot
        x = [position[0] for position in path]
        y = [position[1] for position in path]
        z = [position[2] for position in path]

        # 3d plot and save plot
        fig = plt.figure()
        ax = plt.axes(projection="3d")
        ax.plot(x, y, z)
        plt.savefig(name)

        if save_pickle == True:
            # if user wants to save pickle of plot,
            # get rid of extension from name,
            # add correct pickle extension
            # save figure
            if "." in name:
                name = name.split('.', 1)[0]
            name += '.fig.pickle'
            pickle.dump(fig, open(name, 'wb'))

        return True
