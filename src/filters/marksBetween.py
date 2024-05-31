import pyexcel_ods as pe
from filters.questionFilter import QuestionPoolFilter

class MarksBetween(QuestionPoolFilter):
    default = lambda: None

    def __init__(self, mark_range: list[int], spreadsheet_name: str):
        self.markRange = range(mark_range[0], mark_range[1]+1)
        self.spreadsheetMap = {} # Maps from question tuple to mark.

        spreadsheet = pe.get_data(spreadsheet_name)
        for name, sheet in spreadsheet.items():
            paper = int(name[-1])
            for i, row in enumerate(sheet):
                for j, entry in enumerate(row):
                    try:
                        year = int(row[0])
                        question_number = int(sheet[1][j])

                        if entry == "":
                            entry = -1
                        elif entry == "?":
                            entry = 0
                        else:
                            entry = int(entry) or -2

                        self.spreadsheetMap[hash((paper, year, question_number))] = entry
                    except:
                        continue

    def filter(self, question_tuple: (int, int, int)) -> bool:
        return (-1 in self.markRange and hash(question_tuple) not in self.spreadsheetMap) or (hash(question_tuple) in self.spreadsheetMap \
            and self.spreadsheetMap[hash(question_tuple)] in self.markRange)
