# Curtis Kennedy
# ckennedy@ualberta.ca

import sys
from graph_partition.cli import guided, experiment

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
            print("Try entering the command: 'partition -guide' or 'partition -g'")
            print("Conduct numerical experiments with 'partition -exp' or 'partition -e'")
            return
        if argument in ['-guided','-g']:
            guided()
            return
        if argument in ['-exp','-e']:
            experiment()

    # # * Since only one command is currently supported, just call guided() for now
    # guided()



    


