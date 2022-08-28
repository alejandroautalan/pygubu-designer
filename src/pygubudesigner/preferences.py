import configparser
import logging
import os
import tkinter as tk
from pathlib import Path
from tkinter import filedialog, messagebox

import pygubu
from appdirs import AppDirs

from pygubudesigner.util import get_ttk_style

from .i18n import translator as _

logger = logging.getLogger(__name__)

dirs = AppDirs("pygubu-designer")
CONFIG_FILE = Path(dirs.user_data_dir) / "config"

logger.info(f"Using configfile: {CONFIG_FILE}")

options = {
    "widget_set": {"values": '["tk", "ttk"]', "default": "ttk"},
    "ttk_theme": {"default": "default"},
    "default_layout_manager": {
        "values": '["pack", "grid", "place"]',
        "default": "pack",
    },
    "center_preview": {
        "values": '["yes", "no"]',
        "default": "no",
    },
    "geometry": {
        "default": "640x480",
    },
    "widget_naming_separator": {
        "values": '["NONE", "UNDERSCORE"]',
        "default": "NONE",
    },
    "widget_naming_ufletter": {
        "values": '["yes", "no"]',
        "default": "no",
    },
    "v_style_definition_file": {
        "default": "",
    },
}

SEC_GENERAL = "GENERAL"
SEC_CUSTOM_WIDGETS = "CUSTOM_WIDGETS"
SEC_RECENT_FILES = "RECENT_FILES"
config = configparser.ConfigParser()
config.add_section(SEC_CUSTOM_WIDGETS)
config.add_section(SEC_GENERAL)
config.add_section(SEC_RECENT_FILES)

DATA_DIR = Path(__file__).parent / "data"
TEMPLATE_DIR = DATA_DIR / "code_templates"
NEW_STYLE_FILE_TEMPLATE = TEMPLATE_DIR / "customstyles.py.mako"


def initialize_configfile():
    if not os.path.exists(dirs.user_data_dir):
        os.makedirs(dirs.user_data_dir)

    if not CONFIG_FILE.exists():
        with CONFIG_FILE.open("w") as configfile:
            config.write(configfile)


def save_configfile():
    with CONFIG_FILE.open("w") as configfile:
        config.write(configfile)


def load_configfile():
    defaults = {}
    for k in options:
        defaults[k] = options[k]["default"]
    config[SEC_GENERAL] = defaults
    if CONFIG_FILE.exists():
        try:
            config.read(CONFIG_FILE)
        except configparser.MissingSectionHeaderError as e:
            logger.exception(e)
            msg = _(
                f"Configuration file at {CONFIG_FILE!s} is corrupted, program may not work as expected."
                + "If you delete this file, configuration will be set to default"
            )
            messagebox.showerror(_("Error"), msg)
        except configparser.Error as e:
            logger.exception(e)
            msg = _(
                f"Faild to parse config file at {CONFIG_FILE!s}, program may not work as expected."
            )
            messagebox.showerror(_("Error"), msg)
    else:
        initialize_configfile()


def get_custom_widgets():
    paths = []
    for __, p in config.items(SEC_CUSTOM_WIDGETS):
        paths.append(p)
    return paths


def get_option(key):
    return config.get(SEC_GENERAL, key)


def set_option(key, value, save=False):
    config.set(SEC_GENERAL, key, value)
    if save:
        save_configfile()


def recent_files_get():
    rf = []
    for __, f in config.items(SEC_RECENT_FILES):
        rf.append(f)
    return rf


def recent_files_save(file_list):
    config.remove_section(SEC_RECENT_FILES)
    config.add_section(SEC_RECENT_FILES)
    for j, p in enumerate(file_list):
        config.set(SEC_RECENT_FILES, f"f{j}", p)
    save_configfile()


def save_window_size(geom):
    set_option("geometry", geom, save=True)


def get_window_size():
    return get_option("geometry")


# Get user configuration
load_configfile()


class PreferencesUI:
    def __init__(self, master, translator=None):
        self.master = master
        self.translator = translator
        self.dialog = None
        self.dialog_toplevel = None
        self.builder = None
        self.restore_tk_variables = {}
        self.restore_custom_widgets_list = []
        self._create_preferences_dialog()
        self._load_options()
        self._save_settings_snapshot()

    def _create_preferences_dialog(self):
        self.builder = builder = pygubu.Builder(self.translator)
        uifile = DATA_DIR / "ui/preferences_dialog.ui"
        builder.add_from_file(str(uifile))

        top = self.master.winfo_toplevel()
        self.dialog = builder.get_object("preferences", top)
        self.dialog_toplevel = self.dialog.toplevel

        self.v_style_definition_file = builder.get_variable(
            "v_style_definition_file"
        )

        # setup theme values
        s = get_ttk_style()
        styles = s.theme_names()
        themelist = []
        for name in styles:
            themelist.append((name, name))
        themelist.sort()
        cbox = builder.get_object("cbox_ttk_theme")
        cbox.configure(values=themelist)

        # General
        for key in ("widget_set",):
            cbox = builder.get_object(key)
            cbox.configure(values=options[key]["values"])

        # Preferred layout manager
        cbox_layout_manager = builder.get_object("cbox_layout_manager")
        cbox_layout_manager.configure(
            values=options["default_layout_manager"]["values"]
        )

        self.cwtv = builder.get_object("cwtv")
        self.path_remove = builder.get_object("path_remove")
        builder.connect_callbacks(self)

        # hide options
        fhide = builder.get_object("fhidden")
        fhide.grid_forget()

    def _load_options(self):
        # General
        for key in options:
            var = self.builder.get_variable(key)
            var.set(get_option(key))
        # Custom widgets
        for k, p in config.items(SEC_CUSTOM_WIDGETS):
            self.cwtv.insert("", "end", text=p)
        self._configure_path_remove()

    def _save_options(self):
        # General
        for key in options:
            var = self.builder.get_variable(key)
            config.set(SEC_GENERAL, key, var.get())
        # Custom Widgets
        config.remove_section(SEC_CUSTOM_WIDGETS)
        config.add_section(SEC_CUSTOM_WIDGETS)
        paths = []
        for iid in self.cwtv.get_children():
            txt = self.cwtv.item(iid, "text")
            paths.append(txt)
        for j, p in enumerate(paths):
            config.set(SEC_CUSTOM_WIDGETS, f"w{j}", p)
        save_configfile()
        self._save_settings_snapshot()
        self.master.event_generate("<<PygubuDesignerPreferencesSaved>>")

    def _configure_path_remove(self):
        if len(self.cwtv.get_children()):
            self.path_remove.configure(state="normal")
        else:
            self.path_remove.configure(state="disabled")

    def _cancel_changes(self):
        """
        Restore the preferences Tk variables back to what they were
        from when the user first opened the preferences window.

        This is because the user doesn't want to save the changes.
        """

        # Restore Tk variable values
        for v_name, tk_var in self.builder.tkvariables.items():
            if v_name in self.restore_tk_variables:
                tk_var.set(self.restore_tk_variables[v_name])

        # Restore custom widgets treeview list
        all_items = self.cwtv.get_children()
        self.cwtv.delete(*all_items)
        for custom_widget_path in self.restore_custom_widgets_list:
            self.cwtv.insert(parent="", index=tk.END, text=custom_widget_path)

        # If the treeview list is empty, disable the '-' (remove) button.
        self._configure_path_remove()

    def _deselect_combobox_text(self):
        """
        Deselect all text in all combo boxes.

        If we don't do this, the next time the preference window opens,
        One of the combo boxes may have all its text selected.
        """
        general_frame = self.builder.get_object("general_frame")
        for w in general_frame.winfo_children():
            if w.winfo_class() == "TCombobox":
                w.select_clear()

    def _save_settings_snapshot(self):
        """
        Save the value of all Tk variables related to preferences
        and also the custom widgets list.

        The purpose is: if the user clicks Cancel or closes the window
        without clicking 'OK', we need to revert the Tk variables
        changes the user made.
        """

        # Save Tk variable values
        for v_name, tk_var in self.builder.tkvariables.items():
            self.restore_tk_variables[v_name] = tk_var.get()

        # Save the custom widgets treeview list
        self.restore_custom_widgets_list.clear()
        for custom_widget_path_iid in self.cwtv.get_children():
            item_text = self.cwtv.item(custom_widget_path_iid).get("text")
            self.restore_custom_widgets_list.append(item_text)

    def on_create_new_definition_clicked(self):
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

            if os.path.isfile(fname):
                msg = _("File saved.\n\nPlease edit the style definition file.")
                messagebox.showinfo(_("Styles"), msg)

                # Auto setup this new file definition:
                self.v_style_definition_file.set(fname)

        except OSError:
            msg = _("Error saving template file.")
            messagebox.showerror(_("Styles"), msg)

    def on_clicked_select_style_file(self):
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
            self.v_style_definition_file.set(fname)

    def on_clicked_remove_style_file(self):
        """
        Clear a Ttk style definition.
        """
        suggest_restart = False

        # Is there an existing style definition path?
        if self.v_style_definition_file.get():
            suggest_restart = True
        self.v_style_definition_file.set("")

        if suggest_restart:
            msg = _("Restart Pygubu Designer for\nchanges to take effect.")
            messagebox.showinfo(_("Styles"), msg)

    def on_dialog_close(self, event=None):
        # If the user closed this window from the window manager (ie: 'X' button),
        # event will have a value, which means the user doesn't want to save changes.
        if event:
            # The user closed the window from the window manager.
            # Reverse any preference changes made.
            self._cancel_changes()
        else:
            # The user clicked the OK button, so save the changes.
            self._save_options()

        self._deselect_combobox_text()
        self.dialog.close()

    def on_cancel(self, event=None):
        self._cancel_changes()
        self._deselect_combobox_text()
        self.dialog.close()

    def on_pathremove_clicked(self):
        items = self.cwtv.selection()
        self.cwtv.delete(*items)
        self._configure_path_remove()

    def on_pathadd_clicked(self):
        options = {
            "defaultextension": ".py",
            "filetypes": ((_("Python module"), "*.py"), (_("All"), "*.*")),
        }
        fname = filedialog.askopenfilename(
            parent=self.dialog_toplevel, **options
        )
        if fname:
            self.cwtv.insert("", tk.END, text=fname)
            self._configure_path_remove()
