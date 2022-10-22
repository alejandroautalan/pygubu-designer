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
import sys
import tkinter as tk
import tkinter.ttk as ttk
from collections import OrderedDict
from functools import partial

from pygubu.stockimage import StockImage

import pygubudesigner.actions as actions
from pygubudesigner.widgets.ttkstyleentry import TtkStylePropertyEditor

from .preview import MenuPreview, Preview

logger = logging.getLogger(__name__)


class PreviewHelper:
    indicators_tag = ("top", "bottom", "left", "right")

    def __init__(self, canvas, context_menu_method, center_window_check):
        self.canvas = canvas
        # The method we will call to show the context menu
        self.show_context_menu = context_menu_method

        # A method that will check if we should center
        # the toplevel preview window or not.
        self.center_window_check = center_window_check

        self.previews = OrderedDict()
        self.padding = 20
        self.indicator_stroke = 2
        self.indicator_offset = 2
        self.indicators = None
        self._sel_id = None
        self._sel_widget = None
        self.toplevel_previews = []
        self.resource_paths = []

        self._moving = False
        self._last_event = None
        self._objects_moving = None
        canvas.bind("<Button-1>", self.click_handler)
        canvas.bind("<Button-1>", lambda e: canvas.focus_set(), add=True)
        canvas.bind("<ButtonRelease-1>", self.release_handler)
        canvas.bind("<Motion>", self.motion_handler)
        canvas.bind("<4>", lambda event: canvas.yview("scroll", -1, "units"))
        canvas.bind("<5>", lambda event: canvas.yview("scroll", 1, "units"))
        self._create_indicators()

        self.style = ttk.Style()
        self.style.configure("PreviewFrame.TFrame", background="lightgreen")

        self.selected_widget = None
        canvas.bind_all(
            actions.PREVIEW_TOPLEVEL_CLOSE_ALL,
            lambda e: self.close_toplevel_previews(),
        )

    def add_resource_path(self, path):
        self.resource_paths.append(path)

    def motion_handler(self, event):
        if not self._moving:
            c = event.widget
            x = c.canvasx(event.x)
            y = c.canvasy(event.y)
            if self._over_resizer(x, y):
                c.configure(cursor="fleur")
            else:
                c.configure(cursor="")
        else:
            dx = event.x - self._last_event.x
            dy = event.y - self._last_event.y
            self._last_event = event
            if dx or dy:
                self.resize_preview(dx, dy)

    def click_handler(self, event):
        c = event.widget
        x = c.canvasx(event.x)
        y = c.canvasy(event.y)

        if self._over_resizer(x, y):
            ids = c.find_overlapping(x, y, x, y)
            if ids:
                self._moving = True
                self._objects_moving = ids
                c.configure(cursor="fleur")
                self._last_event = event

    def release_handler(self, event):
        self._objects_moving = None
        self._moving = False

    def _over_resizer(self, x, y):
        "Returns True if mouse is over a resizer"

        over_resizer = False
        c = self.canvas
        ids = c.find_overlapping(x, y, x, y)
        if ids:
            o = ids[0]
            tags = c.gettags(o)
            if "resizer" in tags:
                over_resizer = True
        return over_resizer

    def resize_preview(self, dw, dh):
        "Resizes preview that is currently dragged"

        # identify preview
        if self._objects_moving:
            id_ = self._objects_moving[0]
            tags = self.canvas.gettags(id_)
            for tag in tags:
                if tag.startswith("preview_"):
                    _, ident = tag.split("preview_")
                    preview = self.previews[ident]
                    preview.resize_by(dw, dh)
                    self.move_previews()
                    break
        self._update_cregion()

    def _update_cregion(self):
        # update canvas scrollregion
        bbox = self.canvas.bbox(tk.ALL)
        padd = 20
        if bbox is not None:
            region = (0, 0, bbox[2] + padd, bbox[3] + padd)
            self.canvas.configure(scrollregion=region)

    def move_previews(self):
        "Move previews after a resize event"

        # calculate new positions
        min_y = self._calc_preview_ypos()
        for idx, (key, p) in enumerate(self.previews.items()):
            new_dy = min_y[idx] - p.y
            self.previews[key].move_by(0, new_dy)
        self._update_cregion()
        self.show_selected(self._sel_id, self._sel_widget)

    def _calc_preview_ypos(self):
        "Calculates the previews positions on canvas"

        y = 10
        min_y = [y]
        for k, p in self.previews.items():
            y += p.height() + self.padding
            min_y.append(y)
        return min_y

    def _get_slot(self):
        "Returns the next coordinates for a preview"

        x = y = 10
        for k, p in self.previews.items():
            y += p.height() + self.padding
        return x, y

    def draw(self, identifier, widget_id, uidefinition, wclass):
        logger.debug("Preview.draw: %s,%s", identifier, widget_id)
        preview_class = Preview
        if wclass == "tk.Menu":
            preview_class = MenuPreview
        if identifier not in self.previews:
            x, y = self._get_slot()
            self.previews[identifier] = preview = preview_class(
                identifier, self.canvas, x, y, self.resource_paths
            )
        else:
            preview = self.previews[identifier]
        preview.update(widget_id, uidefinition)
        self.reset_selected(identifier)
        self.move_previews()

        if True:
            # we are allways recreating full preview.
            # create callback and bind widgets
            def callback(event, self=self, previewid=identifier):
                self.preview_click_handler(previewid, event)

            widget = preview.root_widget
            self.bind_preview_widget(widget, callback)

    def _create_indicators(self):
        # selected indicators
        anchors = {"top": tk.SW, "bottom": tk.NW, "left": tk.NE, "right": tk.NW}
        self.indicators = {}
        for tag in anchors:
            frame = ttk.Frame(
                self.canvas,
                style="PreviewIndicator.TFrame",
                width=1,
                height=1,
                borderwidth=0,
            )
            self.canvas.create_window(
                -10, -10, window=frame, anchor=anchors[tag], tags=tag
            )
            self.indicators[tag] = frame

    def _update_indicator_coords(self, tag, widget):
        x = y = 0
        wx = widget.winfo_rootx()
        wy = widget.winfo_rooty()
        ww = widget.winfo_width()
        wh = widget.winfo_height()
        cx = self.canvas.winfo_rootx()
        cy = self.canvas.winfo_rooty()
        x = wx - cx
        y = wy - cy
        x, y = self.canvas.canvasx(x), self.canvas.canvasy(y)

        wx2 = x + ww
        wy2 = y + wh
        stroke = self.indicator_stroke
        offset = self.indicator_offset
        if tag == "top":
            ix = x - (stroke + offset)
            iy = y - offset
            iw = ww + stroke * 2 + offset * 2
            ih = stroke
        if tag == "bottom":
            ix = x - (stroke + offset)
            iy = wy2 + offset
            iw = ww + stroke * 2 + offset * 2
            ih = stroke
        if tag == "right":
            ix = wx2 + offset
            iy = y - (stroke + offset)
            iw = stroke
            ih = wh + stroke * 2 + offset * 2
        if tag == "left":
            ix = x - offset
            iy = y - (stroke + offset)
            iw = stroke
            ih = wh + stroke * 2 + offset * 2

        ox, oy = self.canvas.coords(tag)
        self.canvas.move(tag, ix - ox, iy - oy)
        f = self.indicators[tag]
        f.configure(width=iw, height=ih)
        f.lift()

    def _update_style_editor(self, widget):
        """Setup TtkStylePropertyEditor with the real winfo_class and class name."""
        hints = (widget.winfo_class(), widget.__class__.__name__)
        TtkStylePropertyEditor.set_filter_hints(hints)

    def show_selected(self, identifier, selected_id=None):
        canvas = self.canvas
        if selected_id is None:
            for indicator in self.indicators_tag:
                canvas.itemconfigure(indicator, state=tk.HIDDEN)
        elif identifier in self.previews:
            for indicator in self.indicators_tag:
                canvas.itemconfigure(indicator, state=tk.NORMAL)
            preview = self.previews[identifier]
            canvas.update_idletasks()
            preview.show_selected(selected_id)
            widget = preview.get_widget_by_id(selected_id)
            for tag in self.indicators:
                self._update_indicator_coords(tag, widget)
            self._update_style_editor(widget)
        self._sel_id = identifier
        self._sel_widget = selected_id

    def delete(self, identifier):
        if identifier in self.previews:
            preview = self.previews[identifier]
            preview.erase()
            del self.previews[identifier]
            self.reset_selected(identifier)
            self.move_previews()

    def reset_selected(self, identifier):
        if identifier == self._sel_id:
            self._sel_id = None
            self._sel_widget = None

    def remove_all(self):
        for identifier in list(self.previews):
            self.delete(identifier)
        self.resource_paths = []

    def preview_in_toplevel(self, identifier, widget_id, uidefinition):
        preview = self.previews[identifier]
        top = preview.create_toplevel(widget_id, uidefinition)
        self.toplevel_previews.append(top)

        # Check if we should center the preview window
        if self.center_window_check():
            Preview.center_window_active_monitor(top)

    def close_toplevel_previews(self):
        for top in self.toplevel_previews:
            top.destroy()
        self.toplevel_previews = []

    def preview_click_handler(self, preview_id, event=None):
        preview = self.previews[preview_id]
        wid = preview.builder.get_widget_id(event.widget)
        if wid is not None:
            self.selected_widget = wid
            self.canvas.event_generate("<<PreviewItemSelected>>")
            self.canvas.focus_set()  # add focus to canvas

    def bind_preview_widget(self, widget, callback):
        widget.bind("<Button-1>", callback)

        # The function that will be called when a right-click occurs.
        # The second argument (callback) is used to select the widget before
        # showing the context menu.
        right_click_func = partial(
            self.on_right_clicked_preview_widget, callback
        )

        # For right-clicking - bind to button2 for macos and button3 for a
        # different OS.
        if sys.platform == "darwin":
            widget.bind("<Button-2>", right_click_func)
        else:
            widget.bind("<Button-3>", right_click_func)

        for w in widget.winfo_children():
            self.bind_preview_widget(w, callback)

    def on_right_clicked_preview_widget(self, callback, event):
        """
        A widget in the preview canvas has been right-clicked.

        Arguments:

        - Callback: we need to run this method before we show the context menu.
        This method will cause the widget to be selected.

        - Event: a normal event argument. This will tell us which widget was right-clicked
        on if we ever need that info.
        """

        # Select the widget that was right-clicked.
        callback(event)

        # Show the right-click context menu.
        self.show_context_menu(event)
