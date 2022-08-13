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
import logging
from pathlib import Path
from tkinter import ttk

from pygubudesigner import preferences as pref
from pygubudesigner.widgets.ttkstyleentry import TtkStylePropertyEditor

from .i18n import translator as _

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


class StyleHandler:
    last_definition_file = None
    last_modified_time = None

    def __init__(self, mframe, reselect_item_func):
        self.mframe = mframe
        self.after_token = None
        self.style = StyleRegister()

        # Listen to theme change events
        self.mframe.bind_all(
            "<<PygubuDesignerTtkThemeChanged>>", self._on_theme_changed
        )

        # Used for refreshing/re-populating the styles combobox.
        # Used when the style definition gets updated (simulates clicking on the treeview item.)
        self.reselect_item_func = reselect_item_func

    def start_monitoring(self):
        self.mframe.after_idle(self.check_definition_file)

    def _on_theme_changed(self, event=None):
        logger.debug("Theme changed. Force reload of style definitions.")
        self.check_definition_file(force_reload=True)

    def _apply_ttk_styles(self, style_code):
        logger.debug(_("Applying ttk style definitions"))
        try:
            if style_code:
                available_vars = {
                    "style": self.style,
                    "optiondb": self.style.master,
                }
                exec(style_code, available_vars)
                new_styles = self.style.registered_styles()
                TtkStylePropertyEditor.set_global_style_list(new_styles)
        except Exception as e:
            msg = _("ttk style definition error: %s")
            logger.error(msg, e)

    @classmethod
    def get_ttk_style_definitions(cls):
        contents = None
        style_definition_path = Path(pref.get_option("v_style_definition_file"))

        if style_definition_path.is_file():
            with style_definition_path.open() as f:
                contents = f.read()
        return contents

    def check_definition_file(self, force_reload=False):
        # print('checking definitions')
        # Get the path to the style definition file.
        style_definition_path = Path(pref.get_option("v_style_definition_file"))

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
            contents = None
            with style_definition_path.open() as f:
                contents = f.read()

            # Clear and reload all the definitions.

            # Reason: so that definitions that are no longer in the definition file
            # will no longer populate in the style combobox.
            StyleRegister.STYLE_DEFINITIONS.clear()

            self._apply_ttk_styles(contents)

            # Re-select the selected item so the style combobox
            # will show the latest styles from the definition file.
            if self.reselect_item_func is not None:
                self.reselect_item_func()

        # schedule new check
        self.after_token = self.mframe.after(1000, self.check_definition_file)
