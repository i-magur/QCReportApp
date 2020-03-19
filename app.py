from tkinter import Tk, Frame, BOTH, TOP, messagebox

import gspread
from gspread import Client

import config
import frames
from modules.authentication import Credentials


class Application(Tk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.config = config
        self.iconbitmap(self.config.ICON_PATH)
        self.title(self.config.TITLE)
        self._credentials = None
        self._gc = None
        self.loaded_data = None

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
    def gc(self) -> Client:
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

    def save_sheet(self, name, value, cb=None):
        self.config.set_value(name, value)
        setattr(self.config, name, value)
        callable(cb) and cb()

    def get_sheet(self, name):
        return getattr(self.config, name, None)

    def load_data(self):
        if not self.get_sheet("BASE_SHEET"):
            messagebox.showerror(
                "Не вибрана основна таблиця",
                "Будьласка вибери основну таблицю"
            )
            return None
        self.loaded_data = self.gc.open(self.get_sheet("BASE_SHEET")).sheet1
        self.show_page(frames.LoadedDataPage)
