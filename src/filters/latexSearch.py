from question import Question
from filters.questionFilter import QuestionPoolFilter

class LatexSearch(QuestionPoolFilter):
    default = lambda: ["all"]

    def __init__(self, queries: list[str]):
        self.queries = queries

    def filter(self, question_tuple: (int, int, int)) -> bool:
        temp_question = Question(*question_tuple)
        for query in self.queries:
            if temp_question.tex.lower().find(query.lower()) != -1:
                return True
        return False
