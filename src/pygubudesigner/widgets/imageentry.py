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

import os
import tkinter as tk
import tkinter.filedialog
import tkinter.ttk as ttk

from pygubu.stockimage import StockImage, TK_IMAGE_FORMATS

from pygubudesigner.i18n import translator
from pygubudesigner.widgets.propertyeditor import (
    PropertyEditor,
    register_editor,
)

_ = translator


class ImagePropertyEditor(PropertyEditor):
    def _create_ui(self):
        self._entry = w = ttk.Entry(self, textvariable=self._variable)
        w.grid(sticky="ew")
        w.bind("<FocusOut>", self._on_variable_changed)
        w.bind("<KeyPress>", self._on_keypress)

        btn_style = "ImageSelectorButton.Toolbutton"
        self._button = w = ttk.Button(self, text="…", style=btn_style)
        w.grid(row=0, column=1, padx="5 0")
        w.configure(command=self._on_button_click)

        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)

    def _on_button_click(self):
        ext = [f"*{e}" for e in TK_IMAGE_FORMATS]
        options = {
            "filetypes": [
                (_("Tk image formats"), " ".join(ext)),
                (_("All Files"), "*.*"),
            ]
        }

        fname = tk.filedialog.askopenfilename(**options)
        if fname:
            base, name = os.path.split(fname)
            #  Register image before change event is generated:
            if not StockImage.is_registered(name):
                StockImage.register(name, fname)
            self._set_value(name)
            self._on_variable_changed(event=None)


register_editor("imageentry", ImagePropertyEditor)


if __name__ == "__main__":
    root = tk.Tk()

    entry = ImagePropertyEditor(root)
    entry.grid()

    def see_var():
        print(entry._variable.get())

    entry.edit("image.gif")
    btn = ttk.Button(root, text="Value", command=see_var)
    btn.grid(row=0, column=1)

    root.mainloop()
