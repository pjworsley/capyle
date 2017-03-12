import tkinter as tk
from capyle.guicomponents import _ConfigUIComponent
from capyle.utils import rgb_to_hex
import numpy as np
from tkinter import colorchooser as cc


class _StateColorsUI(tk.Frame, _ConfigUIComponent):
    BLACK = (0, 0, 0), "#000000"
    WHITE = (1, 1, 1), "#FFFFFF"
    DEFAULTCOL = BLACK

    def __init__(self, parent, ca_config, ca_graph):
        tk.Frame.__init__(self, parent)
        _ConfigUIComponent.__init__(self)

        self.CANVASSIZE = 30

        self.ca_config = ca_config
        self.ca_graph = ca_graph
        self.states = ca_config.states
        self.canvas = np.empty((len(self.states)), dtype=object)

        if self.ca_config.state_colors is None:
            self.selected_colors = np.empty((len(self.states)), dtype=tuple)
            # if two states set one to black one to white
            if len(self.states) == 2:
                self.selected_colors[0] = self.BLACK[0]
                self.selected_colors[1] = self.WHITE[0]
            else:
                # Otherwise set all to black
                self.selected_colors.fill(self.DEFAULTCOL[0])
            self.ca_config.state_colors = self.selected_colors
        else:
            self.selected_colors = np.array(self.ca_config.state_colors,
                                            dtype=float)

        for i, state in enumerate(self.states):
            frame = tk.Frame(self)
            label = tk.Label(frame, text=state)
            self.canvas[i] = tk.Canvas(
                frame, height=self.CANVASSIZE, width=self.CANVASSIZE,
                background=rgb_to_hex(*self.selected_colors[i]),
                bd=2, relief=tk.RAISED)
            # bind the on mouse click function to the colored canvas
            self.canvas[i].bind(
                "<Button-1>", lambda e, i=i: self.onclick(e, i))
            label.pack(side=tk.LEFT)
            self.canvas[i].pack(side=tk.RIGHT)
            frame.pack()

    def get_value(self):
        return self.selected_colors

    def set_default(self):
        self.selected_colors.fill(self.DEFAULTCOL[0])

    def set(self, canvas, color, hex=True):
        if not hex:
            color = rgb_to_hex(*color)
        canvas.config(background=color)

    def onclick(self, event, i):
        selected_color = cc.askcolor()
        if selected_color[0] is not None:
            r, g, b = selected_color[0]
            r, g, b = (int(r)/255, int(g)/255, int(b)/255)

            self.selected_colors[i] = (r, g, b)
            self.ca_config.state_colors[i] = (r, g, b)
            self.set(event.widget, selected_color[1])
            self.set_colormap()

    def set_colormap(self):
        if self.ca_graph is not None:
            ls = self.selected_colors
            self.ca_graph.set_colormap(ls)

    def set_colors(self, colorlist):
        c = list(map((lambda x: list(map(lambda y: y*1.0, x))), colorlist))
        self.selected_colors = np.array(c)

    def update(self, ca_config, ca_graph):
        # update handles on config and graph objects
        self.ca_config = ca_config
        self.ca_graph = ca_graph

        self.set_colors(self.ca_config.state_colors)
        for c, color in zip(self.canvas, self.selected_colors):
            self.set(c, color, hex=False)
        self.set_colormap()
