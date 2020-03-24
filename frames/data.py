from UI.widgets import Label, Button, Frame, Notebook
from components.components import WordCountTable, InfoRow, GeneralInfo, ProjectsCountTable, FailuresTable, HandOffTable, \
    GeneralTab, FailuresTab
from tkinter import messagebox, LEFT
from frames.page import Page
from utils.utils import DEFAULT_ORDER, FAULT_LABELS, HAND_OFF_LABELS


class LoadedDataPage(Page):
    def __init__(self, parent, controller):
        super().__init__(parent, controller)
        # Label(self, text="Дані по QC").grid(padx=5, pady=5, row=0, column=0, columnspan=2)
        Label(self, text="Дані по QC").pack(padx=5, pady=5)

        self.notebook = Notebook(self)
        self.notebook.pack(pady=5, padx=5)

        self.tab_general = GeneralTab(self.notebook, self.controller)
        self.notebook.add(self.tab_general, text="General")

        self.failures = FailuresTab(self.notebook, self.controller)
        self.notebook.add(self.failures, text="Failures")

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
        for f in self.notebook.winfo_children():
            f.render()
