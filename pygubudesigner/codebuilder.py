from __future__ import unicode_literals, print_function
import os
from collections import OrderedDict
from pygubu.builder import Builder, CLASS_MAP
from pygubu.builder.builderobject import BuilderObject, grouper
from pygubu.builder.widgetmeta import WidgetMeta
from pygubu.stockimage import TK_BITMAP_FORMATS


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
            }
        return cc
        
    def generate(self, uidef, target, **kw):
        self.uidefinition = uidef
        self._process_options(kw)
        
        mastermeta = WidgetMeta('','master')
        builder = BuilderObject(self, mastermeta)
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
            if wmeta.classname.startswith('tk.'):
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
        
        if vname not in self._tkvariables:
            var_init = ''
            if value is None:
                value = ''
            else:
                if type_from_name == 'string':
                    value = "''".format(value)
            
            if vtype is None:
                var_init = 'tk.{0}Var({1})'.format(type_from_name.capitalize(),
                                                value)
            else:
                var_init = '{0}({1})'.format(str(vtype), value)
            line = '{0} = {1}'.format(vname, var_init)
            self._code.append(line)
            self._tkvariables[vname] = vtype
        return vname
    
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
            layout = builder.code_layout()
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
        for name, cbtype in self._callbacks.items():
            if cbtype == 'command':
                line = '{0}def {1}(self):'.format(' '*tab2, name)
            else:
                line = '{0}def {1}(self, event=None):'.format(' '*tab2, name)
            lines.append(line)
            line = '{0}pass\n'.format(' '*tabspaces)
            lines.append(line)
        return lines
    
    def code_create_callback(self, name, cbtype):
        if name not in self._callbacks:
            self._callbacks[name] = cbtype
        cb_name = 'self.{0}'.format(name)
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
