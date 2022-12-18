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

from pygubu import Builder
from pygubu.api.v1 import BuilderObject, register_widget
from pygubu.component.builderobject import CB_TYPES, CLASS_MAP
from pygubu.component.widgetmeta import WidgetMeta
from pygubu.plugins.tk.tkstdwidgets import TKToplevel
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
            s = f'{pname}="{value}"'
            bag.append(s)
        kwargs = ""
        if bag:
            kwargs = ", {}".format(", ".join(bag))
        if init_args:
            # has init args defined so create a TkToplevel
            s = "{0} = {1}({2}{3})"
        else:
            s = "{0} = tk.Tk() if master is None else {1}({2}{3})"
        s = s.format(
            self.code_identifier(), self._code_class_name(), master, kwargs
        )
        lines.append(s)
        return lines


register_widget(
    "pygubudesigner.ToplevelOrTk", ToplevelOrTk, "ToplevelOrTk", tuple()
)


class ScriptType(Enum):
    APP_WITH_UI = 1
    APP_CODE = 2
    WIDGET = 3
    APP_UI_METHOD = 4
    APP_CODE_METHOD = 5


class RealizeMode(Enum):
    APP = 1
    METHOD = 2


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
        self._with_i18n_support = False
        self._methods = OrderedDict()
        self._methods_target_code_ids = {}
        self._realize_mode = RealizeMode.APP
        self._current_method = None
        self._current_target = None
        self._generated_target_id = None
        self.all_ids_as_attributes = False

    def add_import_line(self, module_name, as_name=None, priority=0):
        if module_name not in self._extra_imports:
            self._extra_imports[module_name] = (as_name, priority)

    def _process_options(self, kw):
        kwdef = {
            "as_class": True,
            "tabspaces": 8,
            "script_type": ScriptType.APP_WITH_UI,
        }
        kwdef.update(kw)
        self._options = kwdef
        self.as_class = self._options["as_class"]
        self.tabspaces = self._options["tabspaces"]
        self._script_type = self._options["script_type"]

    def _process_results(self, target):
        code = []
        for line in self._code:
            line = "{}{}\n".format(" " * self.tabspaces, line)
            code.append(line)
        code = "".join(code)

        code_imports = self._process_imports()
        code_imports = "\n".join(code_imports)
        code_ttk_styles = self._process_ttk_styles()
        code_callbacks = self._process_callbacks()
        code_callbacks = "\n".join(code_callbacks)
        code_methods = "\n".join(self._process_methods())
        code = "".join(code)
        cc = {
            "imports": code_imports,
            target: code,
            "target_code_id": self._generated_target_id,
            "ttkstyles": code_ttk_styles,
            "callbacks": code_callbacks,
            "tkvariables": list(self._tkvariables.keys()),
            "methods": code_methods,
        }
        return cc

    def _toplevel_or_tk(self, target):
        wmeta = self.uidefinition.get_widget(target)
        if wmeta.classname == "tk.Toplevel":
            wmeta.classname = "pygubudesigner.ToplevelOrTk"
            self.uidefinition.replace_widget(target, wmeta)

    def generate(self, uidef, target, **kw):
        self.uidefinition = uidef
        self._process_options(kw)

        mastermeta = WidgetMeta("", "master")
        builder = BuilderObject(self, mastermeta)
        self._toplevel_or_tk(target)
        wmeta = self.uidefinition.get_widget(target)

        if self._realize_mode == RealizeMode.APP:
            self._current_target = target

        if wmeta is not None:
            self._code_realize(builder, wmeta)

    def generate_app_with_ui(self, uidef, target):
        self.generate(
            uidef,
            target,
            as_class=False,
            tabspaces=8,
            script_type=ScriptType.APP_WITH_UI,
        )
        return self._process_results(target)

    def generate_app_code(self, uidef, target, methods_for: list = None):
        self.generate(
            uidef,
            target,
            as_class=True,
            tabspaces=8,
            script_type=ScriptType.APP_CODE,
        )
        if methods_for is not None:
            self._realize_mode = RealizeMode.METHOD
            for target_id in methods_for:
                self._current_method = target_id
                self._methods[target_id] = []
                self._methods_target_code_ids = {}
                self.generate(
                    uidef,
                    target_id,
                    as_class=True,
                    tabspaces=8,
                    script_type=ScriptType.APP_CODE,
                )
            self._realize_mode = RealizeMode.APP

        return self._process_results(target)

    def generate_app_widget(self, uidef, target):
        self.generate_widget_class(uidef, target, script_type=ScriptType.WIDGET)
        return self._process_results(target)

    def generate_widget_class(self, uidef, target, **kw):
        self.uidefinition = uidef
        self._process_options(kw)

        mastermeta = wmeta = self.uidefinition.get_widget(target)
        builder = bmaster = BuilderObject(self, mastermeta)
        if wmeta is not None:
            originalid = wmeta.identifier  # noqa: F841
            wmeta.identifier = "self"

            if wmeta.classname not in CLASS_MAP:
                self._builder._import_class(wmeta.classname)

            if wmeta.classname in CLASS_MAP:
                bclass = CLASS_MAP[wmeta.classname].builder
                builder = bclass.factory(self, wmeta)
                uniqueid = builder.code_identifier()  # noqa: F841
                masterid = bmaster.code_child_master()

                for childmeta in self.uidefinition.widget_children(target):
                    childid = self._code_realize(builder, childmeta)
                    code = builder.code_child_add(childid)
                    self._add_new_code(code)

                # configuration
                configure = builder.code_configure()
                self._add_new_code(configure)

                # layout? TODO: Review if layout is required here.
                layout = builder.code_layout(parentid=masterid)
                self._add_new_code(layout)

    def code_classname_for(self, bobject):
        wmeta = bobject.wmeta
        cname = None
        if bobject.class_ is not None:
            if wmeta.classname == "pygubudesigner.ToplevelOrTk":
                self._import_tk = True
                cname = "tk.Toplevel"
            elif wmeta.classname.startswith("tk."):
                self._import_tk = True
                cname = wmeta.classname
            elif wmeta.classname.startswith("ttk."):
                self._import_ttk = True
                cname = wmeta.classname
            else:
                imports_ = bobject.code_imports()
                if imports_ is None:
                    module = bobject.class_.__module__
                    cname = bobject.class_.__name__
                    if module not in self._code_imports:
                        self._code_imports[module] = {cname}
                    else:
                        self._code_imports[module].add(cname)
                else:
                    # FIXME: review this process.
                    cname = bobject.class_.__name__
                    for module, obj in imports_:
                        if module not in self._code_imports:
                            self._code_imports[module] = {obj}
                        else:
                            self._code_imports[module].add(obj)
        return cname

    def _process_ttk_styles(self):
        """
        Generate the ttk style code.
        """
        style_definition = StyleHandler.get_ttk_style_definitions()

        if not style_definition:
            return ""

        new_lines = []

        # Make sure the ttk style code starts with 8 spaces for proper indentication
        # with the generated class.
        code_lines = style_definition.split("\n")
        for line in code_lines:
            if not line.startswith(" " * self.tabspaces):
                line = " " * self.tabspaces + line

            new_lines.append(line)

        new_code = "\n".join(new_lines)

        return new_code

    def _process_imports(self):
        lines = []
        if self._script_type in (ScriptType.APP_CODE, ScriptType.WIDGET):
            if self._import_tk:
                self.add_import_line("tkinter", "tk")
            if self._import_ttk:
                self.add_import_line("tkinter.ttk", "ttk", priority=2)
        sorted_imports = sorted(
            self._extra_imports.items(), key=lambda x: (x[1][1], x[0])
        )
        for module_name, (as_name, _) in sorted_imports:
            line = f"import {module_name}"
            if as_name is not None:
                line = line + f" as {as_name}"
            lines.append(line)
        # Do not include code imports if using UI file.
        if self._script_type != ScriptType.APP_WITH_UI:
            skeys = sorted(self._code_imports.keys())
            for mname in skeys:
                bag = []
                for cname in sorted(self._code_imports[mname]):
                    if cname is not None:
                        bag.append(cname)
                clist = None
                if len(bag) > 1:
                    clist = "({})".format(", ".join(bag))
                else:
                    clist = "".join(bag)
                line = f"from {mname} import {clist}"
                lines.append(line)
        return lines

    def code_create_variable(self, name_or_desc, value, vtype=None):
        vname, type_from_name = self._process_variable_description(name_or_desc)
        vname_in_code = vname
        if vname not in self._tkvariables:
            var_create = ""
            var_value = ""

            if value:
                if type_from_name == "string":
                    value = f"{self.code_translate_str(value)}"
                var_value = f"value={value}"

            if vtype is None:
                var_create = f"tk.{type_from_name.capitalize()}Var({var_value})"
            else:
                var_create = f"{str(vtype)}({var_value})"

            if self.as_class:
                vname_in_code = f"self.{vname}"
            line = f"{vname_in_code} = {var_create}"
            self._add_new_code([line])
            self._tkvariables[vname] = vname_in_code
            self._import_tk = True
        return self._tkvariables[vname]

    def _add_new_code(self, newcode: list):
        if self._realize_mode == RealizeMode.APP:
            self._code.extend(newcode)
        else:
            self._methods[self._current_method].extend(newcode)

    def _get_unique_id(self, wmeta, uniqueid, masterid):
        if self.as_class:
            if wmeta.is_named or self.all_ids_as_attributes:
                uniqueid = "self." + uniqueid if masterid else "self"
        return uniqueid

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

            uniqueid = self._get_unique_id(wmeta, uniqueid, masterid)

            if (
                self._realize_mode == RealizeMode.APP
                and originalid == self._current_target
            ):
                self._generated_target_id = uniqueid

            if (
                self._realize_mode == RealizeMode.METHOD
                and originalid == self._current_method
            ):
                self._methods_target_code_ids[self._current_method] = uniqueid

            create = builder.code_realize(bmaster, uniqueid)
            self._add_new_code(create)

            # configuration
            configure = builder.code_configure()
            self._add_new_code(configure)

            # Children
            for childmeta in self.uidefinition.widget_children(originalid):
                childid = self._code_realize(builder, childmeta)
                code = builder.code_child_add(childid)
                self._add_new_code(code)

            # Configuration after adding all children
            children_config = builder.code_configure_children()
            self._add_new_code(children_config)

            # layout
            layout = builder.code_layout(parentid=masterid)
            self._add_new_code(layout)

            # callbacks
            commands = builder.code_connect_commands()
            bindings = builder.code_connect_bindings()
            self._add_new_code(commands)
            self._add_new_code(bindings)
        else:
            msg = f'Class "{wmeta.classname}" not mapped'
            raise Exception(msg)

        return uniqueid

    def _process_methods(self):
        tabspaces = self._options["tabspaces"]
        tab2 = tabspaces // 2 if tabspaces == 8 else 1

        code = []
        bsp = " "
        for target_id, mlines in self._methods.items():
            line = f"{bsp*tab2}def create_{target_id}(self, master):"
            code.append(line)
            for line in mlines:
                line = f"{bsp*tabspaces}{line}"
                code.append(line)
            line = f"{bsp*tabspaces}return {self._methods_target_code_ids[target_id]}"
            code.append(line)
        return code

    def _process_callbacks(self):
        tabspaces = self._options["tabspaces"]
        tab2 = tabspaces // 2 if tabspaces == 8 else 1

        lines = []
        for name, value in self._callbacks.items():
            wid, cbtype, args = value
            if cbtype == CB_TYPES.BIND_EVENT:
                line = "{}def {}(self, event=None):".format(" " * tab2, name)
                lines.append(line)
                line = "{}pass\n".format(" " * tabspaces)
                lines.append(line)
            elif cbtype == CB_TYPES.SCROLL:
                fargs = []
                for a in args:
                    fargs.append(f"{a}=None")
                fargs = ", ".join(fargs)
                line = "{}def {}(self, {}):".format(" " * tab2, name, fargs)
                lines.append(line)
                line = "{}pass\n".format(" " * tabspaces)
                lines.append(line)
            else:
                # other types: cb_simple, cb_with_id, etc.
                if args is None:
                    line = "{}def {}(self):".format(" " * tab2, name)
                    lines.append(line)
                    line = "{}pass\n".format(" " * tabspaces)
                    lines.append(line)
                else:
                    fargs = ", ".join(args)
                    line = "{}def {}(self, {}):".format(" " * tab2, name, fargs)
                    lines.append(line)
                    line = "{}pass\n".format(" " * tabspaces)
                    lines.append(line)
        return lines

    def code_create_callback(self, widgetid, cbname, cbtype, args=None):
        # print('on_code_create_callback', widgetid, cbname, cbtype, args)
        if cbname not in self._callbacks:
            self._callbacks[cbname] = (widgetid, cbtype, args)
        cb_name = f"self.{cbname}"
        return cb_name

    def code_create_image(self, filename):
        if filename not in self._tkimages:
            basename = os.path.basename(filename)
            name, file_ext = os.path.splitext(basename)
            name = self._make_identifier(name)
            varname = f"self.img_{name}"

            img_class = "tk.PhotoImage"
            if file_ext in TK_BITMAP_FORMATS:
                img_class = "tk.BitmapImage"
            line = f'{varname} = {img_class}(file="{filename}")'
            self._add_new_code([line])
            self._tkimages[filename] = varname
            self._import_tk = True
        return self._tkimages[filename]

    def code_create_iconbitmap(self, filename):
        TPL = "@{0}"
        if os.name == "nt":
            TPL = "{0}"
        return TPL.format(filename)

    def _make_identifier(self, name):
        output = name.replace(".", "_")
        output = "".join(x for x in output if x.isalnum() or x == "_")
        return output

    def code_translate_str(self, value: str) -> str:
        escaped = BuilderObject.code_escape_str(value)
        if self.with_i18n_support:
            trval = f"_({escaped})"
            return trval
        else:
            return escaped

    @property
    def with_i18n_support(self) -> bool:
        return self._with_i18n_support

    @with_i18n_support.setter
    def with_i18n_support(self, value: bool):
        self._with_i18n_support = value
