# encoding: utf8
# setup.py
import sys
from distutils.core import setup
import py2exe

sys.argv.append("py2exe")

setup(
    console=["myapp.py"],
    data_files=[
        ("", ["myapp.ui"]),
        (
            "imgs",
            [
                "imgs/MenuIcon4.gif",
                "imgs/ps_circle.gif",
                "imgs/ps_cross.gif",
                "imgs/ps_square.gif",
                "imgs/ps_triangle.gif",
            ],
        ),
    ],
    options={
        "py2exe": {
            "includes": [
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
                # Uncomment the following module lines if you are using
                # this plugins:
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
            ]
        }
    },
)
