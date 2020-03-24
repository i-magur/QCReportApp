from tkinter import messagebox

from gspread.utils import a1_to_rowcol, rowcol_to_a1

from UI.styles import TABLE_FONT
from UI.widgets import Label, Frame
from errors import CellIsNotBlank
from utils.utils import bind_tree


def copy_text(comp, content):
    comp.clipboard_clear()
    comp.clipboard_append(content)
    comp.update()

    messagebox.showinfo(
        "Скопійовано",
        ("Текст скопійовано\n"
         "Тепер можеш вставити в таблицю\n\n"
         "%s" % content.replace('\t', ', '))
    )


class BaseComponent(Frame):
    def __init__(self, master=None, controller=None, **kwargs):
        super(BaseComponent, self).__init__(master, **kwargs)
        self.controller = controller or master
        self.pre_render()
        self.render()

    @property
    def date(self):
        try:
            return self.controller.date
        except AttributeError:
            return None

    @property
    def format_date(self):
        try:
            return self.controller.format_date()
        except AttributeError:
            return None

    def pre_render(self):
        pass

    def render(self):
        for f in self.winfo_children():
            f.destroy()


class BaseTableComponent(Frame):
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


class Cell(Frame):
    def __init__(self, master, label, thead=False, **kw):
        super().__init__(master,
                         style=f"{'H' if thead else ''}Cell.TFrame",
                         **kw)
        lbl = Label(self, text=label,
                    style=f"{'H' if thead else ''}Cell.TLabel",
                    font=TABLE_FONT)
        self.rowconfigure((0, 2), weight=1)
        self.columnconfigure((0, 2), weight=1)
        lbl.grid(row=1, column=1)

    def grid(self, **kwargs):
        super(Cell, self).grid(ipadx=5, ipady=2, sticky="nsew", **kwargs)


class BaseTable(BaseTableComponent):
    fill_index = ''
    fill_table = ''

    def __init__(self, *args, labels=None, prepend_date=False, **kwargs):
        self.prepend_date = prepend_date
        self.labels = labels or []
        super().__init__(*args, **kwargs)

    def pack(self, *args, **kwargs):
        super().pack(*args, padx=0, pady=0, **kwargs)

    def copy_text(self, e):
        if not self.data:
            return None
        copy_text(self, self.get_content())

    def add_date(self, row):
        return [self.format_date] + row

    def get_content(self):
        if self.prepend_date:
            return "\n".join(
                ["\t".join(
                    [str(col) for col in self.add_date(row)]
                ) for row in self.prepare_data()]
            )
        return "\n".join(["\t".join([str(col) for col in row]) for row in self.prepare_data()])

    def check_rows(self, cell_range, data):
        for cell, cell_value in zip(cell_range, data):
            if cell.value:
                raise CellIsNotBlank()
            else:
                cell.value = cell_value
        return cell_range

    def get_fill_range(self, ridx, cidx):
        return f"{self.fill_index}:{rowcol_to_a1(ridx, cidx)}"

    def save(self):
        if not self.fill_index or not self.fill_table:
            return self.message("Is not implemented yet...", True)

        table = self.controller.get_sheet(self.fill_table)
        if not table:
            return self.message("Table is not selected", True)

        data = self.prepare_data()
        if not len(data):
            return self.message(f"There is no data to fill")

        ridx, cidx = a1_to_rowcol(self.fill_index)
        ridx += len(data) - 1
        cidx += len(data[0]) - 1
        cell_range = self.get_fill_range(ridx, cidx)

        ws = self.controller.load_table(self.fill_table)
        data_to_fill = [c for row in data for c in row]
        cell_list = ws.range(cell_range)
        try:
            self.check_rows(cell_list, data_to_fill)
        except CellIsNotBlank:
            return self.message(f"Some cells in range {cell_range} are not blank", True)

        ws.update_cells(cell_list)
        self.message(f"Successfully filled {table}, {cell_range}")

    def message(self, message, error=False):
        if error:
            messagebox.showerror("Error", message)
        else:
            messagebox.showinfo("Message", message)

    def prepare_data(self):
        return []

    def initialize(self):
        if not self.data:
            return None
        pd = self.prepare_data()

        frm = Frame(self.frame)
        frm.pack(padx=0, pady=0)
        frm.grid_rowconfigure(0, weight=1)
        frm.grid_columnconfigure(0, weight=1)
        if not pd:
            # TODO: Pack blank data
            return None

        if self.prepend_date:
            Cell(frm, "Date", thead=True).grid(row=0, column=0)
            for ridx in range(1, len(pd)+1):
                Cell(frm, self.format_date).grid(row=ridx, column=0)

        for idx, name in enumerate(self.labels, 1):
            Cell(frm, name, thead=True).grid(row=0, column=idx)
        for ridx, row in enumerate(pd, 1):
            for cidx, col in enumerate(row, 1):
                Cell(frm, col).grid(row=ridx, column=cidx)

        bind_tree(frm, "<Button-1>", self.copy_text)
