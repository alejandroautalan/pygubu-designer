import sys
import os
import pathlib
import logging
import importlib
import tkinter as tk

from pygubu.component.uidefinition import UIDefinition
from ..widgetdescr import WidgetMeta
from ..i18n import translator
from .stylehandler import StyleHandler


logger = logging.getLogger(__name__)
_ = translator


def load_custom_widget(path: pathlib.Path):
    if not path.match("*.py"):
        return
    dirname = str(path.parent)
    modulename = path.name[:-3]
    if dirname not in sys.path:
        sys.path.append(dirname)
    try:
        importlib.import_module(modulename)
    except Exception as e:
        logger.exception(e)
        raise e


class Project:
    """Store project data for designer."""

    settings_default = {
        "name": "",
        "description": "",
        "module_name": "",
        "template": "application",
        "main_widget": "",
        "main_classname": "",
        "main_menu": "",
        "output_dir": "",
        "output_dir2": "",
        "import_tkvariables": False,
        "use_ttk_styledefinition_file": False,
        "use_i18n": False,
        "all_ids_attributes": False,
        "ttk_style_definition_file": "",
        "generate_code_onsave": False,
    }

    def __init__(self):
        self.fpath = None
        self.uidefinition: UIDefinition = None
        self.custom_widgets: list = []
        self.settings: dict = {}

    @property
    def generate_code_onsave(self):
        key = "generate_code_onsave"
        return tk.getboolean(self.settings.get(key, False))

    def get_relative_path(self, path):
        path = pathlib.Path(path).resolve()  # fix windows junction
        return os.path.relpath(path, start=self.fpath.parent)

    def save(self, filename):
        self.fpath = pathlib.Path(filename)
        self.uidefinition.custom_widgets = self.custom_widgets
        self.uidefinition.project_settings = self.settings
        self.uidefinition.save(filename)

    def get_full_settings(self) -> dict:
        settings = self.settings_default.copy()
        settings.update(self.settings)
        cwlist = []
        for path in self.custom_widgets:
            cwlist.append(path)
        settings["custom_widgets"] = cwlist
        return settings

    def set_full_settings(self, new_settings: dict):
        self._process_new_settings(new_settings)
        self.custom_widgets = new_settings.pop("custom_widgets", [])
        self.settings = new_settings

    def _process_new_settings(self, new_settings: dict):
        # reload ttk styles definition file:
        key = "ttk_style_definition_file"
        old_file = self.settings.get(key, None)
        new_file = new_settings.get(key, None)
        if old_file != new_file:
            StyleHandler.clear_definition_file()
            if new_file:
                theme_path: pathlib.Path = self.fpath.parent / new_file
                if theme_path.exists() and theme_path.is_file():
                    # Load definitions file.
                    StyleHandler.set_definition_file(theme_path)
                    logger.debug("New ttk style definition file loaded.")

    def load_custom_widgets(self):
        uidir = pathlib.Path(self.fpath).parent.resolve()
        Project.load_widget_builders(uidir, self.custom_widgets)

    @staticmethod
    def load_widget_builders(uidir: pathlib.Path, custom_widgets: list):
        path_list = []
        notfound_list = []
        # Xml will have relative paths to UI file directory
        for cw in custom_widgets:
            cw_path: pathlib.Path = pathlib.Path(uidir, cw).resolve()
            if cw_path.exists():
                path_list.append(cw_path)
            else:
                notfound_list.append(cw_path)
        if notfound_list:
            # Notify user some path does not exits
            # raise exception
            msg = "Custom widgets not found:\n" + "\n".join(
                (str(f) for f in notfound_list)
            )
            raise Exception(msg)
        else:
            # Load builders
            for path in path_list:
                load_custom_widget(path)

    @staticmethod
    def load(filename) -> "Project":
        uidef = UIDefinition(wmetaclass=WidgetMeta)
        uidef.load_file(filename)
        uidir = pathlib.Path(filename).parent.resolve()

        # Load custom widgets
        Project.load_widget_builders(uidir, uidef.custom_widgets)

        # Load theme file
        theme_file = uidef.project_settings.get("ttk_style_definition_file", "")
        StyleHandler.clear_definition_file()
        if theme_file:
            theme_path: pathlib.Path = uidir / theme_file
            if theme_path.exists() and theme_path.is_file():
                # Load definitions file.
                StyleHandler.set_definition_file(theme_path)

        project = Project()
        project.fpath = filename
        project.uidefinition = uidef
        project.custom_widgets = uidef.custom_widgets
        project.settings = uidef.project_settings
        return project
