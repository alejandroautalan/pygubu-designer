import os
import pathlib
import logging
import json
import platformdirs as pdirs

from pathlib import Path
from enum import auto

try:
    from enum import StrEnum
except ImportError:
    from backports.strenum import StrEnum


logger = logging.getLogger(__name__)

APP_NAME = "pygubu-designer"

USER_DATA_DIR = Path(pdirs.user_data_dir(APP_NAME))
CONFIG_FILE = USER_DATA_DIR / "config.json"

DATA_DIR = Path(__file__).parent / "data"
TEMPLATE_DIR = DATA_DIR / "code_templates"
NEW_STYLE_FILE_TEMPLATE = TEMPLATE_DIR / "customstyles.py.mako"


class CfgOption(StrEnum):
    WIDGET_SET = auto()
    TTK_THEME = auto()
    DEFAULT_LAYOUT_MANAGER = auto()
    CENTER_PREVIEW = auto()
    WINDOW_GEOMETRY = auto()
    WIDGET_NAMING_USE_UNDERSCORE = auto()
    WIDGET_NAMING_UFLETTER = auto()
    MAINDOCK_LAYOUT = auto()
    RECENT_FILES = auto()


default_config = {
    CfgOption.WIDGET_SET: "ttk",
    CfgOption.TTK_THEME: "default",
    CfgOption.DEFAULT_LAYOUT_MANAGER: "pack",
    CfgOption.CENTER_PREVIEW: True,
    CfgOption.WINDOW_GEOMETRY: "1280x720",
    CfgOption.WIDGET_NAMING_USE_UNDERSCORE: False,
    CfgOption.WIDGET_NAMING_UFLETTER: False,
    CfgOption.MAINDOCK_LAYOUT: {},
    CfgOption.RECENT_FILES: {},
}


class AppPreferences:
    def __init__(self):
        self.config = {}

        if CONFIG_FILE.exists():
            self.load()
        else:
            self.config = default_config.copy()
            self.create_file()

    def load(self):
        with CONFIG_FILE.open() as cfile:
            try:
                self.config = json.load(cfile)
            except json.JSONDecodeError as e:
                msg = f"Error in config file {CONFIG_FILE}"
                raise RuntimeError(msg) from e

    def save(self, data: dict):
        with CONFIG_FILE.open("w") as cfile:
            json.dump(data, cfile, indent=2)

    def create_file(self):
        if not USER_DATA_DIR.exists():
            os.makedirs(USER_DATA_DIR)
        self.save(default_config)

    @property
    def recent_files(self):
        return self.config[CfgOption.RECENT_FILES]

    @recent_files.setter
    def recent_files(self, flist: dict):
        self.config[CfgOption.RECENT_FILES] = flist
        self.save(self.config)

    @property
    def geometry(self):
        return self.config[CfgOption.WINDOW_GEOMETRY]

    @geometry.setter
    def geometry(self, value: str):
        self.config[CfgOption.WINDOW_GEOMETRY] = value
        self.save(self.config)

    @property
    def maindock_layout(self):
        return self.config[CfgOption.MAINDOCK_LAYOUT]

    @maindock_layout.setter
    def maindock_layout(self, dock_config: dict):
        self.config[CfgOption.MAINDOCK_LAYOUT] = dock_config
        self.save(self.config)

    @property
    def ttk_theme(self):
        return self.config[CfgOption.TTK_THEME]

    @property
    def preview_indicator_color(self):
        return "red"

    @property
    def center_preview(self):
        return self.config[CfgOption.CENTER_PREVIEW]

    @property
    def default_layout_manager(self):
        return self.config[CfgOption.DEFAULT_LAYOUT_MANAGER]

    @property
    def widget_naming_use_underscore(self):
        return self.config[CfgOption.WIDGET_NAMING_USE_UNDERSCORE]

    @property
    def widget_naming_ufletter(self):
        return self.config[CfgOption.WIDGET_NAMING_UFLETTER]

    @property
    def widget_set(self):
        return self.config[CfgOption.WIDGET_SET]

    @property
    def single_section(self):
        return False


preferences = AppPreferences()
