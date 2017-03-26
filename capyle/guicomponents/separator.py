import tkinter as tk


class _Separator(tk.Frame):
    """Make a horizontal line when packed"""
    def __init__(self, parent, border=True):
        if border:
            tk.Frame.__init__(self, parent, height=2, bd=1, relief=tk.SUNKEN)
        else:
            tk.Frame.__init__(self, parent, height=2, bd=1)
