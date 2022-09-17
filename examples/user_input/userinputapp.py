import pathlib
import random
import pygubu


PROJECT_PATH = pathlib.Path(__file__).parent
PROJECT_UI = PROJECT_PATH / "userinput.ui"


class UserinputApp:
    def __init__(self):
        self.builder = builder = pygubu.Builder()
        builder.add_resource_path(PROJECT_PATH)
        builder.add_from_file(PROJECT_UI)
        self.mainwindow = builder.get_object("mainwindow")
        builder.connect_callbacks(self)

        # Get from builder all variables we need
        # variables will be accesible from self
        self.entryvar = None
        self.spinvar = None
        self.combovar = None
        self.option1var = None
        self.option2var = None
        self.option3var = None
        self.group1var = None
        self.optionmenu_var = None
        builder.import_variables(
            self,
            [
                "entryvar",
                "validated_entry_var",
                "spinvar",
                "combovar",
                "option1var",
                "option2var",
                "option3var",
                "group1var",
                "optionmenu_var",
            ],
        )

        # Fill with random values
        self.random_values()

    def random_values(self):
        # Entry
        txt = "Random string "
        rand = random.sample("0123456789abcdefghijklmnoprstuvwxyz", 10)
        txt = txt + "".join(rand)
        self.entryvar.set(txt)

        # Spinbox
        val = random.randint(0, 100)
        self.spinvar.set(val)

        # combobox
        combo = self.builder.get_object("combobox")
        options = combo.cget("values")
        selection = random.choice(options)
        self.combovar.set(selection)

        # Checkbuttons
        for var in (self.option1var, self.option2var, self.option3var):
            value = 0 if random.random() < 0.5 else 1
            var.set(value)

        # Radiobuttons
        value = random.choice(("A", "B", "C"))
        self.group1var.set(value)

        # Option Menu
        value = random.choice(("None", "A", "B", "C", "D"))
        self.optionmenu_var.set(value)

        # Menubutton
        self._clicked_commands = []

    def on_change_clicked(self):
        self.random_values()

    def validate_entry_cb(self, d_action, p_entry_value):
        is_valid = True
        if d_action == "1":  # Insert
            if not p_entry_value.islower():
                is_valid = False
            if len(p_entry_value) > 10:
                is_valid = False
        return is_valid

    def option_menu_clicked(self, option):
        msg = f"You clicked {option} option."
        print(msg)

    def mb_option_clicked(self, itemid):
        msg = f"You clicked {itemid} menu option"
        if itemid not in self._clicked_commands:
            self._clicked_commands.append(itemid)
        print(msg)

    def on_print_clicked(self):
        line = f"Entry value:{self.entryvar.get()}"
        print(line)
        line = f"Validated Entry value:{self.validated_entry_var.get()}"
        print(line)
        line = f"Spinbox value:{self.spinvar.get()}"
        print(line)
        line = f"Checkbox Option1 value:{self.option1var.get()}"
        print(line)
        line = f"Checkbox Option2 value:{self.option2var.get()}"
        print(line)
        line = f"Checkbox Option3 value:{self.option3var.get()}"
        print(line)
        line = f"Radiobutton Group value:{self.group1var.get()}"
        print(line)
        line = f"Option Menu value:{self.optionmenu_var.get()}"
        print(line)
        line = f"Menubutton commands clicked: {self._clicked_commands}"
        print(line)

    def run(self):
        self.mainwindow.mainloop()


if __name__ == "__main__":
    app = UserinputApp()
    app.run()
