from datetime import datetime
from tkinter import LEFT

from UI.widgets import Frame, Label, Select, Button, InputSelect
from components.base import BaseTable, BaseComponent
from utils.utils import WORDCOUNT, FAULT_IDX, FAULT_INDEXES, HAND_OFF_IDX, HAND_OFF_INDEXES, DEFAULT_ORDER, \
    FAULT_LABELS, HAND_OFF_LABELS, find_a_place_to_fill


class WordCountTable(BaseTable):
    _fill_table = 'INTERNAL_SHEET'
    _worksheet = None
    _find_range = 'A2:A27'
    skip_first = True
    label = "Word Count"

    def __init__(self, *args, **kwargs):
        super(WordCountTable, self).__init__(*args, **kwargs)
        self._worksheet = self.controller.date.strftime('%B')

    def prepare_data(self):
        return [[row[1] for row in self.data]]


class ProjectsCountTable(BaseTable):
    _fill_table = 'INTERNAL_SHEET'
    _worksheet = datetime.now().strftime("%B")
    _find_range = 'A26:A50'
    skip_first = True
    label = "Projects count"

    def prepare_data(self):
        return [[row[2] for row in self.data]]


class InfoRow(BaseTable):
    _fill_table = 'INTERNAL_SHEET'
    _worksheet = datetime.now().strftime("%B")
    _find_range = 'I2:I27'
    skip_first = True
    label = "Info"

    def prepare_data(self):
        return [[
            sum(map(int, [i[WORDCOUNT] for i in self.data])),
            len(self.data),
            150000
        ]]


class GeneralInfo(BaseTable):
    _fill_index = 'R2'
    _fill_table = "BASE_SHEET"
    label = 'General'

    def prepare_data(self):
        return self.data


class FailuresTable(BaseTable):
    _fill_table = 'FAILURES_SHEET'
    _worksheet = 'Sheet1'
    _insert = True
    label = "Failures"

    def find_index(self, ws):
        return find_a_place_to_fill(ws, self.controller.date, self.controller.date_format)

    def prepare_data(self):
        data = []
        for row in self.data:
            if not row[FAULT_IDX]:
                data.append([row[idx] for idx in FAULT_INDEXES])
        return data


class HandOffTable(BaseTable):
    _fill_table = 'HAND_OFF_SHEET'
    _worksheet = 'Sheet1'
    _insert = True
    label = "Handoff time"

    def find_index(self, ws):
        return find_a_place_to_fill(ws, self.controller.date, self.controller.date_format)

    def prepare_data(self):
        data = []
        for row in self.data:
            if row[HAND_OFF_IDX]:
                data.append([row[idx] for idx in HAND_OFF_INDEXES])
        return data


class GeneralTab(BaseComponent):
    tables = []

    def pre_render(self):
        for w, c in zip([0, 1, 1, 0], range(4)):
            self.grid_columnconfigure(c, weight=w)
        for w, r in zip([0, 1, 0], range(3)):
            self.grid_rowconfigure(r, weight=w)

    def render(self):
        super().render()
        frm_left = Frame(self)
        frm_left.grid(row=1, column=1)
        general = GeneralInfo(frm_left, self.controller,
                              data_attr="users_wh", labels=self.controller.wh_headings)
        general.pack()

        frm_right = Frame(self)
        frm_right.grid(row=1, column=2)
        total = WordCountTable(frm_right, self.controller, prepend_date=True,
                               data_attr="users_wh", labels=DEFAULT_ORDER)
        projects = ProjectsCountTable(frm_right, self.controller, prepend_date=True,
                                      data_attr="users_wh", labels=DEFAULT_ORDER)
        info = InfoRow(frm_right, self.controller, prepend_date=True,
                       data_attr="clean_data", labels=self.controller.wh_headings)
        total.pack()
        projects.pack()
        info.pack()
        frm_bottom = Frame(self)
        frm_bottom.grid(row=2, column=1, columnspan=2)
        Button(frm_bottom, text="Save General", command=self.save(general)).pack(side=LEFT, padx=20)
        Button(frm_bottom, text="Save Daily WordCount", command=self.save(total)).pack(side=LEFT)
        Button(frm_bottom, text="Save Daily ProjectsCount", command=self.save(projects)).pack(side=LEFT)
        Button(frm_bottom, text="Save Daily Stats", command=self.save(info)).pack(side=LEFT)
        self.tables = [general, total, projects, info]

    def save(self, table):
        return lambda: table.save()

    def save_all(self):
        for f in self.tables:
            self.save(f)()


class FailuresTab(BaseComponent):
    tables = []

    def render(self):
        super().render()

        fails = FailuresTable(self, self.controller, prepend_date=True,
                              data_attr='clean_data', labels=FAULT_LABELS)
        fails.pack()
        handoff = HandOffTable(self, self.controller, prepend_date=True,
                               data_attr='clean_data', labels=HAND_OFF_LABELS)
        handoff.pack()

        frm_bottom = Frame(self)
        frm_bottom.pack()
        Button(frm_bottom, text="Save Failures", command=self.save(fails)).pack(side=LEFT)
        Button(frm_bottom, text="Save Handoff", command=self.save(handoff)).pack(side=LEFT)
        self.tables = [fails, handoff]

    def save(self, table):
        return lambda: table.save()

    def save_all(self):
        for f in self.tables:
            self.save(f)()


class ConfigTab(BaseComponent):
    def render(self):
        super().render()
        frm1 = Frame(self)
        frm2 = Frame(self)
        frm3 = Frame(self)
        frm1.pack()
        frm2.pack()
        frm3.pack()

        Label(frm1, text="QC Engineers wordcount and project").pack()
        SheetSelect(frm1, self.controller, "INTERNAL_SHEET", True).pack()

        Label(frm2, text="Main report").pack()
        SheetSelect(frm2, self.controller, "FAILURES_SHEET", True).pack()

        Label(frm3, text="HandOff report").pack()
        SheetSelect(frm3, self.controller, "HAND_OFF_SHEET", True).pack()


class SheetSelect(BaseComponent):
    def __init__(self, master=None, controller=None, sheet_name='',
                 handle_change=False, **kwargs):
        self.sheet_name = sheet_name
        self.select = None
        self.handle_change = handle_change
        super().__init__(master, controller, **kwargs)

    @property
    def options(self):
        try:
            return self.controller.sheet_list
        except AttributeError:
            return []

    @property
    def selected_sheet(self):
        try:
            return self.controller.get_sheet(self.sheet_name)
        except AttributeError:
            return ''

    def change_handler(self, e):
        self.controller.save_sheet(
            self.sheet_name, self.select.get()
        )

    def get(self, *args, **kwargs):
        return self.select.get(*args, **kwargs)

    def render(self):
        super(SheetSelect, self).render()
        self.select = InputSelect(
            self,
            width=50,
            on_change=self.change_handler,
            values=self.options
        )
        if self.selected_sheet:
            self.select.set(self.selected_sheet)

        self.select.pack()
