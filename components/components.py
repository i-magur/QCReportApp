from tkinter import ttk

from UI.widgets import Label, Treeview
from components.base import BaseComponent


class Table(BaseComponent):
    def __init__(self, title=None, headings=None, data=None, **kwargs):
        # TODO: Refactor app to use data from a parent component
        self.title = title
        self.headings = headings
        self.data = data
        super(Table, self).__init__(**kwargs)

    def update_data(self, name="data", value=None):
        setattr(self, name, value)
        self.render()

    def initialize(self):
        if not all((self.headings, self.data)):
            return None
        self.title and Label(self.frame, text=self.title).pack()
        table = Treeview(self.frame, show="headings", columns=self.headings)
        for h in self.headings:
            table.heading(h, text=h)

        for idx, r in enumerate(self.data):
            table.insert("", index=idx, values=r)

        title.pack()
        table.pack()
