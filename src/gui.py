import main as stepgen
import tkinter as tk
from argparse import Namespace
from tkinter import ttk, filedialog

# Closure to avoid repeatedly passing row, column etc when
# only trivial listing is required.
def grid_push_generator():
    row_inc = 0
    grid_uniform_pad = lambda obj, i, j: \
        obj.grid(row=i, column=j, padx=5, pady=5)

    def push(objects, **kwargs):
        nonlocal row_inc

        defaults = {"row": row_inc}
        args = {**kwargs, **defaults}
        col = 0

        values = objects.values() if type(objects) is dict else objects
        for obj in values:
            grid_uniform_pad(obj, args["row"], col)
            col += 1

        row_inc += 1
        return objects

    return push

class Gui(tk.Tk):
    def __init__(self):
        super().__init__()

        self.resizable(0,0)
        self.title("STEP Suite")

        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=3)

        self.master = tk.Frame(padx=10, pady=10)
        self.master.pack()

        self.spreadsheet = None

        self.createWidgets()

    def openSpreadsheet(self):
        filetypes = (('Spreadsheet files', '*.ods'), ('All files', '*.*'))
        self.spreadsheet = filedialog.askopenfilename(filetypes=filetypes)

    def onGenerate(self):
        args = Namespace()

        args.categories = [button.state() and category for category, button in self.categoryWidgets.items()]
        args.count = int(self.countWidgets["box"].get())
        args.during = [int(self.fromWidgets["box"].get()), int(self.toWidgets["box"].get())]
        args.marks_between = [int(self.marksLowerWidgets["box"].get()), \
                              int(self.marksUpperWidgets["box"].get())]
        args.papers = [button.state() and i+1 for i, button in enumerate(self.paperWidgets)]
        args.quantity = int(self.quantityWidgets["box"].get())
        args.spreadsheet = self.spreadsheet
        args.title = self.titleWidgets["entry"].get()
        args.topics = [s.strip() for s in self.topicWidgets["entry"].get().split(',')]
        args.latexsearch = [s.strip() for s in self.latexWidgets["entry"].get().split(',')]

        stepgen.main(args)

    def createWidgets(self):
        place_objects = grid_push_generator()

        self.categoryWidgets = place_objects({
            "pure": ttk.Checkbutton(self.master, text="Pure"),
            "mech": ttk.Checkbutton(self.master, text="Mechanics"),
            "stats": ttk.Checkbutton(self.master, text="Statistics"),
        })

        self.paperWidgets = place_objects([
            ttk.Checkbutton(self.master, text="STEP 1"),
            ttk.Checkbutton(self.master, text="STEP 2"),
            ttk.Checkbutton(self.master, text="STEP 3"),
        ])

        count_box = ttk.Spinbox(self.master, **{"from": 1}, to=50)
        count_box.set(6)
        self.countWidgets = place_objects({
            "label": ttk.Label(self.master, text="Number of questions"),
            "box": count_box
        })

        quantity_box = ttk.Spinbox(self.master, **{"from": 1}, to=50)
        quantity_box.set(1)
        self.quantityWidgets = place_objects({
            "label": ttk.Label(self.master, text="Number of papers"),
            "box": quantity_box
        })

        lower_box = ttk.Spinbox(self.master, **{"from": -1}, to=20)
        lower_box.set(-1)
        self.marksLowerWidgets = place_objects({
            "label": ttk.Label(self.master, text="Marks (lower bound)"),
            "box": lower_box
        })

        upper_box = ttk.Spinbox(self.master, **{"from": -1}, to=20)
        upper_box.set(20)
        self.marksUpperWidgets = place_objects({
            "label": ttk.Label(self.master, text="Marks (upper bound)"),
            "box": upper_box
        })

        from_box = ttk.Spinbox(self.master, **{"from": 1987}, to=2018)
        from_box.set(1987)
        self.fromWidgets = place_objects({
            "label": ttk.Label(self.master, text="From (year)"),
            "box": from_box
        })

        to_box = ttk.Spinbox(self.master, **{"from": 1987}, to=2018)
        to_box.set(2018)
        self.toWidgets = place_objects({
            "label": ttk.Label(self.master, text="To (year)"),
            "box": to_box
        })

        self.spreadsheetWidgets = place_objects({
            "label": ttk.Label(self.master, text="Spreadsheet"),
            "button": ttk.Button(self.master, text="Open file",
                command=self.openSpreadsheet)
        })

        self.titleWidgets = place_objects({
            "label": ttk.Label(self.master, text="Title"),
            "entry": ttk.Entry(self.master)
        })

        self.topicWidgets = place_objects({
            "label": ttk.Label(self.master, text="Topics (comma seperated)"),
            "entry": tk.Entry(self.master)
        })

        self.latexWidgets = place_objects({
            "label": ttk.Label(self.master, text="Search"),
            "entry": tk.Entry(self.master)
        })

        self.generateButton = ttk.Button(text="Generate", command=self.onGenerate)
        self.generateButton.pack(pady=5)

if __name__ == "__main__":
    gui = Gui()
    gui.mainloop()
