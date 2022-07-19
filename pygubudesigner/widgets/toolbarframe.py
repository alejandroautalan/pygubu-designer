#
# Copyright 2012-2022 Alejandro Autalán
#
# This program is free software: you can redistribute it and/or modify it
# under the terms of the GNU General Public License version 3, as published
# by the Free Software Foundation.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranties of
# MERCHANTABILITY, SATISFACTORY QUALITY, or FITNESS FOR A PARTICULAR
# PURPOSE.  See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along
# with this program.  If not, see <http://www.gnu.org/licenses/>.

import tkinter as tk
import tkinter.ttk as ttk

from pygubu.binding import ApplicationLevelBindManager as BindManager


class ToolbarFrame(ttk.Frame):
    BTN_LEFT_STYLE = "BtnLeft.ToolbarFrame.Toolbutton"
    BTN_RIGHT_STYLE = "btnRight.ToolbarFrame.Toolbutton"

    def __init__(self, master=None, **kw):
        ttk.Frame.__init__(self, master, **kw)
        # btonbar = ttk.Frame(master)
        fvport = ttk.Frame(self)
        fcontent = ttk.Frame(fvport)
        fcontent.config(height="50", width="30", padding=0)
        fcontent.place(
            anchor="nw", x="0", y="0", bordermode="inside", relheight=1
        )
        fvport.config(height="50", width="30")
        fvport.pack(expand="true", fill="both", side="left")
        fcontrols = ttk.Frame(self)
        bsleft = ttk.Button(fcontrols)
        bsleft.config(
            text="<", width="1", takefocus=True, style=self.BTN_LEFT_STYLE
        )
        bsleft.pack(expand="true", fill="y", side="left")
        bsleft.configure(command=self.scroll_left)
        bsright = ttk.Button(fcontrols)
        bsright.config(
            text=">", width="1", takefocus=True, style=self.BTN_RIGHT_STYLE
        )
        bsright.pack(expand="true", fill="y", side="left")
        bsright.configure(command=self.scroll_right)
        fcontrols.config(height="50", width="50")
        fcontrols.pack(fill="y", side="left")
        # btonbar.config(height='50', width='320')
        # btonbar.pack(expand='true', fill='x', side='top')
        self.config(height="200", width="20")

        self.controls_visible = True
        self.controls_required = False
        self._scrollRecurse = 0
        self.timer = None
        self.fcontrols = fcontrols
        self.fvport = fvport
        self.fcontent = fcontent
        self.fcstart = 0
        self.SCROLL_INCREMENT = 50
        fvport.bind("<Configure>", self._reposition)
        fcontent.bind("<Configure>", self._reposition)
        self._configure_mousewheel()

    def child_master(self):
        return self.fcontent

    def _configure_mousewheel(self):
        BindManager.init_mousewheel_binding(self)
        self.bind(
            "<Enter>",
            lambda event: BindManager.mousewheel_bind(self),
            add="+",
        )
        self.bind(
            "<Leave>", lambda event: BindManager.mousewheel_unbind(), add="+"
        )
        self.on_mousewheel = BindManager.make_onmousewheel_cb(self, "x", 2)

    def xview(self, mode=None, value=None, units=None):
        if mode == "scroll":
            if value > 0:
                self.scroll_right()
            else:
                self.scroll_left()

    def toggle_controls(self):
        self.controls_visible = not self.controls_visible
        if self.controls_visible:
            self.fcontrols.pack(side="left", fill="y")
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
        # fch = self.fcontent.winfo_reqheight()
        fctlw = self.fcontrols.winfo_reqwidth()
        # fctlh = self.fcontrols.winfo_reqheight()
        myw = self.winfo_width()
        # myh = self.winfo_height()
        vpw = self.fvport.winfo_width()
        # vph = self.fvport.winfo_height()

        self.SCROLL_INCREMENT = vpw // 3
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


if __name__ == "__main__":
    root = tk.Tk()
    widget = ToolbarFrame(root)
    widget.pack(expand=True, fill="both")
    root.mainloop()
