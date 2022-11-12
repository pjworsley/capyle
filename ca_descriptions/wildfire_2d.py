# Name: Conway's game of life
# Dimensions: 2

# --- Set up executable path, do not edit ---
import sys
import inspect
this_file_loc = (inspect.stack()[0][1])
main_dir_loc = this_file_loc[:this_file_loc.index('ca_descriptions')]
sys.path.append(main_dir_loc)
sys.path.append(main_dir_loc + 'capyle')
sys.path.append(main_dir_loc + 'capyle/ca')
sys.path.append(main_dir_loc + 'capyle/guicomponents')
# ---

from capyle.ca import Grid2D, Neighbourhood, CAConfig, randomise2d
import capyle.utils as utils
import numpy as np

# constants
P_0 = 0.58
P_W = 1.0
P_VEG = 0.3

# P_VEG = {'chaparral': 0.2, 'canyon': 0.4, 'forest': -0.3, 'lake': -1.0}

def transition_func(grid, neighbourstates, neighbourcounts):
    # with fuel but not burning = state == 0, burning = state == 1, completely burned = state = 2

    # if a cell is burning (state 1), it will be completely burned down (state 2) in the next timestep
    cells_in_state_1 = (grid == 1)
    grid[cells_in_state_1] = 2

    # if at least one nearest-neighbour of a cell is burning (state 1) then catch fire with probability Pburn,
    # (TO ADD LATER!!!) if more than one neighbour is burning, sum Pburn probabilities from each neighbour
    p_burn = P_0 * (1 + P_VEG) * P_W
    probability_arr = np.random.rand(*grid.shape) < p_burn
    cells_in_state_0 = (grid == 0)
    at_least_one_burning_neighbour = (neighbourcounts[1] > 0)
    to_one = cells_in_state_0 & at_least_one_burning_neighbour & probability_arr
    grid[to_one] = 1

    return grid


def setup(args):
    config_path = args[0]
    config = utils.load(config_path)
    # ---THE CA MUST BE RELOADED IN THE GUI IF ANY OF THE BELOW ARE CHANGED---
    config.title = "Wildfire simulation"
    config.dimensions = 2
    config.states = (0, 1, 2)
    # ------------------------------------------------------------------------

    # ---- Override the defaults below (these may be changed at anytime) ----

    config.state_colors = [(0.9,0,0), (0,0.9,0), (0,0,0)]
    config.wrap = False
    # config.num_generations = 150
    # config.grid_dims = (100, 100)

    # ----------------------------------------------------------------------

    if len(args) == 2:
        config.save()
        sys.exit()

    return config


def main():
    # Open the config object
    config = setup(sys.argv[1:])

    # Create grid object
    grid = Grid2D(config, transition_func)

    # Run the CA, save grid state every generation to timeline
    timeline = grid.run()

    # save updated config to file
    config.save()
    # save timeline to file
    utils.save(timeline, config.timeline_path)


if __name__ == "__main__":
    main()
