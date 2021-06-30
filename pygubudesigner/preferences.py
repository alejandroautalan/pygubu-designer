# encoding: utf-8
import os
import sys
import logging
from pygubudesigner.util import get_ttk_style

try:
    import tkinter as tk
    from tkinter import ttk
    from tkinter import filedialog
    from tkinter import messagebox
except:
    import Tkinter as tk
    import ttk
    import tkMessageBox as messagebox
    import tkFileDialog as filedialog
try:
    import ConfigParser as configparser
except:
    import configparser

has_appdir = False
try:
    from appdirs import AppDirs
    has_appdir = True
except:
    pass

import pygubu

logger = logging.getLogger(__name__)
FILE_PATH = os.path.dirname(os.path.abspath(__file__))
CONFIG_FILE = os.path.join(FILE_PATH, 'config')
if has_appdir:
    dirs = AppDirs('pygubu-designer')
    CONFIG_FILE = os.path.join(dirs.user_data_dir, 'config')
logger.info('Using configfile: %s', CONFIG_FILE)

options = {
    'widget_set': {'values': '["tk", "ttk"]', 'default':'ttk'},
    'ttk_theme': {'default': 'default'},
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
    }

SEC_GENERAL = 'GENERAL'
SEC_CUSTOM_WIDGETS = 'CUSTOM_WIDGETS'
SEC_RECENT_FILES = 'RECENT_FILES'
config = configparser.SafeConfigParser()
config.add_section(SEC_CUSTOM_WIDGETS)
config.add_section(SEC_GENERAL)
config.add_section(SEC_RECENT_FILES)


def initialize_configfile():
    if not os.path.exists(dirs.user_data_dir):
        os.makedirs(dirs.user_data_dir)
    if not os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, 'w') as configfile:
            config.write(configfile)

def save_configfile():
    with open(CONFIG_FILE, 'w') as configfile:
        config.write(configfile)

def load_configfile():
    defaults = {}
    for k in options:
        defaults[k] = options[k]['default']
    if sys.version_info < (3,0):
        #Python 2.7
        keys = defaults.keys()
        for i in range(0, len(defaults)):
            config.set(SEC_GENERAL, keys[i], defaults.get(keys[i]))
    else:
        #Python 3
        config[SEC_GENERAL] = defaults
    if not os.path.exists(CONFIG_FILE):
        initialize_configfile()
    else:
        try:
            config.read(CONFIG_FILE)
        except configparser.MissingSectionHeaderError as e:
            logger.exception(e)
            msg = _("Configuration file at '{0}' is corrupted, program may not work as expected.\nIf you delete this file, configuration will be set to default".format(CONFIG_FILE))
            messagebox.showerror(_('Error'), msg)
        except configparser.Error as e:
            logger.exception(e)
            msg = _("Faild to parse config file at '{0}', program may not work as expected.".format(CONFIG_FILE))
            msg = msg.format(CONFIG_FILE)
            messagebox.showerror(_('Error'), msg)

def get_custom_widgets():
    paths = []
    for k, p in config.items(SEC_CUSTOM_WIDGETS):
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
    for k, f in config.items(SEC_RECENT_FILES):
        rf.append(f)
    return rf

def recent_files_save(file_list):
    config.remove_section(SEC_RECENT_FILES)
    config.add_section(SEC_RECENT_FILES)
    for j, p in enumerate(file_list):
        config.set(SEC_RECENT_FILES, 'f{0}'.format(j), p)
    save_configfile()

def save_window_size(geom):
    set_option('geometry', geom, save=True)

def get_window_size():
    return get_option('geometry')

# Get user configuration
load_configfile()


class PreferencesUI(object):

    def __init__(self, master, translator=None):
        self.master = master
        self.translator = translator
        self.dialog = None
        self.builder = None
        self._create_preferences_dialog()
        self._load_options()

    def _create_preferences_dialog(self):
        self.builder = builder = pygubu.Builder(self.translator)
        uifile = os.path.join(FILE_PATH, "ui/preferences_dialog.ui")
        builder.add_from_file(uifile)

        top = self.master.winfo_toplevel()
        self.dialog = dialog = builder.get_object('preferences', top)
        
        # setup theme values
        s = get_ttk_style()
        styles = s.theme_names()
        themelist = []
        for name in styles:
            themelist.append((name, name))
        themelist.sort()
        cbox = builder.get_object('cbox_ttk_theme')
        cbox.configure(values=themelist)
        
        #General
        for key in ('widget_set',):
            cbox = builder.get_object(key)
            cbox.configure(values=options[key]['values'])
        
        #Custom widgets
        self.cwtv = builder.get_object('cwtv')
        self.path_remove = builder.get_object('path_remove')
        builder.connect_callbacks(self)
        
        # hide options
        fhide = builder.get_object('fhidden')
        fhide.pack_forget()
        
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
            config.set(SEC_CUSTOM_WIDGETS, 'w{0}'.format(j), p)
        save_configfile()
        self.master.event_generate('<<PygubuDesignerPreferencesSaved>>')

    def _configure_path_remove(self):
        if len(self.cwtv.get_children()):
            self.path_remove.configure(state='normal')
        else:
            self.path_remove.configure(state='disabled')
        
    def on_dialog_close(self, event=None):
        self._save_options()
        self.dialog.close()

    def on_pathremove_clicked(self):
        items = self.cwtv.selection()
        self.cwtv.delete(*items)
        self._configure_path_remove()

    def on_pathadd_clicked(self):
        options = {
            'defaultextension': '.py',
            'filetypes': ((_('Python module'), '*.py'), (_('All'), '*.*'))}
        fname = filedialog.askopenfilename(**options)
        if fname:
            self.cwtv.insert('', tk.END, text=fname)
            self._configure_path_remove()
        
