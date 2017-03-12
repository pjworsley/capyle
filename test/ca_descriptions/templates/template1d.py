# Name: NAME
# Dimensions: 1

# --- Set up executable path, do not edit ---
import sys
import inspect
this_file_loc = (inspect.stack()[0][1])
main_dir_loc = this_file_loc[:this_file_loc.index('ca_descriptions')]
sys.path.append(main_dir_loc)
sys.path.append(main_dir_loc + 'capyle')
sys.path.append(main_dir_loc + 'capyle/ca')
sys.path.append(main_dir_loc + 'capyle/guicomponents')
# -------------------------------------------

from capyle.ca import Grid1D
import capyle.utils as utils


def setup(args):
    """Set up the config object used to interact with the GUI"""
    config_path = args[0]
    config = utils.load(config_path)
    # -- THE CA MUST BE RELOADED IN THE GUI IF ANY OF THE BELOW ARE CHANGED --
    config.title = "NAME"
    config.dimensions = 1
    config.states = STATES
    # ------------------------------------------------------------------------

    # ---- Override the defaults below (these may be changed at anytime) ----

    # config.state_colors = [(0,0,0),(1,1,1)]
    # config.num_generations = 100

    # ----------------------------------------------------------------------

    # the GUI calls this function to enter the user defined config
    # into the main system with an extra argument
    # do not change
    if len(args) == 2:
        config.save()
        sys.exit()
    # otherwise run as normal
    return config


def transition_function(grid, neighbourstates, neighbourcounts):
    """Function to apply the transition rules and
    return the new row of the next timestep"""
    # Placeholder
    newrow = grid[0]
    return newrow


def main():
    """ Main function that sets up, runs and saves CA"""
    # get the config object
    config = setup(sys.argv[1:])

    # create the grid
    grid = Grid1D(config, transition_function)

    # run the grid and save each timestep to timeline
    timeline = grid.run()
    # save timeline and config
    utils.save(timeline, config.timeline_path)
    config.save()

if __name__ == "__main__":
    main()
