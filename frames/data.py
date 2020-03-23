from UI.widgets import Label, Button, Frame
from components.components import TotalRow, InfoRow, GeneralInfo
from tkinter import messagebox, LEFT
from frames.page import Page
from utils.utils import DEFAULT_ORDER


class LoadedDataPage(Page):
    def __init__(self, parent, controller):
        super().__init__(parent, controller)

        Label(self, text="Дані по QC")
        frm_left = Frame(self)
        frm_left.grid(row=0, column=0)
        self.table = GeneralInfo(frm_left, self.controller,
                                 data_attr="users_wh", labels=self.controller.wh_headings)
        self.table.pack()

        frm_right = Frame(self)
        frm_right.grid(row=0, column=1)

        self.total = TotalRow(frm_right, self.controller,
                              data_attr="users_wh", labels=DEFAULT_ORDER)
        self.total.pack()

        self.info = InfoRow(frm_right, self.controller,
                            data_attr="clean_data", labels=self.controller.wh_headings)
        self.info.pack()

        btn_frame = Frame(self)
        btn_frame.grid(row=1, column=0, columnspan=2)
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
