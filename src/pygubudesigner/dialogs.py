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

from pathlib import Path

import pygubu

from pygubudesigner.i18n import translator

DATA_DIR = Path(__file__).parent / "data"
ASK_SAVE_CHANGES_DIALOG_UI = DATA_DIR / "ui" / "ask_save_changes_dialog.ui"


class AskSaveChangesDialog:
    CANCEL = 0
    SAVE = 1
    DONTSAVE = 3

    def __init__(self, master):
        self.master = master
        self.builder = builder = pygubu.Builder(translator)
        builder.add_from_file(str(ASK_SAVE_CHANGES_DIALOG_UI))
        self.dialog = builder.get_object("ask_save_changes_dialog", master)
        self.lbl_message = builder.get_object("lbl_message")
        self.lbl_detail = builder.get_object("lbl_detail")
        self.btn_save = builder.get_object("btn_save")
        builder.connect_callbacks(self)

        self.user_choice = None

    def on_dontsave(self):
        self.user_choice = self.DONTSAVE
        self.dialog.close()
        self.dialog.destroy()

    def on_cancel(self):
        self.user_choice = self.CANCEL
        self.dialog.close()
        self.dialog.destroy()

    def on_save(self):
        self.user_choice = self.SAVE
        self.dialog.close()
        self.dialog.destroy()

    def on_dialog_close(self, event=None):
        self.user_choice = self.CANCEL
        self.dialog.close()
        self.dialog.destroy()

    def run(self, title, message, detail=""):
        self.dialog.set_title(title)
        self.lbl_message["text"] = message
        self.lbl_detail["text"] = detail
        self.btn_save.focus_set()
        self.dialog.run()
        self.master.wait_window(self.dialog.toplevel)
        return self.user_choice


def ask_save_changes(master, title, message, detail=""):
    dialog = AskSaveChangesDialog(master)
    return dialog.run(title, message, detail)


if __name__ == "__main__":
    import tkinter as tk

    root = tk.Tk()
    app = AskSaveChangesDialog(root)
    app.run()
