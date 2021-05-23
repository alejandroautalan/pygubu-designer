# encoding: utf-8
import os
import sys
import logging
from mako.lookup import TemplateLookup

try:
    import tkinter as tk
    from tkinter import ttk
    from tkinter import filedialog
    from tkinter import messagebox
except:
    import Tkinter as tk
    import ttk
    import tkMessageBox as messagebox
    import tkFileDialog as filedialog
import pygubu
from .codebuilder import UI2Code

logger = logging.getLogger(__name__)
CURRENT_DIR = os.path.abspath(os.path.dirname(__file__))
TEMPLATE_DIR = os.path.join(CURRENT_DIR, 'template')
print('TEMPLATE_DIR', TEMPLATE_DIR)
makolookup = TemplateLookup(directories=[TEMPLATE_DIR])

class ScriptGenerator(object):
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
        myvars = ['widgetlistvar', 'widgetlist_keyvar', 'template_var',
                  'classnamevar', 'template_desc_var', 'import_tkvars_var']
        builder.import_variables(self, myvars)
        
        self.txt_code = builder.get_object('txt_code')
        self.cb_import_tkvars = builder.get_object('cb_import_tkvars')
        
        _ = self.app.translator
        self.msgtitle = _('Script Generator')
        
        self.template_desc = {
            'application': _('Create a pygubu application script using the UI definition.'),
            'codescript': _('Create a coded version of the UI definition.'),
            'widget': _('Create a base class for your custom widget.')
        }
        self.template_var.set('application')
        self.import_tkvars_var.set(True)
        
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
                'callbacks': '',
                'tkvariables': [],
            }
            
            if template == 'application':
                code = generator.generate(uidef, target, as_class=False, tabspaces=8)
                context['callbacks'] = code['callbacks']
                if self.import_tkvars_var.get():
                    context['tkvariables'] = code['tkvariables']
                tpl = makolookup.get_template('app.py.mako')
                final_code = tpl.render(**context)
                self.set_code(final_code)
            elif template == 'widget':
                code = generator.generate_widget_class(uidef, target)
                context['widget_code'] = code[target]
                context['import_lines'] = code['imports']
                context['callbacks'] = code['callbacks']
                tpl = makolookup.get_template('widget.py.mako')
                final_code = tpl.render(**context)
                self.set_code(final_code)
            elif template == 'codescript':
                code = generator.generate(uidef, target, as_class=True, 
                                          tabspaces=8)
                context['widget_code'] = code[target]
                context['import_lines'] = code['imports']
                context['callbacks'] = code['callbacks']
                tpl = makolookup.get_template('script.py.mako')
                final_code = tpl.render(**context)
                self.set_code(final_code)
    
    def on_code_copy_clicked(self):
        text = self.get_code()
        self.txt_code.clipboard_clear()
        self.txt_code.clipboard_append(text)
        
        _ = self.app.translator
        msg = _('Code copied')
        messagebox.showinfo(title=self.msgtitle, message=msg,
                            parent=self.widgetlist.winfo_toplevel())
    
    def on_code_template_changed(self, clear_code=True):
        template = self.template_var.get()
        classname = self.get_classname()
        self.cb_import_tkvars.configure(state="disabled")
        if template == 'application':
            name = '{0}App'.format(classname)
            self.classnamevar.set(name)
            self.cb_import_tkvars.configure(state="normal")
        elif template == 'codescript':
            name = '{0}App'.format(classname)
            self.classnamevar.set(name)
        elif template == 'widget':
            name = '{0}Widget'.format(classname)
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
            'initialfile': '{0}.py'.format(filename),
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
        name = os.path.splitext(self.projectname)[0]
        return self.camel_case(name)
    
    def form_valid(self):
        valid = True
        
        _ = self.app.translator
        mbtitle = self.msgtitle
        widget = self.widgetlist.current()
        parent = self.widgetlist.winfo_toplevel()
        if widget is None:
            valid = False
            messagebox.showwarning(title=mbtitle, message=_('Select widget'),
                                   parent=parent)
        template = self.template_var.get()
        if valid and template is None:
            valid = False
            messagebox.showwarning(title=mbtitle, message=_('Select template'),
                                   parent=parent)
        classname = self.classnamevar.get()
        if valid and classname == '':
            valid = False
            messagebox.showwarning(title=mbtitle, message=_('Enter classname'),
                                   parent=parent)
        
        return valid
    
    def set_code(self, text):
        self.txt_code.delete('0.0', 'end')
        self.txt_code.insert('0.0', text)
    
    def get_code(self):
        return self.txt_code.get('0.0', 'end')

    def reset(self):
        self.set_code('')
        self.configure()
    
