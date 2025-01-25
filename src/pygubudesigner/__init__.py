import os

# Activate translations of pygubu plugin strings
os.environ["PYGUBU_LAZY_TRANSLATOR"] = "Y"

# Notify pygubu is running
os.environ["PYGUBU_DESIGNER_RUNNING"] = "Y"


__version__ = "0.40.1"
