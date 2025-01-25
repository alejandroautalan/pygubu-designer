import sys
import tkinter as tk
import tkinter.ttk as ttk
import logging
from dataclasses import dataclass
from pygubu.stockimage import StockImage, StockImageException
from pygubudesigner import preferences as pref
from pygubudesigner.services.theming import get_ttk_style
from pygubudesigner.util import get_linespace


logger = logging.getLogger(__name__)


class ImgLazyLoader:
    def __init__(self, name):
        self.name = name

    def __str__(self):
        return str(StockImage.get(self.name))


class RowHeightLazy:
    def __init__(self, scale_factor=1):
        self.scale_factor = scale_factor
        self.rowheight = None

    def calculate(self, root):
        # setup rowheight
        self.rowheight = get_linespace(scale_factor=self.scale_factor)

    def __str__(self):
        if self.rowheight is None:
            raise RuntimeError("Too early to use rowheight, value not ready.")
        return str(self.rowheight)


treeview_rowheight = RowHeightLazy(1.1)
palette_rowheight = RowHeightLazy(1.5)


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
    # Default treeview rowheight
    "Treeview": {
        "configure": {
            "rowheight": treeview_rowheight,
        }
    },
    # TreeComponentPalette styles
    "TreeComponentPalette.Treeview": {
        "configure": {
            "rowheight": palette_rowheight,
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


def on_first_window(master: tk.Widget):
    """Setup theme configuration on first boot."""
    s: ttk.Style = get_ttk_style()

    # App is starting
    # calculate rowheight for treviews
    treeview_rowheight.calculate(master)
    palette_rowheight.calculate(master)

    # setup database options
    # master.option_clear()
    for pattern in designer_dboptions:
        for option, value in designer_dboptions[pattern].items():
            fpattern = f"{pattern}{option}"
            master.option_add(fpattern, value)

    # Load preferred ttk theme
    user_theme = pref.get_option("ttk_theme")
    installed_themes = s.theme_names()

    if user_theme not in installed_themes:
        msg = "User theme '%s' was not found. The default theme will be used."
        logger.warn(msg, user_theme)
        user_theme = "default"

    apply_theme(master, user_theme)


def fix_theme(master: tk.Widget, theme_name: str):
    """Do Designer related modifications to theme theme_name."""

    s: ttk.Style = get_ttk_style()

    form_error_fg = "red"
    form_error_bg = "yellow"

    if theme_name not in updated_themes:
        settings = designer_settings.copy()

        if theme_name.startswith("pbs_"):
            # it's a pygubu bootstrap theme
            entry_conf = s.configure("danger.TEntry")
            label_conf = s.configure("danger.TLabel")
            combo_conf = s.configure("danger.TCombobox")
            combo_map = s.map("danger.TCombobox")

            settings["Error.LabelFieldInfo.TLabel"]["configure"] = label_conf
            settings["Error.EntryField.TEntry"]["configure"] = entry_conf
            settings["Error.ComboboxField.TCombobox"]["configure"] = combo_conf
            settings["Error.ComboboxField.TCombobox"]["map"] = combo_map

            form_error_fg = entry_conf.get("bordercolor", form_error_fg)
            form_error_bg = entry_conf.get("fieldbackground", form_error_bg)

        s.theme_settings(theme_name, settings)
        updated_themes.append(theme_name)

        if sys.platform == "linux" and theme_name in (
            "alt",
            "default",
            "clam",
            "classic",
        ):
            # change background of comboboxes
            color = s.lookup("TEntry", "fieldbackground")
            s.map("TCombobox", fieldbackground=[("readonly", color)])
            s.map("TSpinbox", fieldbackground=[("readonly", color)])

        master.option_add("*form_error_fg", form_error_fg)
        master.option_add("*form_error_bg", form_error_bg)


def apply_theme(master: tk.Widget, theme_name: str):
    s: ttk.Style = get_ttk_style()
    current_theme: str = s.theme_use()

    def fix_theme_later():
        fix_theme(master, theme_name)

    try:
        s.theme_use(theme_name)
        master.after_idle(fix_theme_later)
        logger.debug(
            "ttk theme changed from '%s' to '%s'", current_theme, theme_name
        )
    except tk.TclError as e:
        logger.exception(e)
