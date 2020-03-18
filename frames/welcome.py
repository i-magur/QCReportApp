from UI.widgets import Label, Button

from .page import Page


class WelcomePage(Page):
    def __init__(self, parent, controller):
        super().__init__(parent, controller)
        label = Label(self, text="Привіт Іра")
        label.pack()
        btn = Button(text="Увійти")
        btn.pack(pady=10)
