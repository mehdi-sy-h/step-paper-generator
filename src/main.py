import question, paper
import sys, argparse
from questionPool import QuestionPool

def main(args: argparse.Namespace=None):
    parser = argparse.ArgumentParser(prog="stepgen",
            description="Generates custom step papers.",
            formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    parser.add_argument("--categories",
            default="[all]", nargs='*',
            choices=["all", "pure", "mech", "stats"],
            help="List of categories to choose questions from. A category is one of "
            "'pure', 'mech', 'stats' or 'all'. For example, passing '--category stats mech' "
            "chooses statistics and mechanics questions. Passing 'all' considers every category. "
            "NOTE: Questions before 1994 are not given a category and are thus not chosen unless "
            "'all' is passed.")

    parser.add_argument("-c", "--count",
            type=int, default=6,
            help="The maximum number of questions the paper(s) should have.")

    parser.add_argument("-d", "--during",
            type=int, default=[1987,2018], nargs='*',
            help="Either a single value to denote a single year, or two values to denote a closed "
            "interval of years. Questions are chosen according to the year(s) given by this value. "
            "For example, passing '--during 1990 2010' yields questions from [1990, 2010]. Simply "
            "passing '--during 1990' yields questions from 1990.")

    parser.add_argument("-m", "--marks-between",
            type=int, nargs="*",
            help="The spreadsheet file given by --spreadsheet is read and questions have a mark "
            "inclusively within the interval are chosen. Entries labelled '?' in the spreadsheet are always "
            "considered as possible questions, irrespective of the value of MARKS_BETWEEN."
            "An unmarked question is treated as having a mark of -1."
            "NOTE: If MARKS_BETWEEN is given, then a suitable ods spreadsheet must also be given!")

    parser.add_argument("-p", "--papers",
            type=int, default=[1,2,3], nargs='*',
            help="The paper (numbers) from which questions should be chosen. For example, if "
            "'--papers 1 3' is passed then questions are chosen from STEP 1 and STEP 3.")

    parser.add_argument("-q", "--quantity",
            type=int, default=1,
            help="A QUANTITY number of papers are generated. A question in one generated paper "
            "will not appear in another if produced in this fashion. If the possible question "
            "sample has been restricted beyond COUNT*QUANTITY then the entire sample pool is given. "
            "The last paper generated will have an appropriate number of questions less than COUNT.")

    parser.add_argument("-s", "--spreadsheet",
            help="If the --marks-between argument is given then this argument should refer to the "
            "'.ods' spreadsheet of marks. The spreadsheet must have structure identical to the "
            "progress.ods file given in this repository (under the data folder). "
            "NOTE: The spreadsheet must be an ods file! "
            "NOTE: If --marks-below is given then this argument must also be given")

    parser.add_argument("-tit", "--title",
            help="TITLE is used as the file name of the generated paper(s) and is shown in the paper "
            "itself at the top (as a LaTeX \section). By default this is automatically generated from "
            "other arguments given.")

    parser.add_argument("-t", "--topics",
            nargs='*', default = ["all"],
            help="If passed, stepdatabase.maths.org will be queried for questions with tags with each "
            "TOPIC individually. For example if '--topics \"complex numbers\"  \"vectors\"' is passed then "
            "the program will search stepdatabase for questions with tag 'complex numbers' and then "
            "tag 'vectors'. The union of the two results are then considered as possible questions. "
            "NOTE: Wrap each search query around single or double quotes!")

    parser.add_argument("-l", "--latexsearch",
                default = ["all"],
                nargs ='*',
                help= "Only questions which contain LATEXSEARCH in their latex file will be returned. For example "
                "if '--latexsearch \"\\sum \"' is passed then only questions containing sigmas will be returned."
        )

    args = args or parser.parse_args()
    pool = QuestionPool()

    if args.marks_between and args.spreadsheet:
        pool.filter("marksBetween", args.marks_between, args.spreadsheet)
    if args.topics:
        pool.filter("topics", args.topics)

    if not args.title:
        args.title = "STEP {}, Category: {}".format(args.papers, args.categories)

    pool.filter("categories", args.categories)
    pool.filter("during", args.during)
    pool.filter("papers", args.papers)
    pool.filter("latexSearch", args.latexsearch)

    pool.shuffle()

    # Partition pool into count sized subsets (from here we need only the underlying data)
    pool = pool.getQuestionTuples()

    pool_partition = []
    for i in range(0, len(pool), args.count):
        pool_partition.append(pool[i:i+args.count])

    question_partition = [[] for _ in range(len(pool_partition))]
    for i, subset in enumerate(pool_partition):
        for question_tuple in subset:
            newQuestion = question.Question(*question_tuple)
            question_partition[i].append(newQuestion)

    for i in range(min(len(question_partition), args.quantity)):
        paper.Paper(question_partition[i], args.title).compile()

if __name__ == "__main__":
    main()
