from tkinter import LEFT, DISABLED, Toplevel, NORMAL, StringVar

from UI.widgets import Label, Button, Frame, Entry, Select
from frames.page import Page


class HomePage(Page):
    def __init__(self, parent, controller):
        super().__init__(parent, controller)
        self.window = None
        self.sheet_name = StringVar(value=self.controller.get_sheet("BASE_SHEET"))
        frame1 = Frame(self)
        label = Label(frame1, text="Таблиця з данними")

        frame2 = Frame(self)
        self.sheet_input = Entry(frame2, textvar=self.sheet_name, state=DISABLED)
        self.update_widget_name()
        self.update_btn = Button(frame2, text="Змінити", command=self.select_sheet)

        frame1.pack()
        label.pack()
        frame2.pack()
        self.sheet_input.pack(side=LEFT, padx=10)
        self.update_btn.pack(side=LEFT)

        frame3 = Frame(self)
        frame3.pack()
        load_data = Button(frame3, text="Завантажити дані", command=self.controller.load_data)
        load_data.pack()

    def update_widget_name(self):
        self.sheet_name.set(self.controller.get_sheet("BASE_SHEET"))

    def select_sheet(self):
        self.window = Toplevel(self)

        frame1 = Frame(self.window)
        frame1.pack()
        label = Label(frame1, text="Вибери таблицю зі списку:")
        label.pack()

        frame2 = Frame(self.window)
        frame2.pack()
        select = Select(
            frame2,
            state="readonly",
            values=self.get_values()
        )
        select.set(self.controller.get_sheet("BASE_SHEET"))
        select.pack()

        frame3 = Frame(self.window)
        frame3.pack()
        btn1 = Button(frame3, text="Зберегти", command=lambda: self.controller.save_sheet(
            "BASE_SHEET", select.get(), self.select_sheet_callback
        ))
        btn1.pack(side=LEFT, padx=10)
        btn2 = Button(frame3, text="Відмінити", command=self.window.destroy)
        btn2.pack(side=LEFT)

    def select_sheet_callback(self):
        self.update_widget_name()
        self.window and self.window.destroy()

    def get_values(self):
        gc = self.controller.gc
        return [s['name'] for s in gc.list_spreadsheet_files()]
