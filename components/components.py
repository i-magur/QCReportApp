from components.base import BaseTable
from utils.utils import WORDCOUNT, FAULT_IDX, FAULT_INDEXES


# class Table(BaseComponent):
#     def __init__(self, master=None, headings_attr="headings", **kwargs):
#         self.headings_attr = headings_attr
#         super().__init__(master, **kwargs)
#
#     def copy_text(self, e):
#         if not self.data:
#             return None
#         content = "\n".join(["\t".join([str(col) for col in row]) for row in self.data])
#         copy_text(self, content)
#
#     def update_data(self, name="data", value=None):
#         setattr(self, name, value)
#         self.render()
#
#     @property
#     def headings(self):
#         return getattr(self.controller, self.headings_attr)
#
#     def initialize(self):
#         if not self.data:
#             return None
#         table = Treeview(
#             self.frame, show="headings",
#             columns=self.headings
#         )
#         for h in self.headings:
#             table.heading(h, text=h)
#
#         for idx, r in enumerate(self.data):
#             table.insert("", index=idx, values=r)
#
#         table.pack(padx=10, pady=10)
#         bind_tree(table, "<Button-1>", self.copy_text)


class WordCountTable(BaseTable):
    def get_content(self):
        return "\t".join(map(str, self.prepare_data()[0]))

    def prepare_data(self):
        return [[row[1] for row in self.data]]


class ProjectsCountTable(BaseTable):
    def get_content(self):
        return "\t".join(map(str, self.prepare_data()[0]))

    def prepare_data(self):
        return [[row[2] for row in self.data]]


class InfoRow(BaseTable):
    def get_content(self):
        return "\t".join(map(str, self.prepare_data()[0]))

    def prepare_data(self):
        return [[
            sum(map(int, [i[WORDCOUNT] for i in self.data])),
            len(self.data),
            150000
        ]]


class GeneralInfo(BaseTable):
    def get_content(self):
        return "\n".join(["\t".join([str(col) for col in row]) for row in self.prepare_data()])

    def prepare_data(self):
        return self.data


class FailuresTable(BaseTable):
    def prepare_data(self):
        data = []
        for row in self.data:
            if not row[FAULT_IDX]:
                data.append([row[idx] for idx in FAULT_INDEXES])
        return data

