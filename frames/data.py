from UI.widgets import Label, Button
from components.components import Table
from frames.page import Page


class LoadedDataPage(Page):
    def __init__(self, parent, controller):
        super().__init__(parent, controller)

        Label(self, text="Дані по QC")
        self.table = Table(master=self, **self.get_data())
        # self.table.bind('<Mouse-1>', lambda e: print('click', e))

        self.table.pack()

        Button(self, text="Назад", command=lambda: self.controller.show_page("HomePage")).pack()

    @property
    def data(self):
        return self.controller.loaded_data

    def tkraise(self, aboveThis=None):
        super(LoadedDataPage, self).tkraise(aboveThis)
        self.table.render()

    def get_data(self):
        if not self.data:
            return dict(headings=None, data=None)
        print(self.data.row_values(1))
