import tkinter as tk
from capyle.guicomponents import _ConfigUIComponent
from capyle.utils import is_valid_integer


class _GridDimensionsUI(tk.Frame, _ConfigUIComponent):
    DEFAULT = 200
    ROWS = 'rows'
    COLS = 'cols'

    def __init__(self, parent):
        """Create and populate the grid dimensions UI"""
        tk.Frame.__init__(self, parent)
        _ConfigUIComponent.__init__(self)
        gen_label = tk.Label(self, text="Grid size")
        gen_label.pack(side=tk.TOP)
        is_valid_int = (self.register(is_valid_integer), '%P')

        self.cols_entry = tk.Entry(self, validate='key',
                                   validatecommand=is_valid_int, width=4)
        self.rows_entry = tk.Entry(self, validate='key',
                                   validatecommand=is_valid_int, width=4)

        cols_label = tk.Label(self, text="cols by")
        rows_label = tk.Label(self, text="rows")

        self.cols_entry.pack(side=tk.LEFT)
        cols_label.pack(side=tk.LEFT)
        self.rows_entry.pack(side=tk.LEFT)
        rows_label.pack(side=tk.LEFT)

        self.set_default()

    def get_value(self):
        r, c = self.cols_entry.get(), self.rows_entry.get()
        if r == '':
            r = 0
        if c == '':
            c = 0
        return int(r), int(c)

    def set_default(self):
        self.set(self.ROWS, self.DEFAULT)
        self.set(self.COLS, self.DEFAULT)

    def set(self, entryname, value):
        if entryname.lower() == 'rows':
            super(_GridDimensionsUI, self).set(self.rows_entry, value)
        elif entryname.lower() == 'cols':
            super(_GridDimensionsUI, self).set(self.cols_entry, value)

        else:
            print('Entry {name} not found'.format(name=entryname))
