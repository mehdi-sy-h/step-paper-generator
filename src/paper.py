import os.path as path
import os, tempfile, subprocess, shutil

class Paper:
    def __init__(self, questions, title=''):
        self.questions = questions
        self.count = len(questions)
        self.title = title

    def compile(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            tex = ""
            src_dir = path.dirname(__file__)
            rel_dir = "../data/template.tex"
            with open(path.join(src_dir, rel_dir), 'r') as tex_file:
                tex = tex_file.read()

            tex = tex.replace("%title", r"\section*{" + self.title + r'}')

            for i, question in enumerate(self.questions):
                question_file_name = "{}_{}_{}".format(question.paper,
                        str(question.year)[-2:].rjust(2, '0'), question.number)

                question_tex = question.tex \
                    .replace(r"\setcounter{qnumber}{0}", r"\setcounter{qnumber}{"+str(i)+'}')

                with open(path.join(temp_dir, question_file_name+".tex"), 'w') as question_file:
                    question_file.write(question_tex)

                tex = tex.replace(r"%sub", r"\import{" + question_file_name + '}' + "\n%sub")

            tex_file_name = self.title
            increment = 0
            while path.exists(path.join(os.getcwd(), tex_file_name+".pdf")):
                increment += 1
                tex_file_name = self.title + f" ({increment})"

            with open(path.join(temp_dir, tex_file_name+".tex"), 'w') as tex_file:
                tex_file.write(tex)

            subprocess.run(["latexmk", "-f", "-pdf", "--interaction=nonstopmode",
                tex_file_name+".tex"], cwd=temp_dir, stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL)

            shutil.move(path.join(temp_dir, tex_file_name+".pdf"), os.getcwd())
