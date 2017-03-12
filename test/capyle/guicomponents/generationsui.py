import tkinter as tk
from capyle.guicomponents import _ConfigUIComponent
from capyle.utils import is_valid_integer


class _GenerationsUI(tk.Frame, _ConfigUIComponent):
    DEFAULT = 100

    def __init__(self, parent):
        """Create and populate the generations ui"""
        tk.Frame.__init__(self, parent)
        _ConfigUIComponent.__init__(self)
        gen_label = tk.Label(self, text="Generations:")
        gen_label.pack(side=tk.LEFT)
        is_valid_int = (self.register(is_valid_integer), '%P')
        self.gen_entry = tk.Entry(self, validate='key',
                                  validatecommand=is_valid_int, width=4)
        self.set_default()
        self.gen_entry.pack(side=tk.LEFT)

    def get_value(self):
        x = self.gen_entry.get()
        if x == '':
            x = 0
        return int(x)

    def set_default(self):
        self.set(self.DEFAULT)

    def set(self, value):
        super(_GenerationsUI, self).set(entry=self.gen_entry, value=value)
