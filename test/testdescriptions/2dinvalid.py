# Name: Example 2D CA
# Dimensions: 2

# --- Set up executable path, do not edit ---
import sys, inspect
this_file_loc = (inspect.stack()[0][1])
main_dir_loc = this_file_loc[:this_file_loc.index('test/testdescriptions')]
sys.path.append(main_dir_loc)
sys.path.append(main_dir_loc + 'capyle')
sys.path.append(main_dir_loc + 'capyle/ca')
sys.path.append(main_dir_loc + 'capyle/guicomponents')
# ---

from capyle.ca import Grid2D, Neighbourhood, CAConfig, randomise2d
import capyle.utils as utils

def transition_func(grid, neighbour_counts):
    dead_neighbours, live_neighbours = neighbour_counts
    #create boolean arrays for the birth & survival rules
    # if 3 live neighbours and is dead -> cell born
    birth = (live_neighbours == 3) & (grid == 0)
    # if 2 or 3 live neighbours and is alive -> survives
    survive = ((live_neighbours == 2) | (live_neighbours == 3)) & (grid == 1)
    # Set all cells to zero
    grid[:,:] = 0
    # Set cells to 1 where either cell is born or survives
    grid[birth | survive] = 1
    return grid

def setup(args):
    config_path = args[0]
    config = utils.load(config_path)
    # --- THE CA MUST BE RELOADED IN THE GUI IF ANY OF THE BELOW ARE CHANGED ---
    config.title = "Example 2D CA"
    config.dimensions = 2
    config.states = (0,1)
    # --------------------------------------------------------------------------

    # ---- Override the defaults below (these may be changed at anytime) ----
    
    # config.state_colors = [(0,0,0),(1,1,1)]
    # config.num_generations = 150
    # config.grid_dims = (200,200)

    # ----------------------------------------------------------------------

    if len(args) == 2:
        config.save()
        sys.exit()

    return config

def main():
    #take the config path
    config = setup(sys.argv[1:])

    #Create grid object
    grid = Grid2D(
        gridsize=config.grid_dims,
        states=config.states,
        neighbourhood=config.neighbourhood(),
        transition_func=transition_func,
        initial_grid=config.initial_grid)

    #Run the CA, save grid state every generation to timeline
    timeline = grid.run(config.num_generations)

    #save updated config to file
    config.save()
    #save timeline to file
    utils.save(timeline, config.timeline_path)

if __name__ == "__main__":
    main()
