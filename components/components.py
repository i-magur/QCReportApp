from tkinter import ttk

from UI.widgets import Label, Treeview, Frame
from components.base import BaseComponent


class Table(BaseComponent):
    def __init__(self, master=None, headings_attr="headings", data_attr="data", **kwargs):
        self.headings_attr = headings_attr
        self.data_attr = data_attr
        super().__init__(master, **kwargs)

    def update_data(self, name="data", value=None):
        setattr(self, name, value)
        self.render()

    @property
    def data(self):
        return getattr(self.controller, self.data_attr)

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
