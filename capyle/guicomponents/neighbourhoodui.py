import tkinter as tk
from capyle.guicomponents import _ConfigUIComponent, _Separator
import numpy as np
from utils import clip_numeric


class _NeighbourhoodUI(tk.Frame, _ConfigUIComponent):

    def __init__(self, parent, dimensions):
        tk.Frame.__init__(self, parent)
        _ConfigUIComponent.__init__(self)
        # upper frame to hold title and dropdown box
        labelframe = tk.Frame(self)
        gen_label = tk.Label(labelframe, text='Neighbourhood:')
        gen_label.pack(side=tk.LEFT)

        if dimensions == 1:
            self.options = 'Default', 'Custom'
        else:
            self.options = 'Moore', 'Von Neumann', 'Custom'
        self.optvar = tk.StringVar(self)
        self.optvar.set(self.options[0])
        self.optvar.trace("w", self.callback)
        self.optbox = tk.OptionMenu(labelframe, self.optvar, *self.options)
        self.optbox.config(width=9)
        self.optbox.pack(side=tk.LEFT)
        labelframe.pack()

        # lower frame to hold the interactive selector
        selframe = tk.Frame(self)
        self.nhood_selector = _NeighbourhoodSelector(
            selframe, (self.optvar, self.options), dimensions)
        self.nhood_selector.pack()
        selframe.pack()

    def get_value(self):
        return self.nhood_selector.states

    def set_default(self):
        self.set(self.options[0].upper())

    def set(self, value):
        if type(value) is str:
            self.nhood_selector.set_preset(value)
        elif self.nhood_selector.is_preset(value) >= 0:
            i = self.nhood_selector.is_preset(value)
            self.set(self.options[i].upper())
        else:
            self.nhood_selector.set(value)

    def callback(self, *args):
        name = self.optvar.get().upper()
        if (name != self.options[-1].upper()):
            self.set(name)


class _NeighbourhoodSelector(tk.Canvas):
    WIDTH = 90
    HEIGHT = WIDTH
    MOORE = np.array([[True, True, True],
                      [True, True, True],
                      [True, True, True]])
    VONNEUMANN = np.array([[False, True, False],
                           [True, True, True],
                           [False, True, False]])
    WOLFRAM = np.array([[True, True, True]])
    PRESETS2D = MOORE, VONNEUMANN
    PRESETS1D = [WOLFRAM]

    def __init__(self, parent, optionmenu, dimensions):
        self.dimensions = dimensions
        if dimensions == 1:
            self.dimensions = 1
            arr_shape = (1, 3)
            self.HEIGHT = self.WIDTH//3
        else:
            arr_shape = (3, 3)

        tk.Canvas.__init__(self, parent, width=self.WIDTH,
                           height=self.HEIGHT, bd=-2)

        self.optbox, self.options = optionmenu

        self.cells = np.empty(arr_shape, dtype=int)
        self.states = np.empty(arr_shape, dtype=bool)
        self.states.fill(True)

        if dimensions == 1:
            self.draw_1D(offset=5)
        else:
            self.draw_2D(offset=5)

        self.itemconfig(self.cells[self.center_cell], fill="grey", width=0)
        # bind callback function for on click event
        self.bind("<Button-1>", self.callback)

    def draw_2D(self, offset):
        x, y = 0, 0
        self.cell_spacing = self.WIDTH//3
        for i in range(0, self.WIDTH, self.cell_spacing):
            for j in range(0, self.HEIGHT, self.cell_spacing):
                self.cells[y, x] = self.create_rectangle(
                    i+offset, j+offset, i+self.cell_spacing-offset,
                    j+self.cell_spacing-offset, fill="red", width=0)
                y += 1
            y = 0
            x += 1
            # draw grid lines
            if not i == 0:
                self.create_line(offset, i, self.WIDTH-offset, i)
                self.create_line(i, offset, i, self.HEIGHT-offset)
        # set center cell
        self.center_cell = 1, 1

    def draw_1D(self, offset):
        x = 0
        self.cell_spacing = self.WIDTH//3
        for i in range(0, self.WIDTH, self.cell_spacing):
            self.cells[0, x] = self.create_rectangle(
                i+offset, offset, i+self.cell_spacing-offset,
                self.cell_spacing-offset, fill="red", width=0)
            x += 1
            if not i == 0:
                self.create_line(i, offset, i, self.HEIGHT-offset)
        self.center_cell = 0, 1

    def callback(self, event):
        cell_indicies = self.coords_to_cell_indicies(self.canvasx(event.x),
                                                     self.canvasy(event.y))

        # Toggle color + state if not center cell
        if cell_indicies != self.center_cell:
            cell = self.cells[cell_indicies]
            # if cell 'on' then make white and turn 'off'
            if self.states[cell_indicies]:
                self.states[cell_indicies] = False
            else:
                self.states[cell_indicies] = True
            self.color_cell(cell_indicies)

            self.optbox.set(self.options[self.is_preset(self.states)])

    def coords_to_cell_indicies(self, x, y):
        bias = 1
        # coords flipped to represent the array indicies
        cell_coords = (int((y-bias)//self.cell_spacing),
                       int((x-bias)//self.cell_spacing))
        return self.clip_int_tuple(cell_coords, 0, 2)

    def clip_int_tuple(self, t, min, max):
        return clip_numeric(t[0], min, max), clip_numeric(t[1], min, max)

    def remove(self):
        self.pack_forget()

    def color_cell(self, indicies):
        color = "red" if self.states[indicies] else "white"
        self.itemconfig(self.cells[indicies], fill=color)

    def color_all_cells(self):
        # handles non 0 and 1 values with the below operation
        # (its not pointless I promise)
        states = self.states == True
        on_cells = self.cells[states]
        for cell in self.cells.reshape(self.cells.size):
            if cell in on_cells:
                self.itemconfig(cell, fill="red")
            else:
                self.itemconfig(cell, fill="white")
        self.itemconfig(self.cells[self.center_cell], fill="grey", width=0)

    def set_preset(self, name="MOORE"):
        if name == "MOORE":
            self.states = np.copy(self.MOORE)
        elif name == "VON NEUMANN":
            self.states = np.copy(self.VONNEUMANN)
        elif name == "DEFAULT":
            self.states = np.copy(self.WOLFRAM)
        self.color_all_cells()

    def set(self, a):
        arr = self.dimensions_check(a)
        warning = "Shape {} required for {} dimensions, {} given".format(
            self.states.shape, self.dimensions, arr.shape)
        assert arr.shape == self.states.shape, warning
        self.states = np.copy(arr)
        self.color_all_cells()
        self.optbox.set(self.options[self.is_preset(self.states)])

    def dimensions_check(self, arr):
        arr = np.array(arr)
        if arr.ndim == 1:
            return np.array([arr])
        return arr

    def is_preset(self, states):
        presets = self.PRESETS2D if (self.dimensions == 2) else self.PRESETS1D
        states = self.dimensions_check(states)
        states[self.center_cell] = True
        for i, preset in enumerate(presets):
            if np.array_equal(states, preset):
                return i
        return -1
