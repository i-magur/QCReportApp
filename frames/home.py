from tkinter import LEFT, DISABLED, Toplevel

from UI.widgets import Label, Button, Frame, Entry, Select
from config import SHEET_NAME
from frames.page import Page


class HomePage(Page):
    def __init__(self, parent, controller):
        super().__init__(parent, controller)
        self.sheet_name = SHEET_NAME
        frame1 = Frame(self)
        label = Label(frame1, text="Таблиця з данними")

        frame2 = Frame(self)
        self.sheet_input = Entry(frame2, state=DISABLED, textvar=self.sheet_name)
        self.update_btn = Button(frame2, text="Змінити", command=self.select_sheet)

        frame1.pack()
        label.pack()
        frame2.pack()
        self.sheet_input.pack(side=LEFT, padx=10)
        self.update_btn.pack(side=LEFT)

    def select_sheet(self):
        window = Toplevel(self)

        frame1 = Frame(window)
        frame1.pack()
        label = Label(frame1, text="Вибери таблицю зі списку:")
        label.pack()

        frame2 = Frame(window)
        frame2.pack()
        select = Select(frame2, state="readonly", values=("Some value 1", "Some value 2"))
        select.pack()

        frame3 = Frame(window)
        frame3.pack()
        btn1 = Button(frame3, text="Зберегти", command=window.destroy)
        btn1.pack(side=LEFT, padx=10)
        btn2 = Button(frame3, text="Відмінити", command=window.destroy)
        btn2.pack(side=LEFT)
