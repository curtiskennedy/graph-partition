# Curtis Kennedy
# ckennedy@ualberta.ca

import sys
from graph_partition.cli import guided

def cli(args=None):
    """
    OPTIONS

    When the program is run from the command line, you can pass different arguments to affect the output

    passing the -guided command line argument will run a command line menu

    passing the -name <instanceName> -k <k> will automatically partition the provided instance

    any other options??????
    """
    # if not args:
    #     args = sys.argv[1:]

    # if len(args) == 0:
    #     print("Try entering the command: 'partition -guided'")
    #     return

    # # if we are here, then we have command line arguments

    # for argument in args:
    #     if argument in ["-h", "-help"]:
    #         print("Try entering the command: 'partition -guided'")
    #         return
    #     if argument == "-guided":
    #         guided()

    # * Since only one command is currently supported, just call guided() for now
    guided()



    


