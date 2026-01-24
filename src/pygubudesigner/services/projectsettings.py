#!/usr/bin/python3
import pathlib
import tkinter as tk
import tkinter.ttk as ttk
import logging
import pygubu

import pygubudesigner.services.projectsettingsui as baseui
from collections.abc import Iterable
from tkinter import messagebox
from pygubu.forms.transformer.tkboolean import BoolTransformer
from pygubudesigner.preferences import NEW_STYLE_FILE_TEMPLATE
from pygubudesigner.i18n import translator as _
from .project import Project
from .fieldvalidator import (
    IsIdentifier,
    RelativePathExists,
    Choice,
    IsNamespace,
)
from pygubudesigner.services.image_loader import iconset_loader


logger = logging.getLogger(__name__)


class ProjectSettings(baseui.ProjectSettingsUI):
    def __init__(self, master=None, translator=None):
        super().__init__(
            master, translator=translator, image_loader=iconset_loader
        )
        self._current_project: Project = None
        self.on_settings_changed = None
        self.dialog_toplevel = self.mainwindow.toplevel
        self.combo_candidates = {}

        options = {
            "filetypes": ((_("Python module"), "*.py"), (_("All"), "*.*")),
        }
        buttons = (
            self.btn_stylepath_find,
            self.btn_stylepath_new,
            self.btn_cwadd_module,
        )
        for btn in buttons:
            btn.configure(**options)

        self.fb_general = self.frm_general
        self.fb_code = self.frm_code
        self.fb_style = self.frm_style

        self.template_desc = {
            "application": _(
                "Create a class based application that uses the UI definition file."
            ),
            "codescript": _("Create a class based application with coded UI."),
            "fnscript": _("Create a function based application with coded UI."),
            "widget": _(
                "Create a custom widget and the the object builder class file."
            ),
            "widgetds": _(
                "Create a custom widget that uses a tkinter widget as parent class."
            ),
        }
        self.template_keys = {
            "application": _("Application that uses UI file"),
            "codescript": _("Application with coded UI (class)"),
            "fnscript": _("Application with coded UI (function)"),
            "widget": _("Custom widget: compound"),
            "widgetds": _("Custom widget: direct subclass"),
        }

        # field = self.builder.get_object("template")
        self.template.configure(values=self.template_keys.items())

        bool_transformer = BoolTransformer()
        identifier_constraint = IsIdentifier()
        namespace_or_empty = IsNamespace(empty_values=[""])
        path_exists_constraint = RelativePathExists()
        self.main_widget_constraint = Choice()
        self.path_exists_constraint = path_exists_constraint
        frm_general_config = {"name": {}, "description": {}, "translator": _}
        frm_code_config = dict(
            translator=_,
            module_namespace={
                "required": False,
                "constraints": [namespace_or_empty],
            },
            module_name={
                "constraints": [identifier_constraint],
            },
            main_classname={
                "constraints": [identifier_constraint],
            },
            main_widget={
                "constraints": [self.main_widget_constraint],
            },
            output_dir={
                "required": False,
                "constraints": [path_exists_constraint],
            },
            output_dir2={
                "required": False,
                "constraints": [path_exists_constraint],
            },
            builder_namespace={
                "required": False,
                "constraints": [namespace_or_empty],
            },
            import_tkvariables={
                "model_transformer": bool_transformer,
            },
            use_ttk_styledefinition_file={
                "model_transformer": bool_transformer,
            },
            use_i18n={
                "model_transformer": bool_transformer,
            },
            all_ids_attributes={
                "model_transformer": bool_transformer,
            },
            generate_code_onsave={
                "model_transformer": bool_transformer,
            },
            use_window_centering_code={
                "model_transformer": bool_transformer,
            },
        )

        frm_style_config = dict(
            translator=_,
            ttk_style_definition_file={
                "required": False,
                "constraints": [path_exists_constraint],
            },
        )
        self.frm_general = self.fb_general.get_form(frm_general_config)
        self.frm_code = self.fb_code.get_form(frm_code_config)
        self.frm_style = self.fb_style.get_form(frm_style_config)

    def run(self):
        self.mainwindow.run()

    def on_dialog_close(self, event=None):
        self.mainwindow.close()

    def setup(self, options: dict):
        self.combo_candidates = options

    def setup_comboboxes(self):
        template = self.frm_code.fields["template"].data
        options = self.combo_candidates.copy()
        if template in ("widget", "widgetds", "fnscript"):
            options["main_widget"] = options["custom_widget"]
        if template == "fnscript":
            options["main_widget"].update(options["main_menu"])
        keys = ("main_widget",)
        for key in keys:
            if key in options:
                field = getattr(self, key)
                field.configure(values=options[key])
                # setup valid values for constraints
                constraint = getattr(self, f"{key}_constraint")
                choices = list(options[key])
                constraint.valid_choices = choices

    def edit(self, project: Project):
        self._current_project = project
        settings = project.get_full_settings()

        # update template val before loading project settings on form
        template_val = settings["template"]
        self.frm_code.fields["template"].data = template_val
        self.setup_comboboxes()

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
            # form frame builder, form setting, tab index
            (self.fb_general, self.frm_general, 0),
            (self.fb_code, self.frm_code, 1),
            (self.fb_style, self.frm_style, 2),
        )
        # Process forms
        all_valid = True
        for builder, form, tab_index in forms:
            form.submit()
            valid = form.is_valid()
            all_valid = all_valid and valid
            if valid:
                new_settings.update(form.cleaned_data)
            else:
                self.settings_notebook.select(tab_index)
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
            "import_tkvariables": tk.DISABLED,
            "use_i18n": tk.NORMAL,
            "all_ids_attributes": tk.NORMAL,
            "output_dir2": tk.DISABLED,
            "btn_path2_chooser": tk.DISABLED,
            "builder_namespace": tk.DISABLED,
            "use_window_centering_code": tk.NORMAL,
            "use_ttk_styledefinition_file": tk.NORMAL,
        }
        self.class_name_label_var.set(_("Class name:"))
        if template == "application":
            state["import_tkvariables"] = tk.NORMAL
            state["all_ids_attributes"] = tk.DISABLED
        elif template == "codescript":
            pass
        elif template in ("widget", "widgetds"):
            # state["use_i18n"] = tk.DISABLED
            state["output_dir2"] = tk.NORMAL
            state["btn_path2_chooser"] = tk.NORMAL
            state["builder_namespace"] = tk.NORMAL
            state["use_window_centering_code"] = tk.DISABLED
            state["use_ttk_styledefinition_file"] = tk.DISABLED
        elif template == "fnscript":
            state["all_ids_attributes"] = tk.DISABLED
            state["use_window_centering_code"] = tk.DISABLED
            state["use_ttk_styledefinition_file"] = tk.DISABLED
            self.class_name_label_var.set(_("Function name:"))
        for fname, newstate in state.items():
            if fname in self.frm_code.fields:
                self.frm_code.fields[fname].widget.configure(state=newstate)
            else:
                getattr(self, fname).configure(state=newstate)
        self.setup_comboboxes()
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
        # Pathchooser button bug?
        btn.configure(path=None)

    def btn_cwremove_clicked(self):
        items = self.cwtree.selection()
        self.cwtree.delete(*items)
        self._configure_path_remove()


if __name__ == "__main__":
    root = tk.Tk()
    app = ProjectSettings(root)
    app.run()
