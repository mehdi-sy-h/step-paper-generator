import random
from filters import questionFilter, categories, during, latexSearch, marksBetween, papers, topics

def get_question_tuples() -> list((int, int, int)):
    question_tuple_pool = []
    for paper in range(1,4):
        for year in range(1987, 2018):
            question_range = None

            if year in range(1987, 1994):
                question_range = range(1, 17)
            elif year in range(1994, 2008):
                question_range = range(1, 15)
            elif year in range(2008, 2019):
                question_range = range(1, 14)

            for question in question_range:
                question_tuple_pool.append((paper, year, question))

    return question_tuple_pool

class QuestionPool:
    filterMap = {
        "categories": categories.Categories,
        "during": during.During,
        "latexSearch": latexSearch.LatexSearch,
        "marksBetween": marksBetween.MarksBetween,
        "papers": papers.Papers,
        "topics": topics.Topics
    }

    def __init__(self):
        self.__filters = {}
        self.__question_tuples = get_question_tuples()

    def filter(self, filter_method, *args, **kwargs):
        filter_class = QuestionPool.filterMap[filter_method]

        default = filter_class.default()
        if default in args or default in kwargs.values():
            return

        filter_obj = filter_class(*args, **kwargs)
        self.__question_tuples = list(filter(filter_obj.filter, self.__question_tuples))

    def getQuestionTuples(self):
        return self.__question_tuples

    def shuffle(self):
        random.shuffle(self.__question_tuples)
