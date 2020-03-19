from tkinter import Tk, Frame, BOTH, TOP

import gspread

from config import TITLE, ICON_PATH
import frames
from modules.authentication import Credentials


class Application(Tk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.iconbitmap(ICON_PATH)
        self.title(TITLE)
        self._credentials = None
        self._gc = None

        self.container = Frame(self)
        self.container.pack(side=TOP, fill=BOTH, expand=True)
        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)

        self.frames = dict()

        self.fill_frames()
        self.show_page(frames.START_PAGE)

    @property
    def credentials(self):
        if not self._credentials:
            self._credentials = Credentials()
        return self._credentials

    @property
    def gc(self):
        if not self._gc:
            self._gc = gspread.authorize(self.credentials)
        return self._gc

    def fill_frames(self):
        for F in frames.FRAMES:
            frame = F(self.container, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")

    def show_page(self, page):
        if type(page) == str:
            page = getattr(frames, page)
        frame = self.frames[page]
        frame.tkraise()
