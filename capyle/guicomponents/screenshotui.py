import sys
import tkinter as tk
from capyle.utils import screenshot, set_entry, get_dir_dialog


class _ScreenshotUI(tk.Frame):
    DEFAULT_PATH = sys.path[0] + "/screenshots/"

    def __init__(self, parent):
        tk.Frame.__init__(self, parent)
        self.ca_graph = None
        self.title = None

        pathframe = tk.Frame(self)
        # entry label
        tk.Label(pathframe, text="Save to:").pack(side=tk.LEFT)
        # entry
        self.path_entry = tk.Entry(pathframe, width=40)
        self.path_entry.pack(side=tk.LEFT)
        # set to default
        set_entry(self.path_entry, self.DEFAULT_PATH)
        # browse button
        tk.Button(pathframe, text="Browse", command=self.askdir).pack()
        pathframe.pack()

        self.l_saved = tk.Label(self, text="")
        self.l_saved.pack()

        btn_take = tk.Button(self, text="Take screenshot",
                             command=self.take)
        btn_take.pack()

        self.uielements = [btn_take]

        self.disable()

    def askdir(self):
        dirpath = get_dir_dialog(self.getdir())
        if not dirpath == "":
            set_entry(self.path_entry, dirpath)

    def getdir(self):
        return self.path_entry.get()

    def disable(self):
        for e in self.uielements:
            e.config(state=tk.DISABLED)

    def enable(self):
        if self.ca_graph is not None and self.title is not None:
            for e in self.uielements:
                e.config(state=tk.NORMAL)

    def set(self, graph, title):
        self.title = title
        self.ca_graph = graph

    def take(self):
        if self.ca_graph is not None:
            filename = screenshot(self.ca_graph, self.title, self.getdir())
            if filename is not None:
                msg = "Saved to: " + filename
            else:
                msg = "Error supplied path does not exist."
            self.l_saved.config(text=msg)
