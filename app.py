from tkinter import Tk, Frame, BOTH, TOP

import gspread

from config import TITLE, ICON_PATH
from frames import FRAMES, START_PAGE
from modules.authentication import Credentials


class Application(Tk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.iconbitmap(ICON_PATH)
        self.title(TITLE)
        self.credentials = Credentials()
        self.gc = gspread.authorize(self.credentials)

        self.container = Frame(self)
        self.container.pack(side=TOP, fill=BOTH, expand=True)
        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)

        self.frames = dict()

        self.fill_frames()
        self.show_page(START_PAGE)

    def fill_frames(self):
        for F in FRAMES:
            frame = F(self.container, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")

    def show_page(self, page):
        frame = self.frames[page]
        frame.tkraise()
