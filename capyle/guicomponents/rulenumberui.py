import tkinter as tk
from capyle.guicomponents import _ConfigUIComponent
from capyle.utils import is_valid_integer


class _RuleNumberUI(tk.Frame, _ConfigUIComponent):
    DEFAULT = 0

    def __init__(self, parent):
        tk.Frame.__init__(self, parent)
        _ConfigUIComponent.__init__(self)
        label = tk.Label(self, text="Rule number:")
        label.pack(side=tk.LEFT)
        is_valid_int = (self.register(is_valid_integer), '%P')
        self.num_entry = tk.Entry(self, validate='key',
                                  validatecommand=is_valid_int, width=4)
        self.num_entry.pack(side=tk.LEFT)
        self.set_default()

    def get_value(self):
        x = self.num_entry.get()
        if x == '':
            x = 0
        return int(x)

    def set_default(self):
        self.set(0)

    def set(self, val):
        super(_RuleNumberUI, self).set(self.num_entry, val)
