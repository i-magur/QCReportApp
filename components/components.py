from components.base import BaseTable
from utils.utils import WORDCOUNT, FAULT_IDX, FAULT_INDEXES, HAND_OFF_IDX, HAND_OFF_INDEXES


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
