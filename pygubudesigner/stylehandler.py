# encoding: UTF-8
#
# Copyright 2012-2021 Alejandro Autalán
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
from os import path
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
        '''Return list of captured styles'''
        return list(self.STYLE_DEFINITIONS)

    def configure(self, style, query_opt=None, **kw):
        self._add_style(style)
        super(StyleRegister, self).configure(style, query_opt, **kw)


class StyleHandler:
    last_definition_file = None
    last_modified_time = None

    def __init__(self, mframe):
        self.mframe = mframe
        self.after_token = None
        self.style = StyleRegister()

    def start_monitoring(self):
        self.mframe.after_idle(self.check_definition_file)

    def _apply_ttk_styles(self, style_code):
        logger.debug(_("Applying ttk style definitions"))
        try:
            if style_code:
                exec(style_code, {'style': self.style})
                new_styles = self.style.registered_styles()
                TtkStylePropertyEditor.set_global_style_list(new_styles)
        except Exception as e:
            msg = _('ttk style definition error: %s')
            logger.error(msg, e)

    @classmethod
    def get_ttk_style_difinitions(cls):
        contents = None
        style_definition_path = pref.get_option('v_style_definition_file')

        if path.isfile(style_definition_path):
            with open(style_definition_path) as f:
                contents = f.read()
        return contents

    def check_definition_file(self):
        # print('checking definitions')
        # Get the path to the style definition file.
        style_definition_path = pref.get_option('v_style_definition_file')

        do_reload = False
        is_new_file = False
        if path.isfile(style_definition_path):
            file_mtime = path.getmtime(style_definition_path)
            if StyleHandler.last_definition_file != style_definition_path:
                do_reload = True
                is_new_file = True
                StyleHandler.last_definition_file = style_definition_path
                StyleHandler.last_modified_time = file_mtime
            if not is_new_file:
                if file_mtime > StyleHandler.last_modified_time:
                    do_reload = True
                    StyleHandler.last_modified_time = file_mtime
        if do_reload:
            contents = None
            with open(style_definition_path) as f:
                contents = f.read()
                
            # Clear and reload all the definitions.
            
            # Reason: so that definitions that are no longer in the definition file 
            # will no longer populate in the style combobox.
            StyleRegister.STYLE_DEFINITIONS.clear()
            
            self._apply_ttk_styles(contents)
        # schedule new check
        self.after_token = self.mframe.after(1000, self.check_definition_file)
