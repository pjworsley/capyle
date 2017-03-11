#Name: Forest Fire
# --- Set up executable path, do not edit ---
import sys, inspect
import numpy as np

this_file_loc = (inspect.stack()[0][1])
main_dir_loc = this_file_loc[:this_file_loc.index('ca_descriptions')]
sys.path.append(main_dir_loc)
sys.path.append(main_dir_loc + 'capyle')
sys.path.append(main_dir_loc + 'capyle/ca')
sys.path.append(main_dir_loc + 'capyle/guicomponents')
# ---

from capyle.ca import Grid2D, Neighbourhood, CAConfig, randomise2d
import capyle.utils as utils

def setup(args):
    config_path = args[0]
    config = utils.load(config_path)
    # --- THE CA MUST BE RELOADED IN THE GUI IF ANY OF THE BELOW ARE CHANGED ---
    config.title = "Forest fire"
    config.dimensions = 2
    config.states = (0,1,2)
    # --------------------------------------------------------------------------

    # ---- Override the defaults below (these may be changed at anytime) ----

    config.state_colors = [(0.4,0.4,0.4),(0.0,1.0,0.0),(1,0.5,0)]
    config.grid_dims = (200,200)
    init_grid = np.zeros(config.grid_dims)
    init_grid.fill(1)
    init_grid[100,100] = 2
    config.initial_grid = init_grid

    # ----------------------------------------------------------------------

    if len(args) == 2:
        config.save()
        sys.exit()

    return config


def transition_func(grid, neighbourstates, neighbourcounts, fuel):
    # grid of random numbers between 0 and 1
    randgrid = np.random.rand(grid.shape[0], grid.shape[1])

    # influence of the nw, n, ne, e, w, sw, s, se neighbours
    influence = np.array([0.5, 0.5, 0.7, 0.5, 1, 0.7, 1, 1])

    # get the neighbour cells that are in state 2 (burning)
    burning_neighbours = (neighbourstates == 2)
    # apply the wind influence
    with_wind = (burning_neighbours * influence[:, None, None])

    # sum the 8 neighbours influences
    burning_score = np.zeros(grid.shape)
    for n in with_wind:
        burning_score = np.add(burning_score, n)

    # A cell will catch fire if:
    #  - The cell is currently on fire AND
    #  - The cell has at least one burning neighbour
    #    (the score increases as the number of on fire neighbours increases)
    #  - The burning score * random factor is greater than a threshold
    catchfire = (grid == 1) & ((burning_score * randgrid) > 0.7)

    # get the cells that are currently burning
    onfire = (grid == 2)
    # already on fire/caught fire have -1 taken off their fuel value
    fuel[onfire|catchfire] -= 1
    # get the cells that are burned out (fuel level 0)
    dead = (fuel == 0)
    # Set all cells to alive (clear the grid)
    grid[:,:] = 1
    # Set cells to 2 (on fire) where they are already alight or
    grid[onfire|catchfire] = 2
    # set already burned cells to dead
    grid[dead] = 0
    return grid


def main():
    #take the config path
    config = setup(sys.argv[1:])

    fuel = np.zeros(config.grid_dims)
    fuel.fill(10)
    #Create grid object
    grid = Grid2D(config, transition_func=(transition_func, fuel))

    #Run the CA, save grid state every generation to timeline
    timeline = grid.run()

    #save updated config to file
    config.save()
    #save timeline to file
    utils.save(timeline, config.timeline_path)

if __name__ == "__main__":
    main()
