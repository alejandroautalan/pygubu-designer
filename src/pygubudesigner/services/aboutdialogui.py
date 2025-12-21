#!/usr/bin/python3
import tkinter as tk
import tkinter.ttk as ttk
from pygubu.widgets.dialog import Dialog


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


class AboutDialogUI:
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
        aboutdialog = Dialog(master)
        aboutdialog.configure(height=100, modal=False, width=200)
        aboutdialog.toplevel.resizable(True, True)
        aboutdialog.toplevel.title("About")
        # First object created
        on_first_object_cb(aboutdialog)

        frame1 = ttk.Frame(aboutdialog.toplevel)
        frame1.configure(height=250, padding="20p 4p", width=400)
        Frame_1 = ttk.Frame(frame1)
        Frame_1.configure(height=200, width=200)
        logo = ttk.Label(Frame_1)
        self.img_pygubu200 = image_loader(aboutdialog.toplevel, "pygubu200")
        logo.configure(
            anchor="e",
            font="Sans 18 bold",
            image=self.img_pygubu200,
            text=_("pygubu"),
        )
        logo.pack(pady="0 18p")
        frame2 = ttk.Frame(Frame_1)
        frame2.configure(height=200, width=200)
        frame4 = ttk.Frame(frame2)
        frame4.configure(height=200, width=200)
        label1 = ttk.Label(frame4)
        label1.configure(font="{sans} 12 {bold}", text=_("This program:"))
        label1.pack(anchor="center", side="left")
        label2 = ttk.Label(frame4)
        label2.configure(font="{sans} 12 {bold}", text=_("pygubu-designer"))
        label2.pack(anchor="center", padx="5p 0", side="left")
        frame4.pack(side="top")
        label3 = ttk.Label(frame2)
        label3.configure(
            font="{Sans} 10 {}",
            justify="center",
            text=_(
                "A visual design tool for tkinter that generates Python code for the user interface portion of your desktop application."
            ),
            wraplength="290p",
        )
        label3.pack(pady="2p", side="top")
        self.designer_version = ttk.Label(frame2, name="designer_version")
        self.designer_version.configure(
            font="{sans} 10 {}", text=_("Version: %version%")
        )
        self.designer_version.pack(side="top")
        frame7 = ttk.Frame(frame2)
        frame7.configure(height=200, width=200)
        label7 = ttk.Label(frame7)
        label7.configure(font="{sans} 10 {}", text=_("License:"))
        label7.pack(side="left")
        licence_link = ttk.Label(frame7)
        licence_link.configure(
            anchor="center",
            cursor="hand2",
            font="{Sans} 10 {}",
            foreground="#143ee3",
            text=_("GPL3"),
        )
        licence_link.pack(padx="5 0", side="left")
        licence_link.bind("<Button-1>", self.on_gpl3_clicked, add="")
        frame7.pack(side="top")
        frame2.pack(fill="both", pady="0 10", side="top")
        frame3 = ttk.Frame(Frame_1)
        frame3.configure(height=200, width=200)
        frame5 = ttk.Frame(frame3)
        frame5.configure(height=200, width=200)
        label4 = ttk.Label(frame5)
        label4.configure(font="{sans} 11 {bold}", text=_("Associated program:"))
        label4.pack(side="left")
        label5 = ttk.Label(frame5)
        label5.configure(font="{sans} 11 {bold}", text=_("pygubu"))
        label5.pack(padx="5p 0", side="left")
        frame5.pack(side="top")
        label6 = ttk.Label(frame3)
        label6.configure(
            font="{sans} 10 {}",
            justify="center",
            text=_(
                "A run-time library that the designer requires. It is optional for your application."
            ),
            wraplength="290p",
        )
        label6.pack(pady="2p", side="top")
        self.pygubu_version = ttk.Label(frame3, name="pygubu_version")
        self.pygubu_version.configure(
            font="{Sans} 10 {}", text=_("Version: %version%")
        )
        self.pygubu_version.pack()
        frame8 = ttk.Frame(frame3)
        frame8.configure(height=200, width=200)
        label10 = ttk.Label(frame8)
        label10.configure(font="{sans} 10 {}", text=_("License:"))
        label10.pack(side="left")
        label11 = ttk.Label(frame8)
        label11.configure(
            anchor="center",
            cursor="hand2",
            font="{Sans} 10 {}",
            foreground="#143ee3",
            text=_("MIT"),
        )
        label11.pack(padx="5p 0", side="left")
        label11.bind("<Button-1>", self.on_mit_clicked, add="")
        frame8.pack(side="top")
        frame3.pack(fill="both", side="top")
        frame6 = ttk.Frame(Frame_1)
        frame6.configure(height=200, width=200)
        label9 = ttk.Label(frame6)
        label9.configure(
            anchor="center",
            cursor="hand2",
            font="{Sans} 10 {}",
            foreground="#143ee3",
            text=_("More info."),
        )
        label9.pack(pady="10p 0", side="top")
        label9.bind("<Button-1>", self.on_moreinfo_clicked, add="")
        frame6.pack(pady="10 0", side="top")
        Frame_1.pack(expand=True, fill="both", side="top")
        bottom = ttk.Frame(frame1)
        bottom.configure(height=200, padding="0 8p 0 0", width=200)
        close_btn = ttk.Button(bottom)
        close_btn.configure(text=_("Close"))
        close_btn.pack(side="right")
        close_btn.configure(command=self.on_ok_execute)
        bottom.pack(fill="x")
        frame1.pack(expand=True, fill="both")

        # Main widget
        self.mainwindow = aboutdialog

    def run(self):
        self.mainwindow.mainloop()

    def on_gpl3_clicked(self, event=None):
        pass

    def on_mit_clicked(self, event=None):
        pass

    def on_moreinfo_clicked(self, event=None):
        pass

    def on_ok_execute(self):
        pass


if __name__ == "__main__":
    root = tk.Tk()
    app = AboutDialogUI(root)
    app.run()
