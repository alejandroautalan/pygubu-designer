#!/usr/bin/python3
import pathlib
import pygubu

PROJECT_PATH = pathlib.Path(__file__).parent
PROJECT_UI = PROJECT_PATH / "demo1.ui"


class Demo1App:
    def __init__(self, master=None):
        self.builder = builder = pygubu.Builder()
        builder.add_resource_path(PROJECT_PATH)
        builder.add_from_file(PROJECT_UI)
        # Main widget
        self.mainwindow = builder.get_object("toplevel1", master)

        self.var_enable_tab3 = None
        self.var_show_hidden_tab = None
        builder.import_variables(
            self, ["var_enable_tab3", "var_show_hidden_tab"]
        )

        builder.connect_callbacks(self)

        #
        # Set second tab the active tab at start
        #
        self.notebook = builder.get_object("notebook1")
        self.notebook.select(1)

    def run(self):
        self.mainwindow.mainloop()

    def on_option_changed(self, widget_id):
        if widget_id == "cb_enable_tab3":
            enable_tab = self.var_enable_tab3.get()
            new_state = "normal" if enable_tab else "disabled"
            self.notebook.tab(2, state=new_state)
        elif widget_id == "cb_show_hidden_tab":
            hide_tab = self.var_show_hidden_tab.get()
            new_state = "normal" if hide_tab else "hidden"
            self.notebook.tab(3, state=new_state)


if __name__ == "__main__":
    app = Demo1App()
    app.run()
