from UI.widgets import Label, Button, Frame
from components.components import Table, TotalRow, InfoRow
from tkinter import messagebox, LEFT
from frames.page import Page
from utils.utils import DEFAULT_ORDER, WORD_EXP_HEADERS


class LoadedDataPage(Page):
    def __init__(self, parent, controller):
        super().__init__(parent, controller)

        Label(self, text="Дані по QC")
        self.table = Table(master=self, controller=self.controller, data_attr="users_wh", headings_attr="wh_headings")
        self.table.pack()

        self.total = TotalRow(self, self.controller,
                              data_attr="users_wh", labels=DEFAULT_ORDER)
        self.total.pack()

        self.info = InfoRow(self, self.controller,
                            data_attr="clean_data", labels=WORD_EXP_HEADERS)
        self.info.pack()

        btn_frame = Frame(self)
        btn_frame.pack()
        Button(btn_frame, text="Заповнити все", command=self.fill_all).pack(side=LEFT)
        Button(
            btn_frame,
            text="Назад",
            command=lambda: self.controller.show_page("HomePage")
        ).pack(side=LEFT, padx=10, pady=10)

    def fill_all(self):
        messagebox.showinfo("Скоро буде!", "Рано ще. Там багато умов :)")

    def tkraise(self, aboveThis=None):
        super(LoadedDataPage, self).tkraise(aboveThis)
        self.table.render()
        self.total.render()
        self.info.render()
