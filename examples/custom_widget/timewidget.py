import tkinter as tk
import tkinter.ttk as ttk


class TimeWidget(ttk.Frame):
    """HH:MM:SS 24 hours widget"""

    def __init__(self, master=None, **kw):
        ttk.Frame.__init__(self, master, **kw)
        # subwidgets
        self.whour = o = ttk.Entry(self, width=4, justify="right")
        o.grid(row=0, column=0, sticky="nswe")
        o = ttk.Label(self, text="h", width=2)
        o.grid(row=0, column=1)
        self.wmin = o = ttk.Entry(self, width=4, justify="right")
        o.grid(row=0, column=2, sticky="nswe")
        o = ttk.Label(self, text="m", width=2)
        o.grid(row=0, column=3)
        self.wsec = o = ttk.Entry(self, width=4, justify="right")
        o.grid(row=0, column=4, sticky="nswe")
        o = ttk.Label(self, text="s")
        o.grid(row=0, column=5)

        self.columnconfigure(0, weight=1)
        self.columnconfigure(2, weight=1)
        self.columnconfigure(4, weight=1)
        self.configure(hour=0, minute=0, second=0)

    def configure(self, cnf=None, **kw):
        key = "hour"
        if key in kw:
            self.whour.delete(0, "end")
            self.whour.insert(0, kw[key])
            del kw[key]
        key = "minute"
        if key in kw:
            self.wmin.delete(0, "end")
            self.wmin.insert(0, kw[key])
            del kw[key]
        key = "second"
        if key in kw:
            self.wsec.delete(0, "end")
            self.wsec.insert(0, kw[key])
            del kw[key]
        ttk.Frame.configure(self, cnf, **kw)

    config = configure

    def cget(self, key):
        option = "hour"
        if key == option:
            return self.whour.get()
        option = "minute"
        if key == option:
            return self.wmin.get()
        option = "second"
        if key == option:
            return self.wsec.get()
        option = "value"
        if key == option:
            return self.whour.get(), self.wmin.get(), self.wsec.get()
        return ttk.Frame.cget(self, key)


if __name__ == "__main__":
    root = tk.Tk()
    time = TimeWidget(root)
    time.grid()
    time.configure(hour=22, minute=30)

    def showvalue():
        print(time.cget("value"))
        print(time.cget("hour"))
        print(time.cget("minute"))
        print(time.cget("second"))

    b = ttk.Button(root, text="Get value", command=showvalue)
    b.grid()
    root.mainloop()
