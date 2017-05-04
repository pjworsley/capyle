import numpy as np
from capyle.ca import Grid, Neighbourhood
from capyle.utils import clip_numeric


class Grid2D(Grid):

    def __init__(self, ca_config, transition_func):
        # create superclass
        Grid.__init__(self)
        # get the grid size
        numrows, numcols = ca_config.grid_dims
        # Check minimum size
        if not (numrows > 2 and numcols > 2):
            raise ValueError(
                'Invalid grid size {g}'.format(g=ca_config.grid_dims))

        # store a handle on config object
        self.ca_config = ca_config

        # wrap size is 1 col & row all the way round the grid
        wrapsize = 1
        # wrap size doubled for the row/colum on each side of the grid
        # ie. a wrap size of 1 requires 2 extra rows and 2 extra columns
        self.wrapping_grid = np.empty((numrows + wrapsize*2,
                                       numcols + wrapsize*2))
        # initial state fill
        self.wrapping_grid.fill(ca_config.states[0])
        self.grid = self.wrapping_grid[wrapsize:-wrapsize,
                                       wrapsize:-wrapsize]

        # Generate the indices only once per grid
        self.wrapindicies, self.gridindicies = self._gen_wrap_indicies(
            wrapsize)

        # if at t = 0 grid has been supplied, set the states
        if ca_config.initial_grid is not None:
            self.set_grid(ca_config.initial_grid)

        # set neighbourhood
        self.set_neighbourhood(ca_config)

        # Handle any additional variables the user wishes to keep track of
        # for use in the transition function
        self.additional_args = None
        if type(transition_func) == tuple and len(transition_func) > 1:
            self.transition_func = transition_func[0]
            self.additional_args = transition_func[1:]
        else:
            self.transition_func = transition_func

    def _gen_wrap_indicies(self, wrapsize):
        """Create the indecies used when refreshing the wrap"""
        wrap_width = wrapsize
        wrap_height = wrap_width

        wraprowmax, wrapcolmax = self.wrapping_grid.shape
        gridrowmax, gridcolmax = self.grid.shape

        # fromrows, torows, fromcols, tocols
        # start from wrap-top
        wrapindicies = [(0, wrap_height, wrap_width, (-wrap_width)),
                        # wrap-bottom
                        (-wrap_height, wraprowmax, wrap_width, (-wrap_width)),
                        # wrap-left
                        (wrap_height, -wrap_height, 0, wrap_width),
                        # wrap-right
                        (wrap_height, -wrap_height, -wrap_width, wrapcolmax),
                        # wrap-topleft
                        (0, wrap_height, 0, wrap_width),
                        # wrap-topright
                        (0, wrap_height, -wrap_width, wrapcolmax),
                        # wrap-bottomleft
                        (-wrap_height, wraprowmax, 0, wrap_width),
                        # wrap-bottomright
                        (-wrap_height, wraprowmax, -wrap_width, wrapcolmax)]

        # wrapped grid targets in same format
        # start at grid-bottom
        gridindicies = [(-wrap_height, gridrowmax, 0, gridcolmax),
                        # grid-top
                        (0, wrap_height, 0, gridcolmax),
                        # grid-right
                        (0, gridrowmax, -wrap_width, gridcolmax),
                        # grid-left
                        (0, gridrowmax, 0, wrap_width),
                        # grid-bottomright
                        (-wrap_height, gridrowmax, -wrap_width, gridcolmax),
                        # grid-bottomleft
                        (-wrap_height, gridrowmax, 0, wrap_width),
                        # grid-topright
                        (0, wrap_height, -wrap_width, gridcolmax),
                        # grid-topleft
                        (0, wrap_height, 0, wrap_width)]

        return wrapindicies, gridindicies

    def refresh_wrap(self):
        """ Update the wrapping border of the grid to reflect any changes """
        # if wrap false set to default non wrap state (-100)
        wrap = self.ca_config.wrap
        if type(wrap) is bool and wrap is False:
            wrap = -100
        # Normal wrapping behaviour
        if type(wrap) is bool and wrap is True:
            # set the wrap to the oppostite cell bank of the grid
            for w, g in zip(self.wrapindicies, self.gridindicies):
                gridsection = self.grid[g[0]:g[1], g[2]:g[3]]
                self.wrapping_grid[w[0]:w[1], w[2]:w[3]] = gridsection
        elif type(wrap) is int or type(wrap) is float:
            # User specified dead state to surround the grid
            for w in self.wrapindicies:
                self.wrapping_grid[w[0]:w[1], w[2]:w[3]] = wrap
        else:
            sys.exit("Invalid wrap {} of type {}".format(wrap, type(wrap)))

    def get_neighbour_states(self, applyneighbourhood=True):
        """Return the 8 arrays of each neighbours current state"""
        grid = self.wrapping_grid
        if applyneighbourhood:
            nhood_arr = self.neighbourhood.neighbourhood
        else:
            nhood_arr = np.ones((3, 3))
        # Return the NW N NE, W self E, SW S SE neighbourgrids
        nw = nhood_arr[0, 0] * grid[0:-2, 0:-2]
        n = nhood_arr[0, 1] * grid[0:-2, 1:-1]
        ne = nhood_arr[0, 2] * grid[0:-2, 2:]
        w = nhood_arr[1, 0] * grid[1:-1, 0:-2]
        e = nhood_arr[1, 2] * grid[1:-1, 2:]
        sw = nhood_arr[2, 0] * grid[2:, 0:-2]
        s = nhood_arr[2, 1] * grid[2:, 1:-1]
        se = nhood_arr[2, 2] * grid[2:, 2:]
        return np.array([nw, n, ne, w, e, sw, s, se])

    def count_neighbours(self, neighbour_states):
        """
        Taking the 8 neighbour arrays, return n arrays of how many
        neighbours of each state each cell are in each state,
        where n is the number of states
        """
        states = self.ca_config.states
        # create variable to store the counts for each state
        state_counts = np.zeros(len(states), dtype=np.ndarray)
        for i, state in enumerate(states):
            # for each state in the CA
            countg = np.zeros(self.grid.shape)
            for g in neighbour_states:
                # for each neighbour array add the cells in the queried state
                countg += (g == state) + 0
            # save the total counts for this state
            state_counts[i] = countg
        return state_counts

    def step(self):
        """ Calculate the next timestep by applying the transistion function
        and save the new state to grid """
        # collect the 8 arrays of neighbour states
        ns = self.get_neighbour_states()
        # calculate the number of neighbours each cell has of each state
        # return n arrays where n is the number of states
        nc = self.count_neighbours(ns)

        # apply the user's transition function
        # passing in the states and counts to allow complex rules
        # if the user supplied any addition arguments, pass them here
        if self.additional_args is None:
            self.grid = self.transition_func(self.grid, ns, nc)
        else:
            self.grid = self.transition_func(self.grid, ns, nc,
                                             *self.additional_args)
        # refresh wrapping border
        self.refresh_wrap()


def randomise2d(grid, background_state, proportions):
    """ Takes a grid, the background state, and
    proportions for each state in a list of tuples ([(1,0.4), (2,0.3)]) """
    grid[:, :] = background_state
    numcells_per_state = np.zeros(len(proportions), dtype=int)
    for i, p in enumerate(proportions):
        proportion = clip_numeric(p[1], 0, 1)
        numcells_per_state[i] = int(proportion * grid.size)
    randindicies = np.random.choice(grid.size, np.sum(numcells_per_state),
                                    replace=False)
    g = np.copy(grid).reshape(grid.size)
    used = 0
    for i, p in enumerate(proportions):
        state = p[0]
        indicies = randindicies[used:numcells_per_state[i]]
        g[indicies] = state
        used += numcells_per_state[i]

    return g.reshape(grid.shape)
