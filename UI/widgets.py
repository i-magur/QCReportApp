from tkinter import ttk

from .styles import FONT


class Label(ttk.Label):
    def __init__(self, *args, **kwargs):
        super().__init__(font=FONT, *args, **kwargs)


class Button(ttk.Button):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
    def pack(self, *args, **kwargs):
        super(Button, self).pack(*args, **{"ipadx": 5, **kwargs})


class Entry(ttk.Entry):
    def pack(self, *args, **kwargs):
        super(Entry, self).pack(*args, **{"padx": 5, **kwargs})


class Frame(ttk.Frame):
    def pack(self, *args, **kwargs):
        super(Frame, self).pack(*args, **{"pady": 10, "padx": 10, **kwargs})


class Select(ttk.Combobox):
    pass


class Treeview(ttk.Treeview):
    pass
