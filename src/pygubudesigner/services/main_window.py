#!/usr/bin/python3
import sys
import platform
import os
import logging
import traceback
import webbrowser

import tkinter as tk
import tkinter.ttk as ttk

import pygubudesigner.actions as actions
import pygubudesigner.designerstyles as designerstyles

from pathlib import Path
from tkinter import filedialog, messagebox
from pygubu import builder
from pygubu.stockimage import StockImage, StockImageException

from pygubudesigner.preferences import preferences
from pygubudesigner.services.project import Project
from pygubudesigner.services.designersettings import DesignerSettings
from pygubudesigner.services.projectsettings import ProjectSettings
from pygubudesigner.services.aboutdialog import AboutDialog
from pygubudesigner.codegen import ScriptGenerator
from pygubudesigner.widgets.toolbarframe import ToolbarFrame

from pygubudesigner.i18n import translator
from pygubudesigner.logpanel import LogPanelManager
from pygubudesigner.preview import PreviewHelper
from pygubudesigner.rfilemanager import RecentFilesManager
from pygubudesigner.uitreeeditor import WidgetsTreeEditor
from pygubudesigner.util import menu_iter_children, virtual_event, enable_dpi
from pygubudesigner.util.keyboard import Key, key_bind
from pygubudesigner.util.screens import is_visible_in_screens, parse_geometry
from pygubudesigner.util.tkhacks import filedialog_hack
from pygubudesigner.util.loghandler import StatusBarHandler
from pygubudesigner.services.stylehandler import StyleHandler
from pygubudesigner.services.messagebox import show_error
from pygubudesigner.services.theming import get_ttk_style
from pygubudesigner.services.context_menu import create_context_menu
from pygubudesigner.services.main_menu import create_main_menu
from pygubudesigner.services.fileactions import FileActionsManager
from pygubudesigner.services.image_loader import image_loader, iconset_loader

import pygubudesigner.services.main_windowui as baseui


# Initialize logger
logger = logging.getLogger(__name__)


# translator function
_ = translator


class MainWindow(baseui.MainWindowUI):
    def __init__(self, master=None):
        super().__init__(
            master,
            translator=translator,
            image_loader=iconset_loader,
            on_first_object_cb=designerstyles.on_first_window,
        )

        self.translator = translator
        self.preview = None
        self.about_dialog = None
        self.preferences = None
        self.project_settings = None
        # self.builder.image_cache.auto_scaling = True  FIXME
        self.current_project = None
        self.current_title = "new"
        self.mbox_title = _("Pygubu Designer")

        in_macos = sys.platform == "darwin"

        # Enable DPI aware
        enable_dpi()

        # build main ui
        self.main_menu = create_main_menu(
            master=self.mainwindow,
            translator=translator,
            callbacks_bag=self,
            image_loader=iconset_loader,
        )
        self.context_menu = create_context_menu(
            master=self.mainwindow, translator=translator, callbacks_bag=self
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

        # widget tree
        self.treeview = self.project_tree_frame.tvdata

        # Preview
        self.previewer = PreviewHelper(
            self.preview_canvas,
            self.show_context_menu,
            lambda: preferences.center_preview,
        )

        # Bottom Panel
        self.setup_bottom_panel()

        # Recen Files management
        # Setup menu after connect callbacks call above.
        rfmenu = self.mainwindow.nametowidget(".mmain.mfile.mrecent")
        self.rfiles_manager = RecentFilesManager(
            rfmenu, self.on_recentfile_clicked
        )

        # Customize OpenFiledialog window
        filedialog_hack(self.mainwindow)

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

        # Tree palette
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

        self.mainwindow.protocol("WM_DELETE_WINDOW", self.__on_window_close)

        # Start user styles monitoring.
        # Used for refreshing/re-populating the styles combobox.
        # Used when the style definition gets updated (simulates clicking on the treeview item again.)
        StyleHandler.start_monitoring(self.mainwindow)

        # start new Project
        self.mainwindow.after(
            100, lambda: self.mainwindow.event_generate(actions.FILE_NEW)
        )

    def __on_window_close(self):
        """Manage WM_DELETE_WINDOW protocol."""
        if self.on_close_execute():
            self.previewer.close_toplevel_previews()
            self.mainwindow.withdraw()
            self.mainwindow.destroy()

    def quit(self):
        """Exit the app if it is ready for quit."""
        self.__on_window_close()

    def restart(self):
        if self.on_close_execute():
            self.previewer.close_toplevel_previews()
            self.mainwindow.withdraw()
            self.mainwindow.update()
            self.mainwindow.quit()

            python = sys.executable
            args = sys.argv

            if platform.system() == "Windows":
                args = ["-m", "pygubudesigner"]

            logger.debug("Restarting...")
            logger.debug("Python exe: %s", python)

            # Do restart
            logging.shutdown()
            os.execl(python, python, *args)

    def load_file(self, file_path):
        self.mainwindow.after(
            200, lambda: self.fileactions.action_open(file_path)
        )

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

        # New fileactions module
        self.fileactions = FileActionsManager(
            self.mainwindow,
            ".ui",
            ((_("pygubu ui"), "*.ui"), (_("All"), "*.*")),
        )
        MSGID = self.fileactions.MSGID
        self.fileactions.user_file_new = self.on_file_new
        self.fileactions.user_file_open = self.on_file_open
        self.fileactions.user_file_save = self.on_file_save
        self.fileactions.messages = {
            MSGID.SAVECHANGE_MESSAGE: _("Save current changes?"),
            MSGID.SAVECHANGE_DETAIL: _(
                "If you don't save the document, all the changes will be lost."
            ),
            MSGID.SAVECHANGE_TITLE: _("Save Changes"),
        }
        # _("Do you want to save the changes before closing?")

        # Actions Bindings
        w = self.mainwindow
        w.bind(actions.FILE_NEW, lambda e: self.fileactions.action_new())
        w.bind(actions.FILE_OPEN, lambda e: self.fileactions.action_open())
        w.bind(actions.FILE_SAVE, lambda e: self.fileactions.action_save())
        w.bind(actions.FILE_SAVEAS, lambda e: self.fileactions.action_saveas())
        w.bind(actions.FILE_QUIT, lambda e: self.quit())
        w.bind(actions.FILE_RESTART, lambda e: self.restart())
        w.bind(actions.FILE_RECENT_CLEAR, lambda e: self.rfiles_manager.clear())
        # On preferences save binding
        w.bind("<<PygubuDesignerPreferencesSaved>>", self.on_preferences_saved)

    def _setup_theme_menu(self):
        themes_list_menu = self.mainwindow.nametowidget(
            ".mmain.mpreview.mthemes_list"
        )
        s = get_ttk_style()
        styles = sorted(s.theme_names())
        self.__theme_var = var = tk.StringVar()
        theme = preferences.ttk_theme
        var.set(theme)

        for idx, name in enumerate(styles):

            def handler(theme=name):
                self._change_ttk_theme(theme)

            col_break = idx % 20 == 0
            themes_list_menu.add_radiobutton(
                label=name,
                value=name,
                variable=self.__theme_var,
                command=handler,
                columnbreak=col_break,
            )

    def on_add_widget_event(self, classname):
        """Adds a widget to the widget tree."""

        self.tree_editor.add_widget(classname)
        self.tree_editor.treeview.focus_set()

    def setup_app_preferences(self):
        # Restore windows position and size
        self.mainwindow.geometry(preferences.geometry)
        self.mainwindow.after_idle(self._check_window_visibility)

    def _check_window_visibility(self):
        geom = preferences.geometry
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
        theme = preferences.ttk_theme
        self._change_ttk_theme(theme)

        # Get the preferred default layout manager, in case it has changed.
        self.tree_editor.default_layout_manager = (
            preferences.default_layout_manager
        )

    def on_close_execute(self):
        quit = self.fileactions.action_close()
        if quit:
            # prevent tk image errors on python2 ?
            StockImage.clear_cache()

            # Save window size and position
            preferences.geometry = self.mainwindow.geometry()
        return quit

    def set_changed(self, newvalue=True):
        if newvalue and not self.fileactions.file_is_changed:
            self.set_title(f"{self.current_title} (*)")
        self.fileactions.file_is_changed = newvalue

    def on_file_new(self):
        """Implement Fileactions user_file_new."""
        self.previewer.remove_all()
        self.tree_editor.remove_all()
        self.current_project = None
        # self.set_changed(False)
        self.set_title(self.project_name())
        StyleHandler.clear_definition_file()

    def on_file_open(self, filename):
        """Implement Fileactions user_file_open."""
        try:
            fpath = Path(filename).resolve()
            project = Project.load(fpath)
            self.tree_editor.load_file(project)
            self.current_project = project
            self.set_title(self.project_name())
            self.rfiles_manager.add(fpath)
            self.reload_component_palette()
        except Exception as e:
            msg = str(e)
            det = traceback.format_exc()
            show_error(self.mainwindow, _("Error"), msg, det)

    def on_file_save(self, filepath, *, is_update=False, is_saveas=False):
        saved = False
        try:
            # save begin
            project = (
                Project()
                if self.current_project is None
                else self.current_project
            )
            project.uidefinition = self.tree_editor.tree_to_uidef()
            project.save(filepath)
            self.current_project = project
            self.set_title(self.project_name())
            logger.info(_("Project saved to %s"), filepath)
            saved = True

            if self.generate_code_on_save():
                self._project_code_generate()

            if is_saveas or not is_update:
                self.rfiles_manager.add(filepath)
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

    # File Menu
    def on_file_menuitem_clicked(self, itemid):
        action = f"<<ACTION_{itemid}>>"
        self.mainwindow.event_generate(action)

    def on_recentfile_clicked(self, fpath):
        self.fileactions.action_open(fpath)

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

        menu_edit = self.mainwindow.nametowidget(".mmain.medit")

        # Should we enable the 'Duplicate' menu?
        self.duplicate_menu_state = (
            "disabled"
            if self.tree_editor.selection_different_parents()
            else "normal"
        )
        # context menu item duplicate
        self.context_menu.entryconfig(9, state=self.duplicate_menu_state)
        # edit menu item duplicate
        menu_edit.entryconfig(3, state=self.duplicate_menu_state)

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
            self.preferences = DesignerSettings(self.mainwindow)
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
            dock_layout = self.maindock.save_layout()

        preferences.maindock_layout = dock_layout

    def load_dockframe_layout(self):
        """Load layout for maindock widget."""
        try:
            self.maindock.load_layout(preferences.maindock_layout)
        except Exception:
            logger.debug("Error loading maindock layout")


if __name__ == "__main__":
    root = tk.Tk()
    app = MainWindow(root)
    app.run()
