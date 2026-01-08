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

import tkinter as tk
import tkinter.ttk as ttk
import pygubudesigner.services.ask_save_changesui as baseui

from pygubudesigner.i18n import translator
from pygubudesigner.services.image_loader import iconset_loader


class AskSaveChangesDialog(baseui.AskSaveChangesDialogUI):
    CANCEL = 1
    SAVE = 2
    DISCARD = 3

    def __init__(self, master=None):
        self.master = master
        super().__init__(
            master, translator=translator, image_loader=iconset_loader
        )

    def on_discard(self):
        self.user_choice = self.DISCARD
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
        self.message_var.set(message)
        self.detail_var.set(detail)
        self.btn_save.focus_set()
        self.dialog.run()
        self.master.wait_window(self.dialog.toplevel)
        return self.user_choice


def ask_save_changes(master, title, message, detail=""):
    dialog = AskSaveChangesDialog(master)
    return dialog.run(title, message, detail)


if __name__ == "__main__":
    root = tk.Tk()

    def test():
        value = ask_save_changes(
            root,
            "Save",
            "File was modified, save changes?",
            "More detail here.",
        )
        print("User selected: ", value)

    root.after(100, test)
    root.mainloop()
