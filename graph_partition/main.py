
import sys
from graph_partition.cli import guided
from graph_partition.experiment import experiment

def cli(args=None):
    """
    test
    """
    if not args:
        args = sys.argv[1:]

    if len(args) == 0:
        guided()
        return

    # if we are here, then we have command line arguments

    for argument in args:
        if argument in ["-h","-help"]:
            print("Try entering the command: 'partition'")
            print("Conduct numerical experiments with 'partition -exp' or 'partition -e'")
            return
        if argument in ['-exp','-e']:
            experiment()
