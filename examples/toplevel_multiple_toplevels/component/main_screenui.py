#!/usr/bin/python3
import tkinter as tk
import tkinter.ttk as ttk


class MainScreenUI:
    def __init__(self, master=None, data_pool=None):
        # build ui
        self.root = tk.Tk(master)
        self.root.configure(height=200, width=200)
        self.root.minsize(800, 600)
        self.root.title("Main window")
        frame1 = ttk.Frame(self.root)
        frame1.configure(height=200, padding="5p", width=200)
        self.fmiddle = ttk.Frame(frame1, name="fmiddle")
        self.fmiddle.configure(height=200, width=200)
        canvas2 = tk.Canvas(self.fmiddle)
        canvas2.configure(background="#5600d9")
        canvas2.pack(expand=True, fill="both", side="top")
        self.fmiddle.pack(expand=True, fill="both", side="top")
        self.fbottom = ttk.Frame(frame1, name="fbottom")
        self.fbottom.configure(height=200, width=200)
        canvas3 = tk.Canvas(self.fbottom)
        canvas3.configure(background="#006b0b", height=32)
        canvas3.pack(fill="x", side="top")
        self.fbottom.pack(fill="x", side="top")
        label2 = ttk.Label(frame1)
        label2.configure(
            background="#5600d9",
            font="{Helvetica} 36 {}",
            foreground="#ffffae",
            text="MAIN WINDOW",
        )
        label2.place(anchor="center", relx=0.5, rely=0.5, x=0, y=0)
        frame1.pack(expand=True, fill="both", side="top")
        menu1 = tk.Menu(self.root)
        menu1.configure(tearoff=False)

        def mi_quit_cmd(itemid="mi_quit"):
            self.on_menuitem_clicked(itemid)

        menu1.add("command", command=mi_quit_cmd, label="Quit")
        menu1.add("separator")

        def mi_config_cmd(itemid="mi_config"):
            self.on_menuitem_clicked(itemid)

        menu1.add("command", command=mi_config_cmd, label="Configure")

        def mi_about_cmd(itemid="mi_about"):
            self.on_menuitem_clicked(itemid)

        menu1.add("command", command=mi_about_cmd, label="About")
        self.root.configure(menu=menu1)

        # Main widget
        self.mainwindow = self.root

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

    def on_menuitem_clicked(self, itemid):
        pass


if __name__ == "__main__":
    app = MainScreenUI()
    app.run()
