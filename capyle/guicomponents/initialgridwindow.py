import tkinter as tk
import tkinter.font as tkFont
import numpy as np
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from capyle.ca import randomise1d, randomise2d
from capyle.utils import rgb_to_hex, clip_numeric, scale_array
from capyle.utils import set_icon, set_entry, clear_entry
from capyle.guicomponents import _Separator, _CAGraph


class _EditInitialGridWindow(tk.Toplevel):

    def __init__(self, ca_config, proportions=False, custom=False):
        # superclass
        tk.Toplevel.__init__(self)

        set_icon(self)

        self.configframe = None
        self.update_config(ca_config)

        # 1d check
        if self.ca_config.dimensions == 1:
            self.grid = np.empty((1, self.ca_config.grid_dims[1]))
        else:
            self.grid = np.empty(self.ca_config.grid_dims)
        self.grid.fill(self.ca_config.states[0])

        # Display each colour on the grid to
        # initialise the colormap correctly
        # it is reset after the graph has been created
        for i, state in enumerate(self.ca_config.states):
            self.grid[0, i] = state

        # title
        titleframe = tk.Frame(self)
        title_font = tkFont.Font(titleframe, family="Helvetica",
                                 size=18, weight=tkFont.BOLD)
        mode = 'proportions' if proportions else 'custom'
        titletxt = 'Initial configuraion editor - {mode}'.format(mode=mode)
        title = tk.Label(titleframe, text=titletxt, font=title_font)
        title.pack(side=tk.LEFT)
        titleframe.pack(fill=tk.BOTH)

        # Add the graph frame
        rframe = tk.Frame(self)
        graphframe = tk.Frame(rframe, width=400, height=400)
        self.add_graph(graphframe, mode)
        graphframe.pack()

        # hover coords label
        self.coords = tk.Label(rframe, text="[0, 0]")
        self.coords.pack()
        rframe.pack(side=tk.RIGHT)

        # Init the config frame for sidebar
        self.configframe = _ConfigFrame(self, self.ca_config,
                                       proportions=proportions, custom=custom)
        self.configframe.pack(side=tk.LEFT, fill=tk.BOTH, expand=tk.YES)

    def get_initial_grid(self):
        if self.ca_config.dimensions == 2:
            return self.ca_config.initial_grid
        return np.array([self.ca_config.initial_grid[0, :]])

    def update_config(self, ca_config):
        self.ca_config = ca_config
        if self.configframe is not None:
            self.configframe.update_config(ca_config)

    def add_graph(self, parent, mode):
        """Add a _CAGraph object to the window"""
        self.graph = _CAGraph(self.grid, self.ca_config.states)

        self.ca_canvas = FigureCanvasTkAgg(self.graph.fig, master=parent)
        if mode == 'custom':
            self.graph.fig.canvas.mpl_connect("button_press_event",
                                              self.onaxesclick)
        self.graph.fig.canvas.mpl_connect("motion_notify_event",
                                          self.onaxeshover)

        parent.config(bd=5, relief=tk.GROOVE)
        self.ca_canvas.get_tk_widget().pack(padx=10, pady=10)
        self.graph.set_colormap(self.ca_config.state_colors)

    def graphset(self, grid=None, close=False):
        if grid is None:
            grid = self.grid
        else:
            self.grid = grid
        self.ca_config.set_initial_grid(grid)
        self.graph.setdata(grid)
        self.graph.refresh()
        if close:
            self.close()

    def createproportionalgrid(self, background, proportions):
        if self.ca_config.dimensions == 2:
            self.grid = randomise2d(self.grid, background, proportions)
        else:
            self.grid = np.array([randomise1d(self.grid,
                                              background, proportions)[0]])
        return self.grid

    def onaxeshover(self, event):
        """Display the cell index currently being hovered on the graph"""
        row = None
        col = None
        if event.inaxes is not None:
            row, col = self.get_graph_indices(event)
        else:
            row, col = 0, 0
        self.coords.config(text="[{}, {}]".format(row, col))
        
    def get_graph_indices(self, event):
        """Translate mouse position on graph to indicies in grid"""
        col = clip_numeric(int(event.xdata + 0.5),
                           0, self.ca_config.grid_dims[1] - 1)
        row = clip_numeric(int(event.ydata + 0.5),
                           0, self.ca_config.grid_dims[0] - 1)
        return row, col

    def onaxesclick(self, event):
        """Set the state of the cell clicked to the selected state"""
        if event.inaxes is not None:
            row, col = self.get_graph_indices(event) 
            state = self.ca_config.states[
                self.configframe.selected_state_index.get()]

            self.grid[row, col] = state
            self.graphset()
            self.graph.refresh()

    def close(self):
        self.destroy()


class _ConfigFrame(tk.Frame):

    def __init__(self, parent, ca_config, proportions=False, custom=False):
        # superclass frame
        tk.Frame.__init__(self, parent, width=200, height=400)

        self.parent = parent
        # update the config object handle
        self.update_config(ca_config)
        # set the mode of the window
        self.mode = 'proportions' if proportions else 'custom'
        # add the dropdown for background state
        self.add_backgroundselect(parent=self)

        _Separator(self).pack(fill=tk.BOTH, padx=5, pady=10)

        # Add the appropriate state
        if proportions:
            self.add_proportions(parent=self)
        else:
            self.add_paint_states(parent=self)

        self.set_default()

        # set the exit command for when the save and close is clicked
        if custom:
            exit_var = self.parent.graphset
        else:
            exit_var = self.apply_proportions

        btn_save = tk.Button(self, text="Save and close",
                             command=lambda: exit_var(close=True))
        btn_save.pack(side=tk.BOTTOM)

    def update_config(self, ca_config):
        """Reassign the ca_config object with an updated version"""
        self.ca_config = ca_config
        self.options = self.ca_config.states

    def add_backgroundselect(self, parent):
        """Dropdown menu to select the background state in either case"""
        backgroundframe = tk.Frame(parent)

        label = tk.Label(backgroundframe, text="Background state")
        label.pack(side=tk.LEFT)

        self.options = self.ca_config.states
        self.optvar = tk.StringVar(backgroundframe)
        self.optvar.set(self.options[0])

        opt_background = tk.OptionMenu(backgroundframe, self.optvar,
                                       *self.options, command=self.onchange)
        opt_background.pack()
        backgroundframe.pack(fill=tk.BOTH)

    def calc_proportions(self, grid):
        """Calculate the proportions from the current graph"""
        proportions = np.empty((len(self.ca_config.states)), dtype=tuple)
        for i, state in enumerate(self.ca_config.states):
            b = (grid == state)
            count = np.count_nonzero(b)
            total = grid.size
            proportions[i] = int(round(count/total, 2) * 100)
        return proportions

    def colorindicator(self, parent, size, color):
        """Generate a coloured square"""
        return tk.Canvas(parent, width=size, height=size, relief=tk.RAISED,
                         bd=2, background=color)

    def add_proportions(self, parent):
        """Add the state label, color indicator and entries for each state"""
        INDICATORSIZE = 20
        self.proportionentries = []

        titleframe = tk.Frame(parent)
        tk.Label(titleframe, text="Proportion of states").pack(side=tk.LEFT)
        titleframe.pack(fill=tk.BOTH)

        container = tk.Frame(parent)
        for i, state in enumerate(self.ca_config.states):
            frame = tk.Frame(container)
            # label
            label = tk.Label(frame, text=state)
            label.pack(side=tk.LEFT)
            # color indicator
            color = rgb_to_hex(*self.ca_config.state_colors[i])
            colorindicator = self.colorindicator(frame, INDICATORSIZE, color)
            colorindicator.pack(side=tk.LEFT)
            # entry
            entryvar = tk.StringVar(frame)
            entry = tk.Entry(frame, width=3, textvariable=entryvar)
            entry.pack(side=tk.LEFT)
            entry_label = tk.Label(frame, text='%')

            # disable the background state entry
            if str(state) == self.optvar.get():
                entry.config(state=tk.DISABLED)

            # keep handle on the entry
            self.proportionentries.append(entry)
            entry_label.pack(side=tk.LEFT)
            frame.pack(fill=tk.BOTH)
        btn_apply = tk.Button(container, text="Apply",
                              command=self.apply_proportions)
        btn_apply.pack()
        container.pack()

    def add_paint_states(self, parent):
        """Add the state label, color and radiobuttons for each state"""
        INDICATORSIZE = 20

        titleframe = tk.Frame(parent)
        tk.Label(titleframe, text="State selection").pack(side=tk.LEFT)
        titleframe.pack(fill=tk.BOTH)

        self.selected_state_index = tk.IntVar()
        self.radio_states = []

        # outer container for the options
        container = tk.Frame(parent)
        # Add the label, radio button and color for each state
        for i, state in enumerate(self.ca_config.states):
            frame = tk.Frame(container)
            label = tk.Label(frame, text=state)
            label.pack(side=tk.LEFT)
            color = rgb_to_hex(*self.ca_config.state_colors[i])
            color_indicator = self.colorindicator(frame, INDICATORSIZE, color)
            color_indicator.pack(side=tk.LEFT)

            rdo_select = tk.Radiobutton(frame, text="",
                                        variable=self.selected_state_index,
                                        value=i)
            self.radio_states.append(rdo_select)
            rdo_select.pack(side=tk.LEFT)
            frame.pack(fill=tk.BOTH)
        container.pack()

    def onchange(self, event):
        selected = int(event)
        if self.mode == 'proportions':
            for i, e in enumerate(self.proportionentries):
                if i == selected:
                    clear_entry(e)
                    e.config(state=tk.DISABLED)
                else:
                    e.config(state=tk.NORMAL)
                    if e.get() == "":
                        set_entry(e, 0)
            self.apply_proportions()
        else:
            self.parent.createproportionalgrid(self.background_state(), [])
            self.parent.graphset()

    def apply_proportions(self, close=False):
        self.parent.createproportionalgrid(self.background_state(),
                                           self.proportions())
        self.parent.graphset()
        if close:
            self.parent.close()

    def background_state(self):
        state = self.optvar.get()
        return type(self.ca_config.states[0])(state)

    def proportions(self):
        proportions = np.empty((len(self.ca_config.states)), dtype=tuple)
        for i, e in enumerate(self.proportionentries):
            val = float(e.get()) if not e.get() == '' else 0
            proportions[i] = (self.ca_config.states[i], round(val/100, 2))
        return proportions

    def set_default(self):
        self.parent.grid = self.parent.get_initial_grid()
        self.optvar.set(self.options[0])
        if self.mode == 'proportions':
            proportions = self.calc_proportions(self.parent.grid)
            for i, e in enumerate(self.proportionentries):
                set_entry(e, proportions[i])
        else:
            self.selected_state_index.set(0)
        self.parent.graphset()
