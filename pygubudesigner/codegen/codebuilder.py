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
import os
from collections import OrderedDict
from enum import Enum

from pygubu.builder import CB_TYPES, CLASS_MAP, Builder
from pygubu.builder.builderobject import BuilderObject, grouper, register_widget
from pygubu.builder.tkstdwidgets import TKToplevel
from pygubu.builder.widgetmeta import WidgetMeta
from pygubu.stockimage import TK_BITMAP_FORMATS

from pygubudesigner.stylehandler import StyleHandler


class ToplevelOrTk(TKToplevel):
    def code_realize(self, boparent, code_identifier=None):
        if code_identifier is not None:
            self._code_identifier = code_identifier
        lines = []
        master = boparent.code_child_master()
        init_args = self._get_init_args()
        bag = []
        for pname, value in init_args.items():
            s = f"{pname}='{value}'"
            bag.append(s)
        kwargs = ''
        if bag:
            kwargs = ', {}'.format(', '.join(bag))
        if init_args:
            # has init args defined so create a TkToplevel
            s = "{0} = {1}({2}{3})"
        else:
            s = "{0} = tk.Tk() if master is None else {1}({2}{3})"
        s = s.format(self.code_identifier(), self._code_class_name(), master, kwargs)
        lines.append(s)
        return lines


register_widget('pygubudesigner.ToplevelOrTk', ToplevelOrTk, 'ToplevelOrTk', tuple())


class ScriptType(Enum):
    APP_WITH_UI = 1
    APP_CODE = 2
    WIDGET = 3


class UI2Code(Builder):
    def __init__(self):
        super().__init__()

        self._script_type = None
        self.as_class = False
        self._extra_imports = {}
        self._code_imports = OrderedDict()
        self._tkvariables = {}
        self._tkimages = {}
        self._callbacks = {}
        self._import_tk = False
        self._import_ttk = False
        self._code = []
        # Used for preventing duplicate grid row/column configure lines from
        # ending up in the generated code.
        self._unique_grid_properties = []
        self.uidefinition = None
        self._builder = Builder()
        self._options = {}

    def add_import_line(self, module_name, as_name=None, priority=0):
        if module_name not in self._extra_imports:
            self._extra_imports[module_name] = (as_name, priority)

    def _process_options(self, kw):
        kwdef = {
            'as_class': True,
            'tabspaces': 8,
            'script_type': ScriptType.APP_WITH_UI,
        }
        kwdef.update(kw)
        self._options = kwdef
        self.as_class = self._options['as_class']
        self.tabspaces = self._options['tabspaces']
        self._script_type = self._options['script_type']

    def _process_results(self, target):
        code = []
        for line in self._code:
            line = '{}{}\n'.format(' ' * self.tabspaces, line)
            code.append(line)
        code = ''.join(code)

        code_imports = self._process_imports()
        code_imports = '\n'.join(code_imports)
        code_ttk_styles = self._process_ttk_styles()
        code_callbacks = self._process_callbacks()
        code_callbacks = '\n'.join(code_callbacks)
        code = ''.join(code)
        cc = {
            'imports': code_imports,
            target: code,
            'ttkstyles': code_ttk_styles,
            'callbacks': code_callbacks,
            'tkvariables': list(self._tkvariables.keys()),
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

        mastermeta = WidgetMeta('', 'master')
        builder = BuilderObject(self, mastermeta)
        self._toplevel_or_tk(target)
        wmeta = self.uidefinition.get_widget(target)

        if wmeta is not None:
            self._code_realize(builder, wmeta)
        return self._process_results(target)

    def generate_app_with_ui(self, uidef, target):
        return self.generate(
            uidef,
            target,
            as_class=False,
            tabspaces=8,
            script_type=ScriptType.APP_WITH_UI,
        )

    def generate_app_code(self, uidef, target):
        return self.generate(
            uidef, target, as_class=True, tabspaces=8, script_type=ScriptType.APP_CODE
        )

    def generate_app_widget(self, uidef, target):
        return self.generate_widget_class(uidef, target, script_type=ScriptType.WIDGET)

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

                for childmeta in self.uidefinition.widget_children(target):
                    childid = self._code_realize(builder, childmeta)
                    code = builder.code_child_add(childid)
                    self._code.extend(code)

                # configuration
                configure = builder.code_configure()
                self._code.extend(configure)

                # layout? TODO: Review if layout is required here.
                layout = builder.code_layout(parentid=masterid)
                self._code.extend(layout)

        return self._process_results(target)

    def code_classname_for(self, bobject):
        wmeta = bobject.wmeta
        cname = None
        if bobject.class_ is not None:
            if wmeta.classname == 'pygubudesigner.ToplevelOrTk':
                self._import_tk = True
                cname = 'tk.Toplevel'
            elif wmeta.classname.startswith('tk.'):
                self._import_tk = True
                cname = wmeta.classname
            elif wmeta.classname.startswith('ttk.'):
                self._import_ttk = True
                cname = wmeta.classname
            else:
                module = bobject.class_.__module__
                cname = bobject.class_.__name__
                if module not in self._code_imports:
                    self._code_imports[module] = {cname}
                else:
                    self._code_imports[module].add(cname)
        return cname

    def _process_ttk_styles(self):
        """
        Generate the ttk style code.
        """
        style_definition = StyleHandler.get_ttk_style_definitions()

        if not style_definition:
            return ''

        new_lines = []

        # Make sure the ttk style code starts with 8 spaces for proper indentication
        # with the generated class.
        code_lines = style_definition.split('\n')
        for line in code_lines:
            if not line.startswith(' ' * self.tabspaces):
                line = ' ' * self.tabspaces + line

            new_lines.append(line)

        new_code = '\n'.join(new_lines)

        return new_code

    def _process_imports(self):
        lines = []
        if self._script_type in (ScriptType.APP_CODE, ScriptType.WIDGET):
            if self._import_tk:
                self.add_import_line('tkinter', 'tk')
            if self._import_ttk:
                self.add_import_line('tkinter.ttk', 'ttk', priority=2)
        sorted_imports = sorted(
            self._extra_imports.items(), key=lambda x: (x[1][1], x[0])
        )
        for module_name, (as_name, _) in sorted_imports:
            line = f'import {module_name}'
            if as_name is not None:
                line = line + f' as {as_name}'
            lines.append(line)
        # Do not include code imports if using UI file.
        if self._script_type != ScriptType.APP_WITH_UI:
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
                        clist = '({})'.format(', '.join(bag))
                    else:
                        clist = ''.join(bag)
                    line = f'from {mname} import {clist}'
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
                    value = f"'{value}'"
            if vtype is None:
                var_init = 'tk.{}Var(value={})'.format(
                    type_from_name.capitalize(), value
                )
            else:
                var_init = f'{str(vtype)}(value={value})'
            if self.as_class:
                vname_in_code = f'self.{vname}'
            line = f'{vname_in_code} = {var_init}'
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
            for childmeta in self.uidefinition.widget_children(originalid):
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
            msg = f'Class "{wmeta.classname}" not mapped'
            raise Exception(msg)

        return uniqueid

    def _process_callbacks(self):
        tabspaces = self._options['tabspaces']
        tab2 = tabspaces // 2 if tabspaces == 8 else 1

        lines = []
        for name, value in self._callbacks.items():
            wid, cbtype, args = value
            if cbtype == CB_TYPES.BIND_EVENT:
                line = '{}def {}(self, event=None):'.format(' ' * tab2, name)
                lines.append(line)
                line = '{}pass\n'.format(' ' * tabspaces)
                lines.append(line)
            elif cbtype == CB_TYPES.SCROLL:
                fargs = []
                for a in args:
                    fargs.append(f'{a}=None')
                fargs = ', '.join(fargs)
                line = '{}def {}(self, {}):'.format(' ' * tab2, name, fargs)
                lines.append(line)
                line = '{}pass\n'.format(' ' * tabspaces)
                lines.append(line)
            else:
                # other types: cb_simple, cb_with_id, etc.
                if args is None:
                    line = '{}def {}(self):'.format(' ' * tab2, name)
                    lines.append(line)
                    line = '{}pass\n'.format(' ' * tabspaces)
                    lines.append(line)
                else:
                    fargs = ', '.join(args)
                    line = '{}def {}(self, {}):'.format(' ' * tab2, name, fargs)
                    lines.append(line)
                    line = '{}pass\n'.format(' ' * tabspaces)
                    lines.append(line)
        return lines

    def code_create_callback(self, widgetid, cbname, cbtype, args=None):
        # print('on_code_create_callback', widgetid, cbname, cbtype, args)
        if cbname not in self._callbacks:
            self._callbacks[cbname] = (widgetid, cbtype, args)
        cb_name = f'self.{cbname}'
        return cb_name

    def code_create_image(self, filename):
        if filename not in self._tkimages:
            basename = os.path.basename(filename)
            name, file_ext = os.path.splitext(basename)
            name = self._make_identifier(name)
            varname = f'self.img_{name}'

            img_class = 'tk.PhotoImage'
            if file_ext in TK_BITMAP_FORMATS:
                img_class = 'tk.BitmapImage'
            line = f"{varname} = {img_class}(file='{filename}')"
            self._code.append(line)
            self._tkimages[filename] = varname
        return self._tkimages[filename]

    def code_create_iconbitmap(self, filename):
        TPL = '@{0}'
        if os.name == 'nt':
            TPL = '{0}'
        return TPL.format(filename)

    def _make_identifier(self, name):
        output = name.replace('.', '_')
        output = ''.join(x for x in output if x.isalnum() or x == '_')
        return output
