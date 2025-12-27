import tkinter as tk
import tkinter.filedialog
import tkinter.messagebox
import enum
from pygubudesigner.services.ask_save_changes import (
    ask_save_changes,
    AskSaveChangesDialog,
)


class MessageID(enum.IntEnum):
    SAVECHANGE_MESSAGE = enum.auto()
    SAVECHANGE_DETAIL = enum.auto()
    SAVECHANGE_TITLE = enum.auto()
    OPEN_MESSAGE = enum.auto()
    OPEN_DETAIL = enum.auto()
    OPEN_TITLE = enum.auto()


class FileActionsManager:
    MSGID = MessageID

    def __init__(self, tk_master, defaultextension=None, filetypes=None):
        self.tk_master = tk_master
        self.file_current = None
        self.file_is_changed = False
        self.user_file_new = None
        self.user_file_open = None
        self.user_file_save = None
        self.defaultextension = defaultextension
        self.filetypes = filetypes
        self.messages = {
            self.MSGID.SAVECHANGE_MESSAGE: "Save current changes?",
        }

    def action_new(self):
        new = True
        if self.file_is_changed:
            new = self.ask_save_changes(
                self.messages.get(self.MSGID.SAVECHANGE_MESSAGE, None),
                self.messages.get(self.MSGID.SAVECHANGE_DETAIL, None),
                self.messages.get(self.MSGID.SAVECHANGE_TITLE, None),
            )
        if new:
            self.file_current = None
            self.file_is_changed = False
            self.user_file_new()

    def action_open(self, file_path=None):
        openfile = True
        if self.file_is_changed:
            openfile = self.ask_save_changes(
                self.messages.get(self.MSGID.SAVECHANGE_MESSAGE, None),
                self.messages.get(self.MSGID.SAVECHANGE_DETAIL, None),
                self.messages.get(self.MSGID.SAVECHANGE_TITLE, None),
            )
        if openfile:
            if file_path is None:
                options = {
                    "defaultextension": self.defaultextension,
                    "filetypes": self.filetypes,
                    "parent": self.tk_master,
                }
                file_path = tk.filedialog.askopenfilename(**options)
            if file_path:
                self.file_current = file_path
                self.file_is_changed = False
                self.user_file_open(file_path)

    def action_close(self) -> bool:
        do_close = True
        if self.file_is_changed:
            do_close = self.ask_save_changes(
                self.messages.get(self.MSGID.SAVECHANGE_MESSAGE, None),
                self.messages.get(self.MSGID.SAVECHANGE_DETAIL, None),
                self.messages.get(self.MSGID.SAVECHANGE_TITLE, None),
            )
        if do_close:
            self.file_current = None
            self.file_is_changed = False
        return do_close

    def action_save(self) -> bool:
        file_saved = False
        if self.file_current:
            if self.file_is_changed:
                file_saved = self.do_save(self.file_current, is_update=True)
        else:
            file_saved = self.action_saveas()
        return file_saved

    def action_saveas(self) -> bool:
        saved = False
        options = {
            "defaultextension": self.defaultextension,
            "filetypes": self.filetypes,
            "parent": self.tk_master,
        }
        fname = tk.filedialog.asksaveasfilename(**options)
        if fname:
            saved = self.do_save(fname, is_saveas=True)
        return saved

    def do_save(self, file_path, *, is_update=False, is_saveas=False):
        saved = False
        try:
            saved = self.user_file_save(
                file_path, is_update=is_update, is_saveas=is_saveas
            )
            self.file_current = file_path
            self.file_is_changed = False
        except Exception as e:
            raise e
        return saved

    def ask_save_changes(self, message, detail=None, title=None) -> bool:
        do_continue = False
        choice = ask_save_changes(self.tk_master, title, message, detail)
        if choice == AskSaveChangesDialog.SAVE:
            do_continue = self.action_save()
        elif choice == AskSaveChangesDialog.CANCEL:
            do_continue = False
        elif choice == AskSaveChangesDialog.DISCARD:
            do_continue = True
        return do_continue
