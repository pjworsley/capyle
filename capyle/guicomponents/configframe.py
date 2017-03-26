import tkinter as tk
import numpy as np
from capyle.utils import gens_to_dims, alerterror, alertcontinue
from capyle.guicomponents import (_GenerationsUI, _GridDimensionsUI,
                                  _Separator, _NeighbourhoodUI, _RuleNumberUI,
                                  _StateColorsUI, _InitialGridUI)


class _ConfigFrame(tk.Frame):

    def __init__(self, parent, ca_config):
        tk.Frame.__init__(self, parent, padx=10)
        self.ca_config = ca_config
        self.ca_graph = None

        btn_reset = tk.Button(self, text="Reset configuration",
                              command=self.reset)
        btn_reset.pack()

        self.separator()

        if self.ca_config.dimensions == 2:
            self.griddims_entry = _GridDimensionsUI(self)
            self.griddims_entry.pack(fill=tk.BOTH)
        else:
            self.rulenum_entry = _RuleNumberUI(self)
            self.rulenum_entry.pack(fill=tk.BOTH)

        self.separator()

        # Gererations
        self.generations_entry = _GenerationsUI(self)
        self.generations_entry.pack(fill=tk.BOTH)

        self.separator()

        # Neighbourhood selector gui
        self.nhood_select = _NeighbourhoodUI(self, self.ca_config.dimensions)
        self.nhood_select.pack(fill=tk.BOTH)

        self.separator()

        # initial grid config options
        self.init_grid = _InitialGridUI(self, self.ca_config)
        self.init_grid.pack(fill=tk.BOTH)

        self.separator()

        # Colour selector
        self.state_colors = _StateColorsUI(self, self.ca_config, self.ca_graph)
        self.state_colors.pack(fill=tk.BOTH)

        self.separator()

        # refresh the frame and graph
        self.update(self.ca_config, self.ca_graph)

    def separator(self):
        """Generate a separator"""
        return _Separator(self).pack(fill=tk.BOTH, padx=5, pady=10)

    def reset(self):
        """Reset all options to software defaults"""
        if self.ca_config.dimensions == 2:
            self.griddims_entry.set_default()
        else:
            self.rulenum_entry.set_default()
        self.generations_entry.set_default()
        self.nhood_select.set_default()

    def get_config(self, ca_config, validate=False):
        """Get the config from the UI and store in a CAConfig object"""
        ca_config.num_generations = self.generations_entry.get_value()
        ca_config.state_colors = self.state_colors.get_value()

        if ca_config.dimensions == 2:
            ca_config.grid_dims = self.griddims_entry.get_value()
            ca_config.nhood_arr = self.nhood_select.get_value() + 0
        else:
            ca_config.rule_num = self.rulenum_entry.get_value()
            ca_config.nhood_arr = self.nhood_select.get_value()[0] + 0
            centercell = (self.init_grid.selected.get() == 2)
            if centercell:
                ca_config.grid_dims = gens_to_dims(ca_config.num_generations)
                ca_config.initial_grid = np.zeros(ca_config.grid_dims)
                ig = self.__center_cell_set(ca_config.grid_dims,
                                            ca_config.states[-1])
                ca_config.set_initial_grid(ig)

        if not validate:
            return ca_config
        else:
            return self.__validate_and_warn(ca_config)

    def __center_cell_set(self, dims, state):
        new_row = np.zeros((1, dims[1]))
        center = dims[1]//2
        new_row[0, center] = state
        return new_row

    def __validate_and_warn(self, ca_config):
        """Validate the CAConfig object against criteria"""
        errcheck = self.__error_cases(ca_config)
        if errcheck is not None:
            alerterror(*errcheck)
            return ca_config, False

        # If complex task ask if user wishes to proceed
        proceedcheck = self.__ask_proceed_cases(ca_config)
        return ca_config, proceedcheck

    def __error_cases(self, ca_config):
        if ca_config.dimensions == 1:
            if ca_config.rule_num < 0 or ca_config.rule_num > 255:
                s = "Only 0-255 valid, {val} supplied"
                return "Rule number", s.format(val=config.rule_num)

        if ca_config.dimensions == 2:
            if ca_config.grid_dims[0] < 3 or ca_config.grid_dims[1] < 3:
                s = "One or both of the grid dimensions is too small {d}"
                return ("Grid dimensions", s.format(d=ca_config.grid_dims))

        if ca_config.num_generations < 1:
            s = "Invalid value {val} supplied"
            return "Generations", s.format(val=config.num_generations)
        return None

    def __ask_proceed_cases(self, ca_config):
        complexity_val = (ca_config.num_generations * ca_config.grid_dims[0] *
                          ca_config.grid_dims[1])
        if complexity_val > 30000000:
            s = ("The combination of grid dims {d} and {x} generations may" +
                 " take a long time to run. Do you wish to continue?")
            s = s.format(d=ca_config.grid_dims, x=ca_config.num_generations)
            complexitycheck = alertcontinue("Complexity warning!", s)
            return complexitycheck
        return True

    def update(self, ca_config, ca_graph):
        self.ca_config = ca_config
        self.ca_graph = ca_graph
        if ca_config.dimensions == 2:
            self.griddims_entry.set(self.griddims_entry.COLS,
                                    self.ca_config.grid_dims[0])
            self.griddims_entry.set(self.griddims_entry.ROWS,
                                    self.ca_config.grid_dims[1])
        else:
            self.rulenum_entry.set(ca_config.rule_num)
        self.nhood_select.set(self.ca_config.nhood_arr)
        self.generations_entry.set(self.ca_config.num_generations)
        self.init_grid.update_config(self.ca_config)
        self.state_colors.update(self.ca_config, ca_graph)
