import os.path as path
import os, tempfile, subprocess, shutil

from bs4 import BeautifulSoup
from filters.questionFilter import QuestionPoolFilter

class Topics(QuestionPoolFilter):
    default = lambda: ["all"]

    def __init__(self, topics: list[str]):
        src_dir = path.dirname(path.dirname(__file__))
        rel_dir = "../data/STEP_Questions_Database.html"
        topic_question_map = {}

        with open(path.join(src_dir, rel_dir), "r") as step_qns:
            soup = BeautifulSoup(step_qns.read(), "html.parser")

            for element in soup.find_all("li"):
                try:
                    link = element.find("a")
                    question = link.contents[0]

                    item = element.find("i")
                    qn_topics = (item.contents[0].contents[0].contents[0])

                    topic_question_map[question] = qn_topics.lower()
                except:
                    pass

        self.topics = topics
        self.topicQuestionMap = topic_question_map

    def filter(self, question_tuple: (int, int, int)) -> bool:
        if "all" in self.topics:
            return True

        name = str(question_tuple[1])[2:4] + "-S" + str(question_tuple[0]) + "-Q" + str(question_tuple[2])
        if not name in self.topicQuestionMap:
            return False

        questionTopics = self.topicQuestionMap[name]
        for topic in self.topics:
            if questionTopics.find(topic.lower()) != -1:
                return True

        return False
