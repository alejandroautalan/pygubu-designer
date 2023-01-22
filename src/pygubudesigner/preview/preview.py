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

import logging
import re
import sys
import tkinter as tk
import tkinter.ttk as ttk

import pygubu
import screeninfo

from pygubu.component.plugin_manager import PluginManager
from pygubu.utils.font import tkfontstr_to_dict
from pygubudesigner.widgetdescr import WidgetMeta
from .builder import BuilderForPreview

logger = logging.getLogger(__name__)


class Preview:
    def __init__(self, id_, canvas, x=0, y=0, rpaths=None):
        self.id = f"preview_{id_}"
        self.x = x
        self.y = y
        self.w = 10
        self.h = 10
        self.min_w = self.w
        self.min_h = self.h
        self.resizer_h = 10
        self.canvas = canvas
        self.shapes = {}
        self.widget_name = ""
        self._create_shapes()
        # --------
        self.builder = None
        self.canvas_window = None
        self._resource_paths = rpaths if rpaths is not None else []
        # --
        self.selected_widget = None
        self.root_widget = None

    def width(self):
        return self.w

    def height(self):
        return self.h + self.resizer_h

    def _create_builder(self):
        b = BuilderForPreview()
        for p in self._resource_paths:
            b.add_resource_path(p)
        return b

    def _create_shapes(self):
        # Preview box
        c = self.canvas
        x, y, x2, y2 = (-1001, -1000, -1001, -1000)
        s1 = c.create_rectangle(
            x, y, x2, y2, width=2, outline="blue", tags=self.id
        )
        s2 = c.create_rectangle(
            x, y, x2, y2, fill="blue", outline="blue", tags=(self.id, "resizer")
        )
        s3 = c.create_text(
            x, y, text="widget_id", anchor=tk.NW, fill="white", tags=self.id
        )
        s4 = c.create_window(x, y, anchor=tk.NW, tags=self.id)
        self.shapes = {"outline": s1, "resizer": s2, "text": s3, "window": s4}
        self.draw()

    def erase(self):
        self.canvas_window.destroy()
        for key, sid in self.shapes.items():
            self.canvas.delete(sid)

    def draw(self):
        c = self.canvas
        x, y, x2, y2 = (self.x, self.y, self.x + self.w, self.y + self.h)
        c.coords(self.shapes["outline"], x, y, x2, y2)
        tbbox = c.bbox(self.shapes["text"])
        tw, th = tbbox[2] - tbbox[0] + 10, tbbox[3] - tbbox[1] + 8
        self.resizer_h = th
        rx2 = self.x + self.w
        ry2 = self.y + self.h + self.resizer_h
        rx = rx2 - tw
        ry = self.y + self.h
        c.coords(self.shapes["resizer"], rx, ry, rx2, ry2)
        tx = rx + 5
        ty = ry + 6
        c.coords(self.shapes["text"], tx, ty)
        c.coords(self.shapes["window"], x, y)
        text = f"{self.widget_name} ({self.w}x{self.h})"
        c.itemconfigure(self.shapes["text"], text=text)

    def move_by(self, dx, dy):
        self.x += dx
        self.y += dy
        self.draw()

    def resize_to(self, w, h):
        self.resize_by(w - self.w, h - self.h)

    def resize_by(self, dw, dh):
        new_w = self.w + dw
        new_h = self.h + dh
        changed = False
        if new_w >= self.min_w:
            self.w = new_w
            changed = True
        if new_h >= self.min_h:
            self.h = new_h
            changed = True
        if changed:
            self.draw()
            self._resize_preview_window()

    def _resize_preview_window(self):
        if self.canvas_window:
            self.canvas_window.configure(width=self.w, height=self.h)

    def update(self, widget_id, uidefinition):
        # delete current preview
        # FIXME maybe do something to update preview without re-creating all ?
        del self.builder
        self.builder = None
        self.canvas.itemconfigure(self.shapes["window"], window="")
        if self.canvas_window:
            self.canvas_window.destroy()

        # Create preview
        canvas_window = ttk.Frame(self.canvas, style="PreviewFrame.TFrame")
        self.widget_name = widget_id

        self._preview_widget = self.create_preview_widget(
            canvas_window, widget_id, uidefinition
        )
        self.root_widget = self._preview_widget

        self.canvas_window = canvas_window
        self.canvas.itemconfigure(self.shapes["window"], window=canvas_window)
        canvas_window.update_idletasks()
        if canvas_window.pack_slaves():
            canvas_window.pack_propagate(0)
        elif canvas_window.grid_slaves():
            canvas_window.grid_propagate(0)
        self.min_w = self._get_wreqwidth()
        self.min_h = self._get_wreqheight()
        self.w = self.min_w * 2
        self.h = self.min_h * 2
        self.resize_to(self.min_w, self.min_h)

    def create_preview_widget(self, parent, widget_id, uidefinition):
        self.builder = self._create_builder()
        self.builder.uidefinition = uidefinition
        widget = self.builder.get_object(widget_id, parent)
        return widget

    def get_widget_by_id(self, widget_id):
        return self.builder.get_object(widget_id)

    def show_selected(self, select_id):
        self.builder.show_selected(select_id)

    def create_toplevel(self, widget_id, uidefinition):
        # Create preview
        wmeta = uidefinition.get_widget(widget_id)
        builder_uid = wmeta.classname

        # prepare builder
        builder = pygubu.Builder()
        builder.uidefinition = uidefinition

        # Ask plugins for toplevel preview
        top = PluginManager.get_toplevel_preview_for(
            builder_uid, widget_id, builder, self.canvas
        )
        if top is None:
            # Default preview
            top = tk.Toplevel(self.canvas)
            top.columnconfigure(0, weight=1)
            top.rowconfigure(0, weight=1)
            builder.get_object(widget_id, top)
        return top

    def _get_wreqwidth(self):
        return self._preview_widget.winfo_reqwidth()

    def _get_wreqheight(self):
        return self._preview_widget.winfo_reqheight()

    @staticmethod
    def center_window_active_monitor(window: tk.Toplevel) -> bool:
        """
        Center the given window on the monitor that the user's mouse pointer is on.

        For example: if the mouse pointer is on the second monitor, then center
        the given window on the second monitor.

        Arguments:
        - window: a toplevel window that we want to center

        Returns: bool
        True : if the center calculations were done successfully and the window
        has been centered on a monitor.

        False : if for some reason the mouse pointer wasn't found on any of the monitors (shouldn't happen).
        """

        # We need to call the update_idletasks() method before we try and get the window's size,
        # because if the window hasn't been drawn on the screen yet, we won't get the proper dimensions
        # when we try and use winfo_width() and winfo_height().
        # After we run .update_idletasks(), then winfo_width() and winfo_height()
        # will work as expected.
        window.update_idletasks()

        # Hide the toplevel window for now (it will help to minimize flickering when it
        # moves to its center position later on)
        window.withdraw()

        # Get a list of monitors
        monitors = screeninfo.get_monitors()

        mon_sizes = []
        combined_width_so_far = 0

        # Get a list of widths for each monitor.
        # For example, if there are 2 monitors (each 1920x1080),
        # then find out the width of each (incrementing over to the next).
        # Example: first monitor: 0 to 1920 (width), second monitor: 1921x3840

        # We will need to create a tuple that looks like this:
        # (from_x, to_x, center_x, center_y)

        # 'from_x' and 'to_x' represent a monitor's width from 'from_x' to 'to_x'.
        # For example: if the first monitor is 1920 pixels wide, then 'from_x' will be 0, and 'to_x' will be 1920.

        # Then, if the second monitor is also 1920 pixels wide, then for the second monitor,
        # 'from_x' will be 1921, to_x' will be 3840.

        # So if the mouse pointer's X position is within that monitor's 'from_x' to 'to_x', then we will consider
        # the mouse pointer to be inside that monitor (because the mouse pointer's X was inside the 'from_x'
        # and 'to_x' of that monitor's tuple value).

        # center_x, center_y are the center width and center height, respectively,
        # of the single monitor that the mouse pointer is in.

        # Enumerate over each monitor
        for idx, m in enumerate(monitors):

            # If it's the first monitor, then we don't need to add +1 for the first '_from_x'
            if idx == 0:
                _from = 0
                _to = m.width
            else:
                # Add a +1 so that it continues 1 pixel more for the next monitor, so that two monitors don't overlap.
                _from = combined_width_so_far + 1
                _to = combined_width_so_far + m.width

            # Get the center x and y of the current monitor we're looping on.
            center_x = combined_width_so_far + (m.width // 2)
            center_y = m.height // 2

            # We will use this later to find out which of these monitors the specified window is in.
            mon_sizes.append((_from, _to, center_x, center_y))

            # As we continue enumerating over each monitor, the 'from_x' has to continue
            # where the last monitor's width left off.

            # So we keep summing up the width of each monitor that we enumerate so the
            # next monitor can start its 'from_x', where the last monitor's width ended, + 1.
            combined_width_so_far += m.width

        # Find the X position of the mouse pointer.
        # If there are multiple monitors, in Windows it will have a combined width X position.
        mouse_pointer_x = window.winfo_pointerx()

        # Find out which monitor (width-range) the X of the window is on, then center it based on that.
        for size_range in mon_sizes:

            # Is the mouse pointer inside the current monitor in the loop?
            if size_range[0] <= mouse_pointer_x <= size_range[1]:
                win_x_center = size_range[2] - (window.winfo_width() // 2)
                win_y_center = size_range[3] - (window.winfo_height() // 2)

                # Center the window
                window.geometry(f"+{win_x_center}+{win_y_center}")

                # Now show the toplevel window, because we're done centering it.
                window.deiconify()

                return True
        else:
            return False


class DefaultMenuPreview(Preview):
    def create_preview_widget(self, parent, widget_id, uidefinition):
        self.builder = self._create_builder()
        self.builder.uidefinition = uidefinition
        menubutton = ttk.Menubutton(parent, text="Menu preview")
        menubutton.grid()
        widget = self.builder.get_object(widget_id, menubutton)
        menubutton.configure(menu=widget)
        return menubutton

    def create_toplevel(self, widget_id, uidefinition):
        # Create preview
        builder = pygubu.Builder()
        builder.uidefinition = uidefinition
        top = tk.Toplevel(self.canvas)
        top.columnconfigure(0, weight=1)
        top.rowconfigure(0, weight=1)

        menu = builder.get_object(widget_id, top)
        top["menu"] = menu
        return top

    def resize_by(self, dw, hw):
        return


class OnCanvasMenuPreview(Preview):
    fonts = {}

    def __init__(self, id_, canvas, x=0, y=0, rpaths=None):
        super().__init__(id_, canvas, x, y, rpaths)
        self._menu = None
        self._cwidth = 0
        self._cheight = 0

    def _get_wreqwidth(self):
        return self._cwidth

    def _get_wreqheight(self):
        return self._cheight

    def _get_font(self, font):
        fontname = family = "TkMenuFont"
        size = 12
        modifiers = ""
        tclobject = False

        if font and isinstance(font, str):
            fontname = family = font
        elif isinstance(font, tk._tkinter.Tcl_Obj):
            fontname = family = str(font)
            tclobject = True
        elif isinstance(font, tuple):
            fontname = str(font[4])
            tclobject = True
        if tclobject:
            fd = tkfontstr_to_dict(fontname)
            family = fd["family"]
            size_ = fd["size"]
            if size_:
                try:
                    size = int(size_)
                    # limit font size to 128 for invalid entries in the
                    # option database values
                    if size > 128:
                        size = 12
                except TypeError:
                    pass
            modifiers = fd["modifiers"] if fd["modifiers"] else ""
        if fontname not in OnCanvasMenuPreview.fonts:
            weight = "bold" if "bold" in modifiers else "normal"
            slant = "italic" if "italic" in modifiers else "roman"
            underline = "1" if "underline" in modifiers else "0"
            overstrike = "1" if "overstrike" in modifiers else "0"
            kw = {
                "family": family,
                "weight": weight,
                "slant": slant,
                "underline": underline,
                "overstrike": overstrike,
            }
            if size:
                kw["size"] = size
            OnCanvasMenuPreview.fonts[fontname] = tk.font.Font(**kw)
        return OnCanvasMenuPreview.fonts[fontname]

    def _calculate_menu_wh(self):
        """Calculate menu widht and height."""
        w = iw = 50
        h = ih = 0
        # menu.index returns None if there are no choices
        index = self._menu.index(tk.END)
        index = index if index is not None else 0
        count = index + 1

        # First calculate using the font paramters of root menu:
        font = self._menu.cget("font")
        font = self._get_font(font)
        for i in range(0, count):
            mtype = self._menu.type(i)
            if mtype == "tearoff":
                continue
            label = "default"
            ifont = "TkMenuFont"
            if mtype != "separator":
                label = self._menu.entrycget(i, "label")
                ifont = self._menu.entrycget(i, "font")
            wpx = font.measure(label)
            hpx = font.metrics("linespace")
            w += wpx
            if hpx > h:
                h = hpx * 2
            # Calculate using font configured for each subitem
            ifont = self._get_font(ifont)
            wpx = ifont.measure(label)
            hpx = ifont.metrics("linespace")
            iw += wpx
            if hpx > ih:
                ih = hpx * 2
        # Then compare 2 sizes and use the greatest
        w = max(w, iw, 100)
        h = max(h, ih, 25)
        self._cwidth = w + int(w * 0.25)
        self._cheight = h + int(h * 0.25)

    def create_preview_widget(self, parent, widget_id, uidefinition):
        container = tk.Frame(parent, container=True, height=50)
        container.pack(fill="both", expand=True)

        self._top = top = tk.Toplevel(parent, use=container.winfo_id())
        top.maxsize(2048, 50)
        top.resizable(width=True, height=False)
        top.update()

        self.builder = self._create_builder()
        self.builder.uidefinition = uidefinition
        self._menu = widget = self.builder.get_object(widget_id, top)
        top.configure(menu=widget)
        self._calculate_menu_wh()
        return parent

    def create_toplevel(self, widget_id, uidefinition):
        # Create preview
        builder = pygubu.Builder()
        builder.uidefinition = uidefinition
        top = tk.Toplevel(self.canvas)
        top.columnconfigure(0, weight=1)
        top.rowconfigure(0, weight=1)

        menu = builder.get_object(widget_id, top)
        top["menu"] = menu
        return top


MenuPreview = DefaultMenuPreview
if sys.platform == "linux":
    MenuPreview = OnCanvasMenuPreview
