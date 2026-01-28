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

from datetime import datetime
from pathlib import Path
from functools import reduce
from .preferences import preferences
from pygubudesigner.services.image_loader import iconset_loader


class RecentFilesManager:
    def __init__(self, menu, itemcallback):
        self.menu: tk.Menu = menu
        self.item_callback = itemcallback
        self.recent = preferences.recent_files
        self.filelist = []
        self.needs_update = True
        self.menu.configure(postcommand=self._on_menu_post)

    def _on_menu_post(self):
        if self.needs_update:
            self._create_file_list()
            final_list = self.filelist[:20]
            padding = reduce(max, (len(Path(f).name) for f in final_list), 0)
            for f in reversed(final_list):
                self._add_item(f, padding)
            self.needs_update = False

    def _menu_clear(self):
        count = self.menu.index("end")
        index_to = count - 2
        if index_to > 0:
            self.menu.delete(0, index_to)

    def _create_file_list(self):
        FCOUNT = 0
        FDATE = 1
        today_date = datetime.now().date()
        long_time = datetime.fromisoformat("19800915").timestamp()

        def generate_sort_key(pair):
            # files used today first, then older files by usage count.
            file_usage_count = pair[1][FCOUNT]
            file_last_used = pair[1][FDATE]
            file_last_used_date = file_last_used.date()
            file_last_used_ts = file_last_used.timestamp()
            sort_key = (1, long_time, -file_usage_count, -file_last_used_ts)
            if file_last_used_date == today_date:
                sort_key = (0, -file_last_used_ts, 0, 0)
            return sort_key

        self.filelist = [
            key
            for key, value in sorted(
                self.recent.items(),
                key=generate_sort_key,
            )
        ]

    def _add_item(self, filepath, padding=0):
        name = Path(filepath).name
        itemlabel = f"{name:<{padding}} [{filepath}]"

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
            font="TkFixedFont",
        )

    def save(self):
        preferences.recent_files = self.recent

    def add(self, filepath):
        key = str(filepath)
        if key in self.recent:
            count, date = self.recent[key]
            self.recent[key] = [count + 1, datetime.now()]
        else:
            self.recent[key] = [1, datetime.now()]
        self._menu_clear()
        self.needs_update = True
        self.save()

    def clear(self):
        self._menu_clear()
        self.recent = {}
        self.save()
