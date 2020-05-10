from __future__ import unicode_literals, print_function
from collections import OrderedDict
from pygubu.builder import Builder, CLASS_MAP
from pygubu.builder.builderobject import BuilderObject, grouper
from pygubu.builder.widgetmeta import WidgetMeta


class UI2Code(Builder):
    def __init__(self):
        super(UI2Code, self).__init__()
        
        self.buffer = None
        self.as_class = False
        self._code_imports = OrderedDict()
        self._import_ttk = True;
        self._code = []
        self.uidefinition = None
        self._builder = Builder()
        self._options = {}
    
    def generate(self, uidef, target, **kw):
        kwdef = {
            'as_class': True,
            'tabspaces': 8
            }
        kwdef.update(kw)
        self._options = kwdef
        self.as_class = self._options['as_class']
        self.uidefinition = uidef
        tabspaces = self._options['tabspaces']
        
        mastermeta = WidgetMeta('','master')
        builder = BuilderObject(self, mastermeta)
        wmeta = self.uidefinition.get_widget(target)
        code = []
        if wmeta is not None:
            self._code_realize(builder, wmeta)
            
            for line in self._code:
                line = '{0}{1}\n'.format(' ' * tabspaces, line)
                code.append(line)
        code = ''.join(code)
        
        code_imports = self._process_imports()
        code_imports = '\n'.join(code_imports)
        cc = {
            'imports': code_imports,
            target: code
            }
        return cc
    
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
            print(uniqueid, configure)
            self._code.extend(configure)
            
            # layout
            layout = builder.code_layout()
            self._code.extend(layout)
        else:
            msg = 'Class "{0}" not mapped'.format(wmeta.classname)
            raise Exception(msg)
        
        return uniqueid

