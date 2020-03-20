from tkinter.ttk import Frame


class BaseComponent(Frame):
    def __init__(self, master=None, controller=None, data_attr='', **kwargs):
        super().__init__(master, **kwargs)
        self.controller = controller or master
        self.master = master
        self.frame = None
        self.data_attr = data_attr
        self.render()

    @property
    def data(self):
        try:
            return getattr(self.controller, self.data_attr)
        except AttributeError:
            return None

    def render(self):
        self.frame and self.frame.destroy()
        self.frame = Frame(self)
        self.initialize()
        self.frame.pack()

    def initialize(self):
        pass
