import os
import sys
import matplotlib
matplotlib.use('TkAgg')
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from matplotlib import colors
from matplotlib import pyplot as plt
import numpy as np

class _CAGraph(object):
    # increase for high res displays
    GRAPH_SIZE = [8, 8]

    def __init__(self, data, states, sequence=False, placeholder=False):
        """Create a matplotlib graph within a tkinter canvas"""
        # get grid size from file
        try:
            with open(sys.path[0] + "/config.txt", "r") as f:
                for line in f:
                    l = line.split("=")
                    if l[0] == "graph":
                        size = int(l[1].strip())
                custom_size = size, size
        except:
            custom_size = self.GRAPH_SIZE

        if placeholder:
            self.fig = plt.Figure(frameon=False)
        else:
            if sequence:
                self.timeline = data
                data = self.timeline[0]
            self.fig = plt.Figure(frameon=False)
            self.fig.set_size_inches(custom_size)
            ax = self.fig.add_axes([0, 0, 1, 1])
            ax.axis('off')
            self.mat = ax.matshow(data, cmap='gray', interpolation='none',
                                  vmin=states[0], vmax=states[-1])

    def clear(self):
        """Clear the graph"""
        self.fig.clf()

    def update(self, i):
        """Set the graph data to be the timepoint specified"""
        self.mat.set_data(self.timeline[i])

    def setdata(self, data):
        """Set the data displayed on the graph"""
        self.mat.set_data(data)

    def refresh(self):
        """Redraw the graph"""
        self.fig.canvas.draw()

    def set_colormap(self, cmap_ls):
        """Set the colormap of the matplotlib graph"""
        cm = colors.LinearSegmentedColormap.from_list(
            'Custom', cmap_ls, N=len(cmap_ls))
        self.mat.set_cmap(cm)
        self.refresh()

    def screenshot(self, filepath):
        """Save an image of the current graph display"""
        self.fig.savefig(filepath, bbox_inches='tight')
