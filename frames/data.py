from UI.widgets import Label, Button, Frame
from components.components import WordCountTable, InfoRow, GeneralInfo, ProjectsCountTable, FailuresTable, HandOffTable
from tkinter import messagebox, LEFT
from frames.page import Page
from utils.utils import DEFAULT_ORDER, FAULT_LABELS, HAND_OFF_LABELS


class LoadedDataPage(Page):
    def __init__(self, parent, controller):
        super().__init__(parent, controller)
        Label(self, text="Дані по QC").grid(padx=5, pady=5, row=0, column=0, columnspan=2)

        frm_left = Frame(self)
        frm_left.grid(row=1, column=0)
        self.table = GeneralInfo(frm_left, self.controller,
                                 data_attr="users_wh", labels=self.controller.wh_headings)
        self.table.pack()

        frm_right = Frame(self)
        frm_right.grid(row=1, column=1)
        self.total = WordCountTable(frm_right, self.controller,  prepend_date=True,
                                    data_attr="users_wh", labels=DEFAULT_ORDER)
        self.projects = ProjectsCountTable(frm_right, self.controller,  prepend_date=True,
                                           data_attr="users_wh", labels=DEFAULT_ORDER)
        self.info = InfoRow(frm_right, self.controller,  prepend_date=True,
                            data_attr="clean_data", labels=self.controller.wh_headings)
        self.total.pack()
        self.projects.pack()
        self.info.pack()

        frm_bottom = Frame(self)
        frm_bottom.grid(row=2, column=0, columnspan=2)
        self.fails = FailuresTable(frm_bottom, self.controller, prepend_date=True,
                                   data_attr='clean_data', labels=FAULT_LABELS)
        self.fails.pack()
        self.handoff = HandOffTable(frm_bottom, self.controller, prepend_date=True,
                                    data_attr='clean_data', labels=HAND_OFF_LABELS)
        self.handoff.pack()

        btn_frame = Frame(self)
        btn_frame.grid(row=3, column=0, columnspan=2)
        Button(btn_frame, text="Заповнити все", command=self.fill_all).pack(side=LEFT)
        Button(
            btn_frame,
            text="Назад",
            command=lambda: self.controller.show_page("HomePage")
        ).pack(side=LEFT, padx=10, pady=10)

    def fill_all(self):
        messagebox.showinfo("Скоро буде!", "Рано ще. Там багато умов :)")

    @property
    def frames(self):
        return [self.table, self.total, self.projects, self.info, self.fails, self.handoff]

    def tkraise(self, aboveThis=None):
        super(LoadedDataPage, self).tkraise(aboveThis)
        for f in self.frames:
            f.render()
