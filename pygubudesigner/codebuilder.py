from __future__ import unicode_literals, print_function
import os
from collections import OrderedDict
from pygubu.builder import Builder, CLASS_MAP, CB_TYPES
from pygubu.builder.builderobject import BuilderObject, grouper, register_widget
from pygubu.builder.widgetmeta import WidgetMeta
from pygubu.stockimage import TK_BITMAP_FORMATS
from pygubu.builder.tkstdwidgets import TKToplevel


class ToplevelOrTk(TKToplevel):
    def code_realize(self, boparent, code_identifier=None):
        if code_identifier is not None:
            self._code_identifier = code_identifier
        lines = []
        master = boparent.code_child_master()
        init_args = self._get_init_args()
        bag = []
        for pname, value in init_args.items():
            s = "{0}='{1}'".format(pname, value)
            bag.append(s)
        kwargs = ''
        if bag:
            kwargs = ', {0}'.format(', '.join(bag))
        if init_args:
            # has init args defined so create a TkToplevel
            s = "{0} = {1}({2}{3})"
        else:
            s = "{0} = tk.Tk() if master is None else {1}({2}{3})"
        s = s.format(self.code_identifier(), self._code_class_name(),
                     master, kwargs)
        lines.append(s)
        return lines


register_widget('pygubudesigner.ToplevelOrTk',
                ToplevelOrTk, 'ToplevelOrTk', tuple())



class UI2Code(Builder):
    def __init__(self):
        super(UI2Code, self).__init__()
        
        self.buffer = None
        self.as_class = False
        self._code_imports = OrderedDict()
        self._tkvariables = {}
        self._tkimages = {}
        self._callbacks = {}
        self._import_ttk = True;
        self._code = []
        self.uidefinition = None
        self._builder = Builder()
        self._options = {}
    
    def _process_options(self, kw):
        kwdef = {
            'as_class': True,
            'tabspaces': 8
            }
        kwdef.update(kw)
        self._options = kwdef
        self.as_class = self._options['as_class']
        tabspaces = self._options['tabspaces']
        
    def _process_results(self, target):
        tabspaces = self._options['tabspaces']
        code = []
        for line in self._code:
            line = '{0}{1}\n'.format(' ' * tabspaces, line)
            code.append(line)
        code = ''.join(code)
        
        code_imports = self._process_imports()
        code_imports = '\n'.join(code_imports)
        code_callbacks = self._process_callbacks()
        code_callbacks = '\n'.join(code_callbacks)
        code = ''.join(code)
        cc = {
            'imports': code_imports,
            target: code,
            'callbacks': code_callbacks,
            'tkvariables': list(self._tkvariables.keys())
            }
        return cc
    
    def _toplevel_or_tk(self, target):
        wmeta = self.uidefinition.get_widget(target)
        if wmeta.classname == 'tk.Toplevel':
            wmeta.classname = 'pygubudesigner.ToplevelOrTk'
            self.uidefinition.replace_widget(target, wmeta)
    
    def generate(self, uidef, target, **kw):
        self.uidefinition = uidef
        self._process_options(kw)
        
        mastermeta = WidgetMeta('','master')
        builder = BuilderObject(self, mastermeta)
        self._toplevel_or_tk(target)
        wmeta = self.uidefinition.get_widget(target)

        if wmeta is not None:
            self._code_realize(builder, wmeta)
        return self._process_results(target)
    
    def generate_widget_class(self, uidef, target, **kw):
        self.uidefinition = uidef
        self._process_options(kw)
        
        mastermeta = wmeta = self.uidefinition.get_widget(target)
        builder = bmaster = BuilderObject(self, mastermeta)
        if wmeta is not None:
            originalid = wmeta.identifier
            wmeta.identifier = 'self'
            
            if wmeta.classname not in CLASS_MAP:
                self._builder._import_class(wmeta.classname)

            if wmeta.classname in CLASS_MAP:
                bclass = CLASS_MAP[wmeta.classname].builder
                builder = bclass.factory(self, wmeta)
                uniqueid = builder.code_identifier()
                masterid = bmaster.code_child_master()
                
                for childmeta in \
                    self.uidefinition.widget_children(target):
                    childid = self._code_realize(builder, childmeta)
                    code = builder.code_child_add(childid)
                    self._code.extend(code)
        
        return self._process_results(target)
    
    def code_classname_for(self, bobject):
        wmeta = bobject.wmeta
        cname = None
        if bobject.class_ is not None:
            if wmeta.classname == 'pygubudesigner.ToplevelOrTk':
                cname = 'tk.Toplevel'
            elif wmeta.classname.startswith('tk.'):
                cname = wmeta.classname
            elif wmeta.classname.startswith('ttk.'):
                self._import_ttk = True;
                cname = wmeta.classname
            else:
                module = bobject.class_.__module__
                cname = bobject.class_.__name__
                if module not in self._code_imports:
                    self._code_imports[module] = set((cname,))
                else:
                    self._code_imports[module].add(cname)
        return cname
    
    def _process_imports(self):
        lines = []
        s = 'import tkinter as tk'
        lines.append(s)
        if self._import_ttk:
            s = 'import tkinter.ttk as ttk'
            lines.append(s)
        skeys = sorted(self._code_imports.keys())
        for mname in skeys:
            names = sorted(self._code_imports[mname])
            for group in grouper(names, 4):
                bag = []
                for cname in group:
                    if cname is not None:
                        bag.append(cname)
                clist = None
                if len(bag) > 1:
                    clist = '({0})'.format(', '.join(bag))
                else:
                    clist = ''.join(bag)
                line = 'from {0} import {1}'.format(mname, clist)
                lines.append(line)
        return lines
    
    def code_create_variable(self, name_or_desc, value, vtype=None):
        vname, type_from_name = self._process_variable_description(name_or_desc)
        vname_in_code = vname
        if vname not in self._tkvariables:
            var_init = ''
            if value is None:
                value = "''"
            else:
                if type_from_name == 'string':
                    value = "'{0}'".format(value)
            if vtype is None:
                var_init = 'tk.{0}Var(value={1})'.format(
                    type_from_name.capitalize(), value)
            else:
                var_init = '{0}(value={1})'.format(str(vtype), value)
            if self.as_class:
                vname_in_code = 'self.{0}'.format(vname)
            line = '{0} = {1}'.format(vname_in_code, var_init)
            self._code.append(line)
            self._tkvariables[vname] = vname_in_code
        return self._tkvariables[vname]
    
    def _code_realize(self, bmaster, wmeta):
        originalid = wmeta.identifier
        uniqueid = None
        
        if wmeta.classname not in CLASS_MAP:
            self._builder._import_class(wmeta.classname)

        if wmeta.classname in CLASS_MAP:
            bclass = CLASS_MAP[wmeta.classname].builder
            builder = bclass.factory(self, wmeta)
            uniqueid = builder.code_identifier()
            masterid = bmaster.code_child_master()
            
            if self.as_class:
                if not masterid:
                    uniqueid = 'self'
                else:
                    uniqueid = 'self.' + uniqueid
            
            create = builder.code_realize(bmaster, uniqueid)
            self._code.extend(create)
            
            # Children
            for childmeta in \
                self.uidefinition.widget_children(originalid):
                childid = self._code_realize(builder, childmeta)
                code = builder.code_child_add(childid)
                self._code.extend(code)
            
            # configuration
            configure = builder.code_configure()
            self._code.extend(configure)
            
            # layout
            layout = builder.code_layout(parentid=masterid)
            self._code.extend(layout)
            
            # callbacks
            commands = builder.code_connect_commands()
            bindings = builder.code_connect_bindings()
            self._code.extend(commands)
            self._code.extend(bindings)
        else:
            msg = 'Class "{0}" not mapped'.format(wmeta.classname)
            raise Exception(msg)
        
        return uniqueid

    def _process_callbacks(self):
        tabspaces = self._options['tabspaces']
        tab2 = tabspaces//2 if tabspaces == 8 else 1
        
        lines = []
        for name, value in self._callbacks.items():
            wid, cbtype, args = value
            if cbtype == CB_TYPES.BIND_EVENT:
                line = '{0}def {1}(self, event=None):'.format(' '*tab2, name)
                lines.append(line)
                line = '{0}pass\n'.format(' '*tabspaces)
                lines.append(line)
            elif cbtype == CB_TYPES.SCROLL:
                fargs = []
                for a in args:
                    fargs.append('{0}=None'.format(a))
                fargs = ', '.join(fargs)
                line = '{0}def {1}(self, {2}):'.format(' '*tab2, name, fargs)
                lines.append(line)
                line = '{0}pass\n'.format(' '*tabspaces)
                lines.append(line)
            else:
                # other types: cb_simple, cb_with_id, etc.
                if args is None:
                    line = '{0}def {1}(self):'.format(' '*tab2, name)
                    lines.append(line)
                    line = '{0}pass\n'.format(' '*tabspaces)
                    lines.append(line)
                else:
                    fargs = ', '.join(args)
                    line = '{0}def {1}(self, {2}):'.format(' '*tab2, name, fargs)
                    lines.append(line)
                    line = '{0}pass\n'.format(' '*tabspaces)
                    lines.append(line)
        return lines
    
    def code_create_callback(self, widgetid, cbname, cbtype, args=None):
        #print('on_code_create_callback', widgetid, cbname, cbtype, args)
        if cbname not in self._callbacks:
            self._callbacks[cbname] = (widgetid, cbtype, args)
        cb_name = 'self.{0}'.format(cbname)
        return cb_name
    
    def code_create_image(self, filename):
        basename = os.path.basename(filename)
        name, file_ext = os.path.splitext(basename)
        name = self._make_identifier(basename)
        varname = 'self.{0}'.format(name)
            
        if filename not in self._tkimages:
            img_class = 'tk.PhotoImage'
            if file_ext in TK_BITMAP_FORMATS:
                img_class = 'tk.BitmapImage'
            line = "{0} = {1}(file='{2}')".format(varname, img_class, filename)
            self._code.append(line)
            self._tkvariables[varname] = True
        return varname
    
    def code_create_iconbitmap(self, filename):
        TPL = '@{0}'
        if os.name == 'nt':
            TPL = '{0}'
        return TPL.format(filename)
    
    def _make_identifier(self, name):
        output = name.replace('.', '_')
        output = ''.join(x for x in output if x.isalnum() or x == '_')
        return output
