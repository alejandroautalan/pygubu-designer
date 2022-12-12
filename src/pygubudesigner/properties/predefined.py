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

import logging
import platform
import tkinter as tk

from pygubu.component.builderobject import CUSTOM_PROPERTIES

from .propertieshelp import help_for

logger = logging.getLogger(__name__)


TK_BITMAPS = (
    "error",
    "gray75",
    "gray50",
    "gray25",
    "gray12",
    "hourglass",
    "info",
    "questhead",
    "question",
    "warning",
)

TK_BITMAPS_MAC = (
    "document",
    "stationery",
    "edition",
    "application",
    "accessory",
    "forder",
    "pfolder",
    "trash",
    "floppy",
    "ramdisk",
    "cdrom",
    "preferences",
    "querydoc",
    "stop",
    "note",
    "caution",
)

TK_CURSORS = (
    "arrow",
    "based_arrow_down",
    "based_arrow_up",
    "boat",
    "bogosity",
    "bottom_left_corner",
    "bottom_right_corner",
    "bottom_side",
    "bottom_tee",
    "box_spiral",
    "center_ptr",
    "circle",
    "clock",
    "coffee_mug",
    "cross",
    "cross_reverse",
    "crosshair",
    "diamond_cross",
    "dot",
    "dotbox",
    "double_arrow",
    "draft_large",
    "draft_small",
    "draped_box",
    "exchange",
    "fleur",
    "gobbler",
    "gumby",
    "hand1",
    "hand2",
    "heart",
    "icon",
    "iron_cross",
    "left_ptr",
    "left_side",
    "left_tee",
    "leftbutton",
    "ll_angle",
    "lr_angle",
    "man",
    "middlebutton",
    "mouse",
    "none",
    "pencil",
    "pirate",
    "plus",
    "question_arrow",
    "right_ptr",
    "right_side",
    "right_tee",
    "rightbutton",
    "rtl_logo",
    "sailboat",
    "sb_down_arrow",
    "sb_h_double_arrow",
    "sb_left_arrow",
    "sb_right_arrow",
    "sb_up_arrow",
    "sb_v_double_arrow",
    "shuttle",
    "sizing",
    "spider",
    "spraycan",
    "star",
    "target",
    "tcross",
    "top_left_arrow",
    "top_left_corner",
    "top_right_corner",
    "top_side",
    "top_tee",
    "trek",
    "ul_angle",
    "umbrella",
    "ur_angle",
    "watch",
    "xterm",
    "X_cursor",
)

TK_CURSORS_WINDOWS = (
    "no",
    "starting",
    "size",
    "size_ne_sw" "size_ns",
    "size_nw_se",
    "size_we",
    "uparrow",
    "wait",
)

TK_CURSORS_MAC = (
    "copyarrow",
    "aliasarrow",
    "contextualmenuarrow",
    "text",
    "cross-hair",
    "closedhand",
    "openhand",
    "pointinghand",
    "resizeleft",
    "resizeright",
    "resizeleftright",
    "resizeup",
    "resizedown",
    "resizeupdown",
    "notallowed",
    "poof",
    "countinguphand",
    "countingdownhand",
    "countingupanddownhand",
    "spinning",
)

if platform.system() == "Darwin":
    TK_BITMAPS = TK_BITMAPS + TK_BITMAPS_MAC
    TK_CURSORS = TK_CURSORS + TK_CURSORS_MAC
elif platform.system() == "Windows":
    TK_CURSORS = TK_CURSORS + TK_CURSORS_WINDOWS

TK_RELIEFS = (tk.FLAT, tk.RAISED, tk.SUNKEN, tk.GROOVE, tk.RIDGE)

PROPERTY_DEFINITIONS = {
    "class": {
        "editor": "dynamic",
        "params": {"mode": "entry", "state": "readonly"},
        "help": help_for("class"),
    },
    "id": {
        "editor": "dynamic",
        "params": {"mode": "namedid"},
        "help": help_for("id"),
    },
    # - #
    "accelerator": {
        "editor": "dynamic",
        "params": {"mode": "entry"},
        "help": help_for("accelerator"),
    },
    "activerelief": {
        "editor": "dynamic",
        "params": {
            "mode": "choice",
            "values": (
                "",
                tk.FLAT,
                tk.RAISED,
                tk.SUNKEN,
                tk.GROOVE,
                tk.RIDGE,
            ),
            "state": "readonly",
        },
        "help": help_for("activerelief"),
    },
    "activestyle": {
        "editor": "dynamic",
        "params": {
            "mode": "choice",
            "values": ("", "underline", "dotbox", "none"),
            "state": "readonly",
        },
        "help": help_for("activestyle"),
    },
    "activebackground": {
        "editor": "dynamic",
        "params": {"mode": "colorentry"},
        "help": help_for("activebackground"),
    },
    "activeborderwidth": {
        "editor": "dynamic",
        "params": {"mode": "dimensionentry"},
        "help": help_for("activeborderwidth"),
    },
    "activeforeground": {
        "editor": "dynamic",
        "params": {"mode": "colorentry"},
        "help": help_for("activeforeground"),
    },
    "after": {
        "editor": "dynamic",
        "params": {"mode": "entry"},
        "help": help_for("after"),
    },
    # ttk.Label
    "anchor": {
        "editor": "dynamic",
        "params": {
            "mode": "choice",
            "values": (
                "",
                "n",
                "ne",
                "nw",
                "e",
                "w",
                "s",
                "se",
                "sw",
                "center",
            ),
            "state": "readonly",
        },
        "help": help_for("anchor"),
        "ttk.xxxx?": {
            "params": {
                "values": ("", tk.W, tk.CENTER, tk.E),
                "state": "readonly",
            }
        },
    },
    "aspect": {
        "editor": "dynamic",
        "params": {"mode": "naturalnumber"},
        "help": help_for("aspect"),
    },
    "autoseparators": {
        "editor": "dynamic",
        "params": {
            "mode": "choice",
            "values": ("", "false", "true"),
            "state": "readonly",
        },
        "help": help_for("autoseparators"),
    },
    # ttk.Label
    "background": {
        "editor": "dynamic",
        "params": {"mode": "colorentry"},
        "help": {
            "tk": help_for("background-tk"),
            "ttk": help_for("background-ttk"),
        },
    },
    "backgroundimage": {
        "editor": "dynamic",
        "params": {"mode": "imageentry"},
    },
    # ttk.Frame, ttk.Label
    "borderwidth": {
        "editor": "dynamic",
        "params": {"mode": "dimensionentry"},
        "help": help_for("borderwidth"),
    },
    "bigincrement": {
        "editor": "dynamic",
        "params": {"mode": "naturalnumber"},
        "help": help_for("bigincrement"),
    },
    "bitmap": {
        "editor": "dynamic",
        "params": {
            "mode": "choice",
            "values": ("",) + TK_BITMAPS,
            "state": "readonly",
        },
        "help": help_for("bitmap"),
    },
    "blockcursor": {
        "editor": "dynamic",
        "params": {
            "mode": "choice",
            "values": ("", "false", "true"),
            "state": "readonly",
        },
        "help": help_for("blockcursor"),
    },
    "buttonbackground": {
        "editor": "dynamic",
        "params": {"mode": "colorentry"},
        "help": help_for("buttonbackground"),
        "tk.Spinbox": {"help": help_for("buttonbackground-tk.Spinbox")},
    },
    "buttoncursor": {
        "editor": "dynamic",
        "params": {
            "mode": "choice",
            "values": ("",) + TK_CURSORS,
            "state": "readonly",
        },
        "help": help_for("buttoncursor"),
    },
    "buttondownrelief": {
        "editor": "dynamic",
        "params": {
            "mode": "choice",
            "values": ("",) + TK_RELIEFS,
            "state": "readonly",
        },
        "help": help_for("buttondownrelief"),
    },
    "buttonuprelief": {
        "editor": "dynamic",
        "params": {
            "mode": "choice",
            "values": ("",) + TK_RELIEFS,
            "state": "readonly",
        },
        "help": help_for("buttonuprelief"),
    },
    "class_": {
        "editor": "dynamic",
        "params": {"mode": "alphanumentry"},
        "help": help_for("class_"),
    },
    "closeenough": {
        "editor": "dynamic",
        "params": {"mode": "spinbox", "from_": 0, "to": 999},
        "help": help_for("closeenough"),
    },
    "column_anchor": {  # ttk.Treeview.Column
        "editor": "dynamic",
        "params": {
            "mode": "choice",
            "values": ("", tk.W, tk.CENTER, tk.E),
            "state": "readonly",
        },
        "default": tk.W,
        "help": help_for("column_anchor"),
    },
    "columnbreak": {
        "editor": "dynamic",
        "params": {
            "mode": "choice",
            "values": ("", "false", "true"),
            "state": "readonly",
        },
        "help": help_for("columnbreak"),
    },
    "command": {
        "editor": "dynamic",
        "params": {"mode": "commandentry"},
        "tk.Scrollbar": {"params": {"mode": "scrollcommandentry"}},
        "ttk.Scrollbar": {"params": {"mode": "scrollcommandentry"}},
        "ttk.Scale": {"params": {"mode": "scalecommandentry"}},
        "tk.Scale": {"params": {"mode": "scalecommandentry"}},
        "tk.OptionMenu": {"params": {"mode": "simplecommandentry"}},
        "help": help_for("command-pygubu"),
    },
    # ttk.Label
    "compound": {
        "editor": "dynamic",
        "params": {
            "mode": "choice",
            "values": (
                "",
                tk.TOP,
                tk.BOTTOM,
                tk.LEFT,
                tk.RIGHT,
                tk.CENTER,
                tk.NONE,
            ),
            "state": "readonly",
        },
        "help": {
            "tk": help_for("compound-tk"),
            "ttk": help_for("compound-ttk"),
        },
        "ttk.LabeledScale": {
            "params": {
                "values": ("", tk.TOP, tk.BOTTOM),
                "state": "readonly",
            }
        },
    },
    # ttk.Button
    "confine": {
        "editor": "dynamic",
        "params": {
            "mode": "choice",
            "values": ("", "false", "true"),
            "state": "readonly",
        },
        "help": help_for("confine"),
    },
    "container": {
        "editor": "dynamic",
        "params": {
            "mode": "choice",
            "values": ("", "false", "true"),
            "state": "readonly",
        },
        "help": help_for("container"),
    },
    "cursor": {
        "editor": "dynamic",
        "params": {
            "mode": "choice",
            "values": ("",) + TK_CURSORS,
            "state": "readonly",
        },
        "help": help_for("cursor"),
    },
    # ttk.Button
    "default": {
        "editor": "dynamic",
        "params": {
            "mode": "choice",
            "values": ("", "normal", "active", "disabled"),
            "state": "readonly",
        },
        "help": help_for("default"),
    },
    "digits": {
        "editor": "dynamic",
        "params": {"mode": "spinbox", "from_": 0, "to": 999},
        "help": help_for("digits"),
    },
    "direction": {
        "editor": "dynamic",
        "params": {"mode": "choice"},
        "help": help_for("direction"),
        "tk.Menubutton": {
            "params": {
                "values": ("", tk.LEFT, tk.RIGHT, "above"),
                "state": "readonly",
            }
        },
        "ttk.Menubutton": {
            "params": {
                "values": ("", "above", "below", "flush", tk.LEFT, tk.RIGHT),
                "state": "readonly",
            }
        },
        "ttk.OptionMenu": {
            "params": {
                "values": ("", "above", "below", "flush", tk.LEFT, tk.RIGHT),
                "state": "readonly",
            }
        },
    },
    "disabledbackground": {
        "editor": "dynamic",
        "params": {"mode": "colorentry"},
        "help": help_for("disabledbackground"),
    },
    "disabledforeground": {
        "editor": "dynamic",
        "params": {"mode": "colorentry"},
        "help": help_for("disabledforeground"),
    },
    "elementborderwidth": {
        "editor": "dynamic",
        "params": {"mode": "dimensionentry"},
        "help": help_for("elementborderwidth"),
    },
    "endline": {
        "editor": "dynamic",
        "params": {"mode": "naturalnumber"},
        "help": help_for("endline"),
    },
    # ttk.Checkbutton, ttk.Entry
    "exportselection": {
        "editor": "dynamic",
        "params": {
            "mode": "choice",
            "values": ("", "true", "false"),
            "state": "readonly",
        },
        "help": help_for("exportselection"),
    },
    # ttk.Label
    "font": {
        "editor": "dynamic",
        "params": {"mode": "fontentry"},
        "help": help_for("font"),
    },
    # ttk.Label
    "foreground": {
        "editor": "dynamic",
        "params": {"mode": "colorentry"},
        "help": {
            "tk": help_for("foreground-tk"),
            "ttk": help_for("foreground-ttk"),
        },
    },
    # ttk.Spinbox
    "format": {
        "editor": "dynamic",
        "params": {"mode": "entry"},
    },
    # ttk.Scale, ttk.Spinbox
    "from_": {
        "editor": "dynamic",
        "params": {"mode": "realnumber"},
        "help": help_for("from_"),
    },
    "handlepad": {
        "editor": "dynamic",
        "params": {"mode": "dimensionentry"},
        "help": help_for("handlepad"),
    },
    "handlesize": {
        "editor": "dynamic",
        "params": {"mode": "dimensionentry"},
        "help": help_for("handlesize"),
    },
    # ttk.Treeview.Column
    "heading_anchor": {
        "editor": "dynamic",
        "params": {
            "mode": "choice",
            "values": ("", tk.W, tk.CENTER, tk.E),
            "state": "readonly",
        },
        "default": tk.W,
        "help": help_for("heading_anchor"),
    },
    # ttk.Frame,
    "height": {
        "editor": "dynamic",
        "help": help_for("height"),
        "params": {"mode": "dimensionentry"},
        "tk.Button": {"help": help_for("height-tk.Button")},
        "ttk.Combobox": {
            "params": {"mode": "naturalnumber"},
            "help": help_for("height-ttk.Combobox"),
        },
        "tk.Toplevel": {"default": 200},
        "tk.Frame": {"default": 200},
        "ttk.Frame": {"default": 200},
        "tk.LabelFrame": {"default": 200},
        "ttk.Labelframe": {"default": 200},
        "tk.Listbox": {
            "params": {"mode": "naturalnumber"},
        },
        "tk.Menubutton": {
            "params": {"mode": "naturalnumber"},
            "help": help_for("height-tk.Menubutton"),
        },
        "tk.PanedWindow": {"default": 200},
        "ttk.Panedwindow": {"default": 200},
        "ttk.Notebook": {"default": 200},
        "tk.Text": {
            "params": {"mode": "naturalnumber"},
            "default": 10,
            "help": help_for("height-tk.Text"),
        },
        "tk.Radiobutton": {
            "params": {"mode": "naturalnumber"},
        },
        "ttk.Treeview": {
            "params": {"mode": "naturalnumber"},
            "help": help_for("height-ttk.Treeview"),
        },
        "pygubu.builder.widgets.editabletreeview": {
            "params": {"mode": "naturalnumber"},
            "help": help_for("height-ttk.Treeview"),
        },
        "pygubu.builder.widgets.dialog": {"default": 100},
    },
    "hidemargin": {
        "editor": "dynamic",
        "params": {
            "mode": "choice",
            "values": ("", "false", "true"),
            "state": "readonly",
        },
        "help": help_for("hidemargin"),
    },
    "highlightbackground": {
        "editor": "dynamic",
        "params": {
            "mode": "colorentry",
        },
        "help": help_for("highlightbackground"),
    },
    "highlightcolor": {
        "editor": "dynamic",
        "params": {
            "mode": "colorentry",
        },
        "help": help_for("highlightcolor"),
    },
    "highlightthickness": {
        "editor": "dynamic",
        "params": {
            "mode": "dimensionentry",
        },
        "help": help_for("highlightthickness"),
    },
    # ttk.Label
    "image": {
        "editor": "dynamic",
        "params": {"mode": "imageentry"},
        "help": {"tk": help_for("image-tk"), "ttk": help_for("image-ttk")},
        "ttk.Treeview.Column": {
            "help": help_for("image-ttk.Treeview.Column"),
        },
    },
    "inactiveselectbackground": {
        "editor": "dynamic",
        "params": {"mode": "colorentry"},
        "help": help_for("inactiveselectbackground"),
    },
    # ttk.Spinbox
    "increment": {
        "editor": "dynamic",
        "params": {"mode": "realnumber"},
        "help": help_for("increment"),
    },
    "indicatoron": {
        "editor": "dynamic",
        "params": {
            "mode": "choice",
            "values": ("", "false", "true"),
            "state": "readonly",
        },
        "help": help_for("indicatoron"),
    },
    "insertbackground": {
        "editor": "dynamic",
        "params": {"mode": "colorentry"},
        "help": help_for("insertbackground"),
    },
    "insertborderwidth": {
        "editor": "dynamic",
        "params": {"mode": "spinbox", "from_": 0, "to": 999},
        "help": help_for("insertborderwidth"),
    },
    "insertofftime": {
        "editor": "dynamic",
        "params": {
            "mode": "spinbox",
            "from_": 0,
            "to": 9999,
            "increment": 100,
        },
        "help": help_for("insertofftime"),
    },
    "insertontime": {
        "editor": "dynamic",
        "params": {
            "mode": "spinbox",
            "from_": 0,
            "to": 9999,
            "increment": 100,
        },
        "help": help_for("insertontime"),
    },
    "insertunfocussed": {
        "editor": "dynamic",
        "params": {
            "mode": "choice",
            "values": ("", "none", "hollow", "solid"),
            "state": "readonly",
        },
        "help": help_for("insertunfocussed"),
    },
    "insertwidth": {
        "editor": "dynamic",
        "params": {"mode": "spinbox", "from_": 0, "to": 999},
        "help": help_for("insertwidth"),
    },
    # ttk.Entry
    "invalidcommand": {
        "editor": "dynamic",
        "params": {"mode": "entryvalidatecommandentry"},
        "help": help_for("command-pygubu"),
    },
    "jump": {
        "editor": "dynamic",
        "params": {
            "mode": "choice",
            "values": ("", "false", "true"),
            "state": "readonly",
        },
        "help": help_for("jump"),
    },
    # ttk.Label
    "justify": {
        "editor": "dynamic",
        "params": {
            "mode": "choice",
            "values": ("", "left", "center", "right"),
            "state": "readonly",
        },
        "help": help_for("justify"),
        "ttk.Entry": {"help": help_for("justify-ttk.Entry")},
    },
    "label": {
        "editor": "dynamic",
        "params": {"mode": "entry"},
        "help": help_for("label"),
    },
    # ttk.Labelframe
    "labelanchor": {
        "editor": "dynamic",
        "params": {
            "mode": "choice",
            "values": (
                "",
                "nw",
                "n",
                "ne",
                "en",
                "e",
                "es",
                "se",
                "s",
                "sw",
                "ws",
                "w",
            ),
            "state": "readonly",
        },
        "help": help_for("labelanchor"),
    },
    # ttk.Progressbar
    "length": {
        "editor": "dynamic",
        "params": {"mode": "dimensionentry"},
        "help": help_for("length"),
    },
    "listvariable": {
        "editor": "dynamic",
        "params": {"mode": "tkvarentry"},
        "help": help_for("listvariable"),
    },
    # ttk.Progressbar
    "maximum": {
        "editor": "dynamic",
        "params": {"mode": "realnumber"},
        "help": help_for("maximum"),
    },
    "maxundo": {
        "editor": "dynamic",
        "params": {"mode": "integernumber"},
        "help": help_for("maxundo"),
    },
    "minsize": {
        "editor": "dynamic",
        "params": {"mode": "dimensionentry"},
        "help": help_for("minsize"),
        "tk.Toplevel": {
            "params": {"mode": "whentry"},
            "help": help_for("minsize-toplevel"),
        },
        "pygubu.builder.widgets.dialog": {
            "params": {"mode": "whentry"},
            "help": help_for("minsize-toplevel"),
        },
    },
    # ttk.Treeview.Column
    "minwidth": {
        "editor": "dynamic",
        "params": {"mode": "naturalnumber"},
        "default": "20",
        "help": help_for("minwidth"),
    },
    # ttk.Progressbar
    "mode": {
        "editor": "dynamic",
        "params": {
            "mode": "choice",
            "values": ("", "determinate", "indeterminate"),
            "state": "readonly",
        },
    },
    "offrelief": {
        "editor": "dynamic",
        "params": {
            "mode": "choice",
            "values": ("",) + TK_RELIEFS,
            "state": "readonly",
        },
        "help": help_for("offrelief"),
    },
    # ttk.Checkbutton
    "offvalue": {
        "editor": "dynamic",
        "params": {"mode": "entry"},
        "help": help_for("offvalue"),
    },
    # ttk.Checkbutton
    "onvalue": {
        "editor": "dynamic",
        "params": {"mode": "entry"},
        "help": help_for("onvalue"),
    },
    "opaqueresize": {
        "editor": "dynamic",
        "params": {
            "mode": "choice",
            "values": ("", "false", "true"),
            "state": "readonly",
        },
        "help": help_for("opaqueresize"),
    },
    # ttk.Panedwindow
    "orient": {
        "editor": "dynamic",
        "params": {
            "mode": "choice",
            "values": (tk.VERTICAL, tk.HORIZONTAL),
            "state": "readonly",
        },
        "default": tk.HORIZONTAL,
        "help": help_for("orient"),
    },
    "overrelief": {
        "editor": "dynamic",
        "params": {
            "mode": "choice",
            "values": ("",) + TK_RELIEFS,
            "state": "readonly",
        },
        "help": help_for("overrelief"),
    },
    # ttk.Frame, ttk.Label
    "padding": {
        "editor": "dynamic",
        "params": {"mode": "fourdimensionentry"},
        "help": help_for("padding"),
    },
    "padx": {
        "editor": "dynamic",
        "params": {"mode": "dimensionentry"},
        "help": help_for("padx"),
    },
    "pady": {
        "editor": "dynamic",
        "params": {"mode": "dimensionentry"},
        "help": help_for("pady"),
    },
    # ttk.Checkbutton
    "postcommand": {
        "editor": "dynamic",
        "params": {"mode": "simplecommandentry"},
        "help": help_for("postcommand"),
    },
    "proxybackground": {
        "editor": "dynamic",
        "params": {"mode": "colorentry"},
        "help": help_for("proxybackground"),
    },
    "proxyborderwidth": {
        "editor": "dynamic",
        "params": {"mode": "dimensionentry"},
        "help": help_for("proxyborderwidth"),
    },
    "proxyrelief": {
        "editor": "dynamic",
        "params": {
            "mode": "choice",
            "values": ("",) + TK_RELIEFS,
            "state": "readonly",
        },
        "help": help_for("proxyrelief"),
    },
    "readonlybackground": {
        "editor": "dynamic",
        "params": {"mode": "colorentry"},
        "help": help_for("readonlybackground"),
    },
    # ttk.Frame,
    "relief": {
        "editor": "dynamic",
        "params": {
            "mode": "choice",
            "values": ("",) + TK_RELIEFS,
            "state": "readonly",
        },
        "help": help_for("relief"),
    },
    "repeatdelay": {
        "editor": "dynamic",
        "params": {
            "mode": "spinbox",
            "from_": 0,
            "to": 9999,
            "increment": 100,
        },
        "help": help_for("repeatdelay"),
    },
    "repeatinterval": {
        "editor": "dynamic",
        "params": {
            "mode": "spinbox",
            "from_": 0,
            "to": 9999,
            "increment": 100,
        },
        "help": help_for("repeatinterval"),
    },
    "resolution": {
        "editor": "dynamic",
        "params": {
            "mode": "spinbox",
            "from_": 0,
            "to": 999,
            "increment": 0.5,
        },
        "help": help_for("resolution"),
    },
    "sliderlength": {
        "editor": "dynamic",
        "params": {"mode": "dimensionentry"},
        "help": help_for("sliderlength"),
    },
    "sliderrelief": {
        "editor": "dynamic",
        "params": {
            "mode": "choice",
            "values": ("",) + TK_RELIEFS,
            "state": "readonly",
        },
        "help": help_for("sliderrelief"),
    },
    "sashcursor": {
        "editor": "dynamic",
        "params": {
            "mode": "choice",
            "values": ("",) + TK_CURSORS,
            "state": "readonly",
        },
        "help": help_for("sashcursor"),
    },
    "sashpad": {
        "editor": "dynamic",
        "params": {"mode": "dimensionentry"},
        "help": help_for("sashpad"),
    },
    "sashrelief": {
        "editor": "dynamic",
        "params": {
            "mode": "choice",
            "values": ("",) + TK_RELIEFS,
            "state": "readonly",
        },
        "help": help_for("sashrelief"),
    },
    "sashwidth": {
        "editor": "dynamic",
        "params": {"mode": "dimensionentry"},
        "help": help_for("sashwidth"),
    },
    "selectbackground": {
        "editor": "dynamic",
        "params": {"mode": "colorentry"},
        "help": help_for("selectbackground"),
    },
    "selectborderwidth": {
        "editor": "dynamic",
        "params": {"mode": "spinbox", "from_": 0, "to": 999},
        "help": help_for("selectborderwidth"),
    },
    "selectforeground": {
        "editor": "dynamic",
        "params": {"mode": "colorentry"},
        "help": help_for("selectforeground"),
    },
    "scrollregion": {
        "editor": "dynamic",
        "params": {"mode": "fourdimensionentry"},
        "help": help_for("scrollregion"),
    },
    "selectcolor": {
        "editor": "dynamic",
        "params": {"mode": "colorentry"},
        "help": help_for("selectcolor"),
    },
    "selectimage": {
        "editor": "dynamic",
        "params": {"mode": "imageentry"},
        "help": help_for("selectimage"),
    },
    # ttk.Treeview
    "selectmode": {
        "editor": "dynamic",
        "help": help_for("selectmode"),
        "params": {
            "mode": "choice",
            "values": ("", tk.BROWSE, tk.SINGLE, tk.MULTIPLE, tk.EXTENDED),
            "state": "readonly",
        },
        "ttk.Treeview": {
            "params": {
                "values": (tk.EXTENDED, tk.BROWSE, tk.NONE),
                "state": "readonly",
            },
            "default": tk.EXTENDED,
        },
        "pygubu.builder.widgets.editabletreeview": {
            "params": {
                "values": (tk.EXTENDED, tk.BROWSE, tk.NONE),
                "state": "readonly",
            },
            "default": tk.EXTENDED,
        },
    },
    "setgrid": {
        "editor": "dynamic",
        "params": {
            "mode": "choice",
            "values": ("", "false", "true"),
            "state": "readonly",
        },
        "help": help_for("setgrid"),
    },
    # ttk.Entry
    "show": {
        "editor": "dynamic",
        "params": {"mode": "choice", "values": ("", "•"), "state": "normal"},
        "help": help_for("show"),
        "ttk.Treeview": {
            "params": {
                "values": ("", "tree", "headings"),
                "state": "readonly",
            },
            "help": help_for("show-ttk.Treeview"),
        },
        "pygubu.builder.widgets.editabletreeview": {
            "params": {
                "values": ("", "tree", "headings"),
                "state": "readonly",
            },
            "help": help_for("show-ttk.Treeview"),
        },
    },
    "showhandle": {
        "editor": "dynamic",
        "params": {
            "mode": "choice",
            "values": ("", "false", "true"),
            "state": "readonly",
        },
        "help": help_for("showhandle"),
    },
    "showvalue": {
        "editor": "dynamic",
        "params": {
            "mode": "choice",
            "values": ("", "false", "true"),
            "state": "readonly",
        },
        "help": help_for("showvalue"),
    },
    "spacing1": {
        "editor": "dynamic",
        "params": {"mode": "dimensionentry"},
        "help": help_for("spacing1"),
    },
    "spacing2": {
        "editor": "dynamic",
        "params": {"mode": "dimensionentry"},
        "help": help_for("spacing2"),
    },
    "spacing3": {
        "editor": "dynamic",
        "params": {"mode": "dimensionentry"},
        "help": help_for("spacing3"),
    },
    "startline": {
        "editor": "dynamic",
        "params": {"mode": "naturalnumber"},
        "help": help_for("startline"),
    },
    "state": {
        "editor": "dynamic",
        "help": help_for("state"),
        "params": {
            "mode": "choice",
            "values": ("", tk.NORMAL, tk.DISABLED),
            "state": "readonly",
        },
        "tk.Button": {
            "params": {
                "values": ("", tk.NORMAL, tk.ACTIVE, tk.DISABLED),
                "state": "readonly",
            }
        },
        "tk.Checkbutton": {
            "params": {
                "values": ("", tk.NORMAL, tk.ACTIVE, tk.DISABLED),
                "state": "readonly",
            },
            "help": help_for("state-tk.Checkbutton"),
        },
        "tk.Canvas": {
            "params": {
                "values": ("", tk.NORMAL, tk.DISABLED),
                "state": "readonly",
            },
            "help": help_for("state-tk.Canvas"),
        },
        "tk.Entry": {
            "params": {
                "values": ("", tk.NORMAL, tk.DISABLED, "readonly"),
                "state": "readonly",
            }
        },
        "tk.Combobox": {
            "params": {"values": ("", "readonly"), "state": "readonly"}
        },
        "ttk.Entry": {
            "params": {
                "values": ("", tk.NORMAL, tk.DISABLED, "readonly"),
                "state": "readonly",
            }
        },
        "ttk.Combobox": {
            "params": {
                "values": ("", "normal", "readonly", "disabled"),
                "state": "readonly",
            }
        },
        "ttk.Button": {
            "params": {
                "values": ("", "normal", "disabled"),
                "state": "readonly",
            }
        },
        "ttk.Notebook.Tab": {
            "params": {
                "values": ("", "normal", "disabled", "hidden"),
                "state": "readonly",
            }
        },
        "tk.Spinbox": {
            "params": {
                "values": ("", tk.NORMAL, tk.DISABLED, "readonly"),
                "state": "readonly",
            }
        },
        "ttk.Spinbox": {
            "params": {
                "values": ("", tk.NORMAL, tk.DISABLED, "readonly"),
                "state": "readonly",
            }
        },
    },
    # ttk.Notebook.Tab
    "sticky": {
        "editor": "dynamic",
        "params": {"mode": "stickyentry"},
        "help": help_for("sticky"),
    },
    # ttk.Treeview.Column
    "stretch": {
        "editor": "dynamic",
        "help": help_for("stretch"),
        "params": {"mode": "choice"},
        "ttk.Treeview.Column": {
            "params": {"values": ("true", "false"), "state": "readonly"},
            "default": "true",
            "help": help_for("stretch-ttk.Treeview"),
        },
        "tk.PanedWindow.Pane": {
            "params": {
                "values": ("", "always", "first", "last", "middle", "never"),
                "state": "readonly",
            }
        },
    },
    "style": {
        "editor": "dynamic",
        "params": {"mode": "ttkstylechoice"},
        "ttk.Button": {"params": {"values": ("", "Toolbutton")}},
        "help": help_for("style"),
    },
    "tabs": {  # FIXME see tk.Text tab property
        "editor": "dynamic",
        "params": {"mode": "entry"},
        "help": help_for("tabs"),
    },
    "tabstyle": {
        "editor": "dynamic",
        "params": {
            "mode": "choice",
            "values": ("", "tabular", "wordprocessor"),
            "state": "readonly",
        },
        "help": help_for("tabstyle"),
    },
    "takefocus": {
        "editor": "dynamic",
        "params": {
            "mode": "choice",
            "values": ("", "false", "true"),
            "state": "readonly",
        },
        "help": help_for("takefocus"),
    },
    "tearoff": {
        "editor": "dynamic",
        "params": {
            "mode": "choice",
            "values": ("", "false", "true"),
            "state": "readonly",
        },
        "help": help_for("tearoff"),
    },
    "tearoffcommand": {
        "editor": "dynamic",
        "params": {"mode": "simplecommandentry"},
        "help": help_for("tearoffcommand"),
    },
    # ttk.Label
    "text": {
        "editor": "dynamic",
        "params": {"mode": "text"},
        "help": help_for("text"),
    },
    # ttk.Label
    "textvariable": {
        "editor": "dynamic",
        "params": {"mode": "tkvarentry"},
        "help": help_for("textvariable"),
    },
    "tickinterval": {
        "editor": "dynamic",
        "params": {
            "mode": "spinbox",
            "from_": 0,
            "to": 999,
            "increment": 0.5,
        },
        "help": help_for("tickinterval"),
    },
    # ttk.Scale, ttk.Spinbox
    "to": {
        "editor": "dynamic",
        "params": {"mode": "realnumber"},
        "help": help_for("to"),
    },
    "tile": {
        "editor": "dynamic",
        "params": {
            "mode": "choice",
            "values": ("true", "false"),
            "state": "readonly",
        },
        "default": "false",
    },
    "title": {
        "editor": "dynamic",
        "params": {"mode": "entry"},
        "help": help_for("title-menu"),
        "tk.Toplevel": {
            "params": {"mode": "entry"},
            "help": help_for("title-toplevel"),
        },
        "pygubu.builder.widgets.dialog": {
            "params": {"mode": "entry"},
            "help": help_for("title-toplevel"),
        },
    },
    "tristateimage": {
        "editor": "dynamic",
        "params": {"mode": "imageentry"},
        "help": help_for("tristateimage"),
    },
    "tristatevalue": {
        "editor": "dynamic",
        "params": {"mode": "entry"},
        "help": help_for("tristatevalue"),
    },
    "troughcolor": {
        "editor": "dynamic",
        "params": {"mode": "colorentry"},
        "help": help_for("troughcolor"),
    },
    # ttk.Label
    "underline": {
        "editor": "dynamic",
        "params": {"mode": "naturalnumber"},
        "help": help_for("underline"),
    },
    "undo": {
        "editor": "dynamic",
        "params": {
            "mode": "choice",
            "values": ("", "false", "true"),
            "state": "readonly",
        },
        "help": help_for("undo"),
    },
    "value": {
        "editor": "dynamic",
        "help": help_for("value"),
        "params": {"mode": "entry"},
        "ttk.Progressbar": {"params": {"mode": "realnumber"}},
        "ttk.Scale": {"params": {"mode": "realnumber"}},
    },
    # ttk.Checkbutton
    "values": {
        "editor": "dynamic",
        "params": {"mode": "entry"},
        "help": help_for("values"),
        "tk.Spinbox": {"help": help_for("values-tk.Spinbox")},
        "tk.OptionMenu": {"help": help_for("values-tk.OptionMenu")},
        "ttk.OptionMenu": {"help": help_for("values-tk.OptionMenu")},
    },
    "validate": {
        "editor": "dynamic",
        "params": {
            "mode": "choice",
            "values": (
                "",
                "none",
                "focus",
                "focusin",
                "focusout",
                "key",
                "all",
            ),
            "state": "readonly",
        },
        "help": help_for("validate"),
    },
    "validatecommand": {
        "editor": "dynamic",
        "params": {"mode": "entryvalidatecommandentry"},
        "help": help_for("command-pygubu"),
    },
    # ttk.Checkbutton
    "variable": {
        "editor": "dynamic",
        "params": {"mode": "tkvarentry"},
        "help": help_for("variable"),
        "ttk.LabeledScale": {"params": {"type_choices": ("int", "double")}},
    },
    # ttk.Panedwindow.Pane
    "weight": {
        "editor": "dynamic",
        "params": {"mode": "naturalnumber"},
        "default": "1",
        "help": help_for("weight"),
    },
    # ttk.Frame, ttk.Label
    "width": {
        "editor": "dynamic",
        "help": help_for("width"),
        "params": {"mode": "dimensionentry"},
        "tk.Label": {"help": help_for("width-tk.Label")},
        "tk.Message": {"help": help_for("width-tk.Message")},
        "tk.Button": {
            "params": {"mode": "integernumber"},
            "help": help_for("width-tk.Button"),
        },
        "tk.Scale": {"help": help_for("width-scale")},
        "ttk.Button": {
            "params": {"mode": "integernumber"},
            "help": help_for("width-ttk"),
        },
        "tk.Canvas": {"params": {"mode": "entry"}},
        "tk.Checkbutton": {
            "params": {"mode": "integernumber"},
            "help": help_for("width-tk"),
        },
        "tk.Spinbox": {
            "params": {"mode": "integernumber"},
            "help": help_for("width-tk.Spinbox"),
        },
        "tk.Scrollbar": {
            "params": {"mode": "dimensionentry"},
            "help": help_for("width-tk.Scrollbar"),
        },
        "ttk.Checkbutton": {
            "params": {"mode": "integernumber"},
            "help": help_for("width-ttk"),
        },
        "tk.Entry": {
            "params": {"mode": "naturalnumber"},
            "help": help_for("width-tk.Entry"),
        },
        "ttk.Entry": {
            "params": {"mode": "naturalnumber"},
        },
        "tk.Menubutton": {
            "params": {"mode": "naturalnumber"},
            "help": help_for("width-tk.Menubutton"),
        },
        "ttk.Label": {
            "params": {"mode": "integernumber"},
            "help": help_for("width-ttk.Label"),
        },
        "tk.Listbox": {
            "params": {"mode": "naturalnumber"},
        },
        "tk.Frame": {"default": 200},
        "ttk.Frame": {"default": 200},
        "tk.LabelFrame": {"default": 200},
        "ttk.Labelframe": {"default": 200},
        "tk.PanedWindow": {"default": 200},
        "ttk.Panedwindow": {"default": 200},
        "ttk.Notebook": {"default": 200},
        "tk.Radiobutton": {
            "params": {"mode": "naturalnumber"},
        },
        "ttk.Radiobutton": {
            "params": {"mode": "integernumber"},
            "help": help_for("width-ttk"),
        },
        "tk.Text": {
            "params": {"mode": "naturalnumber"},
            "default": 50,
            "help": help_for("width-tk.Text"),
        },
        "tk.Toplevel": {"default": 200},
        "ttk.Treeview.Column": {
            "params": {"mode": "naturalnumber"},
            "default": 200,
            "help": help_for("width-ttk.Treeview.Column"),
        },
        "pygubu.builder.widgets.dialog": {"default": 200},
    },
    # ttk.Spinbox
    "wrap": {
        "editor": "dynamic",
        "params": {
            "mode": "choice",
            "values": ("", "false", "true"),
            "state": "readonly",
        },
        "help": help_for("wrap-ttk.Spinbox"),
        "tk.Text": {
            "params": {
                "values": ("", tk.CHAR, tk.WORD, tk.NONE),
                "state": "readonly",
            },
            "help": help_for("wrap-tk.Text"),
        },
        "pygubu.builder.widgets.tkinterscrolledtext": {
            "params": {
                "values": ("", tk.CHAR, tk.WORD, tk.NONE),
                "state": "readonly",
            },
            "help": help_for("wrap-tk.Text"),
        },
    },
    # ttk.Label
    "wraplength": {
        "editor": "dynamic",
        "params": {"mode": "dimensionentry"},
        "help": help_for("wraplength"),
    },
    # ttk.Entry
    "xscrollcommand": {
        "editor": "dynamic",
        "params": {"mode": "scrollcommandentry"},
        "help": help_for("command-pygubu"),
    },
    "xscrollincrement": {
        "editor": "dynamic",
        "params": {"mode": "dimensionentry"},
        "help": help_for("xscrollincrement"),
    },
    # ttk.Treeview
    "yscrollcommand": {
        "editor": "dynamic",
        "params": {"mode": "scrollsetcommandentry"},
        "help": help_for("command-pygubu"),
    },
    "yscrollincrement": {
        "editor": "dynamic",
        "params": {"mode": "dimensionentry"},
        "help": help_for("yscrollincrement"),
    },
    "geometry": {
        "editor": "dynamic",
        "help": help_for("geometry-custom"),
        "params": {
            "mode": "geometryentry",
            "values": (
                "",
                "320x200",
                "320x240",
                "352x288",
                "384x288",
                "480x320",
                "640x480",
                "768x576",
                "800x480",
                "800x600",
                "854x480",
                "1024x576",
                "1024x600",
                "1024x768",
                "1152x768",
                "1152x864",
                "1280x720",
                "1280x768",
                "1280x800",
                "1280x854",
                "1280x960",
                "1280x1024",
                "1366x768",
                "1400x1050",
                "1440x1080",
                "1440x900",
                "1440x960",
                "1440x1080",
                "1600x900",
                "1600x1050",
                "1600x1200",
                "1920x1080",
                "2048x1080",
                "2048x1536",
                "2560x1600",
                "2560x2048",
            ),
        },
    },
    "iconbitmap": {
        "editor": "dynamic",
        "params": {
            "mode": "imageentry",
        },
        "help": help_for("iconbitmap-custom"),
    },
    "iconphoto": {
        "editor": "dynamic",
        "params": {
            "mode": "imageentry",
        },
        "help": help_for("iconphoto-custom"),
    },
    "maxsize": {
        "editor": "dynamic",
        "params": {"mode": "whentry"},
        "help": help_for("maxsize-toplevel"),
    },
    "overrideredirect": {
        "editor": "dynamic",
        "params": {
            "mode": "choice",
            "values": ("", "True", "False"),
            "state": "readonly",
        },
        "help": help_for("overrideredirect-custom"),
    },
    "resizable": {
        "editor": "dynamic",
        "params": {
            "mode": "choice",
            "values": ("", "both", "horizontally", "vertically", "none"),
            "state": "readonly",
        },
        "help": help_for("resizable-custom"),
    },
    "scrolltype": {
        "editor": "dynamic",
        "params": {
            "mode": "choice",
            "values": ("both", "vertical", "horizontal"),
            "state": "readonly",
        },
        "default": "both",
        "help": help_for("scrolltype-custom"),
    },
    "tree_column": {
        "editor": "dynamic",
        "params": {
            "mode": "choice",
            "values": ("true", "false"),
            "state": "readonly",
        },
        "default": "false",
        "help": help_for("tree_column-custom"),
    },
    "usemousewheel": {
        "editor": "dynamic",
        "params": {
            "mode": "choice",
            "values": ("true", "false"),
            "state": "readonly",
        },
        "default": "false",
    },
    "visible": {
        "editor": "dynamic",
        "params": {
            "mode": "choice",
            "values": ("true", "false"),
            "state": "readonly",
        },
        "default": "true",
        "help": help_for("visible-custom"),
    },
    "specialmenu": {
        "editor": "dynamic",
        "params": {
            "mode": "choice",
            "values": ("apple", "help", "window", "system"),
            "state": "readonly",
        },
    },
}

LAYOUT_OPTIONS = {
    # pack/grid/place common properties
    "padx": {"editor": "twodimensionentry", "help": help_for("padx-layout")},
    "pady": {"editor": "twodimensionentry", "help": help_for("pady-layout")},
    "ipadx": {"editor": "dimensionentry", "help": help_for("ipadx-layout")},
    "ipady": {"editor": "dimensionentry", "help": help_for("ipady-layout")},
    "propagate": {
        "editor": "choice",
        "params": {"values": ("True", "False"), "state": "readonly"},
        "default": "True",
        "help": help_for("propagate-layout"),
    },
    "anchor": {
        "editor": "choice",
        "params": {
            "values": (
                "",
                "n",
                "ne",
                "nw",
                "e",
                "w",
                "s",
                "se",
                "sw",
                "center",
            ),
            "state": "readonly",
        },
        "help": help_for("anchor-layout"),
        "place": {"default": "nw", "help": help_for("anchor-layout-place")},
    },
    # pack properties
    "expand": {
        "editor": "choice",
        "params": {"values": ("", "false", "true"), "state": "readonly"},
        "help": help_for("expand-pack"),
    },
    "fill": {
        "editor": "choice",
        "params": {"values": ("", "x", "y", "both"), "state": "readonly"},
        "help": help_for("fill-pack"),
    },
    "side": {
        "editor": "choice",
        "params": {
            "values": ("top", "bottom", "left", "right"),
            "state": "readonly",
        },
        "default": "top",
        "help": help_for("side-pack"),
    },
    "bordermode": {
        "editor": "choice",
        "params": {
            "values": ("", "inside", "outside", "ignore"),
            "state": "readonly",
        },
        "help": help_for("bordermode-pack"),
    },
    "height": {
        "editor": "pixelcoordinateentry",
        "help": help_for("height-pack"),
    },
    "relheight": {
        "editor": "relativeentry",
        "help": help_for("relheight-pack"),
    },
    "relwidth": {
        "editor": "relativeentry",
        "help": help_for("relwidth-pack"),
    },
    "relx": {"editor": "relativeentry", "help": help_for("relx-pack")},
    "rely": {"editor": "relativeentry", "help": help_for("rely-pack")},
    "width": {
        "editor": "pixelcoordinateentry",
        "help": help_for("width-pack"),
    },
    "x": {
        "editor": "pixelcoordinateentry",
        "default": "0",
        "help": help_for("x-pack"),
    },
    "y": {
        "editor": "pixelcoordinateentry",
        "default": "0",
        "help": help_for("y-pack"),
    },
    #
    # grid packing properties
    #
    "row": {
        "editor": "naturalnumber",
        "default": "0",
        "help": help_for("row-grid"),
    },
    "column": {
        "editor": "naturalnumber",
        "default": "0",
        "help": help_for("column-grid"),
    },
    "sticky": {
        "editor": "stickyentry",
        "params": {},
        "help": help_for("sticky-grid"),
    },
    "rowspan": {"editor": "naturalnumber", "help": help_for("rowspan-grid")},
    "columnspan": {
        "editor": "naturalnumber",
        "help": help_for("columnspan-grid"),
    },
    #
    # grid row and column properties (can be applied to each row or column)
    "minsize": {
        "editor": "dimensionentry",
        "params": {"width": 4, "empty_data": 0},
        "help": help_for("minsize-grid"),
    },
    "pad": {
        "editor": "dimensionentry",
        "params": {"width": 4, "empty_data": 0},
        "help": help_for("pad-grid"),
    },
    "weight": {
        "editor": "naturalnumber",
        "params": {"empty_data": 0},
        "help": help_for("weight-grid"),
    },
    "uniform": {"editor": "alphanumentry", "help": help_for("uniform-grid")},
}

# List properties in display order
MANAGER_PROPERTIES = (
    "anchor",
    "relx",
    "rely",
    "relwidth",
    "relheight",
    "x",
    "y",
    "width",
    "height",
    "bordermode",
    "side",
    "expand",
    "fill",
    "row",
    "column",
    "sticky",
    "rowspan",
    "columnspan",
    "padx",
    "pady",
    "ipadx",
    "ipady",
    "propagate",
)

GRID_PROPERTIES = (
    "row",
    "column",
    "sticky",
    "rowspan",
    "columnspan",
    "padx",
    "pady",
    "ipadx",
    "ipady",
)

PACK_PROPERTIES = (
    "anchor",
    "side",
    "expand",
    "fill",
    "padx",
    "pady",
    "ipadx",
    "ipady",
)

PLACE_PROPERTIES = (
    "anchor",
    "relx",
    "rely",
    "relwidth",
    "relheight",
    "x",
    "y",
    "width",
    "height",
    "bordermode",
)

GRID_RC_PROPERTIES = ("minsize", "pad", "weight", "uniform")

# List properties in display order
CONTAINER_MANAGER_PROPERTIES = ("anchor", "propagate")  # all properties

CONTAINER_GRID_PROPERTIES = ("anchor", "propagate")
CONTAINER_PACK_PROPERTIES = ("propagate",)

TRANSLATABLE_PROPERTIES = (
    "label",
    "text",
    "title",
)


def _register_custom(name, descr):
    if name in PROPERTY_DEFINITIONS:
        PROPERTY_DEFINITIONS[name].update(descr)
        logger.debug("Updated property: %s", name)
    else:
        PROPERTY_DEFINITIONS[name] = descr
        logger.debug("Registered property: %s", name)


def load_custom_properties():
    for name, descr in CUSTOM_PROPERTIES.items():
        _register_custom(name, descr)
