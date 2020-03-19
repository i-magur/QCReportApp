from src.UI.widgets import Label
from src.frames.page import Page


class HomePage(Page):
    def __init__(self, parent, controller):
        super().__init__(parent, controller)
        label = Label(self, text="Hello")
        label.pack()
