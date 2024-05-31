from question import Question
from filters.questionFilter import QuestionPoolFilter

class Categories(QuestionPoolFilter):
    default = lambda: ["all"]

    def __init__(self, categories: list[str]):
        self.categories = [category and Question.questionCategory[category] for category in categories]

    def filter(self, question_tuple: (int, int, int)) -> bool:
        temp_question = Question(*question_tuple, initGetTex=False)
        return temp_question.category in self.categories
