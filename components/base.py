from tkinter.ttk import Frame


class BaseComponent(Frame):
    def __init__(self, master=None, controller=None, data_attr='', date_attr='date', **kwargs):
        super().__init__(master, **kwargs)
        self.controller = controller or master
        self.master = master
        self.frame = None
        self.data_attr = data_attr
        self.date_attr = date_attr
        self.render()

    @property
    def data(self):
        try:
            return getattr(self.controller, self.data_attr)
        except AttributeError:
            return None

    @property
    def date(self):
        try:
            return getattr(self.controller, self.date_attr)
        except AttributeError:
            return None

    @property
    def format_date(self):
        return self.controller.format_date()

    def render(self):
        self.frame and self.frame.destroy()
        self.frame = Frame(self)
        self.initialize()
        self.frame.pack()

    def initialize(self):
        pass
