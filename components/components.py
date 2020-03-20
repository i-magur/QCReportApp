from datetime import date
from functools import reduce
from tkinter import GROOVE, messagebox

from UI.widgets import Label, Treeview, Frame
from components.base import BaseComponent
from utils.utils import DEFAULT_ORDER, bind_tree, WORDCOUNT


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


class Table(BaseComponent):
    def __init__(self, master=None, headings_attr="headings", **kwargs):
        self.headings_attr = headings_attr
        super().__init__(master, **kwargs)

    def copy_text(self, e):
        if not self.data:
            return None
        content = "\n".join(["\t".join([str(col) for col in row]) for row in self.data])
        copy_text(self, content)

    def update_data(self, name="data", value=None):
        setattr(self, name, value)
        self.render()

    @property
    def headings(self):
        return getattr(self.controller, self.headings_attr)

    def initialize(self):
        if not self.data:
            return None
        table = Treeview(
            self.frame, show="headings",
            columns=self.headings
        )
        for h in self.headings:
            table.heading(h, text=h)

        for idx, r in enumerate(self.data):
            table.insert("", index=idx, values=r)

        table.pack(padx=10, pady=10)
        bind_tree(table, "<Button-1>", self.copy_text)


class Cell(Frame):
    def __init__(self, master, label, **kw):
        super().__init__(master, relief=GROOVE, borderwidth=1, **kw)
        lbl = Label(self, text=label)
        self.rowconfigure((0, 2), weight=1)
        self.columnconfigure((0, 2), weight=1)
        lbl.grid(row=1, column=1)

    def grid(self, **kwargs):
        super(Cell, self).grid(ipadx=5, ipady=5, sticky="nsew", **kwargs)


class BaseTable(BaseComponent):
    def __init__(self, *args, labels=None, **kwargs):
        self.labels = labels or []
        super().__init__(*args, **kwargs)

    def copy_text(self, e):
        if not self.data:
            return None
        copy_text(self, self.get_content())

    def get_content(self):
        return ""

    def prepare_data(self):
        return []

    def initialize(self):
        if not self.data:
            return None

        frm = Frame(self.frame)
        frm.pack()
        frm.grid_rowconfigure(0, weight=1)
        frm.grid_columnconfigure(0, weight=1)

        pd = self.prepare_data()
        if len(pd) == 1:
            Cell(frm, "Дата").grid(row=0, column=0)
            Cell(frm, date.today()).grid(row=1, column=0)

        for idx, name in enumerate(self.labels, 1):
            Cell(frm, name).grid(row=0, column=idx)
        for ridx, row in enumerate(pd, 1):
            for cidx, col in enumerate(row, 1):
                Cell(frm, col).grid(row=ridx, column=cidx)

        bind_tree(frm, "<Button-1>", self.copy_text)


class TotalRow(BaseTable):
    def get_content(self):
        return "\t".join(map(str, self.prepare_data()[0]))

    def prepare_data(self):
        return [[row[1] for row in self.data]]


class InfoRow(BaseTable):
    def get_content(self):
        return "\t".join(map(str, self.prepare_data()[0]))

    def prepare_data(self):
        return [[
            sum(map(int, [i[WORDCOUNT] for i in self.data])),
            len(self.data),
            150000
        ]]

