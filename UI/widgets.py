from tkinter import ttk

from .styles import FONT


class Label(ttk.Label):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **{"font": FONT, **kwargs})


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
        kwargs["padx"] = kwargs.get("padx", 10)
        kwargs["pady"] = kwargs.get("pady", 10)
        super(Frame, self).pack(*args, **kwargs)


class FrameSmall(ttk.Frame):
    def pack(self, *args, **kwargs):
        super(FrameSmall, self).pack(*args, **{"pady": 5, "padx": 5, **kwargs})


class Select(ttk.Combobox):
    pass


class Treeview(ttk.Treeview):
    pass


class Notebook(ttk.Notebook):
    pass
