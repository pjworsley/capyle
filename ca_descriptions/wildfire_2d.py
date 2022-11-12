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
P_VEG = {'chaparral': 0.2, 'canyon': 0.4, 'forest': -0.3, 'lake': -1.0}


def transition_func(grid, neighbourstates, neighbourcounts):
    # TODO:
    # - include burning time of each terrain type in the model
    # - increase p_burn probability depending on the number of burning neighbours
    # - implement wind effect
    # - refactor the code (for loop to calculate p_burn? separate function?)
    # - pre define state colors, grid size, grid state in the setup function

    # not burning terrain types:
    # 0 - chaparral
    # 1 - canyon
    # 2 - forest
    # 3 - lake
    # other:
    # 4 - burning
    # 5 - completely burned

    # if a cell is burning (state 4), it will be completely burned down (state 5) in the next timestep
    burning_cells = (grid == 4)

    # if at least one nearest-neighbour of a cell is burning (state 4) then catch fire with probability Pburn,
    at_least_one_burning_neighbour = (neighbourcounts[4] > 0)

    p_burn_chap = P_0 * (1 + P_VEG['chaparral']) * P_W
    p_burn_canyon = P_0 * (1 + P_VEG['canyon']) * P_W
    p_burn_forest = P_0 * (1 + P_VEG['forest']) * P_W
    p_burn_lake = P_0 * (1 + P_VEG['lake']) * P_W

    probability_arr_chap = np.random.rand(*grid.shape) < p_burn_chap
    probability_arr_can = np.random.rand(*grid.shape) < p_burn_canyon
    probability_arr_for = np.random.rand(*grid.shape) < p_burn_forest
    probability_arr_lake = np.random.rand(*grid.shape) < p_burn_lake

    chaparral_cells = (grid == 0)
    canyon_cells = (grid == 1)
    forest_cells = (grid == 2)
    lake_cells = (grid == 3)

    to_burning_state_chap = chaparral_cells & at_least_one_burning_neighbour & probability_arr_chap
    to_burning_state_can = canyon_cells & at_least_one_burning_neighbour & probability_arr_can
    to_burning_state_for = forest_cells & at_least_one_burning_neighbour & probability_arr_for
    to_burning_state_lake = lake_cells & at_least_one_burning_neighbour & probability_arr_lake

    grid[burning_cells] = 5
    grid[to_burning_state_chap] = 4
    grid[to_burning_state_can] = 4
    grid[to_burning_state_for] = 4
    grid[to_burning_state_lake] = 4

    return grid


def setup(args):
    config_path = args[0]
    config = utils.load(config_path)
    # ---THE CA MUST BE RELOADED IN THE GUI IF ANY OF THE BELOW ARE CHANGED---
    config.title = "Wildfire simulation"
    config.dimensions = 2
    config.states = (0, 1, 2, 3, 4, 5)
    # ------------------------------------------------------------------------

    # ---- Override the defaults below (these may be changed at anytime) ----

    #config.state_colors = [(0.9,0,0), (0,0.9,0), (0,0,0)]
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
