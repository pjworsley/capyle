import sys
import pickle
import subprocess
import time
import platform
import os.path
import numpy as np


def prerun_ca(ca_config):
    """Run the setup function of a ca description and load the CAConfig

    Args:
        ca_config (CAConfig): The config object to be saved
            and passed to the CA file.
    Returns:
        CAConfig: The updated config after values have been updated
            while pre-running the ca description

    """
    ca_config.save()
    args = [sys.executable, ca_config.filepath, ca_config.path, '0']
    ca = subprocess.Popen(args, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    #  Collect both stdout and errors & decode to strings
    out_bytes, errors_bytes = ca.communicate()
    errors_str = errors_bytes.decode("utf-8")
    out_str = out_bytes.decode("utf-8")
    if errors_str != "":
        #  show print out and errors
        print('[ERROR] Error in CA description while prerunning')
        print(out_str)
        print(errors_str)
    else:
        #  show print out and reload ca_config
        if not out_str == '':
            print(out_str)
        ca_config = load(ca_config.path)
        ca_config.fill_in_defaults()
        return ca_config


def run_ca(ca_config):
    """Run the ca in a subprocess, saving the timestep to a timeline.
    This timeline is then saved to disk and loaded back in this process

    Args:
        ca_config (CAConfig): The config object to be saved
            and passed to the CA file.

    Returns:
        CAConfig: The updated config after values have been updated
            while pre-running the ca description
        numpy.ndarray: Array containing the grid state for each time step
    """
    ca_config.save()
    args = [sys.executable, ca_config.filepath, ca_config.path]
    ca = subprocess.Popen(args, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    out_bytes, errors_bytes = ca.communicate()
    errors_str = errors_bytes.decode("utf-8")
    out_str = out_bytes.decode("utf-8")

    if errors_str != "":
        #  close progress bar window early
        #  if error at runtime, show print out and errors
        print('[ERROR] Error in CA description while attempting to run CA')
        if not out_str == '':
            print(out_str)
        print(errors_str)
        return None, None
    else:
        #  show print out and reload timeline and ca_config
        if not out_str == '':
            print(out_str)
        ca_config = load(ca_config.path)
        timeline = load(ca_config.timeline_path)
        return ca_config, timeline


def verify_gens(num_gens):
    """Asssert that the number of generations is above 0"""
    if num_gens < 1:
        print("[PARAMETER INVALID] Invalid number of generations:" +
              "{gens}. Defaulting to 1 generation.".format(gens=num_gens))
        return 1
    return num_gens


def check_complexity_warning(num_gens, grid_dims=None):
    """Check the complexity of the computation and if above a threshold
    warn the user via stdout"""
    if grid_dims is None:
        if num_gens > 500:
            print("[WARNING] {gens} generations may take some time to run," +
                  " please be patient.".format(gens=num_gens))
    else:
        warning_threshold = 30000000
        complexity_score = grid_dims[0] * grid_dims[1] * num_gens
        if complexity_score > warning_threshold:
            print("[WARNING] {dim1}x{dim2} cells for {gens} generations may" +
                  " take some time to run, please be patient.".format(
                      dim1=grid_dims[0], dim2=grid_dims[1], gens=num_gens))


def gens_to_dims(gens):
    """Calculate the grid size of a 1D CA from number of generations

    Args:
        gens (int): the number of generations

    Returns:
        (int,int): the grid dimensions of the corresponding grid
    """
    # return (gens + 1, (gens + 1)* 2)
    return (gens + 1, (gens * 2 + 1))


def load(path):
    """Load a picked object from disk"""
    with open(path, 'rb') as input:
        p = pickle.load(input)
    return p


def save(obj, path):
    """Save an object to disk"""
    with open(path, 'wb') as output:
        pickle.dump(obj, output, -1)


def get_metadata(filepath):
    """Parse given description file and infer the dimensionality and title"""
    title, dimensions = None, None
    with open(filepath, 'r') as f:
        # find the values of name and dimensions from first few lines
        i = 0
        while title is None or dimensions is None:
            line = f.readline()
            if 'name' in line.lower():
                title = line[line.index(':')+1:].strip()
            elif 'dimensions' in line.lower():
                dimensions = int(line[line.index(':')+1:].strip())
            i += 1
            # if not in the first few lines,
            # then take best guess based on class called
            if i == 10:
                if 'Grid1D' in f.read():
                    dimensions = 1
                    title = 'Unamed 1D Automata'
                else:
                    dimensions = 2
                    title = 'Unamed 2D Automata'
    return title, dimensions


def clip_numeric(i, min, max):
    """Clip a numerical value between two values

    Note:
        Works with any numerical value int/float...

    Example:
        clip_numeric(5, 2, 6) -> 5
        clip_numeric(5, 6, 8) -> 6
        clip_numeric(5, -2, 3) -> 3
        clip_numeric(1.3, 2.111, 912321.123123) -> 2.111
    """
    if i > max:
        return max
    if i < min:
        return min
    return i


def is_valid_integer(x):
    """Tests if the supplied value is an or can be converted to an int

    Args:
        x: the variable in question

    Returns:
        bool: True indicates x can be safely converted to int"""
    if x == "":
        return True
    try:
        int(x)
    except:
        return False
    else:
        return True


def extract_states(timeline):
    """Given a timeline, extract the states that are present in the timeline

    Note:
        This is only used in extreme cases where we cannot find the states
        anywhere and simply have to have a guess.
    """
    uniques = []
    for i, t in enumerate(timeline):
        uniques.extend(np.unique(t))
    vals = np.unique(np.array(uniques))
    return vals


def rgb_to_hex(r, g, b):
    """Convert rgb components to the hex equivalent

    Example:
        (0, 0, 0) -> #000000
        (255, 255, 255) -> #FFFFFF
        (204, 79, 193) -> #CC4FC1
    """
    r, g, b = map((lambda x: int(x*255)), (r, g, b))
    return "#{r:02X}{g:02X}{b:02X}".format(r=r, g=g, b=b)


def scale_array(old, newrows, newcols):
    """Scale a 2D array to the given size, retainin as much data as possible

    Args:
        old (numpy.ndarray): The array to be scaled
        newrows (int): The new number of rows
        newcols (int): The new number of cols

    Returns:
        numpy.ndarray: The scaled array with information added/removed
    """
    oldrows, oldcols = old.shape
    new = np.empty((newrows, newcols))
    copyrows = oldrows if oldrows < newrows else newrows
    copycols = oldcols if oldcols < newcols else newcols

    new[:copyrows, :copycols] = old[:copyrows, :copycols]
    return new


def int_to_binary(n):
    """Convert an integer to an 8 bit binary array

    Note:
        Clipped to 0-255

    Args:
        n (int): The integer number to be converted

    Returns:
        numpy.ndarray: Array of binary integers

    Example:
        16 -> np.array([0,0,0,1,0,0,0,0])
        -1 -> np.array([0,0,0,0,0,0,0,0])
        1000 -> np.array([1,1,1,1,1,1,1,1])
    """
    n = int(n)
    n = clip_numeric(n, 0, 255)
    b = str(bin(n))[2:]
    b_str = (8-len(b))*"0" + b

    b_arr = np.array(list(b_str), dtype=int)
    return b_arr


def title_to_filename(s):
    """Remove spaces and invalid characters from a string"""
    disallowedchars = ['"', '.', '>', '<', ':', '|', '/', '\\',
                       '*', '?']
    # replace all spaces with underscores
    s = s.replace(' ', '_')
    for c in disallowedchars:
        # replace the above with nothing
        s = s.replace(c, '')
    return s


def screenshot(cagraph, catitle, path=None):
    """Take a screenshot of the supplied CAGraph and save to disk

    Args:
        cagraph (CAGraph): The graph object to screenshot
        catitle (str): The title of the CA
    """
    if path is None:
        screenshot_folder = sys.path[0] + "/screenshots/"
    else:
        if not path.endswith("/"):
            path += "/"
        screenshot_folder = path
    # check path exists
    if os.path.isdir(screenshot_folder):
        extension = ".png"
        i = 0
        title = title_to_filename(catitle)
        titletime = "{}_{}_".format(title, time.strftime("%Y-%m-%d_%H-%M-%S"))
        filename = titletime + str(i) + extension
        # if another screenshot was taken in the same second,
        # increase the numbering until one that is not used
        while os.path.isfile(screenshot_folder + filename):
            i += 1
            filename = titletime + str(i) + extension
        # save the unique filename
            filepath = screenshot_folder + filename
            cagraph.screenshot(filepath)
    else:
        filename = None

    return filename

def get_logo():
    os = platform.system()
    fn = ""
    if os == "Windows":
        fn = "capylewindows.gif"
    elif os == "Darwin":
        fn = "capylemacos.gif"
    else:
        fn = "capylelinux.gif"

    fp = sys.path[0] + "/icons/" + fn
    logo = tk.PhotoImage(file=fp)
    return logo


# The above functions are required before importing the remainder
from capyle.guicomponents.gui_utils import *
