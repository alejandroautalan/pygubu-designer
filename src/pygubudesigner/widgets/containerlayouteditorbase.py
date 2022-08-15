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


class ContainerLayoutEditorBase(ttk.Frame):
    def __init__(self, master=None, **kw):
        super().__init__(master, **kw)
        self.mainpanel = ttk.Frame(self)
        self.lbl_title = ttk.Label(self.mainpanel)
        self.lbl_title.configure(
            font="TkHeadingFont",
            padding="0 2",
            text="Options for {0} container",
        )
        self.lbl_title.grid(column="0", row="0", sticky="ew")
        self.separator4 = ttk.Separator(self.mainpanel)
        self.separator4.configure(orient="horizontal")
        self.separator4.grid(column="0", pady="5", row="1", sticky="ew")
        self.foptions = ttk.Frame(self.mainpanel)
        self.foptions.configure(height="100", padding="5", width="200")
        self.foptions.grid(column="0", row="2", sticky="ew")
        self.gridrcpanel = ttk.Frame(self.mainpanel)
        self.frame2 = ttk.Frame(self.gridrcpanel)
        self.separator1 = ttk.Separator(self.frame2)
        self.separator1.configure(orient="horizontal")
        self.separator1.place(
            relheight="1", relwidth="1", rely="0.5", x="0", y="0"
        )
        self.label1 = ttk.Label(self.frame2)
        self.label1.configure(text="Grid Row / Column options")
        self.label1.pack(side="top")
        self.frame2.configure(height="200", width="200")
        self.frame2.pack(fill="x", side="top")
        self.cellselectorframe = ttk.Frame(self.gridrcpanel)
        self.rcselectorframe = ttk.Frame(self.cellselectorframe)
        self.rcselectorframe.configure(height="180", width="180")
        self.rcselectorframe.pack(side="left")
        self.frame1 = ttk.Frame(self.cellselectorframe)
        self.btn_allrows = ttk.Button(self.frame1)
        self.btn_allrows.configure(text="All row/cols")
        self.btn_allrows.pack(fill="x", pady="0 10", side="top")
        self.btn_allrows.configure(command=self._btn_indexall_clicked)
        self.btn_clear_all = ttk.Button(self.frame1)
        self.btn_clear_all.configure(text="Clear all")
        self.btn_clear_all.pack(fill="x", side="top")
        self.btn_clear_all.configure(command=self._btn_clearall_clicked)
        self.frame1.configure(height="200", width="200")
        self.frame1.pack(anchor="center", side="left")
        self.cellselectorframe.configure(height="200", padding="5", width="200")
        self.cellselectorframe.pack(
            expand="true", fill="x", pady="0 5", side="top"
        )
        self.frame4 = ttk.Frame(self.gridrcpanel)
        self.separator2 = ttk.Separator(self.frame4)
        self.separator2.configure(orient="horizontal")
        self.separator2.place(
            relheight="1", relwidth="1", rely="0.5", x="0", y="0"
        )
        self.rowframe_label = ttk.Label(self.frame4)
        self.rowframe_label.configure(text="Row {0} options")
        self.rowframe_label.pack(padx="10 0", side="left")
        self.frame4.configure(height="200", width="200")
        self.frame4.pack(fill="x", side="top")
        self.rowframe = ttk.Frame(self.gridrcpanel)
        self.rowframe.configure(height="200", padding="5", width="200")
        self.rowframe.pack(fill="x", side="top")
        self.frame6 = ttk.Frame(self.gridrcpanel)
        self.separator3 = ttk.Separator(self.frame6)
        self.separator3.configure(orient="horizontal")
        self.separator3.place(
            relheight="1", relwidth="1", rely="0.5", x="0", y="0"
        )
        self.colframe_label = ttk.Label(self.frame6)
        self.colframe_label.configure(text="Column {0} options")
        self.colframe_label.pack(padx="10 0", side="left")
        self.frame6.configure(height="200", width="200")
        self.frame6.pack(fill="x", side="top")
        self.colframe = ttk.Frame(self.gridrcpanel)
        self.colframe.configure(height="200", padding="5", width="200")
        self.colframe.pack(fill="x", side="top")
        self.gridrcpanel.configure(height="200", width="200")
        self.gridrcpanel.grid(column="0", row="3", sticky="ew")
        self.mainpanel.configure(height="200", width="200")
        self.mainpanel.pack(anchor="w", expand="true", fill="both", side="top")

    def _btn_indexall_clicked(self):
        pass

    def _btn_clearall_clicked(self):
        pass


if __name__ == "__main__":
    root = tk.Tk()
    widget = ContainerLayoutEditorBase(root)
    widget.pack(expand=True, fill="both")
    root.mainloop()
