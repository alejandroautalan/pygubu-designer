#!/usr/bin/python3
"""
Designer settings dialog

Designer Settings dialog.

UI source file: designer_settings.ui
"""
import tkinter as tk
import tkinter.ttk as ttk
from pygubu.forms.pygubuwidget import PygubuCombobox
from pygubu.forms.ttkwidget import Checkbutton, FrameFormBuilder
from pygubu.widgets.dialog import Dialog


def safe_i18n_translator(value):
    """i18n - Setup translator in derived class file"""
    return value


def safe_fo_callback(widget):
    """on first objec callback - Setup callback in derived class file."""
    pass


def safe_image_loader(master, image_name: str):
    """Image loader - Setup image_loader in derived class file."""
    img = None
    try:
        img = tk.PhotoImage(file=image_name, master=master)
    except tk.TclError:
        pass
    return img


class DesignerSettingsUI:
    def __init__(
        self,
        master=None,
        *,
        translator=None,
        on_first_object_cb=None,
        data_pool=None,
        image_loader=None,
    ):
        if translator is None:
            translator = safe_i18n_translator
        _ = translator  # i18n string marker.
        if image_loader is None:
            image_loader = safe_image_loader
        if on_first_object_cb is None:
            on_first_object_cb = safe_fo_callback
        # build ui
        preferences = Dialog(master)
        preferences.configure(height=200, modal=True, width=200)
        mw_ = preferences.toplevel.winfo_pixels(480)
        mh_ = preferences.toplevel.winfo_pixels(360)
        preferences.toplevel.minsize(mw_, mh_)
        preferences.toplevel.resizable(True, True)
        preferences.toplevel.title("Pygubu Preferences")
        # First object created
        on_first_object_cb(preferences)

        frame3 = ttk.Frame(preferences.toplevel)
        frame3.configure(height=200, padding="5p", width=200)
        self.ffb_settings = FrameFormBuilder(
            frame3, name="ffb_settings", field_name="ffb_settings"
        )
        Notebook_1 = ttk.Notebook(self.ffb_settings)
        Notebook_1.configure(
            height=340, style="ProjectSettings.TNotebook", width=350
        )
        frame4 = ttk.Frame(Notebook_1)
        frame4.configure(height=200, width=200)
        fgeneral = ttk.Frame(frame4)
        fgeneral.configure(height=200, padding="5p", width=200)
        lblpt = ttk.Label(fgeneral)
        lblpt.configure(text=_("Preferred widget set:"))
        lblpt.grid(column=0, row=0, sticky="ew")
        self.widget_set = PygubuCombobox(
            fgeneral, name="widget_set", field_name="widget_set"
        )
        self.widget_set.configure(values='[["tk", "tk"], ["ttk", "ttk"]]')
        self.widget_set.grid(column=1, ipady="3p", row=0, sticky="ew")
        label1 = ttk.Label(fgeneral)
        label1.configure(text=_("Preferred ttk theme:"))
        label1.grid(column=0, row=1, sticky="ew")
        self.ttk_theme = PygubuCombobox(
            fgeneral, name="ttk_theme", field_name="ttk_theme"
        )
        self.ttk_theme.grid(column=1, ipady="3p", row=1, sticky="ew")
        lbl_preferred_layout_manager = ttk.Label(fgeneral)
        lbl_preferred_layout_manager.configure(
            text=_("Preferred layout manager:")
        )
        lbl_preferred_layout_manager.grid(column=0, row=2, sticky="ew")
        self.default_layout_manager = PygubuCombobox(
            fgeneral,
            name="default_layout_manager",
            field_name="default_layout_manager",
        )
        self.default_layout_manager.configure(
            values='[["pack", "pack"], ["grid", "grid"], ["place", "place"]]'
        )
        self.default_layout_manager.grid(
            column=1, ipady="3p", row=2, sticky="ew"
        )
        self.center_preview = Checkbutton(
            fgeneral, name="center_preview", field_name="center_preview"
        )
        self.center_preview.configure(text=_("Center toplevel preview window"))
        self.center_preview.grid(
            column=0, columnspan=2, ipady="3p", row=3, sticky="w"
        )
        fgeneral.pack(fill="x", side="top")
        fgeneral.rowconfigure("all", pad=8)
        fgeneral.columnconfigure("all", pad=10)
        fgeneral.columnconfigure(1, weight=1)
        frame1 = ttk.Frame(frame4)
        frame1.configure(height=200, padding="5p", width=200)
        label2 = ttk.Label(frame1)
        label2.configure(text=_("Widget naming"))
        label2.pack(anchor="w", pady="5p", side="top")
        frame2 = ttk.Frame(frame1)
        frame2.configure(height=200, padding="10p 0 10p 0", width=200)
        self.widget_naming_use_underscore = Checkbutton(
            frame2,
            name="widget_naming_use_underscore",
            field_name="widget_naming_use_underscore",
        )
        self.widget_naming_use_underscore.configure(
            text=_('Use "_" as separator (e.g. button_1)')
        )
        self.widget_naming_use_underscore.grid(
            column=0, columnspan=2, ipady="3p", row=0, sticky="ew"
        )
        self.widget_naming_ufletter = Checkbutton(
            frame2,
            name="widget_naming_ufletter",
            field_name="widget_naming_ufletter",
        )
        self.widget_naming_ufletter.configure(
            text=_("Uppercase first letter (e.g. Button…)")
        )
        self.widget_naming_ufletter.grid(
            column=0, columnspan=2, ipady="3p", row=1, sticky="ew"
        )
        frame2.pack(fill="x", side="top")
        frame2.rowconfigure("all", pad=5)
        frame2.columnconfigure("all", pad=5)
        frame2.columnconfigure(1, weight=1)
        label_1 = ttk.Label(frame1)
        label_1.configure(
            text=_("This does not affect previously generated names.")
        )
        label_1.pack(anchor="w", fill="x", padx="10p 5p", pady="5p 0")
        frame1.pack(fill="x")
        self.img_dlg_settings_general = image_loader(
            preferences.toplevel, "dlg_settings_general"
        )
        Notebook_1.add(
            frame4,
            compound="left",
            image=self.img_dlg_settings_general,
            sticky="nsew",
            text=_("General"),
        )
        Notebook_1.pack(expand=True, fill="both", side="top")
        self.ffb_settings.pack(expand=True, fill="both", side="top")
        Frame_4 = ttk.Frame(frame3)
        Frame_4.configure(height=200, padding="0 5p 0 0", width=200)
        cancel = ttk.Button(Frame_4)
        cancel.configure(text=_("Cancel"), width=-8)
        cancel.grid(column=0, padx="0 5", row=0)
        cancel.configure(command=self.btn_cancel_clicked)
        dialog_close = ttk.Button(Frame_4)
        dialog_close.configure(default="active", text=_("Ok"), width=-8)
        dialog_close.grid(column=1, padx="5p 0", row=0)
        dialog_close.configure(command=self.btn_apply_clicked)
        Frame_4.pack(side="right")
        frame3.pack(expand=True, fill="both", side="top")
        preferences.bind("<<DialogClose>>", self.on_dialog_close, add="")

        # Main widget
        self.mainwindow = preferences

    def run(self):
        self.mainwindow.mainloop()

    def btn_cancel_clicked(self):
        pass

    def btn_apply_clicked(self):
        pass

    def on_dialog_close(self, event=None):
        pass


if __name__ == "__main__":
    root = tk.Tk()
    app = DesignerSettingsUI(root)
    app.run()
