import sys
from tkinter import LEFT

from UI.widgets import Label, Button, Frame

from .page import Page


class WelcomePage(Page):
    def __init__(self, parent, controller):
        super().__init__(parent, controller)
        frame1 = Frame(self)
        frame1.pack()
        Label(frame1, text="Привіт Іра").pack()

        frame2 = Frame(self)
        frame2.pack()
        Button(frame2, text="Увійти", command=lambda: controller.show_page("HomePage")).pack(side=LEFT, padx=10)
        Button(frame2, text="Я не Іра!!!", command=sys.exit).pack(side=LEFT)
