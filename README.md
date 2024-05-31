## STEP Paper Generator
A program used to generate test papers using questions previously featured in the STEP examinations. Numerous filters may be applied, and the program features the ability to read from a spreadsheet of marks
so as to generate new papers featuring questions within a certain mark interval.

There is no dependence on any web service or API (however a copy of the stepdatabase html file, and paper tex files, are provided locally under `data/`).

## Usage
1. Download the requisite pip modules (`bs4`, `pyexcel-ods`, tk/ttk).
2. Download the `latexmk` compiler and preferably whatever the largest tex package distribution your system provides (to prevent artifacts and/or errors in compilation).
3. To use the command line interface, run `main.py` (using a python3 interpreter), command line arguments and their explanations may be found by passing the `-h` or `--help` argument. Alternatively, to use the graphical interface (which is a frontend to the command line interface), run `gui.py`.
4. Provide a spreadsheet (.ods file) containing the marks acheived per question if filtration based on marks is desired. An empty template may be found at `data/progress.ods`.

## Dependencies

system
------
- python3
- latexmk

pip
---
- bs4
- pyexcel-ods
- tk
- ttk
