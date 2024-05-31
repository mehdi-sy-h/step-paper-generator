from filters.questionFilter import QuestionPoolFilter

class Papers(QuestionPoolFilter):
    default = lambda: [1, 2, 3]

    def __init__(self, papers: list[int]):
        self.papers = papers

    def filter(self, question_tuple: (int, int, int)) -> bool:
        return question_tuple[0] in self.papers
