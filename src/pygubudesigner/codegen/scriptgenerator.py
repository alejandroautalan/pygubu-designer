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
import codecs
import tkinter as tk
from tkinter import filedialog, messagebox

import autopep8
from mako.lookup import TemplateLookup

from .codebuilder import UI2Code
from pygubudesigner.services.stylehandler import StyleHandler
from pygubudesigner.services.project import Project


logger = logging.getLogger(__name__)
DATA_DIR = pathlib.Path(__file__).parent.parent / "data"
TEMPLATE_DIR = DATA_DIR / "code_templates"
makolookup = TemplateLookup(directories=[TEMPLATE_DIR])


class ScriptGenerator:
    def __init__(self, app):
        self.app = app
        self.builder = app.builder
        self.tree = app.tree_editor
        self.projectname = ""

        _ = self.app.translator
        self.msgtitle = _("Script Generator")

    def _appui_code(self, generator, context):
        uidef = self.tree.tree_to_uidef()

        generator.add_import_line("pathlib")
        # if not main_widget_is_toplevel:
        generator.add_import_line("tkinter", "tk", priority=1)
        generator.add_import_line("pygubu", priority=10)
        target = context["target"]
        main_menu_id = None
        if context["set_main_menu"]:
            main_menu_id = context["main_menu_id"]
        code = generator.generate_app_with_ui(
            uidef, target, main_menu=main_menu_id
        )

        context["import_lines"] = code["imports"]
        # Set project paths
        context["set_project_path"] = True

        # Callbacks
        context["callbacks"] = code["callbacks"]
        # Tk Variables
        if context["import_tk_vars"]:
            context["tkvariables"] = code["tkvariables"]
            context["tkvariablehints"] = code["tkvariablehints"]

        bcontext = context.copy()
        bcontext["class_name"] = context["class_name"] + "UI"
        tpl = makolookup.get_template("app.py.mako")
        final_code = tpl.render(**bcontext)
        final_code = self._format_code(final_code)

        output_dir = context["output_dir"]
        outfn = output_dir / (context["module_name"] + "ui.py")
        with codecs.open(outfn, "w", encoding="utf-8") as outfile:
            outfile.write(final_code)
            logger.info("Generated code file: %s", outfn)

        context["import_lines"] += (
            "\nfrom "
            + context["module_name"]
            + "ui import "
            + bcontext["class_name"]
        )
        tpl = makolookup.get_template("appuser.py.mako")
        final_code = tpl.render(**context)
        final_code = self._format_code(final_code)
        outfn: pathlib.Path = output_dir / (context["module_name"] + ".py")
        # DO NOT overwrite user module.
        if not outfn.exists():
            with codecs.open(outfn, "w", encoding="utf-8") as outfile:
                outfile.write(final_code)
                logger.info("Generated code file: %s", outfn)

    def _script_code(self, generator, context):
        uidef = self.tree.tree_to_uidef()
        target = context["target"]

        if not context["main_widget_is_toplevel"]:
            generator.add_import_line("tkinter", "tk")

        first_object_callback = None
        if context["has_ttk_styles"]:
            ttk_styles_module = context["ttk_styles_module"]
            first_object_callback = f"{ttk_styles_module}.setup_ttk_styles"

        methods = []
        if context["set_main_menu"]:
            methods.append(context["main_menu_id"])
        # Generate code
        code = generator.generate_app_code(
            uidef,
            target,
            methods_for=methods,
            on_first_object_cb=first_object_callback,
        )

        # Prepare template context
        context["widget_code"] = code[target]
        context["import_lines"] = code["imports"]
        context["callbacks"] = code["callbacks"]
        context["methods"] = code["methods"]
        context["target_code_id"] = code["target_code_id"]
        context["with_image_loader"] = code["with_image_loader"]

        bcontext = context.copy()
        bcontext["class_name"] = context["class_name"] + "UI"
        tpl = makolookup.get_template("script.py.mako")
        final_code = tpl.render(**bcontext)
        final_code = self._format_code(final_code)

        output_dir = context["output_dir"]
        outfn = output_dir / (context["module_name"] + "ui.py")
        with codecs.open(outfn, "w", encoding="utf-8") as outfile:
            outfile.write(final_code)

        tpl = makolookup.get_template("scriptuser.py.mako")
        final_code = tpl.render(**context)
        final_code = self._format_code(final_code)
        outfn: pathlib.Path = output_dir / (context["module_name"] + ".py")
        # DO NOT overwrite user module.
        if not outfn.exists():
            with codecs.open(outfn, "w", encoding="utf-8") as outfile:
                outfile.write(final_code)
                logger.info("Generated code file: %s", outfn)

    def _widget_code(self, generator, context):
        uidef = self.tree.tree_to_uidef()
        target = context["target"]

        # generator.with_i18n_support = False
        generator.add_import_line("tkinter", "tk")
        # Generate code
        code = generator.generate_app_widget(uidef, target)
        # Prepare template context
        context["widget_code"] = code[target]
        context["import_lines"] = code["imports"]
        context["callbacks"] = code["callbacks"]
        context["with_image_loader"] = code["with_image_loader"]

        bcontext = context.copy()
        bcontext["class_name"] = context["class_name"] + "UI"
        tpl = makolookup.get_template("widget.py.mako")
        final_code = tpl.render(**bcontext)
        final_code = self._format_code(final_code)

        output_dir = context["output_dir"]
        outfn = output_dir / (context["module_name"] + "ui.py")
        with codecs.open(outfn, "w", encoding="utf-8") as outfile:
            outfile.write(final_code)
            logger.info("Generated code file: %s", outfn)

        tpl = makolookup.get_template("widgetbo.py.mako")
        final_code = tpl.render(**context)
        final_code = self._format_code(final_code)
        output_dir2 = context["output_dir2"]
        outfn: pathlib.Path = output_dir2 / (context["module_name"] + "bo.py")
        # DO NOT overwrite user module.
        if not outfn.exists():
            with codecs.open(outfn, "w", encoding="utf-8") as outfile:
                outfile.write(final_code)
                logger.info("Generated code file: %s", outfn)

        tpl = makolookup.get_template("widgetuser.py.mako")
        final_code = tpl.render(**context)
        final_code = self._format_code(final_code)
        outfn: pathlib.Path = output_dir / (context["module_name"] + ".py")
        # DO NOT overwrite user module.
        if not outfn.exists():
            with codecs.open(outfn, "w", encoding="utf-8") as outfile:
                outfile.write(final_code)
                logger.info("Generated code file: %s", outfn)

    def generate_code(self):
        project = self.app.current_project
        config = project.get_full_settings()
        generator = UI2Code()
        template = config["template"]
        target = config["main_widget"]
        itemid = self.tree.get_tree_topitem_byid(target)
        target_class = self.tree.get_widget_class(itemid)

        toplevel_uids = (
            "tk.Tk",
            "tk.Toplevel",
            "customtkinter.CTk",
            "customtkinter.CTkToplevel",
            "tkmt.ThemedTKinterFrame",
        )

        main_widget_is_toplevel = False
        main_menu_id = ""
        set_main_menu = False
        has_ttk_styles = False

        if target_class in toplevel_uids:
            main_widget_is_toplevel = True
            # Main menu definition
            main_menu_id = config["main_menu"]
            if main_menu_id and template != "widget":
                set_main_menu = True

        # Style definitions
        use_ttk_styles = tk.getboolean(config["use_ttk_styledefinition_file"])
        ttk_styles_module = config["ttk_style_definition_file"]
        if ttk_styles_module:
            mpath = pathlib.Path(ttk_styles_module)
            ttk_styles_module = mpath.stem

        use_first_object_cb = use_ttk_styles
        first_object_func = "None"

        has_ttk_styles = False
        if use_ttk_styles and ttk_styles_module:
            has_ttk_styles = True
            first_object_func = f"{ttk_styles_module}.setup_ttk_styles"

        with_i18n_support = tk.getboolean(config["use_i18n"])
        import_tk_vars = tk.getboolean(config["import_tkvariables"])
        add_window_centering_code = tk.getboolean(
            config["use_window_centering_code"]
        )

        # calculate output dir
        uipath = self.app.current_project.fpath.parent
        output_dir: pathlib.Path = config["output_dir"]
        if output_dir:
            output_dir = uipath / output_dir
        else:
            output_dir = uipath
        output_dir2: pathlib.Path = config["output_dir2"]
        if output_dir2:
            output_dir2 = uipath / output_dir2
        else:
            output_dir2 = uipath

        context = {
            "output_dir": output_dir,
            "output_dir2": output_dir2,
            "target": target,
            "module_name": config["module_name"],
            "project_name": self.app.project_name(),
            "class_name": config["main_classname"],
            "main_widget_is_toplevel": main_widget_is_toplevel,
            "main_widget": target,
            "widget_base_class": target_class,
            "widget_code": None,
            "import_lines": None,
            "callbacks": "",
            "tkvariables": [],
            "use_first_object_cb": use_first_object_cb,
            "first_object_func": first_object_func,
            "has_ttk_styles": has_ttk_styles,
            "ttk_styles_module": ttk_styles_module,
            "set_project_path": False,
            "with_i18n_support": with_i18n_support,
            "set_main_menu": set_main_menu,
            "main_menu_id": main_menu_id,
            "add_window_centering_code": add_window_centering_code,
            "import_tk_vars": import_tk_vars,
        }

        generator.with_i18n_support = with_i18n_support
        generator.all_ids_as_attributes = tk.getboolean(
            config["all_ids_attributes"]
        )

        if template == "application":
            self._appui_code(generator, context)
        elif template == "widget":
            self._widget_code(generator, context)
        elif template == "codescript":
            self._script_code(generator, context)

    def camel_case(self, st):
        output = "".join(x for x in st.title() if x.isalnum())
        return output

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
                title=mbtitle, message=_("Select widget"), parent=parent
            )
        template = self.template_var.get()
        if valid and template is None:
            valid = False
            messagebox.showwarning(
                title=mbtitle, message=_("Select template"), parent=parent
            )
        classname = self.classnamevar.get()
        if valid and classname == "":
            valid = False
            messagebox.showwarning(
                title=mbtitle, message=_("Enter classname"), parent=parent
            )
        if valid and (
            keyword.iskeyword(classname) or not classname.isidentifier()
        ):
            valid = False
            messagebox.showwarning(
                title=mbtitle, message=_("Invalid classname"), parent=parent
            )

        return valid

    def _format_code(self, code):
        return autopep8.fix_code(code, options={"aggressive": 1})
