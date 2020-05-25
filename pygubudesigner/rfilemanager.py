import os
from .preferences import recent_files_get, recent_files_save


class RecentFilesManager(object):
    def __init__(self, menu, itemcallback):
        self.menu = menu
        self.item_callback = itemcallback
        self.filelist = []
        
    def load(self):
        self.filelist = recent_files_get()
        for f in self.filelist:
            self._add_item(f)
    
    def save(self):
        newlist = self.filelist[:10]
        self.filelist = newlist
        recent_files_save(reversed(newlist))
    
    def addfile(self, filepath):
        if filepath not in self.filelist:
            self.filelist.insert(0, filepath)
            self._add_item(filepath)
        else:
            self.filelist.remove(filepath)
            self.filelist.insert(0, filepath)
        self.save()
    
    def _add_item(self, filepath):
        name = os.path.basename(filepath)
        itemlabel = '{0} [{1}]'.format(name, filepath)
        
        def item_command(fname=filepath, cb=self.item_callback):
            cb(filepath)
        
        self.menu.insert_command(0, label=itemlabel, command=item_command)
    
    def clear(self):
        count = self.menu.index('end')
        index_to = count - 2
        if index_to > 0:
            self.menu.delete(0, index_to)
        self.filelist = []
        self.save()


