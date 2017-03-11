import sys
import re
import tkinter as tk
from tkinter import filedialog


class _CreateCA(tk.Toplevel):
    CA_PATH = sys.path[0] + '/ca_descriptions/'
    TEMPLATE_PATH = CA_PATH + 'templates/'

    def __init__(self):
        tk.Toplevel.__init__(self)
        self.wm_title("Create new CA")
        self.add_options(self)

    def add_options(self, parent):
        optionsframe = tk.Frame(parent)

        titleframe = tk.Frame(optionsframe)
        tk.Label(titleframe, text="Title: ").pack(side=tk.LEFT)
        self.title_entry = tk.Entry(titleframe)
        self.title_entry.pack()
        titleframe.pack(fill=tk.BOTH)

        dimsframe = tk.Frame(optionsframe)
        tk.Label(dimsframe, text="Dimensions: ").pack(side=tk.LEFT)
        self.dimsvar = tk.IntVar()
        self.dimsvar.set('2')
        dims_entry = tk.OptionMenu(dimsframe, self.dimsvar, '1', '2')
        dims_entry.pack()
        dimsframe.pack(fill=tk.BOTH)

        tk.Label(optionsframe,
                 text="Optional (you may add these later)").pack()

        statesframe = tk.Frame(optionsframe)
        tk.Label(statesframe,
                 text='States (comma separated): ').pack(side=tk.LEFT)
        self.states_entry = tk.Entry(statesframe)
        self.states_entry.pack()
        statesframe.pack(fill=tk.BOTH)

        optionsframe.pack()

        btnframe = tk.Frame(self)
        btn_cancel = tk.Button(btnframe, text="Cancel", command=self.destroy)
        btn_cancel.pack(side=tk.LEFT)
        btn_save = tk.Button(btnframe, text="Save", command=self.save)
        btn_save.pack()
        btnframe.pack(side=tk.BOTTOM)

    def get_options(self):
        title = self.title_entry.get()
        if title == '':
            title = 'Unamed'

        dims = int(self.dimsvar.get())

        states = self.states_entry.get()
        if states == '':
            states = None
        else:
            states = states.split(',')
            states = tuple(map((lambda x: float(x)), states))

        filepath = filedialog.asksaveasfilename(initialdir=self.CA_PATH)

        return filepath, title, dims, states

    def save(self):
        filepath, title, dims, states = self.get_options()
        if not filepath == '':
            template_name = 'template{dims}d.py'.format(dims=dims)
            with open(self.TEMPLATE_PATH + template_name, 'r') as f:
                template = f.read()

            nameindexes = [m.start() for m in re.finditer('NAME', template)]

            template = self.replace(template, 'NAME', title, nameindexes)

            if states is not None:
                statesindexes = [
                    m.start() for m in re.finditer('STATES', template)
                ]
                template = self.replace(template, 'STATES',
                                        str(states), statesindexes)

            with open(filepath, 'w') as f:
                f.write(template)

            self.destroy()
            savedalert = _SavedAlert(filepath)

    def replace(self, string, toreplace, replacewith, indexls):
        offset = len(replacewith) - len(toreplace)
        for i, index in enumerate(indexls):
            header = string[:index + (i*offset)]
            footer = string[index + len(toreplace) + (i*offset):]
            string = header + replacewith + footer
        return string


class _SavedAlert(tk.Toplevel):
    def __init__(self, filepath):
        tk.Toplevel.__init__(self)
        # set title
        self.wm_title("File save success")

        self.filepath = filepath

        label = tk.Label(self, text='File saved to: ' + filepath)
        label.pack(padx=10, pady=10)
        buttonframe = tk.Frame(self)
        btn_copy = tk.Button(buttonframe, text='Copy path to clipboard',
                             command=self.copypath)
        btn_copy.pack()
        btn_ok = tk.Button(buttonframe, text='Close', command=self.destroy)
        btn_ok.pack()
        buttonframe.pack()

    def copypath(self):
        self.clipboard_clear()
        self.clipboard_append(self.filepath)
