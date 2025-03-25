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


class AboutScreenUI:
    def __init__(self, master=None, data_pool=None):
        _ = i18n_translator  # i18n string marker.
        # build ui
        self.about_screen = tk.Tk() if master is None else tk.Toplevel(master)
        self.about_screen.configure(height=200, width=200)
        self.about_screen.minsize(320, 240)
        self.about_screen.title("About")
        frame1 = ttk.Frame(self.about_screen)
        frame1.configure(height=200, padding="4p", width=200)
        frame2 = ttk.Frame(frame1)
        frame2.configure(height=200, width=200)
        label1 = ttk.Label(frame2)
        label1.configure(font="TkHeadingFont", text=_("About Screen"))
        label1.pack(side="top")
        frame2.pack(side="top")
        frame3 = ttk.Frame(frame1)
        frame3.configure(height=200, padding="10p", width=200)
        label2 = ttk.Label(frame3)
        label2.configure(
            font="{Helvetica} 14 {}",
            text=_(
                "A demo application to show usage of multiple toplevel windows with pygubu."
            ),
            wraplength=300,
        )
        label2.pack(side="top")
        frame3.pack(expand=True, side="top")
        frame1.pack(expand=True, fill="both", side="top")

        # Main widget
        self.mainwindow = self.about_screen

    def center_window(self):
        if self.mainwindow.winfo_ismapped():
            min_w, min_h = self.mainwindow.wm_minsize()
            max_w, max_h = self.mainwindow.wm_maxsize()
            screen_w = self.mainwindow.winfo_screenwidth()
            screen_h = self.mainwindow.winfo_screenheight()
            final_w = min(
                screen_w,
                max_w,
                max(
                    min_w,
                    self.mainwindow.winfo_width(),
                    self.mainwindow.winfo_reqwidth(),
                ),
            )
            final_h = min(
                screen_h,
                max_h,
                max(
                    min_h,
                    self.mainwindow.winfo_height(),
                    self.mainwindow.winfo_reqheight(),
                ),
            )
            x = (screen_w // 2) - (final_w // 2)
            y = (screen_h // 2) - (final_h // 2)
            geometry = f"{final_w}x{final_h}+{x}+{y}"

            def set_geometry():
                self.mainwindow.geometry(geometry)

            self.mainwindow.after_idle(set_geometry)
        else:
            # Window is not mapped, wait and try again later.
            self.mainwindow.after(5, self.center_window)

    def run(self, center=False):
        if center:
            self.center_window()
        self.mainwindow.mainloop()


if __name__ == "__main__":
    app = AboutScreenUI()
    app.run()
