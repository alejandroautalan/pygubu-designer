# encoding: utf8
import pathlib
from tkinter import messagebox
import pygubu


PROJECT_PATH = pathlib.Path(__file__).parent
PROJECT_UI = PROJECT_PATH / "commands.ui"


class Myapp:
    def __init__(self, master=None):
        self.builder = builder = pygubu.Builder()
        builder.add_resource_path(PROJECT_PATH)
        builder.add_from_file(PROJECT_UI)
        self.mainwindow = builder.get_object("mainwindow", master)

        builder.connect_callbacks(self)
        self.set_scrollbars()

    def run(self):
        self.mainwindow.mainloop()

    def on_button_clicked(self):
        messagebox.showinfo(
            "From callback", "Button clicked !!", parent=self.mainwindow
        )

    def validate_number(self, p):
        print("On validate number")
        value = str(p)
        return value == "" or value.isnumeric()

    def entry_invalid(self):
        messagebox.showinfo(
            "Title", "Invalid entry input", parent=self.mainwindow
        )

    def radiobutton_command(self):
        messagebox.showinfo(
            "Title", "Radiobutton command", parent=self.mainwindow
        )

    def checkbutton_command(self):
        messagebox.showinfo(
            "Title", "Checkbutton command", parent=self.mainwindow
        )

    def on_scale1_changed(self, event):
        print(event)
        label = self.builder.get_object("scale1label")
        scale = self.builder.get_object("scale1")
        label.configure(text=scale.get())

    def on_scale2_changed(self, event):
        print(event)
        label = self.builder.get_object("scale2label")
        scale = self.builder.get_object("scale2")
        label.configure(text=int(scale.get()))

    def set_scrollbars(self):
        sb1 = self.builder.get_object("scrollbar_1")
        sb2 = self.builder.get_object("scrollbar_2")
        sb1.set(0.0, 0.20)
        sb2.set(0.0, 0.20)

    def on_scrollbar1_changed(self, *args):
        label = self.builder.get_object("scrollbar1label")
        label.configure(text=repr(args))

    def on_scrollbar2_changed(self, *args):
        label = self.builder.get_object("scrollbar2label")
        label.configure(text=repr(args))

    def on_spinbox_cmd(self):
        def showmessage():
            messagebox.showinfo("Title", "Spinbox command")

        self.mainwindow.after_idle(showmessage)

    def on_combobox_validate(self, p):
        value = str(p)
        return value == "" or value.isnumeric()

    def on_combobox_invalid(self, p):
        messagebox.showinfo(
            "Title", f"Invalid combobox input: {p}", parent=self.mainwindow
        )

    def on_combobox_postcmd(self):
        messagebox.showinfo(
            "Title", "Combobox postcommand", parent=self.mainwindow
        )

    def on_menuitem_clicked(self, itemid):
        messagebox.showinfo(
            "Title", f'Menu item "{itemid}" was clicked', parent=self.mainwindow
        )

    def on_menuitem2_clicked(self):
        messagebox.showinfo(
            "Title", "Callback on_menuitem2_clicked", parent=self.mainwindow
        )


if __name__ == "__main__":
    app = Myapp()
    app.run()
