#!/usr/bin/python3
import pathlib
import tkinter as tk
import pygubu

PROJECT_PATH = pathlib.Path(__file__).parent
PROJECT_UI = PROJECT_PATH / "project_settings.ui"
RESOURCE_PATHS = [PROJECT_PATH]


class ProjectSettingsUI:
    def __init__(self, master=None, translator=None):
        self.builder = pygubu.Builder(translator)
        self.builder.add_resource_paths(RESOURCE_PATHS)
        self.builder.add_from_file(PROJECT_UI)
        # Main widget
        self.mainwindow: pygubu.builder.widgets.dialog = (
            self.builder.get_object("settingsdialog", master)
        )

        self.template_desc_var: tk.StringVar = None
        self.import_tkvariables_var: tk.BooleanVar = None
        self.use_ttk_style_var: tk.BooleanVar = None
        self.use_i18n_var: tk.BooleanVar = None
        self.all_ids_attr_var: tk.BooleanVar = None
        self.generate_code_onsave_var: tk.BooleanVar = None
        self.use_windowcenter_code_var: tk.BooleanVar = None
        self.builder.import_variables(self)

        self.builder.connect_callbacks(self)

    def run(self):
        self.mainwindow.mainloop()

    def on_template_change(self, event=None):
        pass

    def output_dir_changed(self, event=None):
        pass

    def output_dir2_changed(self, event=None):
        pass

    def on_style_new_selected(self, event=None):
        pass

    def on_style_new_create(self, event=None):
        pass

    def on_style_remove(self):
        pass

    def btn_cwadd_clicked(self, event=None):
        pass

    def btn_cwremove_clicked(self):
        pass

    def btn_cancel_clicked(self):
        pass

    def btn_apply_clicked(self):
        pass

    def on_dialog_close(self, event=None):
        pass


if __name__ == "__main__":
    root = tk.Tk()
    app = ProjectSettingsUI(root)
    app.run()
