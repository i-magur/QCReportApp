from tkinter.ttk import Frame


class BaseComponent(Frame):
    def __init__(self, master=None, controller=None, **kwargs):
        super().__init__(master, **kwargs)
        self.controller = controller or master
        self.master = master
        self.frame = None
        self.render()

    def render(self):
        self.frame and self.frame.destroy()
        self.frame = Frame(self)
        self.initialize()
        self.frame.pack()

    def initialize(self):
        pass
