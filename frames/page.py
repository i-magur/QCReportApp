from tkinter import Frame


class Page(Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.mount = False

    def on_mount(self):
        pass

    def tkraise(self, aboveThis=None):
        super(Page, self).tkraise(aboveThis)
        if not self.mount:
            self.on_mount()
            self.mount = True
