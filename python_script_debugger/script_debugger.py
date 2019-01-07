from __future__ import print_function
import pprint
from IPython import get_ipython
from IPython import embed
import IPython
import os
import shutil
import sys
from contextlib import contextmanager

"""
This script allows to launch a python program with some debug and exploration properties.

Can be set up as a bash script, for example by adding to the .bashrc the following:

# launch a python script with the debug script
pds(){
    ipython /home/jrlab/Desktop/Git/python_script_debugger/python_script_debugger/script_debugger.py -- $1
}
"""


@contextmanager
def use_tempfile(exec_location, folder_name_line_by_line='line_exec'):
    """A context mangager for a temp folder ressource. This way, we clean
    after us whatever happens."""
    # acquire resource
    path_folder_line_by_line = os.path.join(exec_location, folder_name_line_by_line)

    if not os.path.exists(path_folder_line_by_line):
        os.makedirs(path_folder_line_by_line)
    else:
        raise Exception('already existing line exec folder at {}'.format(path_folder_line_by_line))

    try:
        yield path_folder_line_by_line
    finally:
        # release resource
        # clear the folder
        shutil.rmtree(path_folder_line_by_line)


def split_code_into_valid_cells(path_to_code, DEBUG=False):
    """Split the code in the file path_to_code into a successions of valid cells
    indexed by integers (from 0) in a dictionary.

    TODO: allow options for other kinds of splitting; for example, using markers or
    spaces between lines of code."""

    crrt_execution_cell = 0
    dict_valid_cells = {}
    dict_valid_cells[crrt_execution_cell] = []

    with open(path_to_code) as fh:
        for crrt_line in fh:
        # if crrt_line == "\n":
            #     continue

            # if not time for a new cell
            if crrt_line[0:4] == "    ":
                dict_valid_cells[crrt_execution_cell].append(crrt_line)

            # otherwise, time for a new cell
            else:
                crrt_execution_cell += 1
                dict_valid_cells[crrt_execution_cell] = []
                dict_valid_cells[crrt_execution_cell].append(crrt_line)

    if DEBUG:
        pprint(dict_valid_cells)

    dict_valid_cells["number_valid_cells"] = crrt_execution_cell

    return(dict_valid_cells)


def write_all_cells(dict_valid_cells, basename_execution_cell, DEBUG=False):
    """Write all cells in dict_valid_cells at the basename_execution_cell location,
    appending with cell number and the .py extension"""

    number_of_cells = dict_valid_cells["number_valid_cells"]

    for crrt_cell in range(number_of_cells):
        crrt_cell += 1

        with open(basename_execution_cell + "{}.py".format(crrt_cell), 'w') as fh:
            # write the cells before; need comment to avoid code re-run; here for clarity of error message and line numbering
            for cell_before in range(crrt_cell):
                for crrt_line in dict_valid_cells[cell_before]:
                    fh.write("#-{}-> ".format(cell_before))
                    fh.write(crrt_line)

            # the whole current valid cell
            for crrt_line in dict_valid_cells[crrt_cell]:
                fh.write(crrt_line)

            # write the cells after; here for clarity of error message and line numbering
            for cell_after in range(crrt_cell + 1, number_of_cells + 1, 1):
                for crrt_line in dict_valid_cells[cell_after]:
                    fh.write("#{}-> ".format(cell_after))
                    fh.write(crrt_line)


# TODO: get it as a command line argument
DEBUG=False

# first arg is what to run
path_to_code = sys.argv[1]

# TODO: allow following args in command line to be used by script

"""Running a script for debugging; cut the script into valid IPython cells, execute one by one,
and give control to the user if some problems.

NOTE: this CANNOT be refactored inside a function without some tricks, otherwise some headache with scope of variables
kills the possibility to interact with the code when the IPython is opened in console.

Consider fixing it by looking for example at:

https://stackoverflow.com/questions/35161324/how-to-make-imports-closures-work-from-ipythons-embed

"""

if DEBUG:
    print(sys.argv)

print("execute {} \n\n".format(path_to_code))

# split the code into execution cells
dict_valid_cells = split_code_into_valid_cells(path_to_code)

# create the folder for line by line execution, at the location of the script
# TODO: changing directory may lead to breaking some dirty hacks, for example imports from relative paths...
# TODO: maybe give option to use some hidden .tmp files?
exec_location = os.getcwd()

# temporary folder exists only in this context
with use_tempfile(exec_location) as path_folder_line_by_line:

    basename_execution_cell = os.path.join(path_folder_line_by_line, 'cell_')

    # write all the cells; the first one is always empty, ignore
    write_all_cells(dict_valid_cells, basename_execution_cell, DEBUG=DEBUG)

    # execute cell by cell
    number_of_cells = dict_valid_cells["number_valid_cells"]

    ipython = get_ipython()
    # ipython.magic("pdb")  # this is to put the magics; but probably we do not want it by default

    # TODO: much can be improved here. For example:
    # TODO: choose between run debugger on cell, run own code in IPython, open cell in vim and re-execute upon quitting
    # TODO: also, how to grab modified code? re-assemble from cells, log (intercept std streams) all inputs outputs, etc
    for crrt_cell in range(number_of_cells ):
        crrt_cell += 1

        with open("{}{}.py".format(basename_execution_cell, crrt_cell), 'r') as myfile:
            code = myfile.read()

            if DEBUG:
                print("running cell {}:\n{}".format(crrt_cell, code))

            res = ipython.run_cell(code)

            if DEBUG:
                print(res)

            # TODO: give more control to the use; relaunch cell in debug mode? jump over? jump over X cells? show more code around? launch IPython?
            if res.error_in_exec is not None:
                print(" ")
                
                embed(banner1="\r", header="start IPython from exception point:", exit_msg="\nresuming at next line\n\n\n")

    # TODO: decide what to do with the user input

