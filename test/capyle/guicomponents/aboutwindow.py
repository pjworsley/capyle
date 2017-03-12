import tkinter as tk
import webbrowser


class _AboutWindow(tk.Toplevel):

    def __init__(self):
        tk.Toplevel.__init__(self)
        self.wm_title("About CAPyLE")

        author = [['CAPyLE was developed by:'],
                  ['Peter Worsley', 'http://www.github.com/pjworsley'],
                  ['under the supervision of'],
                  ['Dr. Dawn Walker',
                   'http://staffwww.dcs.shef.ac.uk/people/D.Walker/'],
                  ['as part of the final year project at'],
                  ['The University of Sheffield',
                   'http://www.sheffield.ac.uk']]

        licence = 'Licenced under a BSD Licence'
        copyright = 'Copyright 2017 Peter Worsley'

        # add to gui
        topframe = tk.Frame(self)

        imgframe = tk.Frame(topframe)
        logo = tk.PhotoImage(file="icons/icon.gif")
        img = tk.Label(imgframe, image=logo)
        img.image = logo
        img.pack(padx=10, pady=10)
        imgframe.pack(side=tk.LEFT)

        authorframe = tk.Frame(topframe)
        for t in author:
            link = len(t) == 2
            label = tk.Label(authorframe, text=t[0])
            if link:
                label.config(fg="blue")
                label.bind('<Button-1>', lambda x, l=t[1]: self.openlink(l))
            label.pack()
        authorframe.pack(side=tk.RIGHT, padx=10, pady=10)

        topframe.pack()

        # Bottom of window
        label = tk.Label(self, text=licence)
        label.pack(pady=5)

        label = tk.Label(self, text=copyright)
        label.pack(pady=5)

        btn_close = tk.Button(self, text="Close", command=self.destroy)

    def openlink(self, link):
        webbrowser.open_new(link)
