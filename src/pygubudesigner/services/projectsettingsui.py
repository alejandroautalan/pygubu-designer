#!/usr/bin/python3
"""
Project settings dialog

Designer Project Settings dialog.

UI source file: project_settings.ui
"""
import tkinter as tk
import tkinter.ttk as ttk
from pygubu.forms.pygubuwidget import PygubuCombobox
from pygubu.forms.tkwidget import Text
from pygubu.forms.ttkwidget import (
    Checkbutton,
    Entry,
    FrameFormBuilder,
    LabelWidgetInfo,
)
from pygubu.widgets.dialog import Dialog
from pygubu.widgets.pathchooserinput import PathChooserButton
from pygubu.widgets.scrollbarhelper import ScrollbarHelper
from pygubu.widgets.scrolledframe import ScrolledFrame


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


class ProjectSettingsUI:
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
        self.settingsdialog = Dialog(master)
        self.settingsdialog.configure(height=100, modal=True, width=200)
        mw_ = self.settingsdialog.toplevel.winfo_pixels(680)
        mh_ = self.settingsdialog.toplevel.winfo_pixels(640)
        self.settingsdialog.toplevel.minsize(mw_, mh_)
        # First object created
        on_first_object_cb(self.settingsdialog)

        frame8 = ttk.Frame(self.settingsdialog.toplevel)
        frame8.configure(height=200, padding="4p", width=200)
        frame9 = ttk.Frame(frame8)
        frame9.configure(height=200, width=200)
        self.settings_notebook = ttk.Notebook(frame9, name="settings_notebook")
        self.settings_notebook.configure(
            height=350, style="ProjectSettings.TNotebook", width=480
        )
        self.frm_general = FrameFormBuilder(
            self.settings_notebook, name="frm_general", field_name="frm_general"
        )
        self.frm_general.configure(padding=5)
        label6 = ttk.Label(self.frm_general)
        label6.configure(text=_("Name:"))
        label6.grid(column=0, row=0, sticky="ew")
        entryfield4 = Entry(self.frm_general, field_name="name")
        entryfield4.configure(style="EntryField.TEntry")
        entryfield4.grid(column=1, ipady="2p", row=0, sticky="ew")
        labelfieldinfo6 = LabelWidgetInfo(self.frm_general, field_name="name")
        labelfieldinfo6.configure(style="LabelFieldInfo.TLabel")
        labelfieldinfo6.grid(column=1, row=1, sticky="ew")
        label7 = ttk.Label(self.frm_general)
        label7.configure(text=_("Description:"))
        label7.grid(column=0, row=2, sticky="ew")
        scrollbarhelper2 = ScrollbarHelper(self.frm_general, scrolltype="both")
        scrollbarhelper2.configure(usemousewheel=True)
        textfield1 = Text(scrollbarhelper2.container, field_name="description")
        textfield1.configure(height=8, width=32)
        scrollbarhelper2.add_child(textfield1)
        scrollbarhelper2.grid(column=0, columnspan=2, row=3, sticky="nsew")
        labelfieldinfo7 = LabelWidgetInfo(
            self.frm_general, field_name="description"
        )
        labelfieldinfo7.configure(style="LabelFieldInfo.TLabel")
        labelfieldinfo7.grid(column=0, columnspan=2, row=4, sticky="ew")
        self.frm_general.rowconfigure("all", pad=10)
        self.frm_general.rowconfigure(3, weight=1)
        self.frm_general.columnconfigure("all", pad=10)
        self.frm_general.columnconfigure(1, weight=1)
        self.img_pp_general = image_loader(
            self.settingsdialog.toplevel, "pp_general"
        )
        self.settings_notebook.add(
            self.frm_general,
            compound="left",
            image=self.img_pp_general,
            sticky="nsew",
            text=_("General"),
        )
        scrolledframe1 = ScrolledFrame(
            self.settings_notebook, scrolltype="both"
        )
        scrolledframe1.configure(usemousewheel=True)
        self.frm_code = FrameFormBuilder(
            scrolledframe1.innerframe, name="frm_code", field_name="frm_code"
        )
        self.frm_code.configure(padding="5p 5p 5p 5p")
        labelframe3 = ttk.Labelframe(self.frm_code)
        labelframe3.configure(
            height=200, padding="4p", text=_("Template"), width=200
        )
        self.template = PygubuCombobox(
            labelframe3, name="template", field_name="template"
        )
        self.template.configure(style="ComboboxField.TCombobox")
        self.template.pack(fill="x", ipady="1p")
        self.template.bind(
            "<<ComboboxSelected>>", self.on_template_change, add=""
        )
        label5 = ttk.Label(labelframe3)
        self.template_desc_var = tk.StringVar(
            value=_("Template description here.")
        )
        label5.configure(
            font="TkHeadingFont",
            padding="2p",
            text=_("Template description here."),
            textvariable=self.template_desc_var,
        )
        label5.pack(expand=True, fill="x")
        lbl_wlist = ttk.Label(labelframe3)
        lbl_wlist.configure(text=_("Main widget:"))
        lbl_wlist.pack(expand=True, fill="x", pady="2p 0")
        self.main_widget = PygubuCombobox(
            labelframe3, name="main_widget", field_name="main_widget"
        )
        self.main_widget.configure(
            state="readonly", style="ComboboxField.TCombobox"
        )
        self.main_widget.pack(fill="x", ipady="1p")
        labelfieldinfo1 = LabelWidgetInfo(labelframe3, field_name="main_widget")
        labelfieldinfo1.configure(style="LabelFieldInfo.TLabel")
        labelfieldinfo1.pack(expand=True, fill="x")
        labelframe3.pack(fill="x", side="top")
        labelframe1 = ttk.Labelframe(self.frm_code)
        labelframe1.configure(
            height=200, padding="4p", text=_("Module"), width=200
        )
        label2 = ttk.Label(labelframe1)
        label2.configure(text=_("Namespace:"))
        label2.pack(expand=True, fill="x")
        self.module_namespace = Entry(
            labelframe1, name="module_namespace", field_name="module_namespace"
        )
        self.module_namespace.configure(style="EntryField.TEntry")
        self.module_namespace.pack(fill="x", ipady="1p")
        labelwidgetinfo3 = LabelWidgetInfo(
            labelframe1, field_name="module_namespace"
        )
        labelwidgetinfo3.configure(style="LabelFieldInfo.TLabel")
        labelwidgetinfo3.pack(expand=True, fill="x")
        label3 = ttk.Label(labelframe1)
        label3.configure(text=_("Name:"))
        label3.pack(expand=True, fill="x", pady="2p 0")
        self.module_name = Entry(
            labelframe1, name="module_name", field_name="module_name"
        )
        self.module_name.configure(style="EntryField.TEntry")
        self.module_name.pack(fill="x", ipady="1p")
        labelfieldinfo4 = LabelWidgetInfo(labelframe1, field_name="module_name")
        labelfieldinfo4.configure(style="LabelFieldInfo.TLabel")
        labelfieldinfo4.pack(expand=True, fill="x")
        label_2 = ttk.Label(labelframe1)
        self.class_name_label_var = tk.StringVar(value=_("Class name:"))
        label_2.configure(
            text=_("Class name:"), textvariable=self.class_name_label_var
        )
        label_2.pack(expand=True, fill="x", pady="2p 0")
        self.main_classname = Entry(
            labelframe1, name="main_classname", field_name="main_classname"
        )
        self.main_classname.configure(style="EntryField.TEntry")
        self.main_classname.pack(fill="x", ipady="1p")
        labelfieldinfo2 = LabelWidgetInfo(
            labelframe1, field_name="main_classname"
        )
        labelfieldinfo2.configure(style="LabelFieldInfo.TLabel")
        labelfieldinfo2.pack(expand=True, fill="x")
        label4 = ttk.Label(labelframe1)
        label4.configure(text=_("Output directory:"))
        label4.pack(expand=True, fill="x", pady="2p 0")
        frame3 = ttk.Frame(labelframe1)
        frame3.configure(height=200, width=200)
        self.output_dir = Entry(
            frame3, name="output_dir", field_name="output_dir"
        )
        self.output_dir.configure(style="EntryField.TEntry")
        self.output_dir.pack(expand=True, fill="x", ipady="1p", side="left")
        self.btn_path_chooser = PathChooserButton(
            frame3, name="btn_path_chooser"
        )
        self.img_path_btn_search = image_loader(
            self.settingsdialog.toplevel, "path_btn_search"
        )
        self.btn_path_chooser.configure(
            image=self.img_path_btn_search,
            text=_("…"),
            title=_("Select output directory"),
            type="directory",
            width=4,
        )
        self.btn_path_chooser.pack(padx="10p 0", side="left")
        self.btn_path_chooser.bind(
            "<<PathChooserPathChanged>>", self.output_dir_changed, add=""
        )
        frame3.pack(fill="x")
        labelfieldinfo5 = LabelWidgetInfo(labelframe1, field_name="output_dir")
        labelfieldinfo5.configure(style="LabelFieldInfo.TLabel")
        labelfieldinfo5.pack(expand=True, fill="x")
        labelframe1.pack(fill="x", pady="5p", side="top")
        labelframe2 = ttk.Labelframe(self.frm_code)
        labelframe2.configure(
            height=200, padding="4p", text=_("Builder"), width=200
        )
        label10 = ttk.Label(labelframe2)
        label10.configure(text=_("Namespace:"))
        label10.pack(expand=True, fill="x")
        self.builder_namespace = Entry(
            labelframe2,
            name="builder_namespace",
            field_name="builder_namespace",
        )
        self.builder_namespace.configure(style="EntryField.TEntry")
        self.builder_namespace.pack(expand=True, fill="x")
        labelwidgetinfo2 = LabelWidgetInfo(
            labelframe2, field_name="builder_namespace"
        )
        labelwidgetinfo2.configure(style="LabelFieldInfo.TLabel")
        labelwidgetinfo2.pack(expand=True, fill="x")
        label9 = ttk.Label(labelframe2)
        label9.configure(text=_("Output directory:"))
        label9.pack(expand=True, fill="x", pady="2p 0")
        frame5 = ttk.Frame(labelframe2)
        frame5.configure(height=200, width=200)
        self.output_dir2 = Entry(
            frame5, name="output_dir2", field_name="output_dir2"
        )
        self.output_dir2.configure(style="EntryField.TEntry")
        self.output_dir2.pack(expand=True, fill="x", ipady="2p", side="left")
        self.btn_path2_chooser = PathChooserButton(
            frame5, name="btn_path2_chooser"
        )
        self.btn_path2_chooser.configure(
            image=self.img_path_btn_search,
            text=_("…"),
            title=_("Select output directory"),
            type="directory",
            width=4,
        )
        self.btn_path2_chooser.pack(padx="10p 0", side="left")
        self.btn_path2_chooser.bind(
            "<<PathChooserPathChanged>>", self.output_dir2_changed, add=""
        )
        frame5.pack(expand=True, fill="x")
        labelwidgetinfo1 = LabelWidgetInfo(
            labelframe2, field_name="output_dir2"
        )
        labelwidgetinfo1.configure(style="LabelFieldInfo.TLabel")
        labelwidgetinfo1.pack(expand=True, fill="x")
        labelframe2.pack(fill="x", side="top")
        frame2 = ttk.Frame(self.frm_code)
        frame2.configure(height=200, padding="0 5p 0 0", width=200)
        self.generate_code_onsave = Checkbutton(
            frame2,
            name="generate_code_onsave",
            field_name="generate_code_onsave",
        )
        self.generate_code_onsave_var = tk.BooleanVar()
        self.generate_code_onsave.configure(
            text=_("Regenerate code when saving the project"),
            variable=self.generate_code_onsave_var,
        )
        self.generate_code_onsave.pack(anchor="w", side="top")
        self.use_i18n = Checkbutton(
            frame2, name="use_i18n", field_name="use_i18n"
        )
        self.use_i18n_var = tk.BooleanVar()
        self.use_i18n.configure(
            text=_("Add i18n support"), variable=self.use_i18n_var
        )
        self.use_i18n.pack(anchor="w", side="top")
        self.all_ids_attributes = Checkbutton(
            frame2, name="all_ids_attributes", field_name="all_ids_attributes"
        )
        self.all_ids_attr_var = tk.BooleanVar()
        self.all_ids_attributes.configure(
            text=_("All IDs as class attributes"),
            variable=self.all_ids_attr_var,
        )
        self.all_ids_attributes.pack(anchor="w", side="top")
        self.import_tkvariables = Checkbutton(
            frame2, name="import_tkvariables", field_name="import_tkvariables"
        )
        self.import_tkvariables_var = tk.BooleanVar()
        self.import_tkvariables.configure(
            text=_("Import Tk Variables"), variable=self.import_tkvariables_var
        )
        self.import_tkvariables.pack(anchor="w", side="top")
        self.use_ttk_styledefinition_file = Checkbutton(
            frame2,
            name="use_ttk_styledefinition_file",
            field_name="use_ttk_styledefinition_file",
        )
        self.use_ttk_style_var = tk.BooleanVar()
        self.use_ttk_styledefinition_file.configure(
            text=_("Use ttk style definitions file"),
            variable=self.use_ttk_style_var,
        )
        self.use_ttk_styledefinition_file.pack(anchor="w", side="top")
        self.use_window_centering_code = Checkbutton(
            frame2,
            name="use_window_centering_code",
            field_name="use_window_centering_code",
        )
        self.use_windowcenter_code_var = tk.BooleanVar()
        self.use_window_centering_code.configure(
            text=_("Add window centering code"),
            variable=self.use_windowcenter_code_var,
        )
        self.use_window_centering_code.pack(anchor="w", side="top")
        frame2.pack(fill="x", side="top")
        self.frm_code.pack(expand=True, fill="both", side="top")
        self.img_pp_code = image_loader(self.settingsdialog.toplevel, "pp_code")
        self.settings_notebook.add(
            scrolledframe1,
            compound="left",
            image=self.img_pp_code,
            sticky="nsew",
            text=_("Code"),
        )
        self.frm_style = FrameFormBuilder(
            self.settings_notebook, name="frm_style", field_name="frm_style"
        )
        self.frm_style.configure(padding="5p")
        label1 = ttk.Label(self.frm_style)
        label1.configure(text=_("Style definition file:"))
        label1.pack(anchor="w", side="top")
        frame4 = ttk.Frame(self.frm_style)
        frame4.configure(height=200, width=200)
        self.ttk_style_definition_file = Entry(
            frame4,
            name="ttk_style_definition_file",
            field_name="ttk_style_definition_file",
        )
        self.ttk_style_definition_file.configure(style="EntryField.TEntry")
        self.ttk_style_definition_file.pack(
            expand=True, fill="x", ipady="2p", side="left"
        )
        self.btn_stylepath_find = PathChooserButton(
            frame4, name="btn_stylepath_find"
        )
        self.btn_stylepath_find.configure(
            defaultextension=".py",
            image=self.img_path_btn_search,
            text=_("…"),
            title=_("Select style definitions file"),
            type="file",
            width=4,
        )
        self.btn_stylepath_find.pack(padx="10p 0", side="left")
        self.btn_stylepath_find.bind(
            "<<PathChooserPathChanged>>", self.on_style_new_selected, add=""
        )
        self.btn_stylepath_new = PathChooserButton(
            frame4, name="btn_stylepath_new"
        )
        self.img_style_add_btn = image_loader(
            self.settingsdialog.toplevel, "style_add_btn"
        )
        self.btn_stylepath_new.configure(
            defaultextension=".py",
            image=self.img_style_add_btn,
            mustexist=False,
            text=_("+"),
            title=_("Create style definitions file"),
            type="file",
            width=3,
        )
        self.btn_stylepath_new.pack(padx="5p 0", side="left")
        self.btn_stylepath_new.bind(
            "<<PathChooserPathChanged>>", self.on_style_new_create, add=""
        )
        separator1 = ttk.Separator(frame4)
        separator1.configure(orient="vertical")
        separator1.pack(fill="y", padx="5p", side="left")
        button2 = ttk.Button(frame4)
        self.img_style_remove_btn = image_loader(
            self.settingsdialog.toplevel, "style_remove_btn"
        )
        button2.configure(image=self.img_style_remove_btn, text=_("Remove"))
        button2.pack(side="left")
        button2.configure(command=self.on_style_remove)
        frame4.pack(fill="x", side="top")
        labelfieldinfo8 = LabelWidgetInfo(
            self.frm_style, field_name="ttk_style_definition_file"
        )
        labelfieldinfo8.configure(style="LabelFieldInfo.TLabel")
        labelfieldinfo8.pack(fill="x", pady="0 5p", side="top")
        self.img_pp_style = image_loader(
            self.settingsdialog.toplevel, "pp_style"
        )
        self.settings_notebook.add(
            self.frm_style,
            compound="left",
            image=self.img_pp_style,
            sticky="nsew",
            text=_("Styles"),
        )
        frame13 = ttk.Frame(self.settings_notebook)
        frame13.configure(height=200, padding="5p", width=200)
        label8 = ttk.Label(frame13)
        label8.configure(text=_("Project widget builders:"))
        label8.pack(anchor="w", pady="5p", side="top")
        scrollbarhelper1 = ScrollbarHelper(frame13, scrolltype="both")
        scrollbarhelper1.configure(usemousewheel=True)
        self.cwtree = ttk.Treeview(scrollbarhelper1.container, name="cwtree")
        self.cwtree.configure(selectmode="extended")
        self.cwtree_cols = []
        self.cwtree_dcols = []
        self.cwtree.configure(
            columns=self.cwtree_cols, displaycolumns=self.cwtree_dcols
        )
        self.cwtree.column(
            "#0", anchor="w", stretch=True, width=200, minwidth=20
        )
        self.cwtree.heading("#0", anchor="center", text=_("Modules"))
        scrollbarhelper1.add_child(self.cwtree)
        scrollbarhelper1.pack(expand=True, fill="both", side="left")
        frame7 = ttk.Frame(frame13)
        frame7.configure(height=200, padding="4 0 4 0", width=200)
        self.btn_cwadd_module = PathChooserButton(
            frame7, name="btn_cwadd_module"
        )
        self.btn_cwadd_module.configure(
            defaultextension=".py",
            text=_("+"),
            title=_("Select a widget builder file"),
            type="file",
            width=-3,
        )
        self.btn_cwadd_module.pack(pady="0 8p", side="top")
        self.btn_cwadd_module.bind(
            "<<PathChooserPathChanged>>", self.btn_cwadd_clicked, add=""
        )
        self.btn_cwremove = ttk.Button(frame7, name="btn_cwremove")
        self.btn_cwremove.configure(text=_("-"), width=-3)
        self.btn_cwremove.pack(side="top")
        self.btn_cwremove.configure(command=self.btn_cwremove_clicked)
        frame7.pack(fill="y", side="left")
        self.img_pp_customwidget = image_loader(
            self.settingsdialog.toplevel, "pp_customwidget"
        )
        self.settings_notebook.add(
            frame13,
            compound="left",
            image=self.img_pp_customwidget,
            sticky="nsew",
            text=_("Custom Widgets"),
        )
        self.settings_notebook.pack(expand=True, fill="both", side="top")
        frame9.pack(expand=True, fill="both", side="top")
        frame10 = ttk.Frame(frame8)
        frame10.configure(height=200, width=200)
        button7 = ttk.Button(frame10)
        button7.configure(text=_("Cancel"), width=-8)
        button7.pack(padx="0 10p", side="left")
        button7.configure(command=self.btn_cancel_clicked)
        button6 = ttk.Button(frame10)
        button6.configure(text=_("Ok"), width=-8)
        button6.pack(side="left")
        button6.configure(command=self.btn_apply_clicked)
        frame10.pack(anchor="e", pady="5p 0", side="top")
        frame8.pack(expand=True, fill="both", side="top")
        self.settingsdialog.bind(
            "<<DialogClose>>", self.on_dialog_close, add="+"
        )

        # Main widget
        self.mainwindow = self.settingsdialog

    def run(self):
        self.mainwindow.mainloop()

    def on_template_change(self, event=None):
        pass

    def output_dir_changed(self, event=None):
        pass

    def output_dir2_changed(self, event=None):
        pass

    def on_style_new_selected(self, event=None):
        pass

    def on_style_new_create(self, event=None):
        pass

    def on_style_remove(self):
        pass

    def btn_cwadd_clicked(self, event=None):
        pass

    def btn_cwremove_clicked(self):
        pass

    def btn_cancel_clicked(self):
        pass

    def btn_apply_clicked(self):
        pass

    def on_dialog_close(self, event=None):
        pass


if __name__ == "__main__":
    root = tk.Tk()
    app = ProjectSettingsUI(root)
    app.run()
