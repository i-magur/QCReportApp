from tkinter import ttk

from .styles import FONT


class Label(ttk.Label):
    def __init__(self, *args, **kwargs):
        super().__init__(font=FONT, *args, **kwargs)


class Button(ttk.Button):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
