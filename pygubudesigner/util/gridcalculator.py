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


class GridCalculator:
    def __init__(self, rdim, cdim, fwidth, fheight):
        self.rdim = rdim
        self.cdim = cdim
        self.fwidth = fwidth
        self.fheight = fheight
        self.rowh = fheight / rdim
        self.colw = fwidth / cdim

    def configure(self, rdim=None, cdim=None, fwidth=None, fheight=None):
        self.rdim = self.rdim if rdim is None else rdim
        self.cdim = self.cdim if cdim is None else cdim
        self.fwidth = self.fwidth if fwidth is None else fwidth
        self.fheight = self.fheight if fheight is None else fheight
        self.rowh = self.fheight / self.rdim
        self.colw = self.fwidth / self.cdim

    def i2rc(self, i):
        """Index to (row, column) coords"""
        c = i % self.cdim
        r = (i - c) // self.cdim
        return (r, c)

    def rowmajor(self):
        """Rowmajor index generator."""
        size = self.rdim * self.cdim
        for i in range(0, size):
            c = i % self.cdim
            r = (i - c) // self.cdim
            yield (i, r, c)

    def cell_coords(self, f, c, ox=0, oy=0):
        x = ox + c * self.colw
        y = oy + f * self.rowh
        x1 = x + self.colw
        y1 = y + self.rowh
        return (x, y, x1, y1)

    def cell_coords_gen(self, ox=0, oy=0):
        """Generate coords for each cell in the grid.
        Input:
          ox: x origin
          oy: y origin

        Output:
          (
            i,  # rowmajor index
            x,  # x coordinate
            y,  # y coordinate
            x1,  # x1 coordinate
            y1,  # y1 coordinate
          )
        """
        for i, f, c in self.rowmajor():
            coords = self.cell_coords(f, c)
            yield (i, *coords)

    def row_coords(self, row, ox=0, oy=0):
        """Calculate box coordinates for a given row"""
        x1 = ox
        y1 = oy + row * self.rowh
        x2 = ox + self.cdim * self.colw
        y2 = oy + row * self.rowh + self.rowh
        return (row, x1, y1, x2, y2)

    def row_coords_gen(self, ox=0, oy=0):
        """Iterate over row coordinates"""
        for r in range(self.rdim):
            yield self.row_coords(r, ox, oy)

    def column_coords(self, col, ox=0, oy=0):
        """Calculate column coordinate for a given column col"""
        x1 = ox + col * self.colw
        y1 = oy
        x2 = ox + col * self.colw + self.colw
        y2 = oy + self.rdim * self.rowh
        return (col, x1, y1, x2, y2)

    def column_coords_gen(self, ox=0, oy=0):
        """Iterate over column coordinates"""
        for c in range(self.cdim):
            yield self.column_coords(c, ox, oy)

    def rowcol_poly(self, row, col, ox=0, oy=0):
        """Polygon coords for the row/col insersection shape."""
        x1, y1, x2, y2 = self.cell_coords(row, col, ox, oy)
        # fmt: off
        return (
            x1, y1,  # p1
            x1, 0,  # p2
            x2, 0,  # p3
            x2, y1,  # p4
            self.fwidth, y1,  # p5
            self.fwidth, y2,  # p6
            x2, y2,  # p7
            x2, self.fheight,  # p8
            x1, self.fheight,  # p9
            x1, y2,  # p10
            0, y2,  # p11
            0, y1,  # p12
        )
        # fmt: on

    def rowcol_center_cross(self, row, col, ox=0, oy=0):
        """Coords for the two row/col insersection lines."""
        x1, y1, x2, y2 = self.cell_coords(row, col, ox, oy)
        xc = x1 + self.colw / 2
        yc = y1 + self.rowh / 2
        return ((xc, oy, xc, self.fheight), (ox, yc, self.fwidth, yc))

    def xy2rowcol(self, x, y):
        column = int(x // self.colw)
        row = int(y // self.rowh)
        return (row, column)
