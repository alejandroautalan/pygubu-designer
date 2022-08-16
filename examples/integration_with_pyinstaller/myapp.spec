# -*- mode: python -*-

block_cipher = None

# specify pygubu modules
hidden_imports = [
    'pygubu.plugins.tk.tkstdwidgets',
    'pygubu.plugins.ttk.ttkstdwidgets',
    'pygubu.plugins.pygubu.dialog',
    'pygubu.plugins.pygubu.editabletreeview',
    'pygubu.plugins.pygubu.scrollbarhelper',
    'pygubu.plugins.pygubu.scrolledframe',
    'pygubu.plugins.pygubu.tkscrollbarhelper',
    'pygubu.plugins.pygubu.tkscrolledframe',
    'pygubu.plugins.pygubu.pathchooserinput',
#
# Uncomment the following module lines if you are using this plugins:
#
# awesometkinter:
#   'pygubu.plugins.awesometkinter.button',
#   'pygubu.plugins.awesometkinter.frame',
#   'pygubu.plugins.awesometkinter.label',
#   'pygubu.plugins.awesometkinter.progressbar',
#   'pygubu.plugins.awesometkinter.scrollbar',
#   'pygubu.plugins.awesometkinter.text',
# tkcalendar:
#   'pygubu.plugins.tkcalendar.calendar',
#   'pygubu.plugins.tkcalendar.dateentry',
# tkintertable:
#   'pygubu.plugins.tkintertable.table',
# tksheet:
#   'pygubu.plugins.tksheet.sheet',
# ttkwidgets:
#   'pygubu.plugins.ttkwidgets.calendar',
#   'pygubu.plugins.ttkwidgets.autocomplete',
#   'pygubu.plugins.ttkwidgets.checkboxtreeview',
#   'pygubu.plugins.ttkwidgets.color',
#   'pygubu.plugins.ttkwidgets.font',
#   'pygubu.plugins.ttkwidgets.frames',
#   'pygubu.plugins.ttkwidgets.itemscanvas',
#   'pygubu.plugins.ttkwidgets.linklabel',
#   'pygubu.plugins.ttkwidgets.scaleentry',
#   'pygubu.plugins.ttkwidgets.scrolledlistbox',
#   'pygubu.plugins.ttkwidgets.table',
#   'pygubu.plugins.ttkwidgets.tickscale',
# tkinterweb:
#   'pygubu.plugins.tkinterweb.htmlwidgets',
]


data_files = [
    ('myapp.ui', '.'),
    ('imgs/*.gif', 'imgs'),
]

a = Analysis(['myapp.py'],
             pathex=['C:\\src\\pyinstaller'],
             binaries=None,
             datas=data_files,
             hiddenimports=hidden_imports,
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          exclude_binaries=True,
          name='myapp',
          debug=False,
          strip=False,
          upx=True,
          console=True )
coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=False,
               upx=True,
               name='myapp')
