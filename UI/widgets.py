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
    def __init__(self, *args, **kwargs):
        kwargs['width'] = kwargs['width'] if kwargs.get('width', None) is not None else 30
        super().__init__(*args, **kwargs)

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
    def __init__(self, *args, **kwargs):
        kwargs['width'] = kwargs['width'] if kwargs.get('width', None) is not None else 30
        super().__init__(*args, **kwargs)


class Treeview(ttk.Treeview):
    pass


class Notebook(ttk.Notebook):
    pass


DEL_CODES = [8, 46]


class InputSelect(ttk.Combobox):
    def __init__(self, master=None, values=None, on_change=None, on_keyup=None, **kwargs):
        self.options = values or []
        self.on_change = on_change
        self.on_keyup = on_keyup
        super().__init__(master, values=values, **kwargs)

        self.bind('<<ComboboxSelected>>', self.handle_change)
        self.bind('<KeyRelease>', self.handle_keyup)
        self.prev_val = self.get() or ''

    def handle_change(self, e=None):
        if self.on_change:
            return self.on_change(self.get())

    def handle_keyup(self, e=None):
        if not e.char and e.keycode not in DEL_CODES:
            return
        if self.on_keyup:
            return self.on_keyup(self.get())
        val = self.get() or ''
        new_vals = [v for v in self.options if str(v).lower().startswith(val.lower())]
        if len(new_vals) == 1 and e.char:
            self.set(new_vals[0])
            self.prev_val = new_vals[0]
        elif not new_vals and self.options:
            if e.char:
                self.set(self.prev_val)
            new_vals = [v for v in self.options if str(v).lower().startswith(self.prev_val.lower())]
        else:
            self.prev_val = val
        self['values'] = new_vals
        if len(new_vals) == 1:
            self.handle_change()
