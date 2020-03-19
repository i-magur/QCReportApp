from UI.widgets import Label, Button

from .page import Page


class WelcomePage(Page):
    def __init__(self, parent, controller):
        super().__init__(parent, controller)
        label = Label(self, text="Привіт Іра")
        label.pack()
        btn = Button(self, text="Увійти", command=lambda: controller.show_page("HomePage"))
        btn.pack(pady=10)
