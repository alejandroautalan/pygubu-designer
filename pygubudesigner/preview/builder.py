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
import pygubu


class BuilderForPreview(pygubu.Builder):
    normalwidgets = [
        'tk.Menu',
        'tk.PanedWindow',
        'tk.PanedWindow.Pane',
        'ttk.Panedwindow',
        'ttk.Notebook',
        'ttk.Panedwindow.Pane',
        'ttk.Notebook.Tab',
        'pygubudesigner.ToplevelFramePreview',
    ]

    def _post_realize(self, bobject):
        '''Configure widget for "preview" mode.'''
        cname = bobject.wmeta.classname
        if cname not in self.normalwidgets:
            if cname.startswith('tk.Menuitem'):
                return
            self.make_previewonly(bobject.widget)
            # TODO: for custom widgets we may need to add a method
            #   'configure_for_preview(self, widget) in BuilderObject' ?

    def make_previewonly(self, w):
        '''Make widget just display with no functionality.'''
        self._crop_widget(w)

    def _crop_widget(self, w):
        '''Remove standard widget functionality.'''
        wclass = w.winfo_class()
        bindtags = w.bindtags()
        if wclass in bindtags:
            bindtags = list(bindtags)
            bindtags.remove(wclass)
            w.bindtags(bindtags)

    def get_widget_id(self, widget):
        wid = None
        for key, o in self.objects.items():
            if o.widget == widget:
                wid = key
                break
        return wid

    def show_selected(self, select_id):
        self._show_notebook_tabs(select_id)

    def _show_notebook_tabs(self, select_id):
        xpath = ".//object[@class='ttk.Notebook.Tab']"
        xpath = xpath.format(select_id)
        # find all tabs
        tabs = self.uidefinition.root.findall(xpath)
        if tabs is not None:
            for tab in tabs:
                # check if selected_id is inside this tab
                tab_id = tab.get('id')
                xpath = f".//object[@id='{select_id}']"
                o = tab.find(xpath)
                if o is not None:
                    # selected_id is inside, find the tab child
                    # and select this tab
                    xpath = './child/object[1]'
                    child = tab.find(xpath)
                    child_id = child.get('id')
                    notebook = self.objects[tab_id].widget
                    current_tab = self.objects[child_id].widget
                    notebook.select(current_tab)
                    # print(select_id, ' inside', tab_id, 'child', child_id)
