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

from typing import List, Dict, DefaultDict
from collections import defaultdict
from pygubudesigner.util import get_linespace
from pygubudesigner.util.gridcalculator import GridCalculator


class Shape:
    FIRST = 1

    def __init__(self, canvas: tk.Canvas, items=None, options=None):
        self.canvas: tk.Canvas = canvas
        self.items: DefaultDict = defaultdict(list) if items is None else items
        self.options: Dict = {} if options is None else options

    def delete(self):
        for itemlist in self.items.values():
            self.canvas.delete(*itemlist)
        self.items.clear()


class SelectedSlotShape(Shape):
    def draw(self, coords, redraw=False):
        redraw = bool(self.items[self.FIRST])
        cicle_coords = self.slot_coords(*coords)
        color = self.options.get("fill", "blue")
        if redraw:
            self.canvas.coords(self.items[self.FIRST][0], *cicle_coords)
        else:
            item = self.canvas.create_oval(
                *cicle_coords, outline=color, width=6
            )
            self.items[self.FIRST].append(item)

    def slot_coords(self, x1, y1, x2, y2):
        w = x2 - x1
        h = y2 - y1
        cx = x1 + (w / 2)
        cy = y1 + (h / 2)
        tmw = w * (2 / 6) / 2
        tmh = h * (2 / 6) / 2
        return (cx - tmw, cy - tmh, cx + tmw, cy + tmh)


class GridShape(Shape):
    ROWS = 2
    COLS = 3
    SLOT = 4

    def __init__(self, canvas, grid):
        super().__init__(canvas)
        self.grid = grid
        self.marked_rows = set()
        self.marked_cols = set()
        self.marked_all = False
        self.marked_slots = set()

    def draw(self, redraw=False):
        self._draw_cells(redraw)
        self._draw_rc_marks(redraw)
        self._draw_slots(redraw)

    def _draw_cells(self, redraw=False):
        redraw = bool(self.items[self.FIRST])
        color = "black"
        if self.marked_all:
            color = "brown"
        for values in self.grid.cell_coords_gen(1, 1):
            idx = values[0]
            coords = values[1:]
            if redraw:
                item_id = self.items[self.FIRST][idx]
                self.canvas.coords(item_id, *coords)
                self.canvas.itemconfigure(item_id, outline=color)
            else:
                item = self.canvas.create_rectangle(*coords, outline=color)
                self.items[self.FIRST].append(item)

    def _draw_rc_marks(self, redraw=False):
        hidden = (-100, 0, -99, 1)
        redraw = bool(self.items[self.ROWS])
        for values in self.grid.cell_coords_gen(1, 1):
            idx = values[0]
            coords = values[1:]
            row_coords = hidden
            col_coords = hidden
            row, col = self.grid.i2rc(idx)
            if row in self.marked_rows:
                row_coords = self.marked_row_coords(*coords)
            if col in self.marked_cols:
                col_coords = self.marked_col_coords(*coords)
            if redraw:
                self.canvas.coords(self.items[self.ROWS][idx], *row_coords)
                self.canvas.coords(self.items[self.COLS][idx], *col_coords)
            else:
                color = "#C0BFBC"
                item = self.canvas.create_rectangle(
                    *row_coords, fill=color, outline=color
                )
                self.items[self.ROWS].append(item)
                item = self.canvas.create_rectangle(
                    *col_coords, fill=color, outline=color
                )
                self.items[self.COLS].append(item)

    def _draw_slots(self, redraw=False):
        hidden = (-100, 0, -99, 1)
        redraw = bool(self.items[self.SLOT])
        for values in self.grid.cell_coords_gen(1, 1):
            idx = values[0]
            coords = values[1:]
            slot_coords = hidden
            row_col = self.grid.i2rc(idx)
            if row_col in self.marked_slots:
                slot_coords = self.marked_slot_coords(*coords)
            if redraw:
                self.canvas.coords(self.items[self.SLOT][idx], *slot_coords)
            else:
                color = "#DC8ADD"
                item = self.canvas.create_oval(
                    *slot_coords, fill=color, outline=color
                )
                self.items[self.SLOT].append(item)

    def marked_slot_coords(self, x1, y1, x2, y2):
        w = x2 - x1
        h = y2 - y1
        cx = x1 + (w / 2)
        cy = y1 + (h / 2)
        tmw = w * (2 / 6) / 2
        tmh = h * (2 / 6) / 2
        return (cx - tmw, cy - tmh, cx + tmw, cy + tmh)

    def marked_row_coords(self, x1, y1, x2, y2):
        # w = x2 - x1
        h = y2 - y1
        mark_h = h * (4 / 100)
        pad = 5
        x1 = x1 + pad
        y1 = y1 + pad
        x2 = x2 - pad
        y2 = y2 - pad
        return (x1, y2 - mark_h, x2, y2)

    def marked_col_coords(self, x1, y1, x2, y2):
        w = x2 - x1
        h = y2 - y1
        mark_h = h * (4 / 100)
        mark_w = w * (4 / 100)
        pad = 5
        x1 = x1 + pad
        y1 = y1 + pad
        x2 = x2 - pad
        y2 = y2 - pad
        return (x1, y1, x1 + mark_w, y2 - mark_h)


#
# Manual user code
#


class GridRCselectorWidget(ttk.Frame):
    """Grid cell selector widget.
    Select a cell when clicked on the grid.

    Properties:
        selection: None or tuple of row and column number.
    Events:
        <<Gridselector:CellSelected>>: generated on mouse click.
        <<Gridselector:CellHover>>: generated on hover change
    """

    BUTTON1 = 0x0100
    EVENT_CELL_SELECTED = "<<Gridselector:CellSelected>>"
    EVENT_CELL_HOVER = "<<Gridselector:CellHover>>"

    def __init__(self, master=None, **kw):
        super().__init__(master, **kw)
        self.canvas = tk.Canvas(self, name="canvas")
        self.canvas.configure(
            background="#ffffff", borderwidth=0, height=100, width=100
        )
        self.canvas.pack(
            expand=True,
            fill="both",
            ipadx=1,
            ipady=1,
            padx=1,
            pady=1,
            side="top",
        )
        self.configure(height=200, width=200)
        self.pack(expand=True, fill="both")

        self._selection = None
        self._redraw_cb = None
        self._motion_rowcol = None

        canvas_wh = get_linespace(scale_factor=16.1)
        self.canvas.configure(width=canvas_wh, height=canvas_wh)
        self.canvas.bind("<Configure>", self._on_canvas_configure)
        self.canvas.bind("<Button-1>", self._on_cell_clicked)
        self.canvas.bind("<Motion>", self._motion_handler)
        self.canvas.bind("<Leave>", self._leave_handler)

        self.grid = GridCalculator(1, 1, 1, 1)
        self.grid_shape = GridShape(self.canvas, self.grid)
        self.selector_shape = SelectedSlotShape(
            self.canvas, None, dict(fill="#000099")
        )
        self.hover_shape = SelectedSlotShape(
            self.canvas, None, dict(fill="#FF7800")
        )
        self.after(200, self._draw_grid)

    @property
    def selection(self):
        """Return tuple representing the current selected (row, col)."""
        return self._selection

    @property
    def selection_hover(self):
        return self._motion_rowcol

    def set_dim(self, rowdim, coldim):
        self._clear_canvas()
        self.grid.configure(rowdim, coldim)
        self._draw_grid()

    def select_cell(self, row, col):
        self._selection = (row, col)
        self._call_redraw()
        self.event_generate(self.EVENT_CELL_SELECTED)

    def selection_clear(self):
        self._selection = None
        self._call_redraw()

    def mark_row(self, index):
        self.grid_shape.marked_rows.add(index)
        self._call_redraw()

    def mark_col(self, index):
        self.grid_shape.marked_cols.add(index)
        self._call_redraw()

    def mark_slot(self, row, col):
        self.grid_shape.marked_slots.add((row, col))
        self._call_redraw()

    def mark_grid_all(self, value=True):
        self.grid_shape.marked_all = value
        self._call_redraw()

    def mark_clear_all(self):
        self.grid_shape.marked_all = False
        self.grid_shape.marked_cols.clear()
        self.grid_shape.marked_rows.clear()
        self.grid_shape.marked_slots.clear()
        self._call_redraw()

    def _clear_canvas(self):
        self.grid_shape.delete()
        self.selector_shape.delete()
        self.hover_shape.delete()

    def _on_cell_clicked(self, event):
        cell = self.grid.xy2rowcol(event.x, event.y)
        self.select_cell(*cell)

    def _on_canvas_configure(self, event=None):
        self._call_redraw()

    def _call_redraw(self):
        if self._redraw_cb is None:
            self._redraw_cb = self.after_idle(self._redraw_grid)

    def _redraw_grid(self):
        self._draw_grid(redraw=True)
        # after idle callback trick
        self._redraw_cb = None

    def _draw_grid(self, redraw=False):
        self.grid.configure(
            fwidth=self.canvas.winfo_width() - 3,
            fheight=self.canvas.winfo_height() - 3,
        )
        self.grid_shape.draw(redraw)
        if self._selection is None:
            self.selector_shape.delete()
        else:
            r, c = self._selection
            cell_coords = self.grid.cell_coords(r, c)
            self.selector_shape.draw(cell_coords, redraw)

    def _leave_handler(self, event: tk.Event):
        # Remove row/col hover on wiget leave.
        if event.state & self.BUTTON1:
            # Mouse click, or other thing - do nothing
            return
        self.hover_shape.delete()
        self._motion_rowcol = None
        self.event_generate(self.EVENT_CELL_HOVER)

    def _motion_handler(self, event):
        rc = self.grid.xy2rowcol(event.x, event.y)

        # Draw Row-Col indicators:
        if self._motion_rowcol != rc:
            self._motion_rowcol = rc
            row, col = rc
            cell_coords = self.grid.cell_coords(row, col)
            self.hover_shape.draw(cell_coords)
            self.event_generate(self.EVENT_CELL_HOVER)


if __name__ == "__main__":
    root = tk.Tk()
    widget = GridRCselectorWidget(root)
    widget.pack(expand=True, fill="both", padx=10, pady=10)
    entry = ttk.Entry(root)
    entry.pack(side=tk.BOTTOM)

    def on_start():
        widget.set_dim(3, 3)
        widget.mark_col(2)
        widget.mark_row(2)
        widget.mark_slot(1, 1)

    def change_dimension():
        widget.set_dim(4, 8)
        widget.mark_clear_all()
        widget.select_cell(3, 4)
        widget.mark_slot(1, 1)
        widget.mark_row(2)
        widget.mark_col(7)
        widget.mark_grid_all()

    def on_cell_selected(event):
        print(widget.selection)

    widget.bind("<<Gridselector:CellSelected>>", on_cell_selected)

    root.after(2000, on_start)
    root.after(5000, change_dimension)
    root.mainloop()
