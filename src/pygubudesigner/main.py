# This file is part of pygubu.

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
#
# For further info, check  http://pygubu.web.here

import argparse
import importlib
import logging
import pkgutil
import platform
import sys
import tkinter as tk
import webbrowser
import traceback
from pathlib import Path
from tkinter import filedialog, messagebox

import pygubu
from pygubu import builder
from pygubu.component.plugin_manager import PluginManager
from pygubu.stockimage import StockImage, StockImageException

import pygubudesigner
import pygubudesigner.actions as actions
import pygubudesigner.designerstyles as designerstyles

from pygubudesigner import preferences as pref
from pygubudesigner.services.project import Project
from pygubudesigner.services.designersettings import DesignerSettings
from pygubudesigner.services.projectsettings import ProjectSettings
from pygubudesigner.services.aboutdialog import AboutDialog
from pygubudesigner.codegen import ScriptGenerator
from pygubudesigner.dialogs import AskSaveChangesDialog, ask_save_changes
from pygubudesigner.widgets.componentpalette import ComponentPalette
from pygubudesigner.widgets.toolbarframe import ToolbarFrame

from .i18n import translator
from .logpanel import LogPanelManager
from .preview import PreviewHelper
from .properties import load_custom_properties
from .rfilemanager import RecentFilesManager
from .uitreeeditor import WidgetsTreeEditor
from .util import menu_iter_children, virtual_event, enable_dpi
from .util.keyboard import Key, key_bind
from .util.screens import is_visible_in_screens, parse_geometry
from .services.stylehandler import StyleHandler
from .services.messagebox import show_error
from .services.theming import get_ttk_style


# Initialize logger
logger = logging.getLogger(__name__)


# translator function
_ = translator


def init_pygubu_widgets():

    # Initialize all builders from plugins
    all_modules = []
    for plugin in PluginManager.builder_plugins():
        all_modules.extend(plugin.get_all_modules())
    for _module in all_modules:
        try:
            importlib.import_module(_module)
        except (ModuleNotFoundError, ImportError) as e:
            logger.exception(e)
            msg = _(f"Failed to load widget module: '{_module}'")
            det = traceback.format_exc()
            show_error(None, _("Error"), msg, det)

    # Initialize designer plugins
    PluginManager.load_designer_plugins()

    # Register custom properties
    load_custom_properties()


# Initialize images
DATA_DIR = Path(__file__).parent / "data"

imgformat = "images-gif"
if tk.TkVersion >= 8.6:
    imgformat = "images-png"

IMAGES_DIR = DATA_DIR / "images"
IMAGE_PATHS = [  # (dir, tag)
    (IMAGES_DIR, ""),
    (IMAGES_DIR / imgformat, ""),
    (IMAGES_DIR / imgformat / "widgets" / "22x22", "22x22-"),
    (IMAGES_DIR / imgformat / "widgets" / "16x16", "16x16-"),
    (IMAGES_DIR / imgformat / "widgets" / "fontentry", ""),
    (IMAGES_DIR / "tabler", ""),
]
for dir_, prefix in IMAGE_PATHS:
    StockImage.register_all_from_dir(dir_, prefix)


class StatusBarHandler(logging.Handler):
    def __init__(self, app, level=logging.NOTSET):
        super().__init__(level)
        self.app = app
        formatter = logging.Formatter(
            "%(asctime)s %(levelname)s:%(message)s", datefmt="%H:%M:%S"
        )
        self.setFormatter(formatter)

    def emit(self, record):
        try:
            msg = self.format(record)
            self.app.log_message(msg, record.levelno)
        except (KeyboardInterrupt, SystemExit):
            raise
        except BaseException:
            self.handleError(record)


class PygubuDesigner:
    """Main gui class"""

    def __init__(self):
        """Creates all gui widgets"""

        self.translator = translator
        self.preview = None
        self.about_dialog = None
        self.preferences = None
        self.project_settings = None
        self.builder = pygubu.Builder(
            translator, on_first_object=designerstyles.on_first_window
        )
        self.current_project = None
        self.is_changed = False
        self.current_title = "new"
        self.mbox_title = _("Pygubu Designer")

        self.builder.add_from_file(str(DATA_DIR / "ui" / "pygubu-ui.ui"))
        self.builder.add_resource_path(str(DATA_DIR / "images"))

        in_macos = sys.platform == "darwin"

        # Enable DPI aware
        enable_dpi()

        # build main ui
        self.mainwindow = self.builder.get_object("mainwindow")
        self.main_menu = self.builder.get_object("mainmenu", self.mainwindow)
        self.context_menu = self.builder.get_object(
            "context_menu", self.mainwindow
        )

        # Initialize duplicate menu state
        self.duplicate_menu_state = "normal"

        if in_macos:
            cmd = "tk::mac::ShowPreferences"
            self.mainwindow.createcommand(cmd, self._edit_preferences)
            # cmd = 'tk::mac::ShowHelp'
            # self.mainwindow.createcommand(cmd, self.on_help_item_clicked)
            cmd = "tk::mac::Quit"
            self.mainwindow.createcommand(cmd, self.quit)
            # In mac add apple menu
            m = tk.Menu(self.main_menu, name="apple")
            m.add_command(
                label=_("Quit …"), accelerator="Cmd-Q", command=self.quit
            )
            self.main_menu.insert_cascade(0, menu=m)

        # Set top menu
        self.mainwindow.configure(menu=self.main_menu)

        # Recen Files management
        rfmenu = self.builder.get_object("file_recent_menu")
        self.rfiles_manager = RecentFilesManager(rfmenu, self.do_file_open)
        self.mainwindow.after_idle(self.rfiles_manager.load)

        # widget tree
        self.treeview = self.builder.get_object("project_tree")
        self.bindings_frame = self.builder.get_object("bindingsframe")
        self.bindings_tree = self.builder.get_object("bindingstree")

        # Preview
        self.preview_canvas = self.builder.get_object("preview_canvas")
        self.previewer = PreviewHelper(
            self.preview_canvas,
            self.show_context_menu,
            self._should_center_preview_window,
        )

        # Bottom Panel
        self.setup_bottom_panel()

        self.builder.connect_callbacks(self)

        # Customize OpenFiledialog window
        if sys.platform == "linux":
            file_dialog_hack = """
# Show button and hide hidden files
catch {tk_getOpenFile -badoption}
set ::tk::dialog::file::showHiddenBtn 1
set ::tk::dialog::file::showHiddenVar 0

# Make dialog window bigger
rename ::tk::dialog::file::Create ::tk::dialog::file::_CreateOriginal
proc ::tk::dialog::file::Create {w class} {
    eval ::tk::dialog::file::_CreateOriginal $w $class
    wm geometry $w 680x350
}"""
            self.mainwindow.tk.eval(file_dialog_hack)

        #
        # Setup dynamic theme submenu
        #
        self._setup_theme_menu()

        # App config
        top = self.mainwindow
        try:
            top.wm_iconname("pygubu")
            top.tk.call("wm", "iconphoto", ".", StockImage.get("pygubu"))
        except StockImageException:
            pass

        # Load all widgets before creating the component pallete
        init_pygubu_widgets()

        # _pallete
        # self.fpalette = self.builder.get_object("fpalette")
        # self.create_component_palette(self.fpalette)

        # Tree palette
        self.tree_palette = self.builder.get_object("tree_palette")
        self.tree_palette.on_add_widget = self.on_add_widget_event
        self.tree_palette.build_tree()

        # tree editor
        self.tree_editor = WidgetsTreeEditor(self)
        # code generator
        self.script_generator: ScriptGenerator = ScriptGenerator(self)
        # App bindings
        self._setup_app_bindings()

        # setup app preferences
        self.setup_app_preferences()

        # project settings
        self.project_settings = ProjectSettings(self.mainwindow, translator)
        self.project_settings.on_settings_changed = (
            self._on_project_settings_changed
        )
        # load maindock state
        self.load_dockframe_layout()

    def run(self):
        self.mainwindow.protocol("WM_DELETE_WINDOW", self.__on_window_close)
        self.mainwindow.mainloop()

    def __on_window_close(self):
        """Manage WM_DELETE_WINDOW protocol."""
        if self.on_close_execute():
            self.previewer.close_toplevel_previews()
            self.mainwindow.withdraw()
            self.mainwindow.destroy()

    def quit(self):
        """Exit the app if it is ready for quit."""
        self.__on_window_close()

    def set_title(self, newtitle):
        self.current_title = newtitle
        default_title = "Pygubu Designer - {0}"
        title = default_title.format(newtitle)
        self.mainwindow.wm_title(title)

    def _setup_app_bindings(self):
        in_macos = sys.platform == "darwin"
        #
        # Context menu binding for object treeview
        #
        if in_macos:
            # tree_editor context menu binding (2nd mouse button for macos)
            self.tree_editor.treeview.bind(
                "<2>", self.on_right_click_object_tree
            )
        else:
            # tree_editor context menu binding (3rd mouse button for linux and
            # windows)
            self.tree_editor.treeview.bind(
                "<3>", self.on_right_click_object_tree
            )

        #
        # Application Keyboard bindings
        #
        CONTROL_KP_SEQUENCE = "<Control-KeyPress>"
        ALT_KP_SEQUENCE = "<Alt-KeyPress>"
        if in_macos:
            CONTROL_KP_SEQUENCE = "<Command-KeyPress>"
            ALT_KP_SEQUENCE = "<Control-KeyPress>"
            # Fix menu accelerators
            for m, itemtype, index in menu_iter_children(self.main_menu):
                if itemtype != "separator":
                    accel = m.entrycget(index, "accelerator")
                    accel = accel.replace("Ctrl+", "Cmd-")
                    accel = accel.replace("Alt+", "Ctrl+")
                    m.entryconfigure(index, accelerator=accel)

        master = self.mainwindow
        master.bind_all(
            CONTROL_KP_SEQUENCE,
            key_bind(Key.N, virtual_event(actions.FILE_NEW)),
        )
        master.bind_all(
            CONTROL_KP_SEQUENCE,
            key_bind(Key.O, virtual_event(actions.FILE_OPEN)),
            add=True,
        )
        master.bind_all(
            CONTROL_KP_SEQUENCE,
            key_bind(Key.S, virtual_event(actions.FILE_SAVE)),
            add=True,
        )
        master.bind_all(
            CONTROL_KP_SEQUENCE,
            key_bind(Key.Q, virtual_event(actions.FILE_QUIT)),
            add=True,
        )
        master.bind_all(
            "<F5>", virtual_event(actions.TREE_ITEM_PREVIEW_TOPLEVEL)
        )
        master.bind_all(
            "<F6>", virtual_event(actions.PREVIEW_TOPLEVEL_CLOSE_ALL)
        )

        # Tree Editing Keyboard events
        for widget in (self.treeview, self.preview_canvas):
            widget.bind(
                CONTROL_KP_SEQUENCE,
                key_bind(Key.I, virtual_event(actions.TREE_ITEM_MOVE_UP)),
            )
            widget.bind(
                CONTROL_KP_SEQUENCE,
                key_bind(Key.K, virtual_event(actions.TREE_ITEM_MOVE_DOWN)),
                add=True,
            )
            widget.bind(
                CONTROL_KP_SEQUENCE,
                key_bind(Key.C, lambda e: self.tree_editor.copy_to_clipboard()),
                add=True,
            )
            widget.bind(
                CONTROL_KP_SEQUENCE,
                key_bind(
                    Key.V, lambda e: self.tree_editor.paste_from_clipboard()
                ),
                add=True,
            )
            widget.bind(
                CONTROL_KP_SEQUENCE,
                key_bind(Key.D, virtual_event(actions.TREE_ITEM_DUPLICATE)),
                add=True,
            )
            widget.bind(
                CONTROL_KP_SEQUENCE,
                key_bind(Key.X, lambda e: self.tree_editor.cut_to_clipboard()),
                add=True,
            )
            widget.bind(
                "<KeyPress>",
                key_bind(Key.I, virtual_event(actions.TREE_NAV_UP)),
            )
            widget.bind(
                "<KeyPress>",
                key_bind(Key.K, virtual_event(actions.TREE_NAV_DOWN)),
                add=True,
            )
            widget.bind(
                "<KeyPress-Delete>", virtual_event(actions.TREE_ITEM_DELETE)
            )
            widget.bind(
                "<KeyPress-BackSpace>", virtual_event(actions.TREE_ITEM_DELETE)
            )

            # grid move bindings
            widget.bind(
                ALT_KP_SEQUENCE,
                key_bind(Key.I, virtual_event(actions.TREE_ITEM_GRID_UP)),
            )
            widget.bind(
                ALT_KP_SEQUENCE,
                key_bind(Key.K, virtual_event(actions.TREE_ITEM_GRID_DOWN)),
                add=True,
            )
            widget.bind(
                ALT_KP_SEQUENCE,
                key_bind(Key.J, virtual_event(actions.TREE_ITEM_GRID_LEFT)),
                add=True,
            )
            widget.bind(
                ALT_KP_SEQUENCE,
                key_bind(Key.L, virtual_event(actions.TREE_ITEM_GRID_RIGHT)),
                add=True,
            )

        # Actions Bindings
        w = self.mainwindow
        w.bind(actions.FILE_NEW, self.on_file_new)
        w.bind(actions.FILE_OPEN, lambda e: self.do_file_open())
        w.bind(actions.FILE_SAVE, self.on_file_save)
        w.bind(actions.FILE_SAVEAS, lambda e: self.do_save_as())
        w.bind(actions.FILE_QUIT, lambda e: self.quit())
        w.bind(actions.FILE_RECENT_CLEAR, lambda e: self.rfiles_manager.clear())
        # On preferences save binding
        w.bind("<<PygubuDesignerPreferencesSaved>>", self.on_preferences_saved)

    def _setup_theme_menu(self):
        menu = self.builder.get_object("preview_themes_submenu")
        s = get_ttk_style()
        styles = sorted(s.theme_names())
        self.__theme_var = var = tk.StringVar()
        theme = pref.get_option("ttk_theme")
        var.set(theme)

        for idx, name in enumerate(styles):

            def handler(theme=name):
                self._change_ttk_theme(theme)

            col_break = idx % 20 == 0
            menu.add_radiobutton(
                label=name,
                value=name,
                variable=self.__theme_var,
                command=handler,
                columnbreak=col_break,
            )

    def _should_center_preview_window(self) -> bool:
        """
        Check whether the option has been enabled to center
        the preview window or not.
        :return: bool (True if we should center the preview window, otherwise False)
        """
        self.tree_editor.center_preview = pref.get_option("center_preview")
        if self.tree_editor.center_preview == "yes":
            return True
        else:
            return False

    def create_treelist(self):
        root_tagset = {"tk", "ttk"}

        # create unique tag set
        tagset = set()
        for c in builder.CLASS_MAP.keys():
            wc = builder.CLASS_MAP[c]
            tagset.update(wc.tags)
        tagset.difference_update(root_tagset)

        treelist = []
        for c in builder.CLASS_MAP.keys():
            wc = builder.CLASS_MAP[c]
            ctags = set(wc.tags)
            roots = root_tagset & ctags
            sections = tagset & ctags
            for r in roots:
                for s in sections:
                    key = f"{r}>{s}"
                    treelist.append((key, wc))

        # sort tags by group and label
        def by_label(t):
            return f"{t[0]}{t[1].group}{t[1].label}"

        treelist.sort(key=by_label)
        return treelist

    def create_component_palette(self, fpalette):
        # Default widget image:
        default_image = ""
        try:
            default_image = StockImage.get("22x22-tk.default")
        except StockImageException:
            pass

        treelist = self.create_treelist()
        self._palette = ComponentPalette(
            fpalette, notebook=(pref.get_option("single_section") == "no")
        )

        # Start building widget tree selector
        roots = {}
        sections = {}
        for key, wc in treelist:
            root, section = key.split(">")
            if section not in sections:
                roots[root] = self._palette.add_tab(section, section)
                sections[section] = 1

            # insert widget
            w_image = default_image
            try:
                w_image = StockImage.get(f"22x22-{wc.classname}")
            except StockImageException:
                pass

            # define callback for button
            def create_cb(cname):
                return lambda: self.on_add_widget_event(cname)

            wlabel = wc.label
            if wlabel.startswith("Menuitem."):
                wlabel = wlabel.replace("Menuitem.", "")
            callback = create_cb(wc.classname)
            self._palette.add_button(
                section, root, wlabel, wc.classname, w_image, callback
            )
        default_group = pref.get_option("widget_set")
        self._palette.show_group(default_group)

    def on_add_widget_event(self, classname):
        """Adds a widget to the widget tree."""

        self.tree_editor.add_widget(classname)
        self.tree_editor.treeview.focus_set()

    def setup_app_preferences(self):
        # Restore windows position and size
        geom = pref.get_window_size()
        self.mainwindow.geometry(geom)
        self.mainwindow.after_idle(self._check_window_visibility)

    def _check_window_visibility(self):
        geom = pref.get_window_size()
        window_visible = is_visible_in_screens(geom)
        logger.debug(_("Checking main window visibility."))
        if not window_visible:
            msg = _("Main window is not visible in current monitors.")
            logger.debug(msg)
            w, h, uu, uu = parse_geometry(geom)
            geom = f"{w}x{h}+0+0"
            msg = _("Main window position fixed.")
            logger.debug(msg)
            self.mainwindow.withdraw()
            self.mainwindow.update()
            self.mainwindow.geometry(geom)
            self.mainwindow.deiconify()

    def _change_ttk_theme(self, theme):
        try:
            designerstyles.apply_theme(self.mainwindow, theme)
            event_name = "<<PygubuDesignerTtkThemeChanged>>"
            self.mainwindow.event_generate(event_name)
        except tk.TclError:
            logger.exception("Invalid ttk theme.")

    def on_preferences_saved(self, event=None):
        # Setup ttk theme if changed
        theme = pref.get_option("ttk_theme")
        self._change_ttk_theme(theme)

        # Get the preferred default layout manager, in case it has changed.
        self.tree_editor.default_layout_manager = pref.get_option(
            "default_layout_manager"
        )

    def ask_save_changes(self, message, detail=None, title=None):
        do_continue = False
        if title is None:
            title = _("Save Changes")
        if detail is None:
            detail = _(
                "If you don't save the document, all the changes will be lost."
            )
        choice = ask_save_changes(self.mainwindow, title, message, detail)
        if choice == AskSaveChangesDialog.SAVE:
            do_continue = self.on_file_save()
        elif choice == AskSaveChangesDialog.CANCEL:
            do_continue = False
        elif choice == AskSaveChangesDialog.DONTSAVE:
            do_continue = True
        return do_continue

    def on_close_execute(self):
        quit = True
        if self.is_changed:
            msg = _("Do you want to save the changes before closing?")
            quit = self.ask_save_changes(msg)
        if quit:
            # prevent tk image errors on python2 ?
            StockImage.clear_cache()

            # Save window size and position
            geom = self.mainwindow.geometry()
            pref.save_window_size(geom)
        return quit

    def do_save(self, fname):
        saved = False
        try:
            self.save_file(fname)
            self.set_changed(False)
            logger.info(_("Project saved to %s"), fname)
            saved = True
            if self.generate_code_on_save():
                self._project_code_generate()
        except Exception as e:
            msg = str(e)
            det = traceback.format_exc()
            show_error(
                self.mainwindow,
                _("Error"),
                msg,
                det,
            )
        return saved

    def do_save_as(self):
        saved = False
        options = {
            "defaultextension": ".ui",
            "filetypes": ((_("pygubu ui"), "*.ui"), (_("All"), "*.*")),
        }
        fname = filedialog.asksaveasfilename(**options)
        if fname:
            saved = self.do_save(fname)
        return saved

    def save_file(self, filename):
        project = self.current_project
        if project is None:
            project = Project()
        project.uidefinition = self.tree_editor.tree_to_uidef()
        project.save(filename)
        self.current_project = project
        title = self.project_name()
        self.set_title(title)
        self.rfiles_manager.addfile(str(filename))

    def set_changed(self, newvalue=True):
        if newvalue and not self.is_changed:
            self.set_title(f"{self.current_title} (*)")
        self.is_changed = newvalue

    def load_file(self, filename):
        """Load xml into treeview"""

        try:
            fpath = Path(filename).resolve()
            project = Project.load(fpath)
            self.tree_editor.load_file(project)
            self.current_project = project
            title = self.project_name()
            self.set_title(title)
            self.set_changed(False)
            self.rfiles_manager.addfile(str(fpath))
            self.reload_component_palette()
        except Exception as e:
            msg = str(e)
            det = traceback.format_exc()
            show_error(self.mainwindow, _("Error"), msg, det)

    def do_file_open(self, filename=None):
        openfile = True
        if self.is_changed:
            msg = _("Do you want to save the changes before opening?")
            openfile = self.ask_save_changes(msg)
        if openfile:
            if filename is None:
                options = {
                    "defaultextension": ".ui",
                    "filetypes": (
                        (_("pygubu ui"), "*.ui"),
                        (_("All"), "*.*"),
                    ),
                }
                filename = filedialog.askopenfilename(**options)
            if filename:
                self.load_file(filename)

    def on_file_new(self, event=None):
        new = True
        if self.is_changed:
            msg = _("Do you want to save the changes before creating?")
            new = self.ask_save_changes(msg)
        if new:
            self.previewer.remove_all()
            self.tree_editor.remove_all()
            self.current_project = None
            self.set_changed(False)
            self.set_title(self.project_name())
            StyleHandler.clear_definition_file()

    def on_file_save(self, event=None):
        file_saved = False
        if self.current_project:
            if self.is_changed:
                file_saved = self.do_save(self.current_project.fpath)
        else:
            file_saved = self.do_save_as()
        return file_saved

    # File Menu
    def on_file_menuitem_clicked(self, itemid):
        action = f"<<ACTION_{itemid}>>"
        self.mainwindow.event_generate(action)

    # Edit menu
    def on_edit_menuitem_clicked(self, itemid):
        if itemid == "edit_preferences":
            self._edit_preferences()

        elif itemid == "reset_layout":
            self._reset_layout()

        else:
            action = f"<<ACTION_{itemid}>>"
            self.mainwindow.event_generate(action)

    # Project menu
    def on_project_menuitem_clicked(self, itemid):
        if itemid == "project_settings":
            self._edit_project_settings()
        if itemid == "project_codegen":
            self._project_code_generate()

    # preview menu
    def on_previewmenu_action(self, itemid):
        action = f"<<ACTION_{itemid}>>"
        self.mainwindow.event_generate(action)

    # Help menu
    def on_help_menuitem_clicked(self, itemid):
        if itemid == "help_online":
            url = "https://github.com/alejandroautalan/pygubu-designer/wiki"
            webbrowser.open_new_tab(url)
        elif itemid == "help_about":
            self.show_about_dialog()

    def evaluate_menu_states(self):
        """
        Check whether some menus (such as 'Duplicate' need to be enabled or disabled.

        The state of the menus is dependant on whether they can be used at the current time or not.
        """

        menu_duplicate_context = self.builder.get_object("menu_duplicate")
        menu_duplicate_edit = self.builder.get_object("TREE_ITEM_DUPLICATE")

        # Should we enable the 'Duplicate' menu?
        self.duplicate_menu_state = (
            "disabled"
            if self.tree_editor.selection_different_parents()
            else "normal"
        )
        menu_duplicate_context.entryconfig(7, state=self.duplicate_menu_state)
        menu_duplicate_edit.entryconfig(3, state=self.duplicate_menu_state)

    def show_context_menu(self, event):
        """
        Show the context menu.
        """
        self.context_menu.tk_popup(event.x_root, event.y_root)

    # Right-click menu (on object tree)
    def on_right_click_object_tree(self, event):
        self.show_context_menu(event)

    def on_context_menu_update_preview(self):
        """
        Request a full redraw of preview
        """
        self.tree_editor.on_user_request_redraw()

    def on_context_menu_go_to_parent_clicked(self):
        """
        Go to parent was clicked from the context menu.

        Select the parent of the currently selected widget.
        """
        current_selected_item = self.tree_editor.current_edit
        if current_selected_item and self.treeview.exists(
            current_selected_item
        ):
            parent_iid = self.treeview.parent(current_selected_item)

            if parent_iid:
                self.treeview.selection_set(parent_iid)
                self.treeview.see(parent_iid)

    def on_context_menu_cut_clicked(self):
        """
        Cut was clicked from the context menu.
        """
        action = actions.TREE_ITEM_CUT
        self.mainwindow.event_generate(action)

    def on_context_menu_copy_clicked(self):
        """
        Copy was clicked from the context menu.
        """
        self.mainwindow.event_generate(actions.TREE_ITEM_COPY)

    def on_context_menu_paste_clicked(self):
        """
        Paste was clicked from the context menu.
        """
        self.mainwindow.event_generate(actions.TREE_ITEM_PASTE)

    def on_context_menu_delete_clicked(self):
        """
        Delete was clicked from the context menu.
        """
        self.mainwindow.event_generate(actions.TREE_ITEM_DELETE)

    def on_context_menu_duplicate_clicked(self):
        """
        Duplicate was clicked from the context menu.
        """
        self.mainwindow.event_generate(actions.TREE_ITEM_DUPLICATE)

    def show_about_dialog(self):
        if self.about_dialog is None:
            self.about_dialog = AboutDialog(self.mainwindow, translator)
        self.about_dialog.run()

    def _edit_preferences(self):
        if self.preferences is None:
            # self.preferences = pref.PreferencesUI(self.mainwindow, translator)
            self.preferences = DesignerSettings(self.mainwindow, translator)
        self.preferences.run()

    def _reset_layout(self):
        """
        Reset the docked frames back to their default positions.
        """
        self.on_dockframe_changed(reset_layout=True)
        msg = _("Restart Pygubu Designer\nfor changes to take effect.")
        messagebox.showinfo(self.mbox_title, msg, parent=self.mainwindow)

    def _require_project_open(self):
        if self.current_project is None:
            msg = _("Open a project first.")
            messagebox.showinfo(self.mbox_title, msg, parent=self.mainwindow)
        return self.current_project is not None

    def _edit_project_settings(self):
        if not self._require_project_open():
            return
        options = self.tree_editor.get_options_for_project_settings()
        self.project_settings.setup(options)
        self.project_settings.edit(self.current_project)
        self.project_settings.run()

    def _on_project_settings_changed(self, new_settings: dict):
        self.current_project.set_full_settings(new_settings)
        self.set_changed()
        self.reload_component_palette()

    def _project_code_generate(self):
        if not self._require_project_open():
            return
        options = self.tree_editor.get_options_for_project_settings()
        self.project_settings.setup(options)
        self.project_settings.edit(self.current_project)
        valid = self.project_settings.validate_for_codegen()
        if valid:
            self.script_generator.generate_code()
            msg = _("Project code generated.")
            logger.info(msg)
        else:
            self.project_settings.run()

    def generate_code_on_save(self):
        return (
            False
            if self.current_project is None
            else self.current_project.generate_code_onsave
        )

    def project_name(self):
        name = None
        if self.current_project is None:
            name = _("newproject")
        else:
            name = self.current_project.fpath.name
        return name

    def setup_bottom_panel(self):
        self.log_panel = LogPanelManager(self)
        self.setup_logger_handler()

    def on_bpanel_button_clicked(self):
        self.log_panel.on_bpanel_button_clicked()

    def setup_logger_handler(self):
        # Status bar
        handler = StatusBarHandler(self)
        # handler.setLevel(logging.INFO)
        # add handler to the root logger:
        logging.getLogger().addHandler(handler)

    def log_message(self, msg, level):
        self.log_panel.log_message(msg, level)

    def reload_component_palette(self):
        """Reload palette with project custom widgets."""
        project = self.current_project
        prefixes = [Path(cw).stem for cw in project.custom_widgets]
        current_prefixes = self.tree_palette.project_custom_widget_prefixes

        prefixes.sort()
        current_prefixes.sort()
        if prefixes != current_prefixes:
            try:
                project.load_custom_widgets()
                self.tree_palette.project_custom_widget_prefixes = prefixes
                self.tree_palette.build_tree()
            except Exception as e:
                msg = str(e)
                det = traceback.format_exc()
                show_error(
                    self.mainwindow,
                    _("Error"),
                    msg,
                    det,
                )

    def on_dockframe_changed(self, event=None, reset_layout=False):
        """
        Save current layout of maindock widget.

        Arguments:

        - event

        - reset_layout: used for resetting the docked frames
        back to their default locations/positions.
        """

        # Should we reset the layout back to the defaults?
        if reset_layout:
            dock_layout = None
        else:
            dock = self.builder.get_object("maindock")
            dock_layout = dock.save_layout()

        pref.save_maindock_layout(dock_layout)

    def load_dockframe_layout(self):
        """Load layout for maindock widget."""
        layout = pref.get_maindock_layout()
        try:
            dock = self.builder.get_object("maindock")
            dock.load_layout(layout)
        except Exception:
            logger.debug("Error loading maindock layout")


def start_pygubu():
    print(f"python: {platform.python_version()} on {sys.platform}")
    print(f"tk: {tk.TkVersion}")
    print(f"pygubu: {pygubu.__version__}")
    print(f"pygubu-designer: {pygubudesigner.__version__}")

    # Setup logging level
    parser = argparse.ArgumentParser()
    parser.add_argument("filename", nargs="?")
    parser.add_argument("--loglevel")
    args = parser.parse_args()

    loglevel = str(args.loglevel).upper()
    loglevel = getattr(logging, loglevel, logging.WARNING)
    logging.getLogger("").setLevel(loglevel)

    #
    # Dependency check
    #
    help = "Hint, If your are using Debian, install package python3-appdirs."
    check_dependency("appdirs", "1.3", help)

    app = PygubuDesigner()

    filename = args.filename
    if filename is not None:
        app.load_file(filename)

    app.run()


def check_dependency(modulename, version, help_msg=None):
    try:
        module = importlib.import_module(modulename)
        for attr in ("version", "__version__", "ver", "PYQT_VERSION_STR"):
            v = getattr(module, attr, None)
            if v is not None:
                break
        logger.info(f"Module {modulename} imported ok, version {v}")
    except ImportError:
        logger.error(
            f"I can't import module {modulename!r}. You need to have installed "
            + f"{modulename!r} version {version} or higher. {help_msg or ''}"
        )
        sys.exit(-1)


if __name__ == "__main__":
    start_pygubu()
