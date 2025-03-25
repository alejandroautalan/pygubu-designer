#!/usr/bin/python3
import tkinter as tk
import tkinter.ttk as ttk


#
# Begin i18n - Setup translator in derived class file
#
def i18n_noop(value):
    return value


i18n_translator = i18n_noop
# End i18n


class ConfigurationScreenUI:
    def __init__(self, master=None, data_pool=None):
        _ = i18n_translator  # i18n string marker.
        # build ui
        self.config_screen = tk.Tk() if master is None else tk.Toplevel(master)
        self.config_screen.configure(height=200, width=200)
        self.config_screen.title("Configuration Panel")
        frame1 = ttk.Frame(self.config_screen)
        frame1.configure(height=200, padding="4p", width=200)
        frame2 = ttk.Frame(frame1)
        frame2.configure(height=200, width=200)
        canvas1 = tk.Canvas(frame2)
        canvas1.configure(background="#702800")
        canvas1.pack(expand=True, fill="both", side="top")
        label1 = ttk.Label(frame2)
        label1.configure(text=_("A Configuration screen"))
        label1.place(anchor="center", relx=0.5, rely=0.5, x=0, y=0)
        frame2.pack(expand=True, fill="both", side="top")
        frame3 = ttk.Frame(frame1)
        frame3.configure(height=200, padding="0 5p 0 0", width=200)
        button1 = ttk.Button(frame3)
        button1.configure(text=_("Close"))
        button1.pack(anchor="e", side="top")
        button1.configure(command=self.on_btn_close_clicked)
        frame3.pack(fill="x", side="top")
        frame1.pack(expand=True, fill="both", side="top")

        # Main widget
        self.mainwindow = self.config_screen

    def run(self):
        self.mainwindow.mainloop()

    def on_btn_close_clicked(self):
        pass


if __name__ == "__main__":
    app = ConfigurationScreenUI()
    app.run()
