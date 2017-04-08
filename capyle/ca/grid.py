import numpy as np
from capyle.ca import Neighbourhood
from capyle.utils import scale_array, verify_gens
import tkinter as tk


class Grid(object):
    """Superclass to the Grid1D and Grid2D classes"""

    def __init__(self):
        pass

    def __str__(self):
        """toString function"""
        return np.array_str(self.grid)

    def step(self):
        """Enforce a step funciton in subclasses"""
        pass

    def set_grid(self, g):
        """Set self.grid to supplied grid, scaling the supplied grid
        if nessacary"""
        g = np.array(g)

        if g.shape[0] > 1:
            # 2d grid
            if not self.grid.shape == g.shape:
                g = scale_array(g, *self.grid.shape)
            self.grid[:, :] = g[:, :]
        else:
            # 1d grid
            if not self.grid.shape[1] == g.shape[1]:
                g = scale_array(g, g.shape[0], self.grid.shape[1])
            self.grid[0, :] = g[0]
        self.refresh_wrap()

    def set_neighbourhood(self, ca_config):
        """Sets self.neighbourhood with a Neighbourhood object
        from ca_config

        Args:
            ca_config (CAConfig): the config object with the
                neighbourhood array stored"""
        self.neighbourhood = ca_config.neighbourhood()
        if not (Neighbourhood is (self.neighbourhood.__class__)):
            self.neighbourhood = Neighbourhood(self.neighbourhood,
                                               dims=ca_config.dimensions)

    def run(self):
        """Set up running the CA for given generations,
        saving each timestep to an array 'timeline'

        Note:
            The actual running of the CA is done by the self.runca
            which is passed to the progress bar so that it can be
            updated

        Returns:
            numpy.ndarray: contains the grid state for each timestep
        """
        num_generations = verify_gens(self.ca_config.num_generations)
        timeline = np.empty(num_generations + 1, dtype=np.ndarray)
        # Progress window
        # pass in the run function and timeline to the progress bar
        # progress bar executes these
        gui = _ProgressWindow(num_generations, self._runca, timeline)
        return timeline

    def _runca(self, num_generations, progressbar, timeline):
        """Running the CA for given generations,
        saving each timestep to an array 'timeline'

        Note:
            This function is passed to the progress bar for it to execute
        """
        # save initial state
        timeline[0] = np.copy(self.grid)
        for i in range(num_generations):
            # calculate the next timestep and save it
            self.step()
            timeline[i+1] = np.copy(self.grid)
            # update the progress bar every 10 generations
            if (i+1) % 10 == 9:
                progressbar.set(i+1)


class _ProgressWindow(object):
    WINDOW_TITLE = 'Running...'
    MAX_WIDTH = 200
    HEIGHT = 20

    def __init__(self, maxval, run, timeline):
        """Create a progress bar window, and use the function 'run' to
        run the CA, update the variable timeline, and the progress gui

        Args:
            maxval (int): The number of generation to be run by the CA
            run (function): The run function that actuall executes the CA
            timeline (numpy.ndarray): the array object to save the grid state
                for each timestep
        """
        self.maxval = maxval
        self.root = tk.Tk()
        # set title
        self.root.wm_title(self.WINDOW_TITLE)
        # lift to top layer
        self.root.lift()
        self.root.attributes('-topmost', True)
        self.root.after_idle(self.root.attributes, '-topmost', False)
        #disable close
        self.root.protocol('WM_DELETE_WINDOW', self.noclose)

        self.progress_canvas = tk.Canvas(self.root,
                                         height=self.HEIGHT,
                                         width=self.MAX_WIDTH)
        bar = self.progress_canvas.create_rectangle(0, 0, 0,
                                                    self.HEIGHT, fill="blue")
        self.progress_canvas.pack()
        self.root.after(1, run(maxval, self, timeline))

    def noclose(self):
        pass

    def set(self, val):
        """Set the progress bar to the given generation number

        Args:
            val (int): The generation number (translated to a progress bar
                length)
        """
        if val >= self.maxval:
            self.root.destroy()
            return
        p = val/self.maxval
        w = int(p * self.MAX_WIDTH)
        self.progress_canvas.create_rectangle(0, 0, w, self.HEIGHT,
                                              fill="blue")
        self.root.update()
