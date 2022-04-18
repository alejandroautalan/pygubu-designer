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

dirs = AppDirs('pygubu-designer')
CONFIG_FILE = Path(dirs.user_data_dir) / 'config'

logger.info(f'Using configfile: {CONFIG_FILE}')

options = {
    'widget_set': {'values': '["tk", "ttk"]', 'default': 'ttk'},
    'ttk_theme': {'default': 'default'},
    'default_layout_manager': {
        'values': '["pack", "grid", "place"]',
        'default': 'pack',
    },
    'geometry': {
        'default': '640x480',
    },
    'widget_naming_separator': {
        'values': '["NONE", "UNDERSCORE"]',
        'default': 'NONE',
    },
    'widget_naming_ufletter': {
        'values': '["yes", "no"]',
        'default': 'no',
    },
    'v_style_definition_file': {
        'default': '',
    },
}

SEC_GENERAL = 'GENERAL'
SEC_CUSTOM_WIDGETS = 'CUSTOM_WIDGETS'
SEC_RECENT_FILES = 'RECENT_FILES'
config = configparser.ConfigParser()
config.add_section(SEC_CUSTOM_WIDGETS)
config.add_section(SEC_GENERAL)
config.add_section(SEC_RECENT_FILES)

CURRENT_DIR = Path(__file__).parent
TEMPLATE_DIR = CURRENT_DIR / 'codegen' / 'template'
NEW_STYLE_FILE_TEMPLATE = TEMPLATE_DIR / 'customstyles.py.mako'


def initialize_configfile():
    if not os.path.exists(dirs.user_data_dir):
        os.makedirs(dirs.user_data_dir)

    if not CONFIG_FILE.exists():
        with CONFIG_FILE.open('w') as configfile:
            config.write(configfile)


def save_configfile():
    with CONFIG_FILE.open('w') as configfile:
        config.write(configfile)


def load_configfile():
    defaults = {}
    for k in options:
        defaults[k] = options[k]['default']
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
            messagebox.showerror(_('Error'), msg)
        except configparser.Error as e:
            logger.exception(e)
            msg = _(
                f"Faild to parse config file at {CONFIG_FILE!s}, program may not work as expected."
            )
            messagebox.showerror(_('Error'), msg)
    else:
        initialize_configfile()


def get_custom_widgets():
    paths = []
    for _, p in config.items(SEC_CUSTOM_WIDGETS):
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
    for _, f in config.items(SEC_RECENT_FILES):
        rf.append(f)
    return rf


def recent_files_save(file_list):
    config.remove_section(SEC_RECENT_FILES)
    config.add_section(SEC_RECENT_FILES)
    for j, p in enumerate(file_list):
        config.set(SEC_RECENT_FILES, f'f{j}', p)
    save_configfile()


def save_window_size(geom):
    set_option('geometry', geom, save=True)


def get_window_size():
    return get_option('geometry')


# Get user configuration
load_configfile()


class PreferencesUI:
    def __init__(self, master, translator=None):
        self.master = master
        self.translator = translator
        self.dialog = None
        self.builder = None
        self._create_preferences_dialog()
        self._load_options()

    def _create_preferences_dialog(self):
        self.builder = builder = pygubu.Builder(self.translator)
        uifile = CURRENT_DIR / "ui/preferences_dialog.ui"
        builder.add_from_file(str(uifile))

        top = self.master.winfo_toplevel()
        self.dialog = dialog = builder.get_object('preferences', top)

        self.v_style_definition_file = builder.get_variable('v_style_definition_file')

        # setup theme values
        s = get_ttk_style()
        styles = s.theme_names()
        themelist = []
        for name in styles:
            themelist.append((name, name))
        themelist.sort()
        cbox = builder.get_object('cbox_ttk_theme')
        cbox.configure(values=themelist)

        # General
        for key in ('widget_set',):
            cbox = builder.get_object(key)
            cbox.configure(values=options[key]['values'])

        # Preferred layout manager
        cbox_layout_manager = builder.get_object('cbox_layout_manager')
        cbox_layout_manager.configure(
            values=options['default_layout_manager']['values']
        )

        self.cwtv = builder.get_object('cwtv')
        self.path_remove = builder.get_object('path_remove')
        builder.connect_callbacks(self)

        # hide options
        fhide = builder.get_object('fhidden')
        fhide.grid_forget()

    def _load_options(self):
        # General
        for key in options:
            var = self.builder.get_variable(key)
            var.set(get_option(key))
        # Custom widgets
        for k, p in config.items(SEC_CUSTOM_WIDGETS):
            self.cwtv.insert('', 'end', text=p)
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
            txt = self.cwtv.item(iid, 'text')
            paths.append(txt)
        for j, p in enumerate(paths):
            config.set(SEC_CUSTOM_WIDGETS, f'w{j}', p)
        save_configfile()
        self.master.event_generate('<<PygubuDesignerPreferencesSaved>>')

    def _configure_path_remove(self):
        if len(self.cwtv.get_children()):
            self.path_remove.configure(state='normal')
        else:
            self.path_remove.configure(state='disabled')

    def on_create_new_definition_clicked(self):
        """
        Prompt the user to save a new Python file which will contain
        some sample code so the user will have an idea on how to change styles.
        """

        options = {
            'defaultextension': '.py',
            'filetypes': ((_('Python module'), '*.py'), (_('All'), '*.*')),
        }
        fname = filedialog.asksaveasfilename(**options)
        if not fname:
            return

        try:
            with open(fname, "w") as f:
                with NEW_STYLE_FILE_TEMPLATE.open() as tfile:
                    sample_script_contents = tfile.read()
                    f.write(sample_script_contents)

            if os.path.isfile(fname):
                msg = _("File saved.\n\nPlease edit the style definition file.")
                messagebox.showinfo(_('Styles'), msg)

                # Auto setup this new file definition:
                self.v_style_definition_file.set(fname)

        except OSError:
            msg = _("Error saving template file.")
            messagebox.showerror(_('Styles'), msg)

    def on_clicked_select_style_file(self):
        """
        A 'Browse...' button was clicked on to select a
        Ttk style definition file.
        """

        options = {
            'defaultextension': '.py',
            'filetypes': ((_('Python module'), '*.py'), (_('All'), '*.*')),
        }
        fname = filedialog.askopenfilename(**options)
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
        self.v_style_definition_file.set('')

        if suggest_restart:
            msg = _("Restart Pygubu Designer for\nchanges to take effect.")
            messagebox.showinfo(_('Styles'), msg)

    def on_dialog_close(self, event=None):
        self._save_options()
        self.dialog.close()

    def on_cancel(self, event=None):
        self.dialog.close()

    def on_pathremove_clicked(self):
        items = self.cwtv.selection()
        self.cwtv.delete(*items)
        self._configure_path_remove()

    def on_pathadd_clicked(self):
        options = {
            'defaultextension': '.py',
            'filetypes': ((_('Python module'), '*.py'), (_('All'), '*.*')),
        }
        fname = filedialog.askopenfilename(**options)
        if fname:
            self.cwtv.insert('', tk.END, text=fname)
            self._configure_path_remove()
