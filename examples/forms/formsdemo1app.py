#!/usr/bin/python3
import os
import pprint as pp
import pathlib


os.environ["PYGUBU_ENABLE_FORMS"] = "Y"


import pygubu  # noqa=E402

try:
    import ttkbootstrap  # noqa=E402
except ImportError:
    pass

import pygubu.forms.config as formconfig  # noqa=E402
import project_styles  # # noqa=E402 Styles definition module
from formsdemo1appui import FormsDemo1AppUI  # noqa=E402

formconfig.ENTRY_MARK_INVALID_USING_VALIDATE = True


class FormsDemo1App(FormsDemo1AppUI):
    def __init__(self, master=None):
        super().__init__(
            master, on_fist_object_cb=project_styles.setup_ttk_styles
        )

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
            print("form data:")
            pp.pprint(self.form.cleaned_data)
        else:
            print("invalid!")
            pp.pprint(self.form.errors)

    def on_check_changed(self):
        if self.form.has_changed():
            print("form has changed data.")
            print("Changed data:")
            pp.pprint(self.form.changed_data)
        else:
            print("form is not changed.")


if __name__ == "__main__":
    app = FormsDemo1App()
    app.run()
