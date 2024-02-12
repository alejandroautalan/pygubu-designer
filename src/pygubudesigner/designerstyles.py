import sys
import tkinter as tk
import tkinter.ttk as ttk
import logging
from dataclasses import dataclass
from pygubu.stockimage import StockImage, StockImageException
from pygubudesigner import preferences as pref
from pygubudesigner.util import get_ttk_style


logger = logging.getLogger(__name__)


class ImgLazyLoader:
    def __init__(self, name):
        self.name = name

    def __str__(self):
        return str(StockImage.get(self.name))


designer_dboptions = {
    "*Dialog.msg.": {
        "width": 34,
        "wrapLength": "6i",
    },
    # Preview panel, Selection indicator color
    "*PreviewIndicatorFrame*": {
        "background": "red",
        "foreground": "red",
    },
}

designer_settings = {
    "ColorSelectorButton.Toolbutton": {
        "configure": {
            "image": ImgLazyLoader("mglass"),
        }
    },
    "ImageSelectorButton.Toolbutton": {
        "configure": {
            "image": ImgLazyLoader("mglass"),
        }
    },
    "ComponentPalette.Toolbutton": {
        "configure": {
            "font": "TkSmallCaptionFont",
        }
    },
    "ComponentPalette.TNotebook.Tab": {
        "configure": {
            "font": "TkSmallCaptionFont",
        }
    },
    "PanelTitle.TLabel": {
        "configure": {
            "background": "#808080",
            "foreground": "white",
            "font": "TkSmallCaptionFont",
        }
    },
    "Template.Toolbutton": {
        "configure": {
            "padding": 5,
        }
    },
    # TreeComponentPalette styles
    "TreeComponentPalette.Treeview": {
        "configure": {
            "rowheight": 30,
        }
    },
    # Forms ??
    # "LabelFieldInfo.TLabel": {"configure": {option:val,}},
    "Error.LabelFieldInfo.TLabel": {
        "configure": {
            "foreground": "red",
        }
    },
    "Error.EntryField.TEntry": {
        "configure": {
            "fieldbackground": "yellow",
        }
    },
    "Error.ComboboxField.TCombobox": {
        "configure": {
            "fieldbackground": "yellow",
        },
        "map": {
            "fieldbackground": [("readonly", "yellow")],
        },
    },
    # "": {"configure": {option:val,}},
}


updated_themes = []


def setup_ttk_styles(master: tk.Widget = None, changed_to=None):
    s = get_ttk_style()

    if changed_to is None:
        # App is starting

        # setup database options
        # master.option_clear()
        for pattern in designer_dboptions:
            for option, value in designer_dboptions[pattern].items():
                fpattern = f"{pattern}{option}"
                master.option_add(fpattern, value, 50)

        # Load preferred ttk theme
        user_theme = pref.get_option("ttk_theme")
        try:
            s.theme_use(user_theme)
        except tk.TclError:
            pass

    current_theme = s.theme_use()

    if current_theme not in updated_themes:
        s.theme_settings(current_theme, designer_settings)
        updated_themes.append(current_theme)

        if sys.platform == "linux" and current_theme in (
            "alt",
            "default",
            "clam",
            "classic",
        ):
            # change background of comboboxes
            color = s.lookup("TEntry", "fieldbackground")
            s.map("TCombobox", fieldbackground=[("readonly", color)])
            s.map("TSpinbox", fieldbackground=[("readonly", color)])
