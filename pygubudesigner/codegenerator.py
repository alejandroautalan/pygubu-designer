from __future__ import unicode_literals, print_function
import itertools
from collections import defaultdict
from pygubu.builder import Builder, CLASS_MAP
from pygubu.builder.builderobject import BuilderObject, CodeGeneratorBase


if getattr(itertools, 'zip_longest', None) is None:
    def zip_longest(*args, **kw):
        # zip_longest('ABCD', 'xy', fillvalue='-') --> Ax By C- D-
        fillvalue = kw.get('fillvalue', None)
        iterators = [iter(it) for it in args]
        num_active = len(iterators)
        if not num_active:
            return
        while True:
            values = []
            for i, it in enumerate(iterators):
                try:
                    value = next(it)
                except StopIteration:
                    num_active -= 1
                    if not num_active:
                        return
                    iterators[i] = itertools.repeat(fillvalue)
                    value = fillvalue
                values.append(value)
            yield tuple(values)
    itertools.zip_longest = zip_longest


def grouper(iterable, n, fillvalue=None):
    "Collect data into fixed-length chunks or blocks"
    # grouper('ABCDEFG', 3, 'x') --> ABC DEF Gxx"
    args = [iter(iterable)] * n
    return itertools.zip_longest(*args, fillvalue=fillvalue)


class UI2Code(object):
    def __init__(self):
        self.buffer = None
        self.as_class = False
        self._imports = []
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
        
        builder = BuilderObject(None, {})
        wmeta = self.uidefinition.get_widget(target)
        code = []
        if wmeta is not None:
            self._realize(builder, '', wmeta)
            
            for line in self._code:
                line = '{0}{1}\n'.format(' ' * tabspaces, line)
                code.append(line)
        code = ''.join(code)
        return code
    
    def code_create(self, builder, parentid, codegen):
        wmeta = builder.wmeta
        comment = '# {0} widget'.format(wmeta.identifier)
        lines = []

        if codegen is not None:
            output = codegen.create()
            if output is None:
                return tuple()
            elif output != 'AUTO':
                #lines.append(comment)
                lines.extend(output)
                return lines
        
        # ro properties
        kwargs = []
        for pname, value in wmeta.properties.items():
            if pname in builder.ro_properties:
                arg_stmt = "{0}='{1}'".format(pname, value)
                kwargs.append(arg_stmt)
        if kwargs:
            kwargs = ', ' + ', '.join(kwargs)
        else:
            kwargs = ''
        
        lines.append(comment)
        line = "{0} = {1}({2}{3})".format(wmeta.identifier,
                                       wmeta.classname, parentid, kwargs)
        lines.append(line)
        return lines
    
    def code_configure(self, builder, codegen):
        wmeta = builder.wmeta
        comment = '# {0} configuration'.format(wmeta.identifier)
        lines = []
        
        if codegen is not None:
            output = codegen.configure()
            if output is None:
                return tuple()
            elif output != 'AUTO':
                #lines.append(comment)
                lines.extend(output)
                return lines
        
        lines.append(comment)
        # properties
        prop_stmt = "{0}.config({1})"
        arg_stmt = "{0}='{1}'"
        properties = wmeta.properties
        sorted_keys = sorted(properties.keys())
        for g in grouper(sorted_keys, 4):
            args_bag = []
            for p in g:
                if p is not None and p not in builder.ro_properties:
                    args_bag.append(arg_stmt.format(p, properties[p]))
            args = ', '.join(args_bag)
            line = prop_stmt.format(wmeta.identifier, args)
            lines.append(line)
        return lines
    
    def code_layout(self, builder, codegen):
        wmeta = builder.wmeta
        comment = '# {0} layout'.format(wmeta.identifier)
        lines = []

        if codegen is not None:
            output = codegen.layout()
            if output is None:
                return tuple()
            elif output != 'AUTO':
                #lines.append(comment)
                lines.extend(output)
                return lines
        
        lines.append(comment)
        layout_stmt = "{0}.{1}({2})"
        arg_stmt = "{0}='{1}'"
        layout = wmeta.layout_properties
        if layout:
            args_bag = []
            for p, v in sorted(layout.items()):
                if p not in ('propagate', ):
                    args_bag.append(arg_stmt.format(p, v))
            args = ', '.join(args_bag)
            
            manager = wmeta.manager
            line = layout_stmt.format(wmeta.identifier, manager, args)
            lines.append(line)
            
            pvalue = str(layout.get('propagate', '')).lower()
            if 'propagate' in layout and  pvalue == 'false':
                line = '{0}.propagate({1})'.format(wmeta.identifier, pvalue)
                lines.append(line)
        
        lrow_stmt = "{0}.rowconfigure({1}, {2})"
        lcol_stmt = "{0}.columnconfigure({1}, {2})"
        rowbag = defaultdict(list)
        colbag = defaultdict(list)
        for type_, num, pname, value in wmeta.gridrc_properties:
            if type_ == 'row':
                arg = lrow_stmt.format(pname, value)
                rowbag[num].append(arg)
            else:
                arg = lcol_stmt.format(pname, value)
                colbag[num].append(arg)
        for k, bag in rowbag:
            args = ', '.join(bag)
            line = lrow_stmt.format(wmeta.identifier, k, args)
            self._code.append(line)
        for k, bag in colbag:
            args = ', '.join(bag)
            line = lcol_stmt.format(wmeta.identifier, k, args)
            self._code.append(line)
        return lines
    
    def code_add_child(self, builder, codegen, childid, childmeta):
        wmeta = builder.wmeta
        comment = '# {0} children config'.format(wmeta.identifier)
        lines = []        
        if codegen is not None:
            output = codegen.add_child(childid, childmeta)
            if output is not None:
                #lines.append(comment)
                lines.extend(output)
        return lines
    
    def _realize(self, bmaster, masterid, wmeta):
        originalid = wmeta.identifier
        uniqueid = None
        
        if wmeta.classname not in CLASS_MAP:
            self._builder._import_class(wmeta.classname)

        if wmeta.classname in CLASS_MAP:
            bclass = CLASS_MAP[wmeta.classname].builder
            builder = bclass.factory(None, wmeta)
            uniqueid = wmeta.identifier
            
            if self.as_class:
                if not masterid:
                    uniqueid = 'self'
                else:
                    uniqueid = 'self.' + uniqueid
            
            codegen = builder.code_generator(masterid)
            builder.wmeta.identifier = uniqueid
            # Creation
            code = self.code_create(builder, masterid, codegen)
            self._code.extend(code)
            
            # configuration
            code = self.code_configure(builder, codegen)
            self._code.extend(code)
            
            # Children
            for childmeta in \
                self.uidefinition.widget_children(originalid):
                cmaster = uniqueid
                if codegen is not None:
                    cmaster = codegen.child_master()
                childid = self._realize(builder, cmaster, childmeta)                                
                code = self.code_add_child(builder, codegen, childid, childmeta)
                self._code.extend(code)
            
            # layout
            code = self.code_layout(builder, codegen)
            self._code.extend(code)
        else:
            msg = 'Class "{0}" not mapped'.format(wmeta.classname)
            raise Exception(msg)
        
        return uniqueid

