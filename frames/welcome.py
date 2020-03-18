from UI.widgets import Label
from .page import Page


class WelcomePage(Page):
    def __init__(self, parent, controller):
        super().__init__(parent, controller)
        label = Label(self, text="Привіт Іра")
        label.pack()
