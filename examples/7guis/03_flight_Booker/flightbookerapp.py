#!/usr/bin/python3
import pathlib
from datetime import datetime
import tkinter as tk
import tkinter.ttk as ttk
import tkinter.messagebox
import pygubu

PROJECT_PATH = pathlib.Path(__file__).parent
PROJECT_UI = PROJECT_PATH / "flight_booker.ui"


class FlightBookerApp:
    ONE_WAY_FLIGHT = 0
    RETURN_FLIGHT = 1

    def __init__(self, master=None):
        self.builder = builder = pygubu.Builder()
        builder.add_resource_path(PROJECT_PATH)
        builder.add_from_file(PROJECT_UI)
        # Main widget
        self.mainwindow = builder.get_object("toplevel1", master)
        self.cbox = builder.get_object("cbox_c")
        self.t1 = builder.get_object("entry_t1")
        self.t2 = builder.get_object("entry_t2")
        self.button = builder.get_object("btn_b")

        self.t1_var = None
        self.t2_var = None
        builder.import_variables(self, ["t1_var", "t2_var"])

        self.style = ttk.Style()
        self.style.configure("Invalid.TEntry", fieldbackground="red")

        builder.connect_callbacks(self)
        self.form_init()
        self.form_validate()

    def run(self):
        self.mainwindow.mainloop()

    def form_init(self):
        value = "10.07.2022"
        self.t1_var.set(value)
        self.t2_var.set(value)
        self.cbox.current(self.ONE_WAY_FLIGHT)

    def form_validate(self):
        t2_enabled = True
        flight_type = self.cbox.current()

        if flight_type == self.ONE_WAY_FLIGHT:
            t2_enabled = False

        # validate date 1
        date1 = self.date_from_string(self.t1_var.get())
        style_invalid = "Invalid.TEntry"
        style = style_invalid if date1 is None else ""
        self.t1.configure(style=style)

        date2 = None
        if t2_enabled:
            # validate date 2
            date2 = self.date_from_string(self.t2_var.get())
            style = style_invalid if date2 is None else ""
            self.t2.configure(style=style)

        # button status
        button_enabled = True
        if date1 is None or date2 is None:
            button_enabled = False
        if flight_type == self.RETURN_FLIGHT:
            if date1 is not None and date2 is not None and (date2 < date1):
                button_enabled = False
        btn_state = "normal" if button_enabled else "disabled"
        self.button.configure(state=btn_state)

        # Entry 2 status
        t2_state = "normal" if t2_enabled else "disabled"
        self.t2.configure(state=t2_state)

    def on_cbox_changed(self, event=None):
        self.form_validate()

    def date_from_string(self, date: str):
        result = None
        try:
            result = datetime.strptime(date, "%d.%m.%Y")
        except ValueError:
            pass
        return result

    def validate_date(self, p_entry_value, w_entry_name):
        self.mainwindow.after_idle(self.form_validate)
        return True

    def book_clicked(self):
        fdate = self.t1_var.get()
        ftype = self.cbox.get()
        msg = f"You have booked a {ftype} on {fdate}."
        tk.messagebox.showinfo(
            title="Message", message=msg, parent=self.mainwindow
        )


if __name__ == "__main__":
    app = FlightBookerApp()
    app.run()
