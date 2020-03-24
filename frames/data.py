from UI.widgets import Label, Button, Frame, Notebook
from components.components import GeneralTab, FailuresTab, ConfigTab
from tkinter import messagebox, LEFT
from frames.page import Page


class LoadedDataPage(Page):
    def __init__(self, parent, controller):
        super().__init__(parent, controller)
        Label(self, text="Дані по QC").pack(padx=5, pady=5)

        self.notebook = Notebook(self)
        self.notebook.pack(pady=5, padx=5)

        tab_general = GeneralTab(self.notebook, self.controller)
        self.notebook.add(tab_general, text="General")

        failures = FailuresTab(self.notebook, self.controller)
        self.notebook.add(failures, text="Failures")

        config = ConfigTab(self.notebook, self.controller)
        self.notebook.add(config, text="Configuration")

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
