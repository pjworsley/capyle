import sys
import inspect
# ---- Set up path to modules ----
this_file_loc = (inspect.stack()[0][1])
main_dir_loc = this_file_loc[:this_file_loc.index('main.py')]
sys.path.append(main_dir_loc)
sys.path.append(main_dir_loc + 'capyle')
sys.path.append(main_dir_loc + 'capyle/ca')
sys.path.append(main_dir_loc + 'capyle/guicomponents')

# import display
from capyle import Display


def main():
    """Initialise the GUI"""
    w = Display()

if __name__ == "__main__":
    main()
