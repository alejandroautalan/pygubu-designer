import getopt
import sys

from pygubudesigner import get_setup_requirements

argv = sys.argv[1:]
opts, args = getopt.getopt(argv, "")


def print_requirements():
    print("'" + ("' '".join(get_setup_requirements())) + "'", end="")


if __name__ == "__main__":
    for arg in args:
        if arg in ["prt_req"]:
            print_requirements()
