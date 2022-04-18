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

from pygubudesigner.widgetdescr import WidgetMeta
from pygubudesigner.widgets.toplevelframe import ToplevelFramePreview

from .builder import BuilderForPreview

logger = logging.getLogger(__name__)

RE_FONT = re.compile(
    "(?P<family>\\{\\w+(\\w|\\s)*\\}|\\w+)\\s?(?P<size>-?\\d+)?\\s?(?P<modifiers>\\{\\w+(\\w|\\s)*\\}|\\w+)?"
)


class Preview:
    def __init__(self, id_, canvas, x=0, y=0, rpaths=None):
        self.id = f'preview_{id_}'
        self.x = x
        self.y = y
        self.w = 10
        self.h = 10
        self.min_w = self.w
        self.min_h = self.h
        self.resizer_h = 10
        self.canvas = canvas
        self.shapes = {}
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
        s1 = c.create_rectangle(x, y, x2, y2, width=2, outline='blue', tags=self.id)
        s2 = c.create_rectangle(
            x, y, x2, y2, fill='blue', outline='blue', tags=(self.id, 'resizer')
        )
        s3 = c.create_text(
            x, y, text='widget_id', anchor=tk.NW, fill='white', tags=self.id
        )
        s4 = c.create_window(x, y, anchor=tk.NW, tags=self.id)
        self.shapes = {'outline': s1, 'resizer': s2, 'text': s3, 'window': s4}
        self.draw()

    def erase(self):
        self.canvas_window.destroy()
        for key, sid in self.shapes.items():
            self.canvas.delete(sid)

    def draw(self):
        c = self.canvas
        x, y, x2, y2 = (self.x, self.y, self.x + self.w, self.y + self.h)
        c.coords(self.shapes['outline'], x, y, x2, y2)
        tbbox = c.bbox(self.shapes['text'])
        tw, th = tbbox[2] - tbbox[0] + 10, tbbox[3] - tbbox[1] + 6
        self.resizer_h = th
        rx2 = self.x + self.w
        ry2 = self.y + self.h + self.resizer_h
        rx = rx2 - tw
        ry = self.y + self.h
        c.coords(self.shapes['resizer'], rx, ry, rx2, ry2)
        tx = rx + 5
        ty = ry + 3
        c.coords(self.shapes['text'], tx, ty)
        c.coords(self.shapes['window'], x, y)

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
        self.canvas.itemconfigure(self.shapes['window'], window='')
        if self.canvas_window:
            self.canvas_window.destroy()

        # Create preview
        canvas_window = ttk.Frame(self.canvas, style='PreviewFrame.TFrame')
        # canvas_window.rowconfigure(0, weight=1)
        # canvas_window.columnconfigure(0, weight=1)

        self.canvas.itemconfigure(self.shapes['text'], text=widget_id)

        self._preview_widget = self.create_preview_widget(
            canvas_window, widget_id, uidefinition
        )
        self.root_widget = self._preview_widget

        self.canvas_window = canvas_window
        self.canvas.itemconfigure(self.shapes['window'], window=canvas_window)
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
        builder = pygubu.Builder()
        builder.uidefinition = uidefinition
        top = tk.Toplevel(self.canvas)
        top.columnconfigure(0, weight=1)
        top.rowconfigure(0, weight=1)
        builder.get_object(widget_id, top)
        return top

    def _get_wreqwidth(self):
        return self._preview_widget.winfo_reqwidth()

    def _get_wreqheight(self):
        return self._preview_widget.winfo_reqheight()


class DefaultMenuPreview(Preview):
    def create_preview_widget(self, parent, widget_id, uidefinition):
        self.builder = self._create_builder()
        self.builder.uidefinition = uidefinition
        menubutton = ttk.Menubutton(parent, text='Menu preview')
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
        top['menu'] = menu
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
        fontname = family = 'TkMenuFont'
        size = 12
        modifiers = ''
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
            s = RE_FONT.search(fontname)
            if s:
                g = s.groupdict()
                family = g['family'].replace('{', '').replace('}', '')
                size = g['size']
                modifiers = g['modifiers'] if g['modifiers'] else ''
        if fontname not in OnCanvasMenuPreview.fonts:
            weight = 'bold' if 'bold' in modifiers else 'normal'
            slant = 'italic' if 'italic' in modifiers else 'roman'
            underline = '1' if 'underline' in modifiers else '0'
            overstrike = '1' if 'overstrike' in modifiers else '0'
            kw = {
                'family': family,
                'weight': weight,
                'slant': slant,
                'underline': underline,
                'overstrike': overstrike,
            }
            if size:
                kw['size'] = size
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
        font = self._menu.cget('font')
        font = self._get_font(font)
        for i in range(0, count):
            mtype = self._menu.type(i)
            if mtype == 'tearoff':
                continue
            label = 'default'
            ifont = 'TkMenuFont'
            if mtype != 'separator':
                label = self._menu.entrycget(i, 'label')
                ifont = self._menu.entrycget(i, 'font')
            wpx = font.measure(label)
            hpx = font.metrics('linespace')
            w += wpx
            if hpx > h:
                h = hpx * 2
            # Calculate using font configured for each subitem
            ifont = self._get_font(ifont)
            wpx = ifont.measure(label)
            hpx = ifont.metrics('linespace')
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
        container.pack(fill='both', expand=True)

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
        top['menu'] = menu
        return top


MenuPreview = DefaultMenuPreview
if sys.platform == 'linux':
    MenuPreview = OnCanvasMenuPreview


class ToplevelPreview(Preview):
    def create_preview_widget(self, parent, widget_id, uidefinition):
        # Change real Toplevel for a preview replacement:
        # Add same behavior of Toplevel. Default expand both sides:
        old = uidefinition.get_widget(widget_id)
        newroot = WidgetMeta('pygubudesigner.ToplevelFramePreview', widget_id, 'pack')
        newroot.copy_properties(old)
        # FIX: Why is not copying in the above function ???
        newroot.gridrc_properties = old.gridrc_properties
        # newroot.widget_property('height', '200')
        # newroot.widget_property('width', '200')
        newroot.layout_property('expand', 'true')
        newroot.layout_property('fill', 'both')

        uidefinition.replace_widget(widget_id, newroot)
        # end add behaviour

        self.builder = self._create_builder()
        self.builder.uidefinition = uidefinition
        widget = self.builder.get_object(widget_id, parent)
        return widget

    def create_toplevel(self, widget_id, uidefinition):
        # Create preview
        builder = pygubu.Builder()
        builder.uidefinition = uidefinition
        top = builder.get_object(widget_id, self.canvas)
        return top


class DialogPreview(ToplevelPreview):
    def create_toplevel(self, widget_id, uidefinition):
        top = super().create_toplevel(widget_id, uidefinition)
        top.run()
        return top
