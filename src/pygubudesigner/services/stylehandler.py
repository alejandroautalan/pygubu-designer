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
import sys
import importlib
import logging
from pathlib import Path
from tkinter import ttk

from pygubudesigner.properties.editors import TtkStylePropertyEditor
from ..i18n import translator as _

logger = logging.getLogger(__name__)


# StyleRegister
# This class y used to capture the styles defined by the user.
#
# Some widgets still need the option database to fully configure the
# style apperance (like the TCombobox) so, you can use the master
# attribute of the style to call the functions option_add, option_get, etc
#
class StyleRegister(ttk.Style):
    STYLE_DEFINITIONS = set()

    def _add_style(self, style):
        if style not in self.STYLE_DEFINITIONS:
            self.STYLE_DEFINITIONS.add(style)

    def registered_styles(self):
        """Return list of captured styles"""
        return list(self.STYLE_DEFINITIONS)

    def configure(self, style, query_opt=None, **kw):
        self._add_style(style)
        super().configure(style, query_opt, **kw)


class StyleHandlerAndMonitor:
    """Monitor changes in a style definitions file and applies them
    in a specified root window.
    """

    current_definition_file = None
    last_definition_file = None
    last_modified_time = None
    required_function_name = "setup_ttk_styles"

    def __init__(self):
        self.root = None
        self.after_token = None

    def start_monitoring(self, root):
        if self.root is None:
            self.root = root
            self.style = StyleRegister(root)
            # Listen to theme change events
            self.root.bind_all(
                "<<PygubuDesignerTtkThemeChanged>>", self._on_theme_changed
            )
            self.root.after_idle(self.check_definition_file)

    def apply_user_styles(self, root):
        """Apply user styles in a toplevel preview."""

        style_definition_path = self.current_definition_file
        file_valid = (
            style_definition_path is not None
            and style_definition_path.is_file()
        )
        if file_valid:
            self._run_styles_module(
                style_definition_path, root, collect_styles=False
            )

    def _on_theme_changed(self, event=None):
        logger.debug("Theme changed. Force reload of style definitions.")
        self.check_definition_file(force_reload=True)

    def _run_styles_module(self, module_path: Path, root, collect_styles=True):

        if not module_path.match("*.py"):
            logger.debug("Invalid python module file name.")
            return

        try:
            module_name = module_path.name[:-3]

            spec = importlib.util.spec_from_file_location(
                module_name, module_path
            )
            module = importlib.util.module_from_spec(spec)

            sys.modules[module_name] = module
            spec.loader.exec_module(module)

            if hasattr(module, self.required_function_name):
                logger.debug(_("Applying ttk style definitions"))
                module.setup_ttk_styles(root)
            else:
                msg = "Styles definition file does not have the required function: %s"
                logger.info(msg, self.required_function_name)

            if collect_styles:
                new_styles = self.style.registered_styles()
                TtkStylePropertyEditor.set_global_style_list(new_styles)
        except Exception as e:
            msg = _("ttk style definition error: %s")
            logger.error(msg, e)

    @classmethod
    def get_ttk_styles_module(cls):
        module = None
        if cls.current_definition_file is not None:
            if cls.current_definition_file.is_file():
                module = cls.current_definition_file.stem
        return module

    @classmethod
    def set_definition_file(cls, filepath):
        if not isinstance(filepath, Path):
            raise ValueError()
        cls.current_definition_file = filepath
        logger.debug("New definitions file %s", str(filepath))

    @classmethod
    def clear_definition_file(cls):
        StyleRegister.STYLE_DEFINITIONS.clear()
        TtkStylePropertyEditor.set_global_style_list([])
        cls.current_definition_file = None

    def check_definition_file(self, force_reload=False):
        # Get the path to the style definition file.
        style_definition_path = self.current_definition_file
        if style_definition_path is not None:
            do_reload = False
            has_definition_file = False
            is_new_file = False
            if style_definition_path.is_file():
                has_definition_file = True
                file_mtime = style_definition_path.stat().st_mtime
                if StyleHandler.last_definition_file != style_definition_path:
                    do_reload = True
                    is_new_file = True
                    StyleHandler.last_definition_file = style_definition_path
                    StyleHandler.last_modified_time = file_mtime
                if not is_new_file:
                    if file_mtime > StyleHandler.last_modified_time:
                        do_reload = True
                        StyleHandler.last_modified_time = file_mtime
            if do_reload or (has_definition_file and force_reload):
                # Clear and reload all the definitions.

                # Reason: so that definitions that are no longer in the definition file
                # will no longer populate in the style combobox.
                StyleRegister.STYLE_DEFINITIONS.clear()

                self._run_styles_module(style_definition_path, self.root)

                # Re-select the selected item so the style combobox
                # will show the latest styles from the definition file.
                self.root.event_generate("<<PygubuDesignerUserStylesApplied>>")

        # schedule new check
        self.after_token = self.root.after(1000, self.check_definition_file)


# Patch ttk module, so designer can "see" style changes.
if not hasattr(ttk, "_style_original"):
    ttk._style_original = ttk.Style
    ttk.Style = StyleRegister


StyleHandler = StyleHandlerAndMonitor()
