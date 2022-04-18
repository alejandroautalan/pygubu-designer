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
import keyword
import logging
import pathlib
import re
from tkinter import filedialog, messagebox

import black
from mako.lookup import TemplateLookup

from .codebuilder import UI2Code

logger = logging.getLogger(__name__)
CURRENT_DIR = pathlib.Path(__file__).parent
TEMPLATE_DIR = CURRENT_DIR / 'template'
makolookup = TemplateLookup(directories=[TEMPLATE_DIR])
RE_IDENTIFIER = re.compile('[_A-Za-z][_a-zA-Z0-9]*$')


class ScriptGenerator:
    def __init__(self, app):
        self.app = app
        self.builder = builder = app.builder
        self.tree = app.tree_editor
        self.projectname = ''

        self.widgetlist = builder.get_object('widgetlist')

        self.widgetlistvar = None
        self.widgetlist_keyvar = None
        self.template_var = None
        self.classnamevar = None
        self.template_desc_var = None
        self.import_tkvars_var = None
        self.use_ttkdefs_file_var = None
        myvars = [
            'widgetlistvar',
            'widgetlist_keyvar',
            'template_var',
            'classnamevar',
            'template_desc_var',
            'import_tkvars_var',
            'use_ttkdefs_file_var',
        ]
        builder.import_variables(self, myvars)

        self.txt_code = builder.get_object('txt_code')
        self.cb_import_tkvars = builder.get_object('cb_import_tkvars')

        _ = self.app.translator
        self.msgtitle = _('Script Generator')

        self.template_desc = {
            'application': _(
                'Create a pygubu application script using the UI definition.'
            ),
            'codescript': _('Create a coded version of the UI definition.'),
            'widget': _('Create a base class for your custom widget.'),
        }
        self.template_var.set('application')
        self.import_tkvars_var.set(True)
        self.use_ttkdefs_file_var.set(True)

    def camel_case(self, st):
        output = ''.join(x for x in st.title() if x.isalnum())
        return output

    def on_code_generate_clicked(self):
        if self.form_valid():
            tree_item = self.widgetlist_keyvar.get()
            template = self.template_var.get()
            generator = UI2Code()
            uidef = self.tree.tree_to_uidef()
            target = self.tree.get_widget_id(tree_item)
            target_class = self.tree.get_widget_class(tree_item)
            class_name = self.classnamevar.get()

            main_widget_is_toplevel = False
            if target_class == 'tk.Toplevel':
                main_widget_is_toplevel = True

            context = {
                'project_name': self.projectname,
                'class_name': class_name,
                'main_widget_is_toplevel': main_widget_is_toplevel,
                'main_widget': target,
                'widget_base_class': target_class,
                'widget_code': None,
                'import_lines': None,
                'ttk_styles': None,
                'callbacks': '',
                'tkvariables': [],
                'has_ttk_styles': False,
                'set_project_path': False,
            }

            black_fm = black.FileMode()
            if template == 'application':
                generator.add_import_line('pathlib')
                if self.use_ttkdefs_file_var.get():
                    generator.add_import_line('tkinter.ttk', 'ttk', priority=1)
                generator.add_import_line('pygubu', priority=10)
                code = generator.generate_app_with_ui(uidef, target)

                context['import_lines'] = code['imports']
                # Set project paths
                context['set_project_path'] = True
                # Style definitions
                ttk_styles_code = code['ttkstyles']
                if self.use_ttkdefs_file_var.get() and ttk_styles_code:
                    context['has_ttk_styles'] = True
                context['ttk_styles'] = ttk_styles_code
                # Callbacks
                context['callbacks'] = code['callbacks']
                # Tk Variables
                if self.import_tkvars_var.get():
                    context['tkvariables'] = code['tkvariables']
                tpl = makolookup.get_template('app.py.mako')
                final_code = tpl.render(**context)
                final_code = black.format_str(final_code, mode=black_fm)
                self.set_code(final_code)
            elif template == 'widget':
                generator.add_import_line('tkinter', 'tk')
                if self.use_ttkdefs_file_var.get():
                    generator.add_import_line('tkinter.ttk', 'ttk', priority=1)
                code = generator.generate_app_widget(uidef, target)
                context['widget_code'] = code[target]
                context['import_lines'] = code['imports']
                context['callbacks'] = code['callbacks']
                # Style definitions
                ttk_styles_code = code['ttkstyles']
                if self.use_ttkdefs_file_var.get() and ttk_styles_code:
                    context['has_ttk_styles'] = True
                context['ttk_styles'] = ttk_styles_code

                tpl = makolookup.get_template('widget.py.mako')
                final_code = tpl.render(**context)
                final_code = black.format_str(final_code, mode=black_fm)
                self.set_code(final_code)
            elif template == 'codescript':
                if not main_widget_is_toplevel:
                    generator.add_import_line('tkinter', 'tk')
                if self.use_ttkdefs_file_var.get():
                    generator.add_import_line('tkinter.ttk', 'ttk', priority=1)
                code = generator.generate_app_code(uidef, target)
                context['widget_code'] = code[target]
                context['import_lines'] = code['imports']
                context['callbacks'] = code['callbacks']
                # Style definitions
                ttk_styles_code = code['ttkstyles']
                if self.use_ttkdefs_file_var.get() and ttk_styles_code:
                    context['has_ttk_styles'] = True
                context['ttk_styles'] = ttk_styles_code

                tpl = makolookup.get_template('script.py.mako')
                final_code = tpl.render(**context)
                final_code = black.format_str(final_code, mode=black_fm)
                self.set_code(final_code)

    def on_code_copy_clicked(self):
        text = self.get_code()
        self.txt_code.clipboard_clear()
        self.txt_code.clipboard_append(text)

        _ = self.app.translator
        msg = _('Code copied')
        messagebox.showinfo(
            title=self.msgtitle, message=msg, parent=self.widgetlist.winfo_toplevel()
        )

    def on_code_template_changed(self, clear_code=True):
        template = self.template_var.get()
        classname = self.get_classname()
        self.cb_import_tkvars.configure(state="disabled")
        if template == 'application':
            name = f'{classname}App'
            self.classnamevar.set(name)
            self.cb_import_tkvars.configure(state="normal")
        elif template == 'codescript':
            name = f'{classname}App'
            self.classnamevar.set(name)
        elif template == 'widget':
            name = f'{classname}Widget'
            self.classnamevar.set(name)
        # Update template description
        self.template_desc_var.set(self.template_desc[template])
        if clear_code:
            self.set_code('')

    def on_code_save_clicked(self):
        _ = self.app.translator
        filename = (self.classnamevar.get()).lower()
        options = {
            'defaultextension': '.py',
            'filetypes': ((_('Python Script'), '*.py'), (_('All'), '*.*')),
            'initialfile': f'{filename}.py',
        }
        fname = filedialog.asksaveasfilename(**options)
        if fname:
            with open(fname, 'w') as out:
                out.write(self.get_code())

    def configure(self):
        self.projectname = self.app.project_name()
        wlist = self.tree.get_topwidget_list()
        self.widgetlist.configure(values=wlist)
        self.classnamevar.set(self.get_classname())

        if len(wlist) > 0:
            key = wlist[0][0]
            self.widgetlist_keyvar.set(key)
        self.on_code_template_changed(False)

    def get_classname(self):
        name = pathlib.Path(self.projectname).stem
        return self.camel_case(name)

    def form_valid(self):
        valid = True

        _ = self.app.translator
        mbtitle = self.msgtitle
        widget = self.widgetlist.current()
        parent = self.widgetlist.winfo_toplevel()
        if widget is None:
            valid = False
            messagebox.showwarning(
                title=mbtitle, message=_('Select widget'), parent=parent
            )
        template = self.template_var.get()
        if valid and template is None:
            valid = False
            messagebox.showwarning(
                title=mbtitle, message=_('Select template'), parent=parent
            )
        classname = self.classnamevar.get()
        if valid and classname == '':
            valid = False
            messagebox.showwarning(
                title=mbtitle, message=_('Enter classname'), parent=parent
            )
        if valid and (
            keyword.iskeyword(classname) or not RE_IDENTIFIER.match(classname)
        ):
            valid = False
            messagebox.showwarning(
                title=mbtitle, message=_('Invalid classname'), parent=parent
            )

        return valid

    def set_code(self, text):
        self.txt_code.delete('0.0', 'end')
        self.txt_code.insert('0.0', text)

    def get_code(self):
        return self.txt_code.get('0.0', 'end-1c')

    def reset(self):
        self.set_code('')
        self.configure()
