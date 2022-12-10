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
from tkinter import filedialog, messagebox

import autopep8
from mako.lookup import TemplateLookup

from .codebuilder import UI2Code

logger = logging.getLogger(__name__)
DATA_DIR = pathlib.Path(__file__).parent.parent / "data"
TEMPLATE_DIR = DATA_DIR / "code_templates"
makolookup = TemplateLookup(directories=[TEMPLATE_DIR])


class ScriptGenerator:
    def __init__(self, app):
        self.app = app
        self.builder = builder = app.builder
        self.tree = app.tree_editor
        self.projectname = ""

        self.widgetlist = w = builder.get_object("widgetlist")
        w.bind("<<ComboboxSelected>>", self._configure_menulist)
        self.menulist = builder.get_object("menulist")

        self.widgetlistvar = None
        self.widgetlist_keyvar = None
        self.template_var = None
        self.classnamevar = None
        self.template_desc_var = None
        self.import_tkvars_var = None
        self.use_ttkdefs_file_var = None
        self.add_i18n_var = None
        self.menulist_keyvar = None
        myvars = [
            "widgetlistvar",
            "widgetlist_keyvar",
            "template_var",
            "classnamevar",
            "template_desc_var",
            "import_tkvars_var",
            "use_ttkdefs_file_var",
            "add_i18n_var",
            "menulist_keyvar",
            "all_ids_attributes_var",
        ]
        builder.import_variables(self, myvars)

        self.txt_code = builder.get_object("txt_code")
        self.cb_import_tkvars = builder.get_object("cb_import_tkvars")
        self.cb_add_i18n = builder.get_object("cb_add_i18n")
        self.cb_all_ids_attributes = builder.get_object("cb_all_ids_attributes")

        _ = self.app.translator
        self.msgtitle = _("Script Generator")

        self.template_desc = {
            "application": _(
                "Create a pygubu application script using the UI definition."
            ),
            "codescript": _("Create a coded version of the UI definition."),
            "widget": _("Create a base class for your custom widget."),
        }
        self.template_var.set("application")
        self.import_tkvars_var.set(True)
        self.use_ttkdefs_file_var.set(False)

    def camel_case(self, st):
        output = "".join(x for x in st.title() if x.isalnum())
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
            with_i18n_support = self.add_i18n_var.get()
            all_ids_attributes = self.all_ids_attributes_var.get()

            main_widget_is_toplevel = False
            set_main_menu = False
            main_menu_id = None
            toplevel_uids = (
                "tk.Toplevel",
                "customtkinter.CTk",
                "customtkinter.CTkToplevel",
            )
            if target_class in toplevel_uids:
                main_widget_is_toplevel = True

                # Main menu definition
                menu_item = self.menulist_keyvar.get()
                if menu_item not in ("empty", "None") and template != "widget":
                    main_menu_id = self.tree.get_widget_id(menu_item)
                    set_main_menu = True

            context = {
                "project_name": self.projectname,
                "class_name": class_name,
                "main_widget_is_toplevel": main_widget_is_toplevel,
                "main_widget": target,
                "widget_base_class": target_class,
                "widget_code": None,
                "import_lines": None,
                "ttk_styles": None,
                "callbacks": "",
                "tkvariables": [],
                "has_ttk_styles": False,
                "set_project_path": False,
                "with_i18n_support": with_i18n_support,
                "set_main_menu": set_main_menu,
                "main_menu_id": main_menu_id,
            }

            generator.with_i18n_support = with_i18n_support
            generator.all_ids_as_attributes = all_ids_attributes

            if template == "application":
                generator.add_import_line("pathlib")
                if not main_widget_is_toplevel:
                    generator.add_import_line("tkinter", "tk", priority=1)
                if self.use_ttkdefs_file_var.get():
                    generator.add_import_line("tkinter.ttk", "ttk", priority=1)
                generator.add_import_line("pygubu", priority=10)
                code = generator.generate_app_with_ui(uidef, target)

                context["import_lines"] = code["imports"]
                # Set project paths
                context["set_project_path"] = True
                # Style definitions
                ttk_styles_code = code["ttkstyles"]
                if self.use_ttkdefs_file_var.get() and ttk_styles_code:
                    context["has_ttk_styles"] = True
                context["ttk_styles"] = ttk_styles_code
                # Callbacks
                context["callbacks"] = code["callbacks"]
                # Tk Variables
                if self.import_tkvars_var.get():
                    context["tkvariables"] = code["tkvariables"]
                tpl = makolookup.get_template("app.py.mako")
                final_code = tpl.render(**context)
                final_code = self._format_code(final_code)
                self.set_code(final_code)
            elif template == "widget":
                generator.with_i18n_support = False
                generator.add_import_line("tkinter", "tk")
                if self.use_ttkdefs_file_var.get():
                    generator.add_import_line("tkinter.ttk", "ttk", priority=1)
                # Generate code
                code = generator.generate_app_widget(uidef, target)
                # Prepare template context
                context["widget_code"] = code[target]
                context["import_lines"] = code["imports"]
                context["callbacks"] = code["callbacks"]
                # Style definitions
                ttk_styles_code = code["ttkstyles"]
                if self.use_ttkdefs_file_var.get() and ttk_styles_code:
                    context["has_ttk_styles"] = True
                context["ttk_styles"] = ttk_styles_code

                tpl = makolookup.get_template("widget.py.mako")
                final_code = tpl.render(**context)
                final_code = self._format_code(final_code)
                self.set_code(final_code)
            elif template == "codescript":
                if not main_widget_is_toplevel:
                    generator.add_import_line("tkinter", "tk")
                if self.use_ttkdefs_file_var.get():
                    generator.add_import_line("tkinter.ttk", "ttk", priority=1)

                methods = []
                if set_main_menu:
                    methods.append(main_menu_id)
                # Generate code
                code = generator.generate_app_code(
                    uidef, target, methods_for=methods
                )

                # Prepare template context
                context["widget_code"] = code[target]
                context["import_lines"] = code["imports"]
                context["callbacks"] = code["callbacks"]
                context["methods"] = code["methods"]
                context["target_code_id"] = code["target_code_id"]
                # Style definitions
                ttk_styles_code = code["ttkstyles"]
                if self.use_ttkdefs_file_var.get() and ttk_styles_code:
                    context["has_ttk_styles"] = True
                context["ttk_styles"] = ttk_styles_code

                tpl = makolookup.get_template("script.py.mako")
                final_code = tpl.render(**context)
                final_code = self._format_code(final_code)
                self.set_code(final_code)

    def on_code_copy_clicked(self):
        text = self.get_code()
        self.txt_code.clipboard_clear()
        self.txt_code.clipboard_append(text)

        _ = self.app.translator
        msg = _("Code copied")
        messagebox.showinfo(
            title=self.msgtitle,
            message=msg,
            parent=self.widgetlist.winfo_toplevel(),
        )

    def on_code_template_changed(self, clear_code=True):
        template = self.template_var.get()
        classname = self.get_classname()
        import_tkvars_state = "disabled"
        add_i18n_state = "normal"
        menulist_state = "normal"
        all_ids_state = "normal"
        if template == "application":
            name = f"{classname}App"
            self.classnamevar.set(name)
            import_tkvars_state = "normal"
            all_ids_state = "disabled"
        elif template == "codescript":
            name = f"{classname}App"
            self.classnamevar.set(name)
        elif template == "widget":
            name = f"{classname}Widget"
            self.classnamevar.set(name)
            add_i18n_state = "disabled"
            menulist_state = "disabled"
        self.cb_import_tkvars.configure(state=import_tkvars_state)
        self.cb_add_i18n.configure(state=add_i18n_state)
        self.cb_all_ids_attributes.configure(state=all_ids_state)
        self.menulist.configure(state=menulist_state)
        # Update template description
        self.template_desc_var.set(self.template_desc[template])
        if clear_code:
            self.set_code("")

    def on_code_save_clicked(self):
        _ = self.app.translator
        filename = (self.classnamevar.get()).lower()
        options = {
            "defaultextension": ".py",
            "filetypes": ((_("Python Script"), "*.py"), (_("All"), "*.*")),
            "initialfile": f"{filename}.py",
        }
        fname = filedialog.asksaveasfilename(**options)
        if fname:
            with open(fname, "w") as out:
                out.write(self.get_code())

    def _configure_menulist(self, event=None):
        tree_item = self.widgetlist_keyvar.get()
        target_class = self.tree.get_widget_class(tree_item)
        newstate = "normal" if target_class == "tk.Toplevel" else "disabled"
        self.menulist.configure(state=newstate)

    def configure(self):
        self.projectname = self.app.project_name()
        # Top level widgets
        wlist = self.tree.get_top_widget_list()
        self.widgetlist.configure(values=wlist)
        self.classnamevar.set(self.get_classname())
        # Top level menues
        mlist = self.tree.get_top_menu_list()
        mlist.insert(0, ("empty", ""))
        self.menulist.configure(values=mlist)
        # self.menulist_keyvar.set('None')

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

    def set_code(self, text):
        self.txt_code.delete("0.0", "end")
        self.txt_code.insert("0.0", text)

    def get_code(self):
        return self.txt_code.get("0.0", "end-1c")

    def reset(self):
        self.set_code("")
        self.configure()

    def _format_code(self, code):
        return autopep8.fix_code(code, options={"aggressive": 1})
