import configparser
import logging
import os
import json
import tkinter as tk
from pathlib import Path
from tkinter import filedialog, messagebox

import pygubu
from appdirs import AppDirs

from pygubudesigner.services.theming import get_ttk_style

from .i18n import translator as _

logger = logging.getLogger(__name__)

dirs = AppDirs("pygubu-designer")
CONFIG_FILE = Path(dirs.user_data_dir) / "config"

logger.info(f"Using configfile: {CONFIG_FILE}")

options = {
    "widget_set": {"values": '["tk", "ttk"]', "default": "ttk"},
    "ttk_theme": {"default": "default"},
    "default_layout_manager": {
        "values": '["pack", "grid", "place"]',
        "default": "pack",
    },
    "center_preview": {
        "values": '["yes", "no"]',
        "default": "no",
    },
    "auto_generate_code": {
        "values": '["yes", "no"]',
        "default": "no",
    },
    "auto_generate_code_on_prop_change": {
        "values": '["yes", "no"]',
        "default": "no",
    },
    "single_section": {
        "values": '["yes", "no"]',
        "default": "no",
    },
    "geometry": {
        "default": "640x480",
    },
    "widget_naming_separator": {
        "values": '["NONE", "UNDERSCORE"]',
        "default": "NONE",
    },
    "widget_naming_ufletter": {
        "values": '["yes", "no"]',
        "default": "no",
    },
    "v_style_definition_file": {
        "default": "",
    },
    "maindock_layout": {
        "default": "",
    },
}

SEC_GENERAL = "GENERAL"
SEC_CUSTOM_WIDGETS = "CUSTOM_WIDGETS"  # Not used anymore
SEC_RECENT_FILES = "RECENT_FILES"
config = configparser.ConfigParser()
config.add_section(SEC_CUSTOM_WIDGETS)
config.add_section(SEC_GENERAL)
config.add_section(SEC_RECENT_FILES)

DATA_DIR = Path(__file__).parent / "data"
TEMPLATE_DIR = DATA_DIR / "code_templates"
NEW_STYLE_FILE_TEMPLATE = TEMPLATE_DIR / "customstyles.py.mako"


def initialize_configfile():
    if not os.path.exists(dirs.user_data_dir):
        os.makedirs(dirs.user_data_dir)

    if not CONFIG_FILE.exists():
        with CONFIG_FILE.open("w") as configfile:
            config.write(configfile)


def save_configfile():
    with CONFIG_FILE.open("w") as configfile:
        config.write(configfile)


def load_configfile():
    defaults = {}
    for k in options:
        defaults[k] = options[k]["default"]
    config[SEC_GENERAL] = defaults
    if CONFIG_FILE.exists():
        try:
            config.read(CONFIG_FILE)
        except configparser.MissingSectionHeaderError as e:
            logger.exception(e)
            msg = _(
                f"Configuration file at {CONFIG_FILE!s} is corrupted, program may not work as expected."
                + "If you delete this file, configuration will be set to default"
            )
            messagebox.showerror(_("Error"), msg)
        except configparser.Error as e:
            logger.exception(e)
            msg = _(
                f"Faild to parse config file at {CONFIG_FILE!s}, program may not work as expected."
            )
            messagebox.showerror(_("Error"), msg)
    else:
        initialize_configfile()


def get_option(key):
    return config.get(SEC_GENERAL, key)


def set_option(key, value, save=False):
    config.set(SEC_GENERAL, key, value)
    if save:
        save_configfile()


def recent_files_get():
    rf = []
    for __, f in config.items(SEC_RECENT_FILES):
        rf.append(f)
    return rf


def recent_files_save(file_list):
    config.remove_section(SEC_RECENT_FILES)
    config.add_section(SEC_RECENT_FILES)
    for j, p in enumerate(file_list):
        config.set(SEC_RECENT_FILES, f"f{j}", p)
    save_configfile()


def save_window_size(geom):
    set_option("geometry", geom, save=True)


def get_window_size():
    return get_option("geometry")


def get_preview_indicator_color():
    return "red"


def save_from_dict(new_values: dict):
    # General
    for key, value in new_values.items():
        config.set(SEC_GENERAL, key, value)
    # Custom Widgets
    config.remove_section(SEC_CUSTOM_WIDGETS)
    save_configfile()


def save_maindock_layout(layout: dict):
    value = json.dumps(layout)
    set_option("maindock_layout", value, True)


def get_maindock_layout():
    layout = {}
    try:
        jvalue = get_option("maindock_layout")
        layout = json.loads(jvalue)
    except json.JSONDecodeError:
        pass
    return layout


# Get user configuration
load_configfile()
