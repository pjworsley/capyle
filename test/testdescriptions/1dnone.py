# --- Set up executable path, do not edit ---
import sys, inspect
this_file_loc = (inspect.stack()[0][1])
main_dir_loc = this_file_loc[:this_file_loc.index('testdescriptions')]
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

    if len(args) == 2:
        config.save()
        sys.exit()
    return config

def transition_function(grid, neighbourstates, rulebool):
        left, center, right = neighbourstates
        left = left == 1
        center = center == 1
        right = right == 1
        not_left, not_center, not_right = np.invert(left), np.invert(center), np.invert(right)

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
        for i in range(rule_application.shape[0] - 2):
            newrow += rule_application[i+1]
        return newrow

def main():
    config = setup(sys.argv[1:])

    rulebool = utils.int_to_binary(config.rule_num) * True

    grid = Grid1D(num_generations=config.num_generations, 
                  states=config.states,
                  neighbourhood=config.neighbourhood(),
                  transition_func=(transition_function, rulebool),
                  initial_grid=config.initial_grid)

    timeline = grid.run()
    utils.save(timeline, config.timeline_path)
    config.save()

if __name__ == "__main__":
    main()
