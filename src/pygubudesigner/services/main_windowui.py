#!/usr/bin/python3
import tkinter as tk
import tkinter.ttk as ttk
from pygubu.widgets.dockfw.dockframe import DockFrame
from pygubu.widgets.editabletreeview import EditableTreeview
from pygubu.widgets.scrollbarhelper import ScrollbarHelper
from pygubudesigner.services.widgets.custom_root import CustomRoot
from pygubudesigner.services.widgets.layout_editor import LayoutEditor
from pygubudesigner.services.widgets.project_tree_frame import ProjectTreeFrame
from pygubudesigner.services.widgets.properties_editor import PropertiesEditor
from pygubudesigner.services.widgets.treecomponentpalette import (
    TreeComponentPalette,
)


def i18n_translator_noop(value):
    """i18n - Setup translator in derived class file"""
    return value


def first_object_callback_noop(widget):
    """on first objec callback - Setup callback in derived class file."""
    pass


def image_loader_default(master, image_name: str):
    """Image loader - Setup image_loader in derived class file."""
    img = None
    try:
        img = tk.PhotoImage(file=image_name, master=master)
    except tk.TclError:
        pass
    return img


class MainWindowUI:
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
            translator = i18n_translator_noop
        _ = translator  # i18n string marker.
        if image_loader is None:
            image_loader = image_loader_default
        if on_first_object_cb is None:
            on_first_object_cb = first_object_callback_noop
        # build ui
        self.mainroot = CustomRoot(master, className="PygubuDesigner")
        self.mainroot.configure(height=100, width=100)
        mw_ = self.mainroot.winfo_pixels(854)
        mh_ = self.mainroot.winfo_pixels(480)
        self.mainroot.minsize(mw_, mh_)
        self.mainroot.resizable(True, True)
        self.mainroot.title("Pygubu Designer")
        # First object created
        on_first_object_cb(self.mainroot)

        mainframe = ttk.Frame(self.mainroot)
        mainframe.configure(padding="2p")
        self.mainpw = ttk.Panedwindow(
            mainframe, orient="vertical", name="mainpw"
        )
        self.mainpw.configure(height=200, width=200)
        newmain = ttk.Frame(self.mainpw)
        self.maindock = DockFrame(newmain, name="maindock", uid="maindock")
        dockpane1 = self.maindock.new_pane(
            orient="horizontal", uid="dockpane1", main_pane=True
        )
        self.img_sec_components = image_loader(self.mainroot, "sec_components")
        self.dw_cpalette = dockpane1.maindock.new_widget(
            name="dw_cpalette", uid="dw_cpalette"
        )
        self.dw_cpalette.configure(
            compound="left",
            image=self.img_sec_components,
            title=_("Components Palette"),
        )
        dockpane1.add_widget(self.dw_cpalette, grouped=False, weight=0)
        self.tree_palette = TreeComponentPalette(
            self.dw_cpalette.fcenter, name="tree_palette"
        )
        self.tree_palette.pack(
            expand=True, fill="both", padx="2p", pady="2p", side="top"
        )
        dockpane2 = dockpane1.maindock.new_pane(
            orient="vertical", uid="dockpane2"
        )
        dockpane1.add_pane(dockpane2, weight=0)
        self.img_sec_project_tree = image_loader(
            self.mainroot, "sec_project_tree"
        )
        self.dw_ptree = dockpane2.maindock.new_widget(
            name="dw_ptree", uid="dw_ptree"
        )
        self.dw_ptree.configure(
            compound="left",
            image=self.img_sec_project_tree,
            title=_("Project Tree"),
        )
        dockpane2.add_widget(self.dw_ptree, grouped=False, weight=1)
        self.project_tree_frame = ProjectTreeFrame(
            self.dw_ptree.fcenter, name="project_tree_frame"
        )
        self.project_tree_frame.pack(
            expand=True, fill="both", padx="2p", pady="2p", side="top"
        )
        self.img_sec_properties = image_loader(self.mainroot, "sec_properties")
        self.dw_props = dockpane2.maindock.new_widget(
            name="dw_props", uid="dw_props"
        )
        self.dw_props.configure(
            compound="left",
            image=self.img_sec_properties,
            title=_("Properties"),
        )
        dockpane2.add_widget(self.dw_props, grouped=False, weight=2)
        frame_1 = ttk.Frame(self.dw_props.fcenter)
        frame_1.configure(height=200, width=200)
        notebook1 = ttk.Notebook(frame_1)
        notebook1.configure(height=200, padding="0 2p 0 0", width=375)
        self.propertieseditor1 = PropertiesEditor(
            notebook1, name="propertieseditor1"
        )
        self.img_prop_apperance = image_loader(self.mainroot, "prop_apperance")
        notebook1.add(
            self.propertieseditor1,
            compound="left",
            image=self.img_prop_apperance,
            padding="2p 6p 2p 6p",
            sticky="nsew",
            text=_("Appearance"),
        )
        self.layouteditor1 = LayoutEditor(notebook1, name="layouteditor1")
        self.img_prop_layout = image_loader(self.mainroot, "prop_layout")
        notebook1.add(
            self.layouteditor1,
            compound="left",
            image=self.img_prop_layout,
            padding="2p 6p 2p 6p",
            sticky="nsew",
            text=_("Layout"),
        )
        bindingscontainer = ttk.Frame(notebook1)
        bindingscontainer.configure(height=200, padding="2p", width=200)
        self.bindings_frame = ScrollbarHelper(
            bindingscontainer, scrolltype="both", name="bindings_frame"
        )
        self.bindings_frame.configure(usemousewheel=True)
        self.bindings_tree = EditableTreeview(
            self.bindings_frame.container, name="bindings_tree"
        )
        self.bindings_tree.configure(
            show="headings", style="BindingsEditor.Treeview"
        )
        self.bindings_tree_cols = ["sequence", "handler", "add", "actions"]
        self.bindings_tree_dcols = ["sequence", "handler", "add", "actions"]
        self.bindings_tree.configure(
            columns=self.bindings_tree_cols,
            displaycolumns=self.bindings_tree_dcols,
        )
        self.bindings_tree.column(
            "sequence", anchor="w", stretch=True, width=200, minwidth=20
        )
        self.bindings_tree.column(
            "handler", anchor="w", stretch=True, width=200, minwidth=20
        )
        self.bindings_tree.column(
            "add", anchor="w", stretch=True, width=50, minwidth=50
        )
        self.bindings_tree.column(
            "actions", anchor="w", stretch=True, width=50, minwidth=50
        )
        self.bindings_tree.heading(
            "sequence", anchor="w", text=_("Sequence descriptor")
        )
        self.bindings_tree.heading(
            "handler", anchor="w", text=_("Event Handler")
        )
        self.bindings_tree.heading("add", anchor="w", text=_("Add"))
        self.bindings_tree.heading("actions", anchor="w", text=_("actions"))
        self.bindings_frame.add_child(self.bindings_tree)
        self.bindings_frame.pack(expand=True, fill="both", side="top")
        self.img_prop_bindings = image_loader(self.mainroot, "prop_bindings")
        notebook1.add(
            bindingscontainer,
            compound="left",
            image=self.img_prop_bindings,
            padding="2p 6p 2p 6p",
            sticky="nsew",
            text=_("Bindings"),
        )
        notebook1.pack(expand=True, fill="both", side="top")
        frame_1.pack(expand=True, fill="both", side="top")
        self.img_sec_preview = image_loader(self.mainroot, "sec_preview")
        self.dw_preview = dockpane1.maindock.new_widget(
            name="dw_preview", uid="dw_preview"
        )
        self.dw_preview.configure(
            compound="left", image=self.img_sec_preview, title=_("Preview")
        )
        dockpane1.add_widget(self.dw_preview, grouped=False, weight=2)
        Frame_1 = ttk.Frame(self.dw_preview.fcenter)
        Frame_1.configure(height=250, padding="1p", width=250)
        scrollbarhelper_1 = ScrollbarHelper(Frame_1, scrolltype="both")
        scrollbarhelper_1.configure(usemousewheel=True)
        self.preview_canvas = tk.Canvas(
            scrollbarhelper_1.container, name="preview_canvas"
        )
        self.preview_canvas.configure(highlightthickness=0, takefocus=True)
        scrollbarhelper_1.add_child(self.preview_canvas)
        scrollbarhelper_1.pack(expand=True, fill="both", side="top")
        Frame_1.pack(expand=True, fill="both", side="top")
        self.maindock.pack(expand=True, fill="both", side="top")
        self.maindock.bind(
            "<<DocFrame::LayoutChanged>>", self.on_dockframe_changed, add=""
        )
        newmain.pack(expand=True, fill="both", side="top")
        self.mainpw.add(newmain, weight="1")
        self.bpanel = ttk.Frame(self.mainpw, name="bpanel")
        self.bpanel.configure(height=200, width=200)
        self.bp_container = ttk.Frame(self.bpanel, name="bp_container")
        self.bp_container.configure(height=200, width=200)
        scrollbarhelper_3 = ScrollbarHelper(
            self.bp_container, scrolltype="both"
        )
        scrollbarhelper_3.configure(usemousewheel=False)
        self.txt_log = tk.Text(scrollbarhelper_3.container, name="txt_log")
        self.txt_log.configure(
            font="TkFixedFont", height=8, state="disabled", width=50
        )
        scrollbarhelper_3.add_child(self.txt_log)
        scrollbarhelper_3.pack(expand=True, fill="both", side="top")
        self.bp_container.pack(expand=True, fill="both", side="top")
        self.bp_buttons = ttk.Frame(self.bpanel, name="bp_buttons")
        self.bp_buttons.configure(height=200, padding="1p", width=200)
        self.btn_messages = ttk.Checkbutton(
            self.bp_buttons, name="btn_messages"
        )
        self.bpanel_buttonsvar = tk.StringVar()
        self.btn_messages.configure(
            offvalue=0,
            onvalue="messages",
            style="Toolbutton",
            text=_("Messages"),
            variable=self.bpanel_buttonsvar,
        )
        self.btn_messages.pack(side="left")
        self.btn_messages.configure(command=self.on_bpanel_button_clicked)
        self.bp_buttons.pack(fill="x", side="bottom")
        self.bpanel.pack(side="top")
        self.mainpw.add(self.bpanel, weight="0")
        self.mainpw.pack(expand=True, fill="both", side="top")
        mainframe.pack(expand=True, fill="both", side="top")

        # Main widget
        self.mainwindow = self.mainroot

    def run(self):
        self.mainwindow.mainloop()

    def on_dockframe_changed(self, event=None):
        pass

    def on_bpanel_button_clicked(self):
        pass


if __name__ == "__main__":
    root = tk.Tk()
    app = MainWindowUI(root)
    app.run()
