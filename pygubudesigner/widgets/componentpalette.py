try:
    import tkinter as tk
    import tkinter.ttk as ttk
except:
    import Tkinter as tk
    import ttk
import pygubu.widgets.simpletooltip as tooltip
from .toolbarframe import ToolbarFrame


class ComponentPalette(ttk.Frame):
    def __init__(self, master=None, **kw):
        ttk.Frame.__init__(self, master, **kw)
        component_pallete = ttk.Frame(master)
        fbuttons = ttk.Frame(component_pallete)
        fbuttons.configure(padding=1)
        rb_tk = ttk.Radiobutton(fbuttons)
        self.gvalue = gvalue = tk.StringVar(value='')
        rb_tk.config(style='Toolbutton', text='tk', value='tk',
                     variable=gvalue, command=self._on_tk_clicked)
        rb_tk.pack(expand='true', fill='both', side='top')
        rb_ttk = ttk.Radiobutton(fbuttons)
        rb_ttk.config(style='Toolbutton', text='ttk', value='ttk',
                      variable=gvalue, command=self._on_ttk_clicked)
        rb_ttk.pack(expand='true', fill='both', side='top')
        fbuttons.pack(fill='y', side='left')
        fbntab = ttk.Frame(component_pallete)
        self.notebook = notebook = ttk.Notebook(fbntab)
        notebook.config(height='50', width='300',
                        style='ComponentPalette.TNotebook',
                        takefocus=True)
        notebook.pack(side='top', expand=True, fill='x')
        fbntab.config(height='200', width='200')
        fbntab.pack(side='left', expand=True, fill='x')
        component_pallete.config(height='200', padding='2', width='200')
        component_pallete.pack(side='top', expand=True, fill='x')
        
        self._tabs = {}
        self._buttons = []
        
    def _on_tk_clicked(self):
        self.show_group('tk')
        
    def _on_ttk_clicked(self):
        self.show_group('ttk')
    
    def add_tab(self, tabid, label):
        #frame_1 = ttk.Frame(self.notebook)
        frame_1 = ToolbarFrame(self.notebook)
        frame_1.configure(padding=2)
        frame_1.pack(expand='true', fill='both', side='top')
        self.notebook.add(frame_1, text=label)
        self._tabs[tabid] = frame_1
    
    def add_button(self, tabid, group, label, ttiplabel, image, callback):
        master = self._tabs[tabid].child_master()
        #master = self._tabs[tabid]
        b = ttk.Button(master, text=label, image=image,
                           style='ComponentPalette.Toolbutton', command=callback,
                           compound='top', takefocus=True)
        tooltip.create(b, ttiplabel)
        b.pack(side='left')
        self._buttons.append((b, group))
    
    def show_group(self, group):
        for b, g in self._buttons:
            if g == group:
                b.pack(side='left')
            else:
                b.pack_forget()
        self.gvalue.set(group)


if __name__ == '__main__':
    root = tk.Tk()
    widget = ComponentPallete(root)
    widget.pack(expand=True, fill='both')
    root.mainloop()


