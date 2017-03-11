import sys
import tkinter as tk
from tkinter import messagebox
from capyle.guicomponents import _Separator


def set_icon(root):
    root_path = sys.path[0]
    img = tk.PhotoImage(file=root_path + '/icons/icon.gif')
    try:
        root.call('wm', 'iconphoto', root._w, img)
    except:
        root.tk.call('wm', 'iconphoto', root._w, img)


def get_filename_dialog(ca_descriptions=True):
    """Open a GUI file dialogue to get the filename of a file"""
    if ca_descriptions:
        openpath = sys.path[0] + '/ca_descriptions'
        filename = tk.filedialog.askopenfilename(initialdir=openpath)
    else:
        filename = tk.filedialog.askopenfilename()
    return filename


def get_dir_dialog(initpath=None):
    if initpath is not None:
        dir = tk.filedialog.askdirectory(initialdir=initpath)
    else:
        dir = tk.filedialog.askdirectory()
    return dir


def clear_entry(entry):
    """Clear the supplied entry"""
    for c in entry.get():
        entry.delete(0)


def set_entry(entry, value):
    """Set the given entry to the given value"""
    clear_entry(entry)
    for i, c in enumerate(str(value)):
        entry.insert(i, c)


def separator(parent):
    """Generate a separator"""
    _Separator(parent).pack(fill=tk.BOTH, padx=5, pady=10)


def alerterror(title, message):
    """Alert error with given title and message"""
    messagebox.showerror(title, message)


def alertwarning(title, message):
    """Alert warning with given title and message"""
    messagebox.showerror(title, message)


def alertcontinue(title, message):
    """Proceed warning with given title and message"""
    return messagebox.askokcancel(title, message)
