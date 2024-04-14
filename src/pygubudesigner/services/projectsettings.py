#!/usr/bin/python3
import pathlib
import tkinter as tk
import tkinter.ttk as ttk
import logging
import pygubu

import pygubudesigner.services.projectsettingsui as psbase
from collections.abc import Iterable
from tkinter import messagebox
from pygubu.forms.transformer.tkboolean import BoolTransformer
from pygubudesigner.preferences import DATA_DIR, NEW_STYLE_FILE_TEMPLATE
from pygubudesigner.i18n import translator as _
from .project import Project
from .fieldvalidator import IsIdentifier, RelativePathExists, Choice


logger = logging.getLogger(__name__)


psbase.PROJECT_PATH = DATA_DIR / "ui"
psbase.PROJECT_UI = psbase.PROJECT_PATH / "project_settings.ui"


class ProjectSettings(psbase.ProjectSettingsUI):
    def __init__(self, master=None, translator=None):
        super().__init__(master, translator)
        self._current_project: Project = None
        self.on_settings_changed = None
        self.dialog_toplevel = self.mainwindow.toplevel

        options = {
            "filetypes": ((_("Python module"), "*.py"), (_("All"), "*.*")),
        }
        buttons = (
            "btn_stylepath_find",
            "btn_stylepath_new",
            "btn_cwadd_module",
        )
        for name in buttons:
            btn = self.builder.get_object(name)
            btn.configure(**options)

        self.fb_general = self.builder.get_object("frm_general")
        self.fb_code = self.builder.get_object("frm_code")
        self.fb_style = self.builder.get_object("frm_style")
        self.cwtree: ttk.Treeview = self.builder.get_object("cwtree")
        self.btn_cwremove = self.builder.get_object("btn_cwremove")

        self.template_desc_var: tk.StringVar = None
        self.builder.import_variables(self, ["template_desc_var"])

        self.template_desc = {
            "application": _(
                "Create a pygubu application script using the UI definition."
            ),
            "codescript": _("Create a coded version of the UI definition."),
            "widget": _("Create a base class for your custom widget."),
        }
        self.template_keys = {
            "application": _("Application"),
            "codescript": _("Code Script"),
            "widget": _("Custom Widget"),
        }

        field = self.builder.get_object("template")
        field.configure(values=self.template_keys.items())

        bool_transformer = BoolTransformer()
        identifier_constraint = IsIdentifier()
        path_exists_constraint = RelativePathExists()
        self.main_widget_constraint = Choice()
        self.main_menu_constraint = Choice()
        self.path_exists_constraint = path_exists_constraint
        frm_general_config = {"name": {}, "description": {}, "translator": _}
        frm_code_config = {
            "translator": _,
            "module_name": {
                "constraints": [identifier_constraint],
            },
            "main_classname": {
                "constraints": [identifier_constraint],
            },
            "main_widget": {
                "constraints": [self.main_widget_constraint],
            },
            "main_menu": {
                "required": False,
                "constraints": [self.main_menu_constraint],
            },
            "output_dir": {
                "required": False,
                "constraints": [path_exists_constraint],
            },
            "output_dir2": {
                "required": False,
                "constraints": [path_exists_constraint],
            },
            "import_tkvariables": {
                "model_transformer": bool_transformer,
            },
            "use_ttk_styledefinition_file": {
                "model_transformer": bool_transformer,
            },
            "use_i18n": {
                "model_transformer": bool_transformer,
            },
            "all_ids_attributes": {
                "model_transformer": bool_transformer,
            },
            "generate_code_onsave": {
                "model_transformer": bool_transformer,
            },
            "use_window_centering_code": {
                "model_transformer": bool_transformer,
            },
        }

        frm_style_config = {
            "translator": _,
            "ttk_style_definition_file": {
                "required": False,
                "constraints": [path_exists_constraint],
            },
        }
        self.frm_general = self.fb_general.get_form(frm_general_config)
        self.frm_code = self.fb_code.get_form(frm_code_config)
        self.frm_style = self.fb_style.get_form(frm_style_config)

    def run(self):
        self.mainwindow.run()

    def on_dialog_close(self, event=None):
        self.mainwindow.close()

    def setup(self, options: dict):
        keys = ("main_widget", "main_menu")
        for key in keys:
            if key in options:
                field = self.builder.get_object(key)
                field.configure(values=options[key])
                # setup valid values for constraints
                constraint = getattr(self, f"{key}_constraint")
                choices = list(options[key])
                if key == "main_menu":
                    choices.append("")
                constraint.valid_choices = choices

    def edit(self, project: Project):
        self._current_project = project
        settings = project.get_full_settings()
        self.frm_general.edit(settings, project.settings_default)
        self.frm_code.edit(settings, project.settings_default)
        self.frm_style.edit(settings, project.settings_default)

        template = self.frm_code.fields["template"].data
        self.template_desc_var.set(self.template_desc[template])

        children = self.cwtree.get_children()
        self.cwtree.delete(*children)
        cwlist = settings.get("custom_widgets", [])
        for path in cwlist:
            self.cwtree.insert("", tk.END, text=path)

        self.path_exists_constraint.start_path = project.fpath.parent
        self._configure_path_remove()
        self.on_template_change()

    def process_forms(self):
        new_settings = {}
        forms = (
            (self.fb_general, self.frm_general),
            (self.fb_code, self.frm_code),
            (self.fb_style, self.frm_style),
        )
        # Process forms
        all_valid = True
        for builder, form in forms:
            form.submit()
            valid = form.is_valid()
            all_valid = all_valid and valid
            if valid:
                new_settings.update(form.cleaned_data)
            else:
                notebook: ttk.Notebook = builder.nametowidget(
                    builder.winfo_parent()
                )
                index = notebook.index(builder)
                notebook.select(index)
                # Stop validation here
                break

        # Process custom widgets section
        # FIXME: improve this
        new_settings["custom_widgets"] = self._get_custom_widget_list()
        return all_valid, new_settings

    def validate_for_codegen(self):
        all_valid, new_settings = self.process_forms()
        return all_valid

    def btn_apply_clicked(self):
        all_valid, new_settings = self.process_forms()
        if all_valid:
            if self.on_settings_changed is not None:
                self.on_settings_changed(new_settings)
            self.mainwindow.close()

    def btn_cancel_clicked(self):
        self.mainwindow.close()

    def output_dir_changed(self, event=None):
        btn = event.widget
        output_field = self.frm_code.fields["output_dir"]
        new_value = btn.cget("path")
        new_value = self._current_project.get_relative_path(new_value)
        output_field.data = new_value

    def output_dir2_changed(self, event=None):
        btn = event.widget
        output_field = self.frm_code.fields["output_dir2"]
        new_value = btn.cget("path")
        new_value = self._current_project.get_relative_path(new_value)
        output_field.data = new_value

    def on_template_change(self, event=None):
        template_field = self.frm_code.fields["template"]
        template = template_field.data
        state = {
            "import_tkvariables": "disabled",
            "use_i18n": "normal",
            "all_ids_attributes": "normal",
            "main_menu": "normal",
            "output_dir2": "disabled",
            "btn_path2_chooser": "disabled",
        }
        if template == "application":
            state["import_tkvariables"] = "normal"
            state["all_ids_attributes"] = "disabled"
        elif template == "codescript":
            pass
        elif template == "widget":
            # state["use_i18n"] = "disabled"
            state["main_menu"] = "disabled"
            state["output_dir2"] = "normal"
            state["btn_path2_chooser"] = "normal"
        for fname, newstate in state.items():
            if fname in self.frm_code.fields:
                self.frm_code.fields[fname].widget.configure(state=newstate)
            else:
                self.builder.get_object(fname).configure(state=newstate)
        # Update template description
        self.template_desc_var.set(self.template_desc[template])

    def on_style_new_selected(self, event=None):
        """
        A 'Browse...' button was clicked on to select a
        Ttk style definition file.
        """

        btn = event.widget
        form_field = self.frm_style.fields["ttk_style_definition_file"]
        new_value = btn.cget("path")
        new_value = self._current_project.get_relative_path(new_value)
        form_field.data = new_value

    def on_style_remove(self):
        """
        Clear a Ttk style definition.
        """
        suggest_restart = False

        fieldname = "ttk_style_definition_file"
        current_definition = self.frm_style.fields[fieldname].data
        # Is there an existing style definition path?
        if current_definition:
            suggest_restart = True
        self.frm_style.fields[fieldname].data = ""

        if suggest_restart:
            msg = _("Restart Pygubu Designer for\nchanges to take effect.")
            messagebox.showinfo(_("Styles"), msg, parent=self.dialog_toplevel)

    def on_style_new_create(self, event=None):
        """
        Prompt the user to save a new Python file which will contain
        some sample code so the user will have an idea on how to change styles.
        """

        btn = event.widget
        fname = btn.cget("path")

        try:
            with open(fname, "w") as f:
                with NEW_STYLE_FILE_TEMPLATE.open() as tfile:
                    sample_script_contents = tfile.read()
                    f.write(sample_script_contents)

            if pathlib.Path(fname).exists():
                msg = _("File saved.\n\nPlease edit the style definition file.")
                messagebox.showinfo(
                    _("Styles"), msg, parent=self.dialog_toplevel
                )

                # Auto setup this new file definition:
                fieldname = "ttk_style_definition_file"
                fname = self._current_project.get_relative_path(fname)
                self.frm_style.fields[fieldname].data = fname

        except OSError:
            msg = _("Error saving template file.")
            messagebox.showerror(_("Styles"), msg, parent=self.dialog_toplevel)

    def _configure_path_remove(self):
        has_children = len(self.cwtree.get_children())
        newstate = "normal" if has_children else "disabled"
        self.btn_cwremove.configure(state=newstate)

    def _get_custom_widget_list(self) -> list:
        cwlist = []
        for item in self.cwtree.get_children():
            value = self.cwtree.item(item, "text")
            cwlist.append(value)
        return cwlist

    def btn_cwadd_clicked(self, event=None):
        btn = event.widget
        fname = btn.cget("path")
        if fname:
            fname = self._current_project.get_relative_path(fname)
            self.cwtree.insert("", tk.END, text=fname)
            self._configure_path_remove()

    def btn_cwremove_clicked(self):
        items = self.cwtree.selection()
        self.cwtree.delete(*items)
        self._configure_path_remove()


if __name__ == "__main__":
    root = tk.Tk()
    app = ProjectSettings(root)
    app.run()
