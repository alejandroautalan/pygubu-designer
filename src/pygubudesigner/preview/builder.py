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
import pygubu
from pygubu.utils.widget import crop_widget
from pygubu.component.plugin_manager import PluginManager


logger = logging.getLogger("pygubu.designer")


class BuilderForPreview(pygubu.Builder):
    normalwidgets = [
        "tk.Menu",
        "tk.PanedWindow",
        "tk.PanedWindow.Pane",
        "ttk.Panedwindow",
        "ttk.Notebook",
        "ttk.Panedwindow.Pane",
        "ttk.Notebook.Tab",
    ]

    def _get_builder_for(self, builder_uid):
        builder = PluginManager.get_preview_builder_for(builder_uid)
        if builder is not None:
            return builder
        return super()._get_builder_for(builder_uid)

    def _post_realize(self, bobject):
        """Configure widget for "preview" mode."""
        cname = bobject.wmeta.classname
        if cname not in self.normalwidgets:
            if cname.startswith("tk.Menuitem"):
                return
            self.make_previewonly(bobject)

    def make_previewonly(self, bobject):
        """Make widget just display with no functionality."""
        crop_widget(bobject.widget, recursive=False)
        builder_uid = bobject.wmeta.classname
        PluginManager.configure_for_preview(builder_uid, bobject.widget)

    def get_widget_id(self, widget):
        wid = None
        # first search for exact match
        for key, o in self.objects.items():
            if o.widget == widget:
                wid = key
                break
        if wid is None:
            # If no match found, try to match with a children widget
            for key, o in self.objects.items():
                for childw in o.widget.winfo_children():
                    if childw == widget:
                        wid = key
                        break
                if wid is not None:
                    break
        return wid

    def show_selected(self, selected_id):
        PluginManager.ensure_visibility_in_preview(self, selected_id)
