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

from pygubudesigner.util.gridcalculator import GridCalculator


class GridRCselectorWidget(ttk.Frame):
    """Grid cell selector widget.
    Select a cell when clicked on the grid.

    Properties:
        selection: None or tuple of row and column number.
    Events:
        <<Gridselector:CellSelected>>: generated on mouse click.
    """

    def __init__(self, master=None, **kw):
        super().__init__(master, **kw)
        self.canvas = tk.Canvas(self)
        self.canvas.configure(
            background="#ffffff",
            borderwidth="0",
            cursor="hand1",
            highlightthickness="0",
            width=150,
            height=150,
        )
        self.canvas.pack(expand="true", fill="both", side="top")
        self.configure(height="200", padding="5", width="200")
        self.pack(side="top")

        self.canvas.create_line(-100, -100, -99, -99, tag="grid")
        self.grid = GridCalculator(1, 1, 1, 1)
        self.__redraw_cb = None
        self._motion_rowcol = None
        self._sel_hover = None
        self._selection = None
        self._selection_items = []
        self.row_line_items = [0 for _ in range(0, self.grid.rdim)]
        self.col_line_items = [0 for _ in range(0, self.grid.cdim)]
        self._marked_rows = set()
        self._marked_rows_items = {}
        self._marked_cols = set()
        self._marked_cols_items = {}
        self._grid_mark_allrows = False
        self._grid_mark_allcols = False
        self.canvas.bind("<Configure>", self._on_canvas_configure)
        self.canvas.bind("<Motion>", self._motion_handler)
        self.canvas.bind("<Leave>", self._leave_handler)
        self.canvas.bind("<Button-1>", self._on_cell_clicked)
        self._draw_grid()

    def _clear_canvas(self):
        for item in self.row_line_items + self.col_line_items:
            self.canvas.delete(item)
        for item in self._selection_items:
            self.canvas.delete(item)
        self._selection_items = []
        self._selection = None

    def set_dim(self, rowdim, coldim):
        self._clear_canvas()
        self.grid.configure(rowdim, coldim)
        self.row_line_items = [0 for _ in range(0, self.grid.rdim)]
        self.col_line_items = [0 for _ in range(0, self.grid.cdim)]
        self._draw_grid()

    def mark_row(self, index):
        self._marked_rows.add(index)
        self._call_redraw()

    def mark_column(self, index):
        self._marked_cols.add(index)
        self._call_redraw()

    def select_cell(self, row, col):
        self._selection = (row, col)
        self._call_redraw()
        self.event_generate("<<Gridselector:CellSelected>>")

    def selection_clear(self):
        self._selection = None
        self._call_redraw()

    def mark_clear_all(self):
        self._marked_cols.clear()
        self._marked_rows.clear()
        for item in self._marked_cols_items.values():
            self.canvas.delete(item)
        for item in self._marked_rows_items.values():
            self.canvas.delete(item)
        self._marked_rows_items.clear()
        self._marked_cols_items.clear()
        self._call_redraw()

    def mark_grid_rows(self, value=True):
        self._grid_mark_allrows = value
        self._call_redraw()

    def mark_grid_cols(self, value=True):
        self._grid_mark_allcols = value
        self._call_redraw()

    def _on_canvas_configure(self, event=None):
        self._call_redraw()

    def _on_cell_clicked(self, event):
        cell = self.grid.xy2rowcol(event.x, event.y)
        self.select_cell(*cell)

    def _leave_handler(self, event):
        # Remove row/col hover on wiget leave.
        if event.state != 0:
            # Mouse click, or other thing - do nothing
            return
        if self._sel_hover is not None:
            self.canvas.delete(self._sel_hover[0])
            self.canvas.delete(self._sel_hover[1])
            self._sel_hover = None

    def _motion_handler(self, event):
        rc = self.grid.xy2rowcol(event.x, event.y)

        # Draw Row-Col indicators:
        options = {"fill": "#E2E21D"}
        if self._motion_rowcol != rc:
            self._motion_rowcol = rc
            row, col = rc
            line1c, line2c = self.grid.rowcol_center_cross(row, col)
            if self._sel_hover is None:
                line1 = self.canvas.create_line(*line1c, **options)
                line2 = self.canvas.create_line(*line2c, **options)
                self._sel_hover = (line1, line2)
            else:
                self.canvas.coords(self._sel_hover[0], *line1c)
                self.canvas.coords(self._sel_hover[1], *line2c)
            self.canvas.tag_lower(self._sel_hover[0], "grid")
            self.canvas.tag_lower(self._sel_hover[1], "grid")

    def _call_redraw(self):
        if self.__redraw_cb is None:
            self.__redraw_cb = self.after_idle(self._redraw_grid)

    def _redraw_grid(self):
        self._draw_grid(redraw=True)
        # after idle callback trick
        self.__redraw_cb = None

    def _draw_grid(self, redraw=False):
        canvas = self.canvas
        grid = self.grid
        grid.configure(
            fwidth=canvas.winfo_width(), fheight=canvas.winfo_height()
        )

        #
        # Draw Grid lines
        #
        default_options = {"tags": "grid", "fill": "darkgray", "dash": (1, 3)}
        marked_options = {"tags": "grid", "fill": "lightgray", "dash": ""}
        options = default_options
        if self._grid_mark_allrows:
            options = marked_options

        for r, x1, y1, x2, y2 in grid.row_coords_gen():
            if r == grid.rdim - 1:
                break
            # draw bottom side of the rectangle
            coords = (x1, y2, x2, y2)
            if redraw:
                item = self.row_line_items[r]
                canvas.coords(item, *coords)
                canvas.itemconfigure(item, **options)
            else:
                self.row_line_items[r] = item = canvas.create_line(
                    *coords, **options
                )

        options = default_options
        if self._grid_mark_allcols:
            options = marked_options
        for c, x1, y1, x2, y2 in grid.column_coords_gen():
            if c == grid.cdim - 1:
                break
            # draw bottom side of the rectangle
            coords = (x2, y1, x2, y2)
            if redraw:
                item = self.col_line_items[c]
                canvas.coords(item, *coords)
                canvas.itemconfigure(item, **options)
            else:
                self.col_line_items[c] = item = canvas.create_line(
                    *coords, **options
                )

        # Drak marked rows
        marked_options = {
            "fill": "#F2F2F2",
            "outline": "",
        }
        for r in self._marked_rows:
            coords = self.grid.row_coords(r)[1:]
            if r not in self._marked_rows_items:
                item = self.canvas.create_rectangle(*coords, **marked_options)
                self._marked_rows_items[r] = item
            else:
                self.canvas.coords(self._marked_rows_items[r], *coords)
            self.canvas.tag_lower(self._marked_rows_items[r], "grid")

        # Drak marked columns
        for r in self._marked_cols:
            coords = self.grid.column_coords(r)[1:]
            if r not in self._marked_cols_items:
                item = self.canvas.create_rectangle(*coords, **marked_options)
                self._marked_cols_items[r] = item
            else:
                self.canvas.coords(self._marked_cols_items[r], *coords)
            self.canvas.tag_lower(self._marked_cols_items[r], "grid")

        #
        # Draw current selection
        options = {"fill": "blue"}
        if self._selection is None:
            for item in self._selection_items:
                self.canvas.delete(item)
            self._selection_items = []
        else:
            row, col = self._selection
            line1c, line2c = self.grid.rowcol_center_cross(row, col)
            if not self._selection_items:
                line1 = self.canvas.create_line(*line1c, **options)
                line2 = self.canvas.create_line(*line2c, **options)
                self._selection_items = (line1, line2)
            else:
                self.canvas.coords(self._selection_items[0], *line1c)
                self.canvas.coords(self._selection_items[1], *line2c)
            self.canvas.tag_lower(self._selection_items[0], "grid")
            self.canvas.tag_lower(self._selection_items[1], "grid")

    @property
    def selection(self):
        """Return a datetime representing the current selected date."""
        return self._selection


if __name__ == "__main__":
    root = tk.Tk()
    widget = GridRCselectorWidget(root)
    widget.pack(expand=True, fill="both")

    def on_start():
        widget.set_dim(3, 3)
        widget.mark_column(2)
        widget.mark_row(2)

    def change_dimension():
        widget.set_dim(4, 8)
        widget.mark_clear_all()
        widget.select_cell(3, 4)
        widget.mark_row(2)
        widget.mark_column(7)
        widget.mark_grid_cols()

    def on_cell_selected(event):
        print(widget.selection)

    widget.bind("<<Gridselector:CellSelected>>", on_cell_selected)

    root.after(2000, on_start)
    root.after(5000, change_dimension)
    root.mainloop()
