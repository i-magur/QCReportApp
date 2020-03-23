from tkinter import messagebox, GROOVE
from tkinter.ttk import Style

from UI.styles import TABLE_FONT
from UI.widgets import Label, Frame
from utils.utils import bind_tree


def copy_text(comp, content):
    comp.clipboard_clear()
    comp.clipboard_append(content)
    comp.update()

    messagebox.showinfo(
        "Скопійовано",
        ("Текст скопійовано\n"
         "Тепер можеш вставити в таблицю\n\n"
         "%s" % content.replace('\t', ', '))
    )


class BaseComponent(Frame):
    def __init__(self, master=None, controller=None, data_attr='', date_attr='date', **kwargs):
        super().__init__(master, **kwargs)
        self.controller = controller or master
        self.master = master
        self.frame = None
        self.data_attr = data_attr
        self.date_attr = date_attr
        self.render()

    @property
    def data(self):
        try:
            return getattr(self.controller, self.data_attr)
        except AttributeError:
            return None

    @property
    def date(self):
        try:
            return getattr(self.controller, self.date_attr)
        except AttributeError:
            return None

    @property
    def format_date(self):
        return self.controller.format_date()

    def render(self):
        self.frame and self.frame.destroy()
        self.frame = Frame(self)
        self.initialize()
        self.frame.pack()

    def initialize(self):
        pass


class Cell(Frame):
    def __init__(self, master, label, thead=False, **kw):
        super().__init__(master,
                         style=f"{'H' if thead else ''}Cell.TFrame",
                         **kw)
        lbl = Label(self, text=label,
                    style=f"{'H' if thead else ''}Cell.TLabel",
                    font=TABLE_FONT)
        self.rowconfigure((0, 2), weight=1)
        self.columnconfigure((0, 2), weight=1)
        lbl.grid(row=1, column=1)

    def grid(self, **kwargs):
        super(Cell, self).grid(ipadx=5, ipady=2, sticky="nsew", **kwargs)


class BaseTable(BaseComponent):
    def __init__(self, *args, labels=None, prepend_date=False, **kwargs):
        self.prepend_date = prepend_date
        self.labels = labels or []
        super().__init__(*args, **kwargs)

    def pack(self, *args, **kwargs):
        super().pack(*args, padx=0, pady=0, **kwargs)

    def copy_text(self, e):
        if not self.data:
            return None
        copy_text(self, self.get_content())

    def add_date(self, row):
        return [self.format_date] + row

    def get_content(self):
        if self.prepend_date:
            return "\n".join(
                ["\t".join(
                    [str(col) for col in self.add_date(row)]
                ) for row in self.prepare_data()]
            )
        return "\n".join(["\t".join([str(col) for col in row]) for row in self.prepare_data()])

    def prepare_data(self):
        return []

    def initialize(self):
        if not self.data:
            return None
        pd = self.prepare_data()

        frm = Frame(self.frame)
        frm.pack(padx=0, pady=0)
        frm.grid_rowconfigure(0, weight=1)
        frm.grid_columnconfigure(0, weight=1)
        if not pd:
            # TODO: Pack blank data
            return None

        if self.prepend_date:
            Cell(frm, "Date", thead=True).grid(row=0, column=0)
            for ridx in range(1, len(pd)+1):
                Cell(frm, self.format_date).grid(row=ridx, column=0)

        for idx, name in enumerate(self.labels, 1):
            Cell(frm, name, thead=True).grid(row=0, column=idx)
        for ridx, row in enumerate(pd, 1):
            for cidx, col in enumerate(row, 1):
                Cell(frm, col).grid(row=ridx, column=cidx)

        bind_tree(frm, "<Button-1>", self.copy_text)
