from datetime import date
from tkinter import LEFT, DISABLED, Toplevel, StringVar

from UI.widgets import Label, Button, Frame, Entry, Select
from components.components import SheetSelect
from frames.page import Page


class HomePage(Page):
    def __init__(self, parent, controller):
        super().__init__(parent, controller)

        self.window = None
        self.sheet_name = StringVar(value=self.controller.get_sheet("BASE_SHEET"))
        frame1 = Frame(self)
        label = Label(frame1, text="Вибрана таблиця і день")

        frame2 = Frame(self)
        self.day_input = Select(
            frame2,
            state="readonly",
            width=3,
            values=self.worksheet_list
        )
        self.day_input.set(self.controller.date.day)
        self.day_input.bind(
            '<<ComboboxSelected>>',
            self.day_change_callback
        )
        self.sheet_input = Entry(frame2, textvar=self.sheet_name, state=DISABLED)
        self.update_widget_name()
        self.update_btn = Button(frame2, text="Змінити", command=self.select_sheet)

        frame1.pack()
        label.pack()
        frame2.pack()
        self.day_input.pack(side=LEFT)
        self.sheet_input.pack(side=LEFT, padx=10)
        self.update_btn.pack(side=LEFT)

        frame3 = Frame(self)
        frame3.pack()
        load_data = Button(frame3, text="Завантажити дані", command=self.controller.show_data)
        load_data.pack()

    def day_change_callback(self, e):
        self.controller.save_date(self.day_input.get())

    def update_widget_name(self):
        self.sheet_name.set(self.controller.get_sheet("BASE_SHEET"))

    def update_day_select(self):
        self.day_input['values'] = self.worksheet_list
        val = self.controller.date.day \
            if str(self.controller.date.day) in self.worksheet_list \
            else self.worksheet_list[-1]
        self.day_input.set(val)
        self.day_change_callback(None)

    @property
    def worksheet_list(self):
        return self.controller.worksheet_list or list(range(1, date.today().day + 1))

    def select_sheet(self):
        self.window = Toplevel(self)

        frame1 = Frame(self.window)
        frame1.pack()
        label = Label(frame1, text="Вибери таблицю зі списку:")
        label.pack()

        frame2 = Frame(self.window)
        frame2.pack()
        select = SheetSelect(frame2, self.controller, "BASE_SHEET")
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
        self.controller.load_data(True)
        self.update_day_select()
        self.window and self.window.destroy()

    def on_mount(self):
        self.controller.load_sheet_list()
        if self.sheet_name:
            self.controller.load_data()
            self.update_day_select()
