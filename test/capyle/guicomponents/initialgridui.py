import tkinter as tk
import numpy as np
from capyle.guicomponents import _ConfigUIComponent, _Separator
from capyle.guicomponents import _EditInitialGridWindow


class _InitialGridUI(tk.Frame, _ConfigUIComponent):

    def __init__(self, parent, ca_config):
        """UI element to customise the initial grid"""
        # superclasses
        tk.Frame.__init__(self, parent)
        _ConfigUIComponent.__init__(self)

        self.parent = parent
        self.ca_config = ca_config

        labelframe = tk.Frame(self)
        label = tk.Label(labelframe, text="Initial grid:")
        label.pack(side=tk.LEFT)
        labelframe.pack(fill=tk.BOTH)

        self.selected = tk.IntVar()
        optionsframe = tk.Frame(self)

        # Initial grid options
        # if 1d then add the center cell option
        rdo_centercell = None
        if self.ca_config.dimensions == 1:
            centerframe = tk.Frame(optionsframe)
            rdo_centercell = tk.Radiobutton(centerframe, text="Center cell",
                                            variable=self.selected, value=2,
                                            command=self.set_centercell)
            rdo_centercell.pack(side=tk.LEFT)
            centerframe.pack(fill=tk.BOTH)

        # proportions of states
        propframe = tk.Frame(optionsframe)
        rdo_proportions = tk.Radiobutton(propframe, text="% Initialised",
                                         variable=self.selected, value=0)
        btn_proportions = tk.Button(propframe, text="Edit", command=lambda:
                                    self.editinitgrid(proportions=True))
        rdo_proportions.pack(side=tk.LEFT)
        btn_proportions.pack(side=tk.LEFT)
        propframe.pack(fill=tk.BOTH)

        # custom specific cells
        customframe = tk.Frame(optionsframe)
        rdo_custom = tk.Radiobutton(customframe, text="Custom",
                                    variable=self.selected, value=1)
        btn_custom = tk.Button(customframe, text="Edit", command=lambda:
                               self.editinitgrid(custom=True))
        rdo_custom.pack(side=tk.LEFT)
        btn_custom.pack(side=tk.LEFT)
        customframe.pack(fill=tk.BOTH)
        optionsframe.pack()

        # keep handle on radio buttons
        self.radiobuttons = [rdo_proportions, rdo_custom, rdo_centercell]
        self.set_default()

    def update_config(self, ca_config):
        self.ca_config = ca_config

    def get_value(self):
        return int(self.selected)

    def set_default(self):
        """Set to default configuration"""
        if self.ca_config.dimensions == 2:
            # Proportions for 2D
            self.set(0)
        else:
            # Centercell for 1D
            self.set(2)
            self.set_centercell()

    def set(self, index):
        self.selected.set(index)

    def set_centercell(self):
        new_row = np.zeros((1, self.ca_config.grid_dims[1]))
        center = int(self.ca_config.grid_dims[1]/2)
        new_row[0, center] = 1
        self.ca_config.set_initial_grid(new_row)

    def editinitgrid(self, proportions=False, custom=False):
        args = proportions, custom
        if args[0] or args[1]:
            if self.ca_config.dimensions == 2:
                self.ca_config.set_grid_dims(
                    dims=self.parent.griddims_entry.get_value())
            else:
                self.ca_config.set_grid_dims(
                    num_generations=self.parent.generations_entry.get_value())
            self.selected.set(args.index(True))
            editwindow = _EditInitialGridWindow(self.ca_config, *args)
