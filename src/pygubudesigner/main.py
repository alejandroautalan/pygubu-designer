# This file is part of pygubu.

#
# Copyright 2012-2022 Alejandro Autalán
#
# This program is free software: you can redistribute it and/or modify it
# under the terms of the GNU General Public License version 3, as published
# by the Free Software Foundation.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranties of
# MERCHANTABILITY, SATISFACTORY QUALITY, or FITNESS FOR A PARTICULAR
# PURPOSE.  See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along
# with this program.  If not, see <http://www.gnu.org/licenses/>.
#
# For further info, check  http://pygubu.web.here

import sys
import os
import argparse
import importlib
import importlib.metadata as pkgmeta
import logging
import platform
import tkinter as tk

from pathlib import Path

from pygubu.component.plugin_manager import PluginManager
from pygubu.stockimage import StockImage, StockImageException


selected_level = os.getenv("LOGLEVEL", "WARNING")
loglevel = getattr(logging, selected_level, logging.WARNING)

logging.basicConfig(
    level=loglevel,
    format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
    datefmt="%Y%m%d %H:%M:%S",
)

# Initialize logger
logger = logging.getLogger(__name__)


# Initialize images
DATA_DIR = Path(__file__).parent / "data"

imgformat = "images-gif"
if tk.TkVersion >= 8.6:
    imgformat = "images-png"

IMAGES_DIR = DATA_DIR / "images"
IMAGE_PATHS = [  # (dir, tag)
    (IMAGES_DIR, ""),
    (IMAGES_DIR / imgformat, ""),
    (IMAGES_DIR / imgformat / "widgets" / "22x22", "22x22-"),
    (IMAGES_DIR / imgformat / "widgets" / "16x16", "16x16-"),
    (IMAGES_DIR / imgformat / "widgets" / "fontentry", ""),
]
for dir_, prefix in IMAGE_PATHS:
    StockImage.register_all_from_dir(dir_, prefix)


def init_plugin_widgets():
    """Loads all widgets from registered plugins.

    This needs to be run before the root window is created.
    """
    # Initialize all builders from plugins
    all_modules = []
    for plugin in PluginManager.builder_plugins():
        all_modules.extend(plugin.get_all_modules())
    for _module in all_modules:
        try:
            importlib.import_module(_module)
        except (ModuleNotFoundError, ImportError) as e:
            logger.exception(e)
            msg = f"Failed to load widget module: '{_module}'"
            raise RuntimeError(msg) from e

    # Initialize designer plugins
    PluginManager.load_designer_plugins()


def start_pygubu():
    pugubu_version = pkgmeta.version("pygubu")
    designer_version = pkgmeta.version("pygubu-designer")
    print(f"python: {platform.python_version()} on {sys.platform}")
    print(f"tk: {tk.TkVersion}")
    print(f"pygubu: {pugubu_version}")
    print(f"pygubu-designer: {designer_version}")

    # Setup logging level
    parser = argparse.ArgumentParser()
    parser.add_argument("filename", nargs="?")
    parser.add_argument("--loglevel")
    args = parser.parse_args()

    if args.loglevel:
        loglevel = str(args.loglevel).upper()
        loglevel = getattr(logging, loglevel, logging.WARNING)
        logging.getLogger("").setLevel(loglevel)

    #
    # Dependency check
    #
    help = "Hint, If your are using Debian, install package python3-appdirs."
    check_dependency("platformdirs", "4.4.0", help)

    init_plugin_widgets()

    from .services.main_window import MainWindow

    app = MainWindow()

    filename = args.filename
    if filename is not None:
        app.load_file(filename)

    app.run()


def check_dependency(modulename, version, help_msg=None):
    try:
        module = importlib.import_module(modulename)
        for attr in ("version", "__version__", "ver", "PYQT_VERSION_STR"):
            v = getattr(module, attr, None)
            if v is not None:
                break
        logger.info(f"Module {modulename} imported ok, version {v}")
    except ImportError:
        logger.error(
            f"I can't import module {modulename!r}. You need to have installed "
            + f"{modulename!r} version {version} or higher. {help_msg or ''}"
        )
        sys.exit(-1)


if __name__ == "__main__":
    start_pygubu()
