from datetime import date
from tkinter import Tk, Frame, BOTH, TOP, messagebox, ttk

import gspread
from gspread import Client, WorksheetNotFound
from gspread.exceptions import APIError

import config
import frames
from UI.styles import STYLES
from modules.authentication import Credentials
from utils.utils import collect_users_wh, get_clean_data


class Application(Tk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.config = config
        self.iconbitmap(self.config.ICON_PATH)
        self.title(self.config.TITLE)
        self.date_format = "%#m/%#d/%Y"
        self.sheet = None
        self.worksheet_list = []
        self.sheet_list = []
        self._credentials = None
        self._gc = None
        self.loaded_data = None
        self.date = date.today()
        self.clean_data = None
        self.users_wh = None
        self.wh_headings = ["QC", "Words", "Tasks"]

        self.container = Frame(self)
        self.container.pack(side=TOP, fill=BOTH, expand=True)
        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)

        self.frames = dict()

        self.fill_frames()
        self.show_page(frames.START_PAGE)

        self.style = ttk.Style()
        self.apply_styles()

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

    def save_date(self, day=None, month=None):
        try:
            if day:
                self.date = self.date.replace(day=int(day))
            if month:
                self.date = self.date.replace(month=self.config.MONTH_NAMES.index(month) + 1)
        except ValueError:
            self.date = date.today()

    def format_date(self):
        return self.date.strftime(self.date_format)

    def get_sheet(self, name):
        return getattr(self.config, name, None)

    def get_worksheet(self):
        return str(self.date.day)

    def set_users_wh(self):
        try:
            self.users_wh = collect_users_wh(self.clean_data)
        except IndexError:
            messagebox.showerror("Помилка з данними", "Можливо вибрана не та таблиця")

    def set_clean(self):
        self.clean_data = get_clean_data(self.loaded_data.get_all_values())

    def worksheet_not_found(self):
        messagebox.showerror("Не знайдено",
                             f"Вибрана таблиця не має вкладки {self.date.day}")

    def load_data(self, force=False):
        if force or not self.sheet:
            self.sheet = self.gc.open(self.get_sheet("BASE_SHEET"))
        self.set_worksheet_list()

    def set_worksheet_list(self):
        if self.sheet:
            self.worksheet_list = [s.title for s in self.sheet.worksheets()]

    def show_data(self):
        if not self.get_sheet("BASE_SHEET"):
            messagebox.showerror(
                "Не вибрана основна таблиця",
                "Будьласка вибери основну таблицю"
            )
            return None

        try:
            self.loaded_data = self.sheet.worksheet(self.get_worksheet())
        except WorksheetNotFound:
            return self.worksheet_not_found()
        self.set_clean()
        self.set_users_wh()

        self.show_page(frames.LoadedDataPage)

    def load_table(self, name, worksheet=None):
        name = self.get_sheet(name)
        try:
            return self.gc.open(name).worksheet(worksheet or self.get_worksheet())
        except APIError:
            messagebox.showerror("Error", "Google connection problem")
            return None
        except WorksheetNotFound as e:
            messagebox.showerror("Error", f"Не знайдена вкладка {str(e)}")
            return None

    def apply_styles(self):
        for name, style in STYLES.items():
            self.style.configure(
                name,
                **style
            )

    def load_sheet_list(self):
        self.sheet_list = [s['name'] for s in self.gc.list_spreadsheet_files()]
