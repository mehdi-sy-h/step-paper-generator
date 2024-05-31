from filters.questionFilter import QuestionPoolFilter

class During(QuestionPoolFilter):
    default = lambda: [1987, 2018]

    def __init__(self, time_interval: list[int]):
        if len(time_interval) == 1:
            self.interval = range(time_interval[0], time_interval[0]+1)
        elif len(time_interval) == 2:
            self.interval = range(*time_interval)
        else:
            raise ValueError

    def filter(self, question_tuple: (int, int, int)) -> bool:
        return question_tuple[1] in self.interval
