import os
from enum import Enum

class Question:
    questionCategory = Enum("Category", "pure mech stats unknown")

    def __init__(self, paper, year, question_number, initGetTex=True):
        assert(year in range(1987, 2019), "Question must be from 1987-2018")
        self.year = year
        self.paper = paper
        self.number = question_number
        self.category = self.__getCategory()
        if initGetTex:
            self.tex = self.getTex()

    def getTex(self):
        file_name = "{}-{}.tex".format(str(self.year)[-2:].rjust(2, '0'), 'S'+str(self.paper))
        src_dir = os.path.dirname(__file__)
        rel_dir = f"../data/papers/{file_name}"
        data = ""
        with open(os.path.join(src_dir, rel_dir), 'r') as tex_file:
            data = tex_file.read()

        data = data.replace(r"\pagestyle{myheadings}", '')

        # Prune other questions
        question_index = -1
        for i in range(self.number):
            question_index = data.find("\\begin{question}", question_index+1)

        question_tex = data[question_index:data.find("\\end{question}", question_index)] + \
                "\n\\textbf{{(S{0} {1} Q{2})}}\n" \
                .format(self.paper, str(self.year)[-2:].rjust(2,  '0'), self.number) + "\\end{question}"

        question_tex = data[:data.find("\\begin{document}")]+ "\\begin{document}" + '\n' \
            + question_tex + '\n' + data[data.find("\\end{document}"):]

        return question_tex

    def __getCategory(self):
        year = self.year
        num = self.number

        if year in range(1994, 2008):
            if num in range(1, 9):
                return Question.questionCategory.pure
            elif num in range(9, 12):
                return Question.questionCategory.mech
            elif num in range(12, 15):
                return Question.questionCategory.stats

        elif year in range(2008, 2018):
            if num in range(1, 9):
                return Question.questionCategory.pure
            elif num in range(9, 11):
                return Question.questionCategory.mech
            elif num in range(12, 14):
                return Question.questionCategory.stats

        return Question.questionCategory.unknown
