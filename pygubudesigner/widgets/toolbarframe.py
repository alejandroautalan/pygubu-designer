try:
    import tkinter as tk
    import tkinter.ttk as ttk
except:
    import Tkinter as tk
    import ttk


class ToolbarFrame(ttk.Frame):
    
    def __init__(self, master=None, **kw):
        ttk.Frame.__init__(self, master, **kw)
        #btonbar = ttk.Frame(master)
        fvport = ttk.Frame(self)
        fcontent = ttk.Frame(fvport)
        fcontent.config(height='50', width='30', padding=0)
        fcontent.place(anchor='nw', x='0', y='0', bordermode='inside',
                       relheight=1)
        fvport.config(height='50', width='30')
        fvport.pack(expand='true', fill='both', side='left')
        fcontrols = ttk.Frame(self)
        bsleft = ttk.Button(fcontrols)
        bsleft.config(text='<', width='1', takefocus=True)
        bsleft.pack(expand='true', fill='y', side='left')
        bsleft.configure(command=self.scroll_left)
        bsright = ttk.Button(fcontrols)
        bsright.config(text='>', width='1', takefocus=True)
        bsright.pack(expand='true', fill='y', side='left')
        bsright.configure(command=self.scroll_right)
        fcontrols.config(height='50', width='50')
        fcontrols.pack(fill='y', side='left')
        #btonbar.config(height='50', width='320')
        #btonbar.pack(expand='true', fill='x', side='top')
        self.config(height='200', width='20')
        
        self.controls_visible = True
        self.controls_required = False
        self._scrollRecurse = 0
        self.timer = None
        self.fcontrols = fcontrols
        self.fvport = fvport
        self.fcontent = fcontent
        self.fcstart = 0
        self.SCROLL_INCREMENT = 50
        fvport.bind('<Configure>', self._reposition)
        fcontent.bind('<Configure>', self._reposition)
    
    def child_master(self):
        return self.fcontent
    
    def toggle_controls(self):
        self.controls_visible = not self.controls_visible
        if self.controls_visible:
            self.fcontrols.pack(side='left', fill='y')
        else:
            self.fcontrols.pack_forget()
    
    def reposition(self):
        if self.timer is None:
            self.timer = self.after_idle(self._reposition)
    
    def _reposition(self, event):
        self.timer = None

        # Call update_idletasks to make sure that the containing frame
        # has been resized before we attempt to set the scrollbars.
        # Otherwise the scrollbars may be mapped/unmapped continuously.
        self._scrollRecurse = self._scrollRecurse + 1
        self.update_idletasks()
        self._scrollRecurse = self._scrollRecurse - 1
        if self._scrollRecurse != 0:
            return
        
        fcw = self.fcontent.winfo_reqwidth()
        #fch = self.fcontent.winfo_reqheight()
        fctlw = self.fcontrols.winfo_reqwidth()
        #fctlh = self.fcontrols.winfo_reqheight()
        myw = self.winfo_width()
        #myh = self.winfo_height()
        vpw = self.fvport.winfo_width()
        #vph = self.fvport.winfo_height()
        
        self.SCROLL_INCREMENT = vpw//3
        hole = myw - fctlw
        diff = hole - fcw
        
        if diff < 0:
            # requires controls
            self.controls_required = True
        else:
            # remove controls
            self.controls_required = False
            if self.fcstart != 0:
                self.fcstart = 0
                self.fcontent.place(x=self.fcstart)
        
        if self.controls_required != self.controls_visible:
            self.toggle_controls()

    def scroll_right(self):
        newstart = self.fcstart - self.SCROLL_INCREMENT
        cw = self.fcontent.winfo_reqwidth()
        limit = cw - self.SCROLL_INCREMENT
        if newstart > -(limit):
            self.fcstart = newstart
            self.fcontent.place(x=self.fcstart)

    def scroll_left(self):
        newstart = self.fcstart + self.SCROLL_INCREMENT
        if newstart <= 0:
            self.fcstart = newstart
            self.fcontent.place(x=self.fcstart)


if __name__ == '__main__':
    root = tk.Tk()
    widget = ToolbarFrame(root)
    widget.pack(expand=True, fill='both')
    root.mainloop()


