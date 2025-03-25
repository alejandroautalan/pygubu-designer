#!/usr/bin/python3
import tkinter as tk
import tkinter.ttk as ttk


#
# Begin image loader - Setup image_loader in derived class file
#
def default_image_loader(image_name):
    img = None
    try:
        img = tk.PhotoImage(file=image_name)
    except tk.TclError:
        pass
    return img


image_loader = default_image_loader
# End image loader


class SplashScreenUI:
    def __init__(self, master=None, data_pool=None):
        # build ui
        self.splash_screen = tk.Tk() if master is None else tk.Toplevel(master)
        self.splash_screen.configure(borderwidth=0, height=200, width=200)
        self.splash_screen.maxsize(699, 400)
        self.splash_screen.minsize(699, 400)
        self.splash_screen.overrideredirect("true")
        self.splash_screen.resizable(False, False)
        simage = ttk.Label(self.splash_screen)
        self.img_splash01 = image_loader("splash01.png")
        simage.configure(borderwidth=0, image=self.img_splash01)
        simage.place(
            anchor="nw",
            bordermode="ignore",
            relheight=1.0,
            relwidth=1.0,
            x=0,
            y=0,
        )
        self.progress_bar = ttk.Progressbar(
            self.splash_screen, name="progress_bar"
        )
        self.progress_bar.configure(mode="indeterminate", orient="horizontal")
        self.progress_bar.pack(
            fill="x", padx="5p", pady="5p 10p", side="bottom"
        )
        self.lbl_progress = ttk.Label(self.splash_screen, name="lbl_progress")
        self.txt_progress_var = tk.StringVar(value="Loading ... ")
        self.lbl_progress.configure(
            background="#262626",
            font="{TkTextFont } 16 {bold}",
            foreground="#d9ac00",
            relief="flat",
            text="Loading ... ",
            textvariable=self.txt_progress_var,
        )
        self.lbl_progress.pack(anchor="w", padx="5p", side="bottom")

        # Main widget
        self.mainwindow = self.splash_screen

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
    app = SplashScreenUI()
    app.run()
