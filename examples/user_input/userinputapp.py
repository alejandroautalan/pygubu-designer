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
        self.mainwindow = builder.get_object('mainwindow')
        builder.connect_callbacks(self)

        # Get from builder all variables we need
        # variables will be accesible from self
        guivars = ('entryvar', 'spinvar', 'combovar',
                   'option1var', 'option2var', 'option3var',
                   'group1var')
        builder.import_variables(self, guivars)

        # Fill with random values
        self.random_values()

    def random_values(self):
        # Entry
        txt = 'Random string '
        rand = random.sample('0123456789abcdefghijklmnoprstuvwxyz', 10)
        txt = txt + ''.join(rand)
        self.entryvar.set(txt)

        # Spinbox
        val = random.randint(0, 100)
        self.spinvar.set(val)

        # combobox
        combo = self.builder.get_object('combobox')
        options = combo.cget('values')
        selection = random.choice(options)
        self.combovar.set(selection)

        # Checkbuttons
        for var in (self.option1var, self.option2var, self.option3var):
            value = 0 if random.random() < 0.5 else 1
            var.set(value)

        # Radiobuttons
        value = random.choice(('A', 'B', 'C'))
        self.group1var.set(value)

    def on_change_clicked(self):
        self.random_values()

    def on_print_clicked(self):
        line = f'Entry value:{self.entryvar.get()}'
        print(line)
        line = f'Spinbox value:{self.spinvar.get()}'
        print(line)
        line = f'Checkbox Option1 value:{self.option1var.get()}'
        print(line)
        line = f'Checkbox Option2 value:{self.option2var.get()}'
        print(line)
        line = f'Checkbox Option3 value:{self.option3var.get()}'
        print(line)
        line = f'Radiobutton Group value:{self.group1var.get()}'
        print(line)

    def run(self):
        self.mainwindow.mainloop()

if __name__ == '__main__':
    app = UserinputApp()
    app.run()

