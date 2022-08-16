# encoding: utf8
import sys
from cx_Freeze import setup, Executable

# Dependencies are automatically detected, but it might need fine tuning.
build_exe_options = {
    "packages": [
        "os",
        "tkinter",
        "tkinter.messagebox",
        "tkinter.ttk",
        # Pygubu packages:
        "pygubu.plugins.tk.tkstdwidgets",
        "pygubu.plugins.ttk.ttkstdwidgets",
        "pygubu.plugins.pygubu.dialog",
        "pygubu.plugins.pygubu.editabletreeview",
        "pygubu.plugins.pygubu.scrollbarhelper",
        "pygubu.plugins.pygubu.scrolledframe",
        "pygubu.plugins.pygubu.tkscrollbarhelper",
        "pygubu.plugins.pygubu.tkscrolledframe",
        "pygubu.plugins.pygubu.pathchooserinput",
        #
        # Uncomment the following module lines if you are using this plugins:
        #
        # awesometkinter:
        #   'pygubu.plugins.awesometkinter.button',
        #   'pygubu.plugins.awesometkinter.frame',
        #   'pygubu.plugins.awesometkinter.label',
        #   'pygubu.plugins.awesometkinter.progressbar',
        #   'pygubu.plugins.awesometkinter.scrollbar',
        #   'pygubu.plugins.awesometkinter.text',
        # tkcalendar:
        #   'pygubu.plugins.tkcalendar.calendar',
        #   'pygubu.plugins.tkcalendar.dateentry',
        # tkintertable:
        #   'pygubu.plugins.tkintertable.table',
        # tksheet:
        #   'pygubu.plugins.tksheet.sheet',
        # ttkwidgets:
        #   'pygubu.plugins.ttkwidgets.calendar',
        #   'pygubu.plugins.ttkwidgets.autocomplete',
        #   'pygubu.plugins.ttkwidgets.checkboxtreeview',
        #   'pygubu.plugins.ttkwidgets.color',
        #   'pygubu.plugins.ttkwidgets.font',
        #   'pygubu.plugins.ttkwidgets.frames',
        #   'pygubu.plugins.ttkwidgets.itemscanvas',
        #   'pygubu.plugins.ttkwidgets.linklabel',
        #   'pygubu.plugins.ttkwidgets.scaleentry',
        #   'pygubu.plugins.ttkwidgets.scrolledlistbox',
        #   'pygubu.plugins.ttkwidgets.table',
        #   'pygubu.plugins.ttkwidgets.tickscale',
        # tkinterweb:
        #   'pygubu.plugins.tkinterweb.htmlwidgets',
    ],
    "include_files": ["myapp.ui", "imgs"],
}

# GUI applications require a different base on Windows (the default is for a
# console application).
base = None
if sys.platform == "win32":
    base = "Win32GUI"

setup(
    name="myapp",
    version="0.1",
    description="My GUI application!",
    options={"build_exe": build_exe_options},
    executables=[Executable("myapp.py", base=base)],
)
