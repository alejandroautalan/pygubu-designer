#!/usr/bin/python3
import tkinter as tk
import tkinter.ttk as ttk


#
# Begin i18n - Setup translator in derived class file
#
def i18n_noop(value):
    return value


i18n_translator = i18n_noop
# End i18n

#
# Base class definition
#


class ContainerLayoutEditorUI(ttk.Frame):
    def __init__(self, master=None, **kw):
        super().__init__(master, **kw)
        _ = i18n_translator  # i18n string marker.
        self.mainpanel = ttk.Frame(self, name="mainpanel")
        self.mainpanel.configure(height=200, width=200)
        self.lbl_title = ttk.Label(self.mainpanel, name="lbl_title")
        self.lbl_title.configure(
            font="TkHeadingFont",
            padding="0 4p",
            text=_("Options for {0} container"),
        )
        self.lbl_title.grid(column=0, row=0, sticky="ew")
        self.foptions = ttk.Frame(self.mainpanel, name="foptions")
        self.foptions.configure(height=100, padding="5p", width=200)
        self.foptions.grid(column=0, row=1, sticky="ew")
        self.gridrcpanel = ttk.Frame(self.mainpanel, name="gridrcpanel")
        self.gridrcpanel.configure(height=200, width=200)
        frame2 = ttk.Frame(self.gridrcpanel)
        frame2.configure(height=200, padding="0 2p", width=200)
        label1 = ttk.Label(frame2)
        label1.configure(text=_("Grid Row / Column options"))
        label1.pack(expand=True, fill="x", side="top")
        frame2.pack(expand=True, fill="x", side="top")
        self.cellselectorframe = ttk.Frame(
            self.gridrcpanel, name="cellselectorframe"
        )
        self.cellselectorframe.configure(height=200, width=200)
        self.rcselectorframe = ttk.Frame(
            self.cellselectorframe, name="rcselectorframe"
        )
        self.rcselectorframe.configure(height=180, width=150)
        self.rcselectorframe.pack(expand=True, fill="both", side="top")
        frame1 = ttk.Frame(self.cellselectorframe)
        frame1.configure(height=200, padding="0 2p 0 5p", width=200)
        self.btn_allrows = ttk.Button(frame1, name="btn_allrows")
        self.btn_allrows.configure(text=_("All row/cols"))
        self.btn_allrows.pack(padx="0 10p", side="left")
        self.btn_allrows.configure(command=self._btn_indexall_clicked)
        btn_clear_all = ttk.Button(frame1)
        btn_clear_all.configure(text=_("Clear all"))
        btn_clear_all.pack(side="left")
        btn_clear_all.configure(command=self._btn_clearall_clicked)
        frame1.pack(anchor="center", fill="x", side="top")
        frame5 = ttk.Frame(self.cellselectorframe)
        frame5.configure(height=200, width=200)
        label2 = ttk.Label(frame5)
        label2.configure(anchor="w", text=_("Selected"))
        label2.grid(column=0, row=0, sticky="w")
        label5 = ttk.Label(frame5)
        label5.configure(anchor="e", text=_("Hover"))
        label5.grid(column=1, row=0, sticky="w")
        self.sel_pos = ttk.Label(frame5, name="sel_pos")
        self.sel_pos.configure(anchor="w")
        self.sel_pos.grid(column=0, row=1, sticky="w")
        self.sel_widget = ttk.Label(frame5, name="sel_widget")
        self.sel_widget.configure(anchor="w")
        self.sel_widget.grid(column=0, row=2, sticky="w")
        self.hover_pos = ttk.Label(frame5, name="hover_pos")
        self.hover_pos.configure(anchor="w")
        self.hover_pos.grid(column=1, row=1, sticky="w")
        self.hover_widget = ttk.Label(frame5, name="hover_widget")
        self.hover_widget.configure(anchor="w")
        self.hover_widget.grid(column=1, row=2, sticky="w")
        frame5.pack(expand=True, fill="x", side="top")
        frame5.rowconfigure("all", pad="5p")
        frame5.columnconfigure("all", pad="5p")
        frame5.columnconfigure(0, weight=1)
        frame5.columnconfigure(1, pad="5p", weight=1)
        frame5.columnconfigure(2, pad="5p", weight=1)
        self.cellselectorframe.pack(
            expand=True, fill="x", pady="0 5", side="top"
        )
        frame4 = ttk.Frame(self.gridrcpanel)
        frame4.configure(height=200, padding="0 2p", width=200)
        self.rowframe_label = ttk.Label(frame4, name="rowframe_label")
        self.rowframe_label.configure(text=_("Row {0} options"))
        self.rowframe_label.pack(expand=True, fill="x", side="top")
        separator2 = ttk.Separator(frame4)
        separator2.configure(orient="horizontal")
        separator2.pack(expand=True, fill="x", side="top")
        frame4.pack(expand=True, fill="x", side="top")
        self.rowframe = ttk.Frame(self.gridrcpanel, name="rowframe")
        self.rowframe.configure(height=200, padding="5p", width=200)
        self.rowframe.pack(fill="x", side="top")
        frame6 = ttk.Frame(self.gridrcpanel)
        frame6.configure(height=200, padding="0 2p", width=200)
        self.colframe_label = ttk.Label(frame6, name="colframe_label")
        self.colframe_label.configure(text=_("Column {0} options"))
        self.colframe_label.pack(expand=True, fill="x", side="top")
        separator3 = ttk.Separator(frame6)
        separator3.configure(orient="horizontal")
        separator3.pack(expand=True, fill="x", side="top")
        frame6.pack(expand=True, fill="x", side="top")
        self.colframe = ttk.Frame(self.gridrcpanel, name="colframe")
        self.colframe.configure(height=200, padding="5p", width=200)
        self.colframe.pack(fill="x", side="top")
        self.gridrcpanel.grid(column=0, row=2, sticky="ew")
        self.mainpanel.pack(anchor="w", expand=True, fill="both", side="top")
        self.configure(height=200, width=200)
        self.grid(column=0, row=0, sticky="nsew")

    def _btn_indexall_clicked(self):
        pass

    def _btn_clearall_clicked(self):
        pass


if __name__ == "__main__":
    root = tk.Tk()
    widget = ContainerLayoutEditorUI(root)
    widget.pack(expand=True, fill="both")
    root.mainloop()
