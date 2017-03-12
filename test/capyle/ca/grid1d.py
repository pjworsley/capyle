import numpy as np
from capyle.ca import Neighbourhood, Grid
from capyle.utils import gens_to_dims, clip_numeric


class Grid1D(Grid):

    def __init__(self, ca_config, transition_func):
        """
        1D grid constructor - takes the generations, states and
        transition function to create the appropriate grid.
            If no neighbourhood specified [1,1,1] will be used
            Default grid configuration; center cell in state[-1]
        """
        # init superclass
        Grid.__init__(self)

        self.ca_config = ca_config

        # check the generations are valid
        if ca_config.num_generations < 1:
            raise ValueError('Invalid generation number {n}, there must be 1' +
                             ' or more generations.'.format(
                                 n=ca_config.num_generations))

        # calculate the grid dimensions from the generations
        numrows, numcols = gens_to_dims(ca_config.num_generations)
        # wrapsize is the width of the columns at either side (hidden)
        # used for wrapping behavior
        # a wrapsize of 1 leads to 2 extra columns (1 either side of the grid)
        wrapsize = 1
        self.wrapping_grid = np.zeros((numrows, numcols + wrapsize*2))

        # set neighbourhood
        self.set_neighbourhood(ca_config)

        # initial grid
        self.wrapping_grid.fill(ca_config.states[0])
        self.grid = self.wrapping_grid[:, 1:-1]
        if ca_config.initial_grid is not None:
            self.set_grid(ca_config.initial_grid)
        self.refresh_wrap()

        # initialise variable to keep track of t
        self.current_gen = 0

        # handle transition function and any addional variables passed
        self.additional_args = None
        if type(transition_func) == tuple and len(transition_func) > 1:
            self.transition_func = transition_func[0]
            self.additional_args = transition_func[1:]
        else:
            self.transition_func = transition_func


    def refresh_wrap(self):
        """ Update the wrapping border of the grid to reflect any changes """
        if not self.ca_config.wrap:
            # if not wrapping set outer borders to 'dead'
            self.wrapping_grid[:, 0] = 0
            self.wrapping_grid[:, -1] = 0
        else:
            # if wrapping set to grid states
            self.wrapping_grid[:, 0] = self.grid[:, -1]
            self.wrapping_grid[:, -1] = self.grid[:, 0]

    def get_neighbour_arrays(self):
        """ Get the states of the cells left and right neighbours
        and apply the neighbourhood """
        nhood_bool = (self.neighbourhood.neighbourhood == 1)
        self_states = self.grid[self.current_gen]
        left_neighbour_states = (nhood_bool[0] *
                                 self.wrapping_grid[self.current_gen, :-2])
        right_neighbour_states = (nhood_bool[2] *
                                  self.wrapping_grid[self.current_gen, 2:])
        return left_neighbour_states, self_states, right_neighbour_states

    def count_neighbours(self, neighbourstates):
        l, c, r = neighbourstates
        states = self.ca_config.states
        counts = np.empty(len(states), dtype=np.ndarray)
        for i, s in enumerate(states):
            counts[i] = (l == s) + (r == s)
        return counts

    def step(self):
        """ Calculate the next timestep by applying the transistion function
        and save the new state to grid """

        ns = self.get_neighbour_arrays()
        nc = self.count_neighbours(ns)
        if self.additional_args is None:
            # if no additional variables supplied
            newrow = self.transition_func(self.grid, ns, nc)
        else:
            # otherwise pass in the arguments to the transision function
            newrow = self.transition_func(self.grid, ns, nc,
                                          *self.additional_args)

        self.current_gen += 1
        self.grid[self.current_gen] = newrow
        self.refresh_wrap()


def randomise1d(grid, background_state, proportions):
    """ Randomise a 2D grid for a 1D cellular automata

    Takes a grid, the background state, and
    proportions for each state in a list of tuples ([(1,0.4), (2,0.3)])"""
    grid[0, :] = background_state
    numcells_per_state = np.zeros(len(proportions), dtype=int)
    for i, p in enumerate(proportions):
        proportion = clip_numeric(p[1], 0, 1)
        numcells_per_state[i] = int(proportion * grid.size)
    randindicies = np.random.choice(grid[0].size,
                                    np.sum(numcells_per_state), replace=False)
    g = np.copy(grid[0])
    used = 0
    for i, p in enumerate(proportions):
        state = p[0]
        indicies = randindicies[used:numcells_per_state[i]]
        g[indicies] = state
        used += numcells_per_state[i]

    grid[0, :] = g[:]
    return grid
