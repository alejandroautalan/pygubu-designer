#!/usr/bin/python3
import pathlib
import pygubu

try:
    import ttkbootstrap
except ImportError:
    pass

import pygubu.forms.config as formconfig
from formsdemo1base import FormsDemo1Base


formconfig.ENTRY_MARK_INVALID_USING_VALIDATE = True


class FormsDemo1App(FormsDemo1Base):
    def __init__(self, master=None):
        super().__init__(master)

        self.form = self.builder.get_object("form1")
        data = {
            "id": 36912,
            "name": "Alex",
            "lastname": "Doe",
        }
        self.form.edit(data, data)

    def run(self):
        self.mainwindow.mainloop()

    def on_submit_clicked(self):
        self.form.submit()
        if self.form.is_valid():
            print("valid!")
            print("form data:", self.form.cleaned_data)
        else:
            print("invalid!")
            print(self.form.errors)

    def on_check_changed(self):
        if self.form.has_changed():
            print("form has changed data.")
            print("Changed data:")
            print(self.form.changed_data)
        else:
            print("form is not changed.")


if __name__ == "__main__":
    app = FormsDemo1App()
    app.run()
