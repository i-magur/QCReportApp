import sys
from tkinter import LEFT

from UI.widgets import Label, Button, Frame

from .page import Page


class WelcomePage(Page):
    def __init__(self, parent, controller):
        super().__init__(parent, controller)
        for i, weight in zip(range(3), [0, 1, 0]):
            self.grid_rowconfigure(i, weight=weight)
            self.grid_columnconfigure(i, weight=weight)
        div = Frame(self)
        div.grid(row=1, column=1, padx=0, pady=0)
        frame1 = Frame(div)
        frame1.pack()
        Label(frame1, text="Привіт Іра").pack()

        frame2 = Frame(div)
        frame2.pack()
        Button(frame2, text="Увійти", command=lambda: controller.show_page("HomePage")).pack(side=LEFT, padx=10)
        Button(frame2, text="Я не Іра!!!", command=sys.exit).pack(side=LEFT)
