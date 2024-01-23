#!/usr/bin/python3
import pathlib
import tkinter as tk
import tkinter.ttk as ttk
import pprint as pp
import pygubu

from tkinter import filedialog, messagebox
from pygubu.forms.transformer import DataTransformer
from pygubu.forms.exceptions import ValidationError
from pygubu.forms.forms import FormWidget
from projectsettingsbase import ProjectSettingsBase
from pygubudesigner.preferences import NEW_STYLE_FILE_TEMPLATE


def _(value):
    return value


class BoolTransformer(DataTransformer):
    def transform(self, value):
        tval = False
        try:
            tval = bool(value)
        except ValueError:
            pass
        return tval

    def reversetransform(self, value):
        tval = False
        try:
            tval = tk.getboolean(value)
        except tk.TclError:
            pass
        print(f"reversetransform: {tval}", type(tval))
        return tval


class ProjectSettings(ProjectSettingsBase):
    def __init__(self, master=None):
        super().__init__(master)
        self.dialog_toplevel = self.mainwindow.toplevel
        self.frm_general: FormWidget = self.builder.get_object("frm_general")
        self.frm_code: FormWidget = self.builder.get_object("frm_code")
        self.frm_style: FormWidget = self.builder.get_object("frm_style")
        # self.frm_general = self.builder.get_object("frm_custom_widgets")
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
        bool_options = (
            "import_tkvariables",
            "use_ttk_styledefinition_file",
            "use_i18n",
            "all_ids_attributes",
            "generate_code_onsave",
        )
        bool_transformer = BoolTransformer()
        for key in bool_options:
            field = self.builder.get_object(key)
            field.model_transformer = bool_transformer

    def run(self):
        self.mainwindow.run()

    def on_dialog_close(self, event=None):
        # If the user closed this window from the window manager (ie: 'X' button),
        # event will have a value, which means the user doesn't want to save changes.
        if event:
            # The user closed the window from the window manager.
            # Reverse any preference changes made.
            # self._cancel_changes()
            pass
        else:
            # The user clicked the OK button, so save the changes.
            # self._save_options()
            pass
        self.mainwindow.close()

    def setup(self, options: dict):
        keys = ("main_widget", "main_menu")
        for key in keys:
            if key in options:
                field = self.builder.get_object(key)
                field.configure(values=options[key])

    def edit_settings(self, settings, default):
        self.frm_general.edit(settings, default)
        self.frm_code.edit(settings, default)
        self.frm_style.edit(settings, default)

        template = self.frm_code.fields["template"].data
        self.template_desc_var.set(self.template_desc[template])

        self._configure_path_remove()

    def btn_apply_clicked(self):
        forms = (self.frm_general, self.frm_code, self.frm_style)
        all_valid = True
        for form in forms:
            form.submit()
            valid = form.is_valid()
            all_valid = all_valid and valid
            if valid:
                print("valid!")
                print("form data:")
                pp.pprint(form.cleaned_data)
            else:
                print("invalid!")
                pp.pprint(form.errors)
        if all_valid:
            self.mainwindow.close()

    def btn_cancel_clicked(self):
        self.mainwindow.close()

    def on_template_change(self, event=None):
        template_field = self.frm_code.fields["template"]
        template = template_field.data
        state = {
            "import_tkvariables": "disabled",
            "use_i18n": "normal",
            "all_ids_attributes": "normal",
            "main_menu": "normal",
        }
        if template == "application":
            state["import_tkvariables"] = "normal"
            state["all_ids_attributes"] = "disabled"
        elif template == "codescript":
            pass
        elif template == "widget":
            state["use_i18n"] = "disabled"
            state["main_menu"] = "disabled"
        for fname, newstate in state.items():
            if fname in self.frm_code.fields:
                self.frm_code.fields[fname].configure(state=newstate)
        # Update template description
        self.template_desc_var.set(self.template_desc[template])

    def on_style_browse(self):
        """
        A 'Browse...' button was clicked on to select a
        Ttk style definition file.
        """

        options = {
            "defaultextension": ".py",
            "filetypes": ((_("Python module"), "*.py"), (_("All"), "*.*")),
        }
        fname = filedialog.askopenfilename(
            parent=self.dialog_toplevel, **options
        )
        if fname:
            fieldname = "ttk_style_definition_file"
            self.frm_style.fields[fieldname].data = fname

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

    def on_style_new(self):
        """
        Prompt the user to save a new Python file which will contain
        some sample code so the user will have an idea on how to change styles.
        """

        options = {
            "defaultextension": ".py",
            "filetypes": ((_("Python module"), "*.py"), (_("All"), "*.*")),
        }
        fname = filedialog.asksaveasfilename(
            parent=self.dialog_toplevel, **options
        )
        if not fname:
            return

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
                self.frm_style.fields[fieldname].data = fname

        except OSError:
            msg = _("Error saving template file.")
            messagebox.showerror(_("Styles"), msg, parent=self.dialog_toplevel)

    def _configure_path_remove(self):
        has_children = len(self.cwtree.get_children())
        newstate = "normal" if has_children else "disabled"
        self.btn_cwremove.configure(state=newstate)

    def btn_cwadd_clicked(self):
        options = {
            "defaultextension": ".py",
            "filetypes": ((_("Python module"), "*.py"), (_("All"), "*.*")),
        }
        fname = filedialog.askopenfilename(
            parent=self.dialog_toplevel, **options
        )
        if fname:
            self.cwtree.insert("", tk.END, text=fname)
            self._configure_path_remove()

    def btn_cwremove_clicked(self):
        items = self.cwtree.selection()
        self.cwtree.delete(*items)
        self._configure_path_remove()


if __name__ == "__main__":
    root = tk.Tk()
    app = ProjectSettingsBase(root)
    app.run()
