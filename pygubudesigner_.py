import getopt
import sys
import re

from pygubudesigner import get_setup_requirements

argv = sys.argv[1:]
opts, args = getopt.getopt(argv, "")


def print_requirements():
    print("'" + ("' '".join(get_setup_requirements())) + "'", end="")


if __name__ == "__main__":
    for arg in args:
        if arg in ["prt_req"]:
            print_requirements()

        if arg in ["start"]:
            from pygubudesigner.main import start_pygubu

            sys.argv[0] = re.sub(r"(-script\.pyw|\.exe)?$", "", sys.argv[0])
            del sys.argv[1]  # sys.argv[1] -> 'start' is not a path.
            sys.exit(start_pygubu())
