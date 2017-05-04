# Name: Wolfram's 1D CA
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

import numpy as np
from capyle.ca import Grid1D
import capyle.utils as utils


def setup(args):
    config_path = args[0]
    config = utils.load(config_path)
    # ---THE CA MUST BE RELOADED IN THE GUI IF ANY OF THE BELOW ARE CHANGED---
    config.title = "Wolframs 1D CA"
    config.dimensions = 1
    config.states = (0, 1)
    # ------------------------------------------------------------------------

    # ---- Override the defaults below (these may be changed at anytime) ----
    config.wrap = True
    # config.state_colors = [(0,0,0),(1,1,1)]
    # config.num_generations = 100
    # config.grid_dims = (200,200)

    # ----------------------------------------------------------------------

    if len(args) == 2:
        config.save()
        sys.exit()
    return config


def transition_function(grid, neighbourstates, neighbourcounts, rulebool):
    left, center, right = neighbourstates
    left = left == 1
    center = center == 1
    right = right == 1
    not_left, not_center, not_right = (np.invert(left),
                                       np.invert(center),
                                       np.invert(right))
    rule_application = np.array([
        rulebool[0] & left     & center     & right,
        rulebool[1] & left     & center     & not_right,
        rulebool[2] & left     & not_center & right,
        rulebool[3] & left     & not_center & not_right,
        rulebool[4] & not_left & center     & right,
        rulebool[5] & not_left & center     & not_right,
        rulebool[6] & not_left & not_center & right,
        rulebool[7] & not_left & not_center & not_right,
        ])

    newrow = rule_application[0]
    for i in range(rule_application.shape[0] - 1):
        newrow += rule_application[i+1]
    return newrow


def main():
    config = setup(sys.argv[1:])

    # Translate rule numer to boolean array:
    # 30 -> [0,0,0,1,1,1,1,0] -> [F,F,F,T,T,T,T,F]
    rulebool = utils.int_to_binary(config.rule_num) * True

    # Create grid object
    # passing transition function and rulebool as tuple to
    # keep track of rulebool
    grid = Grid1D(config, (transition_function, rulebool))

    timeline = grid.run()
    utils.save(timeline, config.timeline_path)
    config.save()

if __name__ == "__main__":
    main()
