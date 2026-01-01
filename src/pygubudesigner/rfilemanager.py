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
from pathlib import Path
from .preferences import preferences
from pygubudesigner.services.image_loader import iconset_loader


class RecentFilesManager:
    def __init__(self, menu, itemcallback):
        self.menu: tk.Menu = menu
        self.item_callback = itemcallback
        self.recent = {}
        self.filelist = []
        self.load()

    def load(self):
        self.recent = preferences.recent_files
        self.filelist = [
            key
            for key, value in sorted(
                self.recent.items(), key=lambda item: item[1]
            )
        ]
        for f in self.filelist:
            self._add_item(f)

    def save(self):
        preferences.recent_files = self.recent

    def add(self, filepath):
        key = str(filepath)
        if key in self.recent:
            self.recent[key] += 1
        else:
            self.recent[key] = 1
            self._add_item(filepath)
        self.save()

    def _add_item(self, filepath):
        name = Path(filepath).name
        itemlabel = f"{name} [{filepath}]"

        def item_command(fname=filepath, cb=self.item_callback):
            cb(fname)

        master = self.menu.nametowidget(self.menu.winfo_parent())
        item_image = iconset_loader(master, "mi_recentfiles_open")
        self.menu.insert_command(
            0,
            label=itemlabel,
            command=item_command,
            compound=tk.LEFT,
            image=item_image,
        )

    def clear(self):
        count = self.menu.index("end")
        index_to = count - 2
        if index_to > 0:
            self.menu.delete(0, index_to)
        self.recent = {}
        self.save()
