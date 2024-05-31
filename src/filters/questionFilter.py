from abc import ABC, abstractmethod

class QuestionPoolFilter(ABC):
    @abstractmethod
    def __init__(self):
        pass

    @staticmethod
    @abstractmethod
    def default():
        """
        Abstract static member used by caller to determine whether or not to construct a filter.

        That is, if the user does not wish to filter by a certain method then the filter need not
        be constructed after comparing arguments with the below value. (Ad-hoc construction)
        """
        pass

    @abstractmethod
    def filter(self, question_tuple: (int, int, int)) -> bool:
        """
        Predicate used to filter questions in a QuestionPool.
        """
        pass
