from tkinter import LEFT

from UI.widgets import Frame, Label
from components.base import BaseTable, BaseComponent
from utils.utils import WORDCOUNT, FAULT_IDX, FAULT_INDEXES, HAND_OFF_IDX, HAND_OFF_INDEXES, DEFAULT_ORDER, \
    FAULT_LABELS, HAND_OFF_LABELS


class WordCountTable(BaseTable):
    def prepare_data(self):
        return [[row[1] for row in self.data]]


class ProjectsCountTable(BaseTable):
    def prepare_data(self):
        return [[row[2] for row in self.data]]


class InfoRow(BaseTable):
    def prepare_data(self):
        return [[
            sum(map(int, [i[WORDCOUNT] for i in self.data])),
            len(self.data),
            150000
        ]]


class GeneralInfo(BaseTable):
    def prepare_data(self):
        return self.data


class FailuresTable(BaseTable):
    def prepare_data(self):
        data = []
        for row in self.data:
            if not row[FAULT_IDX]:
                data.append([row[idx] for idx in FAULT_INDEXES])
        return data


class HandOffTable(BaseTable):
    def prepare_data(self):
        data = []
        for row in self.data:
            if row[HAND_OFF_IDX]:
                data.append([row[idx] for idx in HAND_OFF_INDEXES])
        return data


class GeneralTab(BaseComponent):
    def pre_render(self):
        for w, c in zip([0, 1, 1, 0], range(4)):
            self.grid_columnconfigure(c, weight=w)
        for w, r in zip([0, 1, 0], range(3)):
            self.grid_rowconfigure(r, weight=w)

    def render(self):
        super().render()
        frm_left = Frame(self)
        frm_left.grid(row=1, column=1)
        table = GeneralInfo(frm_left, self.controller,
                            data_attr="users_wh", labels=self.controller.wh_headings)
        table.pack()

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


class FailuresTab(BaseComponent):
    def render(self):
        super().render()

        fails = FailuresTable(self, self.controller, prepend_date=True,
                              data_attr='clean_data', labels=FAULT_LABELS)
        fails.pack()
        handoff = HandOffTable(self, self.controller, prepend_date=True,
                               data_attr='clean_data', labels=HAND_OFF_LABELS)
        handoff.pack()


class ConfigTab(BaseComponent):
    def render(self):
        super().render()
        Label(self, text="Coming soon...").pack()
