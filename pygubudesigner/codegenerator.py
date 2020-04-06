from __future__ import unicode_literals, print_function
import itertools
import xml.etree.ElementTree as ET
try:
    from StringIO import StringIO ## for Python 2
except ImportError:
    from io import StringIO ## for Python 3

from pygubu.builder import data_xmlnode_to_dict


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
    
    def generate(self, uixml, target, as_class=True, tabspaces=8):
        self.as_class = as_class
        tree = uixml
        tree.getroot()
        xpath = ".//object[@id='{0}']".format(target)
        node = tree.find(xpath)
        code = []
        self.buffer = StringIO()
        if node is not None:
            self._realize('', node)
            self.buffer.seek(0)
            for line in self.buffer.readlines():
                line = ' ' * tabspaces + line
                code.append(line)
            self.buffer.close()
        code = ''.join(code)
        return code
    
    def _realize(self, master, node):
        data = data_xmlnode_to_dict(node)
        cname = data['class']
        uniqueid = data['id']
        
        if self.as_class:
            if not master:
                uniqueid = 'self'
            else:
                uniqueid = 'self.' + uniqueid
                stmt = "{0} = {1}({2})".format(uniqueid, cname, master)
                print(stmt, file=self.buffer)                
        else:
            stmt = '# {0} widget'.format(uniqueid)
            print(stmt, file=self.buffer)
            stmt = "{0} = {1}({2})".format(uniqueid, cname, master)
            print(stmt, file=self.buffer)
        
        # properties
        prop_stmt = "{0}.configure({1})"
        arg_stmt = "{0}='{1}'"
        properties = data['properties']
        sorted_keys = sorted(properties.keys())
        for g in grouper(sorted_keys, 4):
            args_bag = []
            for p in g:
                if p is not None:
                    args_bag.append(arg_stmt.format(p, properties[p]))
            args = ', '.join(args_bag)
            print(prop_stmt.format(uniqueid, args), file=self.buffer)
        
        xpath = "./child"
        children = node.findall(xpath)
        for child in children:
            child_xml = child.find('./object')
            print('', file=self.buffer)
            self._realize(uniqueid, child_xml)
        
        #layout:
        layout_stmt = "{0}.grid({1})"
        lrow_stmt = "{0}.rowconfigure({1}, {2})"
        lcol_stmt = "{0}.columnconfigure({1}, {2})"
        arg_stmt = "{0}='{1}'"
        layout = data['layout']
        if layout:
            args_bag = []
            for p, v in sorted(layout.items()):
                if p not in ('columns', 'rows', 'propagate'):
                    args_bag.append(arg_stmt.format(p, v))
            args = ', '.join(args_bag)
            print(layout_stmt.format(uniqueid, args), file=self.buffer)
            if 'propagate' in layout and layout['propagate'] == 'False': 
                stmt = '{0}.propagate({1})'.format(uniqueid, layout['propagate'])
                print(stmt, file=self.buffer)
            # rows
            for idx, pd in layout['rows'].items():
                args_bag = []
                for p, v in sorted(pd.items()):
                    args_bag.append(arg_stmt.format(p, v))
                if args_bag:
                    args = ', '.join(args_bag)
                    stmt = lrow_stmt.format(uniqueid, idx, args)
                    print(stmt, file=self.buffer)
            # cols
            for idx, pd in sorted(layout['columns'].items()):
                args_bag = []
                for p, v in sorted(pd.items()):
                    args_bag.append(arg_stmt.format(p, v))
                if args_bag:
                    args = ', '.join(args_bag)
                    stmt = lcol_stmt.format(uniqueid, idx, args)
                    print(stmt, file=self.buffer)
