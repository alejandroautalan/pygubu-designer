#!/usr/bin/python3
import pygubu
from formsdemo1appui import FormsDemo1AppUI
from pygubu.forms.transformer.tkboolean import BoolTransformer
from pygubu.forms.validation.constraint.istrue import IsTrue
from pygubu.forms.validation.constraint.notblank import NotBlank

bool_transformer = BoolTransformer()

form_config = {
    "id": {"required": False, "initial": "ID-999999"},
    "first_name": {
        "constraints": [NotBlank()],
        "help": "Your first name",
    },
    "last_name": {
        "help": "Your last name",
    },
    "age": {
        "help": "How old are you?",
    },
    "height": {
        "help": "How tall are you?",
    },
    "bio": {
        "initial": "Hello, I like to ...",
        "help": "Your short bio here",
        "required": False,
    },
    "terms": {
        "constraints": [IsTrue(message="You must accept terms of use!")],
        "model_transformer": bool_transformer,
    },
}


class FormsDemo1App(FormsDemo1AppUI):
    def __init__(self, master=None):
        super().__init__(master)
        self.form_builder = self.builder.get_object("form_builder")
        self.form = self.form_builder.get_form(form_config)
        data = {
            "first_name": "Alex",
            "last_name": "Bot",
        }
        self.form.edit(data)

    def on_submit_clicked(self):
        self.form.submit()
        if self.form.is_valid():
            data = self.form.get_data()
            print(data)
        else:
            print("The form has errors!")


if __name__ == "__main__":
    app = FormsDemo1App()
    app.run()
