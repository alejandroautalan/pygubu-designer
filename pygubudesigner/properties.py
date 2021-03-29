# encoding: UTF-8
#
# Copyright 2012-2013 Alejandro Autalán
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
#
# For further info, check  http://pygubu.web.here
from __future__ import unicode_literals
import platform
import logging

try:
    import tkinter as tk
except:
    import Tkinter as tk

from pygubu.builder import builderobject
from .propertieshelp import help_for, _

logger = logging.getLogger(__name__)


TK_BITMAPS = (
    'error', 'gray75', 'gray50', 'gray25', 'gray12',
    'hourglass', 'info', 'questhead', 'question', 'warning',
    )

TK_BITMAPS_MAC = (
    'document', 'stationery', 'edition', 'application', 'accessory',
    'forder', 'pfolder', 'trash', 'floppy', 'ramdisk', 'cdrom',
    'preferences', 'querydoc', 'stop', 'note', 'caution'
    )

TK_CURSORS = (
    'arrow', 'based_arrow_down', 'based_arrow_up', 'boat',
    'bogosity', 'bottom_left_corner', 'bottom_right_corner',
    'bottom_side', 'bottom_tee', 'box_spiral', 'center_ptr',
    'circle', 'clock', 'coffee_mug', 'cross', 'cross_reverse',
    'crosshair', 'diamond_cross', 'dot', 'dotbox', 'double_arrow',
    'draft_large', 'draft_small', 'draped_box', 'exchange', 'fleur',
    'gobbler', 'gumby', 'hand1', 'hand2', 'heart', 'icon',
    'iron_cross', 'left_ptr', 'left_side', 'left_tee', 'leftbutton',
    'll_angle', 'lr_angle', 'man', 'middlebutton', 'mouse', 'none',
    'pencil', 'pirate', 'plus', 'question_arrow', 'right_ptr',
    'right_side', 'right_tee', 'rightbutton', 'rtl_logo',
    'sailboat', 'sb_down_arrow', 'sb_h_double_arrow',
    'sb_left_arrow', 'sb_right_arrow', 'sb_up_arrow',
    'sb_v_double_arrow', 'shuttle', 'sizing', 'spider', 'spraycan',
    'star', 'target', 'tcross', 'top_left_arrow', 'top_left_corner',
    'top_right_corner', 'top_side', 'top_tee', 'trek', 'ul_angle',
    'umbrella', 'ur_angle', 'watch', 'xterm', 'X_cursor')

TK_CURSORS_WINDOWS = (
    'no', 'starting', 'size', 'size_ne_sw'
    'size_ns', 'size_nw_se', 'size_we','uparrow', 'wait'
    )

TK_CURSORS_MAC = (
    'copyarrow', 'aliasarrow', 'contextualmenuarrow', 'text',
    'cross-hair', 'closedhand', 'openhand', 'pointinghand',
    'resizeleft', 'resizeright', 'resizeleftright', 'resizeup',
    'resizedown', 'resizeupdown', 'notallowed', 'poof',
    'countinguphand', 'countingdownhand', 'countingupanddownhand', 'spinning'
    )

if platform.system() == 'Darwin':
    TK_BITMAPS = TK_BITMAPS + TK_BITMAPS_MAC
    TK_CURSORS = TK_CURSORS + TK_CURSORS_MAC
elif platform.system() == 'Windows':
    TK_CURSORS = TK_CURSORS + TK_CURSORS_WINDOWS

TK_RELIEFS = (tk.FLAT, tk.RAISED, tk.SUNKEN, tk.GROOVE, tk.RIDGE)

TK_WIDGET_OPTIONS = {
    'accelerator': {
        'editor': 'entry',
        'help': help_for('accelerator')
        },
    'activerelief': {
        'editor': 'choice',
        'params': {
            'values': ('', tk.FLAT, tk.RAISED, tk.SUNKEN,
                       tk.GROOVE, tk.RIDGE),
            'state': 'readonly'},
        'help': help_for('activerelief')
        },
    'activestyle': {
        'editor': 'choice',
        'params': {
            'values': ('', 'underline', 'dotbox', 'none'),
            'state': 'readonly'},
        'help': help_for('activestyle')
        },
    'activebackground': {
        'editor': 'colorentry',
        'help': help_for('activebackground')
        },
    'activeborderwidth': {
        'editor': 'dimensionentry',
        'help': help_for('activeborderwidth')
        },
    'activeforeground': {
        'editor': 'colorentry',
        'help': help_for('activeforeground')
        },
    'after': {
        'editor': 'entry',
        'help': help_for('after')
        },
    # ttk.Label
    'anchor': {
        'editor': 'choice',
        'params': {
            'values': ('', 'n', 'ne', 'nw', 'e', 'w', 's', 'se', 'sw', 'center'),
            'state': 'readonly'},
        'help': help_for('anchor'),
        'ttk.xxxx?': {
            'params': {
                'values': ('', tk.W, tk.CENTER, tk.E),
                'state': 'readonly'}
            },
        },
    'aspect': {
        'editor': 'naturalnumber'
        },
    'autoseparators': {
        'editor': 'choice',
        'params': {'values': ('', 'false', 'true'), 'state': 'readonly'}
        },
    # ttk.Label
    'background': {
        'editor': 'colorentry',
        'help': {
            'tk': help_for('background-tk'),
            'ttk': help_for('background-ttk'),
            }
        },
    # ttk.Frame, ttk.Label
    'borderwidth': {
        'editor': 'dimensionentry',
        'help': help_for('borderwidth')
        },
    'bigincrement': {
        'editor': 'naturalnumber',
        'help': help_for('bigincrement')
        },
    'bitmap': {
        'editor': 'choice',
        'params': {'values': ('',) + TK_BITMAPS, 'state': 'readonly'},
        'help': help_for('bitmap')
        },
    'blockcursor': {
        'editor': 'choice',
        'params': {'values': ('', 'false', 'true'), 'state': 'readonly'}
        },
    'buttonbackground': {
        'editor': 'colorentry',
        'help': help_for('buttonbackground')
        },
    'buttoncursor': {
        'editor': 'choice',
        'params': {'values': ('',) + TK_CURSORS, 'state': 'readonly'}
        },
    'buttondownrelief': {
        'editor': 'choice',
        'params': {'values': ('',) + TK_RELIEFS, 'state': 'readonly'}
        },
    'buttonuprelief': {
        'editor': 'choice',
        'params': {'values': ('',) + TK_RELIEFS, 'state': 'readonly'}
        },
    'class_': {
        'editor': 'alphanumentry',
        'help': help_for('class_')
        },
    'closeenough': {
        'editor': 'spinbox',
        'params': {'from_': 0, 'to': 999},
        'help': help_for('closeenough')
        },
    'column_anchor': { # ttk.Treeview.Column
        'editor': 'choice',
        'params': {'values': ('', tk.W, tk.CENTER, tk.E), 'state': 'readonly'},
        'default': tk.W,
        'help': help_for('column_anchor')
        },
    'columnbreak': {
        'editor': 'choice',
        'params': {'values': ('', 'false', 'true'), 'state': 'readonly'}
        },
    'command': {
        'editor': 'dynamic',
        'params': {'mode': 'commandentry'},
        'ttk.Scrollbar': {
             'params': {'mode': 'scrollcommandentry'}
             },
        'ttk.Scale': {
             'params': {'mode': 'scalecommandentry'}
             },
        'tk.Scale': {
             'params': {'mode': 'scalecommandentry'}
             },
        'tk.OptionMenu': {
             'params': {'mode': 'simplecommandentry'}
             },
        'help': help_for('command-pygubu')
        },
    # ttk.Label
    'compound': {
        'editor': 'choice',
        'params': {
            'values': ('', tk.TOP, tk.BOTTOM, tk.LEFT, tk.RIGHT, tk.CENTER, tk.NONE),
            'state': 'readonly'},
        'help': {
            'tk': help_for('compound-tk'),
            'ttk': help_for('compound-ttk')}
        },
    # ttk.Button
    'confine': {
        'editor': 'choice',
        'params': {'values': ('', 'false', 'true'), 'state': 'readonly'},
        'help': help_for('confine')
        },
    'container': {
        'editor': 'choice',
        'params': {'values': ('', 'false', 'true'), 'state': 'readonly'},
        'help': help_for('container')
        },
    'cursor': {
        'editor': 'choice',
        'params': {'values': ('',) + TK_CURSORS, 'state': 'readonly'},
        'help': help_for('cursor')
        },
    # ttk.Button
    'default': {
        'editor': 'choice',
        'params': {
            'values': ('', 'normal', 'active', 'disabled'),
            'state': 'readonly'},
        'help': help_for('default')
        },
    'digits': {
        'editor': 'spinbox',
        'params': {'from_': 0, 'to': 999},
        'help': help_for('digits')
        },
    'direction': {
        'editor': 'choice',
        'tk.Menubutton': {
            'params': {'values': ('', tk.LEFT, tk.RIGHT, 'above'),
                       'state': 'readonly'}},
        'ttk.Menubutton': {
            'params': {
                'values': ('', 'above', 'below', 'flush',
                           tk.LEFT, tk.RIGHT),
                'state': 'readonly'}},
        },
    'disabledbackground': {
        'editor': 'colorentry'
        },
    'disabledforeground': {
        'editor': 'colorentry',
        'help': help_for('disabledforeground')
        },
    'elementborderwidth': {
        'editor': 'entry'
        },
    'endline': {
        'editor': 'entry'
        },
    # ttk.Checkbutton, ttk.Entry
    'exportselection': {
        'editor': 'choice',
        'params': {'values': ('', 'true', 'false'), 'state': 'readonly'},
        'help': help_for('exportselection')
        },
    # ttk.Label
    'font': {
        'editor': 'fontentry',
        'help': help_for('font')
        },
    # ttk.Label
    'foreground': {
        'editor': 'colorentry',
        'help': {
            'tk': help_for('foreground-tk'),
            'ttk': help_for('foreground-ttk')
            }
        },
    # ttk.Spinbox
    'format': {
        'editor': 'entry'
        },
    # ttk.Scale, ttk.Spinbox
    'from_': {
        'editor': 'realnumber',
        'help': help_for('from_')
        },
    'handlepad': {
        'editor': 'entry'
        },
    'handlesize': {
        'editor': 'entry'
        },
    # ttk.Treeview.Column
    'heading_anchor': {
        'editor': 'choice',
        'params': {
            'values': ('', tk.W, tk.CENTER, tk.E), 'state': 'readonly'},
        'default': tk.W,
        'help': help_for('heading_anchor')
        },
    # ttk.Frame,
    'height': {
        'editor': 'dynamic',
        'help': help_for('height'),
        'params': {'mode': 'dimensionentry'},
        'tk.Button': {
            'help': help_for('height-tk.Button')
            },
        'ttk.Combobox': {
            'params': {'mode': 'naturalnumber'},
            },
        'tk.Toplevel': {'default': 200},
        'tk.Frame': {'default': 200},
        'ttk.Frame': {'default': 200},
        'tk.LabelFrame': {'default': 200},
        'ttk.Labelframe': {'default': 200},
        'tk.Listbox': {
            'params': {'mode': 'naturalnumber'},
            },
        'tk.Menubutton': {
            'params': {'mode': 'naturalnumber'},
            },        
        'tk.PanedWindow': {'default': 200},
        'ttk.Panedwindow': {'default': 200},
        'ttk.Notebook': {'default': 200},
        'tk.Text': {
            'params': {'mode': 'naturalnumber'},
            'default': 10
            },
        'tk.Radiobutton':{
            'params': {'mode': 'naturalnumber'},
            },
        'ttk.Treeview': {
            'params': {'mode': 'naturalnumber'},
            'help': help_for('height-ttk.Treeview')
            },
        'pygubu.builder.widgets.editabletreeview': {
            'params': {'mode': 'naturalnumber'},
            'help': help_for('height-ttk.Treeview')
            },
        'pygubu.builder.widgets.dialog': {'default': 100}
        },
    'hidemargin': {
        'editor': 'choice',
        'params': {'values': ('', 'false', 'true'), 'state': 'readonly'}
        },
    'highlightbackground': {
        'editor': 'colorentry',
        'help': help_for('highlightbackground')
        },
    'highlightcolor': {
        'editor': 'colorentry',
        'help': help_for('highlightcolor')
        },
    'highlightthickness': {
        'editor': 'dimensionentry',
        'help': help_for('highlightthickness')
        },
    # ttk.Label
    'image': {
        'editor': 'imageentry',
        'help': {
            'tk': help_for('image-tk'),
            'ttk': help_for('image-ttk')
            },
        'ttk.Treeview.Column': {
            'help': help_for('image-ttk.Treeview.Column'),
            }
        },
    'inactiveselectbackground': {
        'editor': 'colorentry'
        },
    # ttk.Spinbox
    'increment': {
        'editor': 'spinbox',
        'params': {'from_': -999, 'to': 999}
        },
    'indicatoron': {
        'editor': 'choice',
        'params': {'values': ('', 'false', 'true'), 'state': 'readonly'}
        },
    'insertbackground': {
        'editor': 'colorentry',
        'help': help_for('insertbackground')
        },
    'insertborderwidth': {
        'editor': 'spinbox',
        'params': {'from_': 0, 'to': 999},
        'help': help_for('insertborderwidth')
        },
    'insertofftime': {
        'editor': 'spinbox',
        'params': {'from_': 0, 'to': 9999, 'increment': 100},
        'help': help_for('insertofftime')
        },
    'insertontime': {
        'editor': 'spinbox',
        'params': {'from_': 0, 'to': 9999, 'increment': 100},
        'help': help_for('insertontime')
        },
    'insertunfocussed': {
        'editor': 'choice',
        'params': {
            'values': ('', 'none', 'hollow', 'solid'),
            'state': 'readonly'}},
    'insertwidth': {
        'editor': 'spinbox',
        'params': {'from_': 0, 'to': 999},
        'help': help_for('insertwidth')
        },
    # ttk.Entry
    'invalidcommand': {
        'editor': 'entryvalidatecommandentry',
        'help': help_for('command-pygubu')
        },
    'jump': {
        'editor': 'choice',
        'params': {'values': ('', 'false', 'true'), 'state': 'readonly'},
        'help': help_for('jump')
        },
    # ttk.Label
    'justify': {
        'editor': 'choice',
        'params': {
            'values': ('', 'left', 'center', 'right'), 'state': 'readonly'},
        'help': help_for('justify'),
        'ttk.Entry': {
            'help': help_for('justify-ttk.Entry')}
        },
    'label': {
        'editor': 'entry',
        'help': help_for('label')
        },
    # ttk.Labelframe
    'labelanchor': {
        'editor': 'choice',
        'params': {
            'values': ('', 'nw', 'n', 'ne', 'en', 'e', 'es',
                       'se', 's', 'sw', 'ws', 'w'),
            'state': 'readonly'},
        'help': help_for('labelanchor')
        },
    # ttk.Progressbar
    'length': {
        'editor': 'dimensionentry',
        'help': help_for('length')
        },
    'listvariable': {
        'editor': 'tkvarentry',
        'help': help_for('listvariable')
        },
    # ttk.Progressbar
    'maximum': {
        'editor': 'realnumber'},
    'maxundo': {
        'editor': 'spinbox',
        'params': {'from_': 0, 'to': 999}},
    'minsize': {
        'editor': 'entry'},
    # ttk.Treeview.Column
    'minwidth': {
        'editor': 'naturalnumber',
        'default': '20',
        'help': help_for('minwidth')
        },
    # ttk.Progressbar
    'mode': {
        'editor': 'choice',
        'params': {
            'values': ('', 'determinate', 'indeterminate'),
            'state': 'readonly'}},
    'offrelief': {
        'editor': 'choice',
        'params': {'values': ('',) + TK_RELIEFS, 'state': 'readonly'}},
    # ttk.Checkbutton
    'offvalue': {
        'editor': 'entry',
        'help': help_for('offvalue')
        },
    # ttk.Checkbutton
    'onvalue': {
        'editor': 'entry',
        'help': help_for('onvalue')
        },
    'opaqueresize': {
        'editor': 'choice',
        'params': {'values': ('', 'false', 'true'), 'state': 'readonly'}},
    # ttk.Panedwindow
    'orient': {
        'editor': 'choice',
        'params': {'values': (tk.VERTICAL, tk.HORIZONTAL),
                   'state': 'readonly'},
        'default': tk.HORIZONTAL,
        'help': help_for('orient')
        },
    'overrelief': {
        'editor': 'choice',
        'params': {'values': ('',) + TK_RELIEFS, 'state': 'readonly'},
        'help': help_for('overrelief')
        },
    # ttk.Frame, ttk.Label
    'padding': {
        'editor': 'fourdimensionentry',
        'help': help_for('padding')
        },
    'padx': {
        'editor': 'dimensionentry',
        'help': help_for('padx')
        },
    'pady': {
        'editor': 'dimensionentry',
        'help': help_for('pady')
        },
    # ttk.Checkbutton
    'postcommand': {
        'editor': 'simplecommandentry'},
    'readonlybackground': {
        'editor': 'colorentry'},
    # ttk.Frame,
    'relief': {
        'editor': 'choice',
        'params': {'values': ('',) + TK_RELIEFS, 'state': 'readonly'},
        'help': help_for('relief')
        },
    'repeatdelay': {
        'editor': 'spinbox',
        'params': {'from_': 0, 'to': 9999, 'increment': 100},
        'help': help_for('repeatdelay')
        },
    'repeatinterval': {
        'editor': 'spinbox',
        'params': {'from_': 0, 'to': 9999, 'increment': 100},
        'help': help_for('repeatinterval')
        },
    'resolution': {
        'editor': 'spinbox',
        'params': {'from_': 0, 'to': 999, 'increment': 0.5},
        'help': help_for('resolution')
        },
    'sliderlength': {
        'editor': 'dimensionentry',
        'help': help_for('sliderlength')
        },
    'sliderrelief': {
        'editor': 'choice',
        'params': {'values': ('',) + TK_RELIEFS, 'state': 'readonly'},
        'help': help_for('sliderrelief')
        },
    'sashcursor': {
        'editor': 'choice',
        'params': {'values': ('',) + TK_CURSORS, 'state': 'readonly'}
        },
    'sashpad': {
        'editor': 'entry'},
    'sashrelief': {
        'editor': 'choice',
        'params': {'values': ('',) + TK_RELIEFS, 'state': 'readonly'}},
    'sashwidth': {
        'editor': 'entry'},
    'selectbackground': {
        'editor': 'colorentry',
        'help': help_for('selectbackground')
        },
    'selectborderwidth': {
        'editor': 'spinbox',
        'params': {'from_': 0, 'to': 999},
        'help': help_for('selectborderwidth')
        },
    'selectforeground': {
        'editor': 'colorentry',
        'help': help_for('selectforeground')
        },
    'scrollregion': {
        'editor': 'fourdimensionentry',
        'help': help_for('scrollregion')
        },
    'selectcolor': {
        'editor': 'colorentry'
        },
    'selectimage': {
        'editor': 'imageentry'
        },
    # ttk.Treeview
    'selectmode': {
        'editor': 'choice',
        'help': help_for('selectmode'),
        'params': {
            'values': ('', tk.BROWSE, tk.SINGLE, tk.MULTIPLE, tk.EXTENDED),
            'state': 'readonly'},
        'ttk.Treeview': {
            'params': {
                'values': (tk.EXTENDED, tk.BROWSE, tk.NONE),
                'state': 'readonly'},
            'default': tk.EXTENDED,
            }
        },
    'setgrid': {
        'editor': 'choice',
        'params': {'values': ('', 'false', 'true'), 'state': 'readonly'}},
    # ttk.Entry
    'show': {
        'editor': 'choice',
        'params': {'values': ('', '•'), 'state': 'normal'},
        'help': help_for('show'),
        'ttk.Treeview': {
            'params': {
                'values': ('', 'tree', 'headings'), 'state': 'readonly'},
            'help': help_for('show-ttk.Treeview')
            },
        'pygubu.builder.widgets.editabletreeview': {
            'params': {
                'values': ('', 'tree', 'headings'), 'state': 'readonly'},
            'help': help_for('show-ttk.Treeview')
            },
        },
    'showhandle': {
        'editor': 'choice',
        'params': {'values': ('', 'false', 'true'), 'state': 'readonly'}},
    'showvalue': {
        'editor': 'choice',
        'params': {'values': ('', 'false', 'true'), 'state': 'readonly'},
        'help': help_for('showvalue')
        },
    'spacing1': {
        'editor': 'entry'},
    'spacing2': {
        'editor': 'entry'},
    'spacing3': {
        'editor': 'entry'},
    'startline': {
        'editor': 'entry'},
    'state': {
        'editor': 'choice',
        'help': help_for('state'),
        'params': {'values': ('', tk.NORMAL, tk.DISABLED),
                   'state': 'readonly'},
        'tk.Button': {
            'params': {
                'values': ('', tk.NORMAL, tk.ACTIVE, tk.DISABLED),
                'state': 'readonly'}},
        'tk.Canvas': {
            'params': {
                'values': ('', tk.NORMAL, tk.DISABLED),
                'state': 'readonly'},
            'help': help_for('state-tk.Canvas')
            },
        'tk.Entry': {
            'params': {
                'values': ('', tk.NORMAL, tk.DISABLED, 'readonly'),
                'state': 'readonly'}},
        'tk.Combobox': {
            'params': {
                'values': ('', 'readonly'), 'state': 'readonly'}},
        'ttk.Entry': {
            'params': {
                'values': ('', tk.NORMAL, tk.DISABLED, 'readonly'),
                'state': 'readonly'}},
        'ttk.Combobox': {
            'params': {
                'values': ('', 'normal', 'readonly', 'disabled'),
                'state': 'readonly'}},
        'ttk.Button': {
            'params': {
                'values': ('', 'normal', 'disabled'),
                'state': 'readonly'}},
        'ttk.Notebook.Tab': {
            'params': {
                'values': ('', 'normal', 'disabled', 'hidden'),
                'state': 'readonly'
                }},
        'tk.Spinbox': {
            'params': {
                'values': ('', tk.NORMAL, tk.DISABLED, 'readonly'),
                'state': 'readonly'
                }
            },
    },
    # ttk.Notebook.Tab
    'sticky': {
        'editor': 'stickyentry',
        'params': {}
        },
    # ttk.Treeview.Column
    'stretch': {
        'editor': 'choice',
        'help': help_for('stretch'),
        'ttk.Treeview.Column': {
            'params': {'values': ('true', 'false'), 'state': 'readonly'},
            'default': 'true',
            'help': help_for('stretch-ttk.Treeview')
            },
        'tk.PanedWindow.Pane': {
            'params': {
                'values': ('', 'always', 'first', 'last', 'middle', 'never'),
                'state': 'readonly'}}
        },
    'style': {
        'editor': 'ttkstylechoice',
        'ttk.Button': {
            'params': {'values': ('', 'Toolbutton')}
            },
        'help': help_for('style')
        },
    'tabs': { # FIXME see tk.Text tab property
        'editor': 'entry'
        },
    'tabstyle': {
        'editor': 'choice',
        'params': {
            'values': ('', 'tabular', 'wordprocessor'),
            'state': 'readonly'}
        },
    'takefocus': {
        'editor': 'choice',
        'params': {'values': ('', 'false', 'true'), 'state': 'readonly'},
        'help': help_for('takefocus')
        },
    'tearoff': {
        'editor': 'choice',
        'params': {'values': ('', 'false', 'true'), 'state': 'readonly'}
        },
    'tearoffcommand': {
        'editor': 'simplecommandentry'
        },
    # ttk.Label
    'text': {
        'editor': 'text',
        'help': help_for('text')
        },
    # ttk.Label
    'textvariable': {
        'editor': 'tkvarentry',
        'help': help_for('textvariable')
        },
    'tickinterval': {
        'editor': 'spinbox',
        'params': {'from_': 0, 'to': 999, 'increment': 0.5},
        'help': help_for('tickinterval')
        },
    # ttk.Scale, ttk.Spinbox
    'to': {
        'editor': 'realnumber',
        'help': help_for('to')
        },
    'tristateimage': {
        'editor': 'imageentry'
        },
    'tristatevalue': {
        'editor': 'entry'
        },
    'troughcolor': {
        'editor': 'colorentry',
        'help': help_for('troughcolor')
        },
    # ttk.Label
    'underline': {
        'editor': 'naturalnumber',
        'help': help_for('underline')
        },
    'undo': {
        'editor': 'choice',
        'params': {'values': ('', 'false', 'true'), 'state': 'readonly'}},
    'value': {
        'editor': 'dynamic',
        'help': help_for('value'),
        'params': {'mode': 'entry'},
        'ttk.Progressbar':{
            'params':{'mode':'realnumber'}
            },
        'ttk.Scale':{
            'params':{'mode':'realnumber'}
            },
        },
    # ttk.Checkbutton
    'values': {
        'editor': 'entry'
        },
    'validate': {
        'editor': 'choice',
        'params': {
            'values': ('', 'none', 'focus', 'focusin',
                       'focusout', 'key', 'all'),
            'state': 'readonly'},
        'help': help_for('validate')
        },
    'validatecommand': {
        'editor': 'entryvalidatecommandentry',
        'help': help_for('command-pygubu')
        },
    # ttk.Checkbutton
    'variable': {
        'editor': 'tkvarentry',
        'help': help_for('variable')
        },
    # ttk.Panedwindow.Pane
    'weight': {
        'editor': 'spinbox',
        'params': {'from_': 0, 'to': 999},
        'default': '1',
        },
    # ttk.Frame, ttk.Label
    'width': {
        'editor': 'dynamic',
        'help': help_for('width'),
        'params': {'mode': 'dimensionentry'},
        'tk.Label': {
            'help': help_for('width-tk.Label')
            },
        'tk.Button': {
            'params': {'mode': 'integernumber'},
            'help': help_for('width-tk.Button')
            },
        'tk.Scale': {
            'help': help_for('width-scale')
            },
        'ttk.Button': {
            'params': {'mode': 'integernumber'},
            'help': help_for('width-ttk')
            },
        'tk.Canvas': {
            'params': {'mode': 'entry'}
            },
        'tk.Checkbutton': {
            'params': {'mode': 'integernumber'},
            'help': help_for('width-tk')
            },        
        'ttk.Checkbutton': {
            'params': {'mode': 'integernumber'},
            'help': help_for('width-ttk')
            },
        'tk.Entry': {
            'params': {'mode': 'naturalnumber'},
            'help': help_for('width-tk.Entry')
            },
        'ttk.Entry': {
            'params': {'mode': 'naturalnumber'},
            },
        'tk.Menubutton': {
            'params': {'mode': 'naturalnumber'},
            },
        'ttk.Label': {
            'params': {'mode': 'integernumber'},
            'help': help_for('width-ttk.Label')
            },
        'tk.Listbox': {
            'params': {'mode': 'naturalnumber'},
            },
        'tk.Frame': {
            'default': 200
            },
        'ttk.Frame': {
            'default': 200},
        'tk.LabelFrame': {
            'default': 200},
        'ttk.Labelframe': {
            'default': 200},
        'tk.PanedWindow': {
            'default': 200},
        'ttk.Panedwindow': {
            'default': 200},
        'ttk.Notebook': {
            'default': 200},
        'tk.Radiobutton':{
            'params': {'mode': 'naturalnumber'},
            },
        'ttk.Radiobutton':{
            'params': {'mode': 'integernumber'},
            'help': help_for('width-ttk')
            },
        'tk.Text': {
            'params': {'mode': 'naturalnumber'},
            'default': 50},
        'tk.Toplevel': {
            'default': 200},
        'ttk.Treeview.Column': {
            'params': {'mode': 'naturalnumber'},
            'default': 200,
            'help': help_for('width-ttk.Treeview.Column')
            },
        'pygubu.builder.widgets.dialog': {
            'default': 200}},
    # ttk.Spinbox
    'wrap': {
        'editor': 'choice',
        'params': {
            'values': ('', 'false', 'true'),
            'state': 'readonly'},
        'tk.Text': {
            'params': {
                'values': ('', tk.CHAR, tk.WORD, tk.NONE),
                'state': 'readonly'}}
        },
    # ttk.Label
    'wraplength': {
        'editor': 'dimensionentry',
        'help': help_for('wraplength')
        },
    # ttk.Entry
    'xscrollcommand': {
        'editor': 'scrollsetcommandentry',
        'help': help_for('command-pygubu')
        },
    'xscrollincrement': {
        'editor': 'dimensionentry',
        'help': help_for('xscrollincrement')
        },
    # ttk.Treeview
    'yscrollcommand': {
        'editor': 'scrollsetcommandentry',
        'help': help_for('command-pygubu')
        },
    'yscrollincrement': {
        'editor': 'dimensionentry',
        'help': help_for('yscrollincrement')
        },
    }

REQUIRED_OPTIONS = {
    'class': {
        'editor': 'entry',
        'params': {'state': 'readonly'},
        'help': help_for('class')
    },
    'id': {
        'editor': 'identifierentry',
        'help': help_for('id')
    },
}

CUSTOM_OPTIONS = {
    'geometry': {
        'editor': 'dynamic',
        'params': {
            'mode': 'geometryentry',
            'values': ('', '320x200', '320x240', '352x288', '384x288',
                       '480x320', '640x480', '768x576', '800x480', '800x600',
                       '854x480', '1024x576', '1024x600', '1024x768',
                       '1152x768', '1152x864', '1280x720', '1280x768',
                       '1280x800', '1280x854', '1280x960', '1280x1024',
                       '1366x768', '1400x1050', '1440x1080', '1440x900',
                       '1440x960', '1440x1080', '1600x900', '1600x1050',
                       '1600x1200', '1920x1080', '2048x1080'),
            },
        },
    'iconbitmap': {
        'editor': 'imageentry' },
    'iconphoto': {
        'editor': 'imageentry' },
    'maxsize': {
        'editor': 'whentry'},
    'minsize': {
        'editor': 'whentry'},
    'overrideredirect': {
        'editor': 'choice',
        'params': {'values': ('', 'True', 'False'), 'state': 'readonly'}},
    'resizable': {
        'editor': 'choice',
        'params': {
            'values': ('', 'both', 'horizontally', 'vertically', 'none'),
            'state': 'readonly'}},
    'scrolltype': {
        'editor': 'choice',
        'params': {
            'values': ('both', 'vertical', 'horizontal'),
            'state': 'readonly'},
        'default': 'both'},
    'text': {
        'editor': 'text',
        'help': help_for('text-custom')
        },
    'title': {
        'editor': 'entry'
        },
    'tree_column': {
        'editor': 'choice',
        'params': {'values': ('true', 'false'), 'state': 'readonly'},
        'default': 'false',
        'help': help_for('tree_column-custom')
        },
    'usemousewheel': {
        'editor': 'choice',
        'params': {
            'values': ('true', 'false'),
            'state': 'readonly'},
        'default': 'false'},
    'visible': {
        'editor': 'choice',
        'params': {'values': ('true', 'false'), 'state': 'readonly'},
        'default': 'true',
        'help': help_for('visible-custom')
        },
    'specialmenu': {
        'editor': 'choice',
        'params': {'values': ('apple', 'help', 'window', 'system'), 'state': 'readonly'}
        },
    }

WIDGET_REQUIRED_OPTIONS = ('class', 'id')
WIDGET_STANDARD_OPTIONS = (
    'activerelief', 'activestyle', 'activebackground',
    'activeborderwidth', 'activeforeground', 'after',
    'anchor', 'background', 'bitmap', 'borderwidth',
    'class_', 'compound', 'cursor', 'disabledforeground',
    'exportselection',
    'font', 'foreground', 'jump', 'highlightbackground',
    'highlightcolor', 'highlightthickness', 'image',
    'indicatoron', 'insertbackground',
    'insertborderwidth', 'insertofftime', 'insertontime', 'insertwidth',
    'justify', 'orient', 'padx', 'pady', 'relief',
    'repeatdelay', 'repeatinterval', 'selectbackground', 'selectborderwidth',
    'selectforeground', 'setgrid', 'state', 'style', 'takefocus', 'text',
    'textvariable', 'troughcolor', 'underline', 'width', 'wraplength',
    'xscrollcommand', 'yscrollcommand')

WIDGET_SPECIFIC_OPTIONS = (
    'accelerator', 'activestyle', 'activerelief', 'anchor', 'aspect',
    'autoseparators', 'background', 'bigincrement',
    'blockcursor', 'borderwidth', 'buttonbackground', 'buttoncursor',
    'buttondownrelief', 'buttonuprelief',
    'class_', 'column_anchor', 'columnbreak', 'command', 'compound', 'container',
    'closeenough', 'confine', 'default', 'digits', 'direction',
    'disabledbackground', 'disabledforeground', 'elementborderwidth',
    'endline', 'exportselection', 'font',
    'foreground', 'format', 'from_', 'to',
    'handlepad', 'handlesize', 'hidemargin', 'heading_anchor', 'height', 'image',
    'inactiveselectbackground', 'increment', 'indicatoron', 'insertunfocussed',
    'invalidcommand', 'justify',
    'label', 'labelanchor', 'listvariable', 'length',
    'maximum', 'maxundo',
    'minsize', 'minwidth', 'mode', 'offrelief', 'offvalue',
    'onvalue', 'opaqueresize', 'orient', 'overrelief',
    'padding', 'padx', 'pady',
    'postcommand', 'readonlybackground', 'relief', 'resolution',
    'scrollregion', 'sashcursor', 'sashpad', 'sashrelief', 'sashwidth',
    'selectcolor', 'selectimage', 'selectmode', 'show',
    'showhandle', 'showvalue', 'sliderlength', 'sliderrelief',
    'spacing1', 'spacing2', 'spacing3', 'startline',
    'state', 'sticky', 'stretch', 'tabs', 'tabstyle',
    'text', 'textvariable', 'tickinterval', 'tristateimage',
    'tristatevalue', 'underline', 'validate', 'undo', 'validatecommand',
    'value', 'values', 'variable', 'weight', 'width', 'wrap',
    'wraplength', 'xscrollcommand', 'xscrollincrement', 'yscrollincrement',
    'tearoff', 'tearoffcommand'
    )

WIDGET_CUSTOM_OPTIONS = [
    'tree_column', 'visible', 'scrolltype', 'text', 'title',
    'geometry', 'overrideredirect', 'resizable', 'minsize',
    'maxsize', 'usemousewheel', 'iconbitmap', 'iconphoto',
    'specialmenu', 
    ]

WIDGET_PROPERTIES = wp = dict(TK_WIDGET_OPTIONS)
wp.update(REQUIRED_OPTIONS)
wp.update(CUSTOM_OPTIONS)

LAYOUT_OPTIONS = {
    # pack/grid/place common properties
    'padx': {
        'editor': 'twodimensionentry',
        'help': help_for('padx-layout')
        },
    'pady': {
        'editor': 'twodimensionentry',
        'help': help_for('pady-layout')
        },
    'ipadx': {
        'editor': 'twodimensionentry',
        'help': help_for('ipadx-layout')
        },
    'ipady': {
        'editor': 'twodimensionentry',
        'help': help_for('ipady-layout')
        },
    'propagate': {
        'editor': 'choice',
        'params': {'values': ('True', 'False'), 'state': 'readonly'},
        'default': 'True',
        'help': help_for('propagate-layout')
        },
    'anchor': {
        'editor': 'choice',
        'params': {
            'values': ('', 'n', 'ne', 'nw', 'e', 'w', 's', 'se', 'sw', 'center'),
            'state': 'readonly'
            },
        'help': help_for('anchor-layout'),
        'place': {
            'default': 'nw',
            'help': help_for('anchor-layout-place')
            }
        },
    
    # pack properties
    'expand':{
        'editor': 'choice',
        'params': {'values': ('', 'false', 'true'), 'state': 'readonly'},
        'help': help_for('expand-pack')
        },
    'fill':{
        'editor': 'choice',
        'params': {'values': ('', 'x', 'y', 'both'), 'state': 'readonly'},
        'help': help_for('fill-pack')
        },
    'side':{
        'editor': 'choice',
        'params': {
            'values': ('top', 'bottom', 'left', 'right'),
            'state': 'readonly'
            },
        'default': 'top',
        'help': help_for('side-pack')
        },
    'bordermode':{
        'editor': 'choice',
        'params':{
            'values': ('', 'inside', 'outside', 'ignore'),
            'state': 'readonly'},
        'help': help_for('bordermode-pack')
        },
    'height':{
        'editor': 'pixelcoordinateentry',
        'help': help_for('height-pack')
        },
    'relheight':{
        'editor': 'relativeentry',
        'help': help_for('relheight-pack')
        },
    'relwidth':{
        'editor': 'relativeentry',
        'help': help_for('relwidth-pack')
        },
    'relx':{
        'editor': 'relativeentry',
        'help': help_for('relx-pack')
        },
    'rely':{
        'editor': 'relativeentry',
        'help': help_for('rely-pack')
        },
    'width':{
        'editor': 'pixelcoordinateentry',
        'help': help_for('width-pack')
        },
    'x':{
        'editor': 'pixelcoordinateentry',
        'default': '0',
        'help': help_for('x-pack')
        },
    'y':{
        'editor': 'pixelcoordinateentry',
        'default': '0',
        'help': help_for('y-pack')
        },
    #
    # grid packing properties
    #
    'row': {
        'editor': 'naturalnumber',
        'default': '0',
        'help': help_for('row-grid')
        },
    'column': {
        'editor': 'naturalnumber',
        'default': '0',
        'help': help_for('column-grid')
        },
    'sticky': {
        'editor': 'stickyentry',
        'params': {},
        'help': help_for('sticky-grid')
        },
    'rowspan': {
        'editor': 'naturalnumber',
        'help': help_for('rowspan-grid')
        },
    'columnspan': {
        'editor': 'naturalnumber',
        'help': help_for('columnspan-grid')
        },
    #
    # grid row and column properties (can be applied to each row or column)
    'minsize': {
        'editor': 'dimensionentry',
        'params': {'width': 4, 'empty_data': 0},
        'help': help_for('minsize-grid')
        },
    'pad': {
        'editor': 'dimensionentry',
        'params': {'width': 4, 'empty_data': 0},
        'help': help_for('pad-grid')
        },
    'weight': {
        'editor': 'naturalnumber',
        'help': help_for('weight-grid')
    },
    'uniform': {
        'editor': 'alphanumentry',
        'help': help_for('uniform-grid')
    }
}

# List properties in display order
MANAGER_PROPERTIES = (
    'anchor', 
    'relx', 'rely', 'relwidth', 'relheight',
    'x', 'y', 'width', 'height', 'bordermode',
    'side', 'expand', 'fill',
    'row', 'column', 'sticky', 'rowspan', 'columnspan', 'padx', 'pady',
    'ipadx', 'ipady', 'propagate'
)

GRID_PROPERTIES = (
    'row', 'column', 'sticky', 'rowspan', 'columnspan', 'padx', 'pady',
    'ipadx', 'ipady', 'propagate')

PACK_PROPERTIES = (
    'anchor', 'side', 'expand', 'fill', 'padx', 'pady',
    'ipadx', 'ipady', 'propagate')

PLACE_PROPERTIES = (
    'anchor', 'relx', 'rely', 'relwidth', 'relheight',
    'x', 'y', 'width', 'height', 'bordermode', 
)

GRID_RC_PROPERTIES = ('minsize', 'pad', 'weight', 'uniform')

TRANSLATABLE_PROPERTIES = (
    'label', 'text', 'title',
)


def _register_custom(name, descr):
    if name not in CUSTOM_OPTIONS:
        CUSTOM_OPTIONS[name] = descr
        WIDGET_PROPERTIES.update(CUSTOM_OPTIONS)
        WIDGET_CUSTOM_OPTIONS.append(name)
        WIDGET_CUSTOM_OPTIONS.sort()
        logger.debug('Registered property: %s', name)

def register_property(name, descr):
    _register_custom(name, descr)
    builderobject._old_register_property(name, descr)

if not hasattr(builderobject, '_register_fixed_'):
    for name, descr in builderobject.CUSTOM_PROPERTIES.items():
        _register_custom(name, descr)
    builderobject._register_fixed_ = True
    builderobject._old_register_property = builderobject.register_property
    builderobject.register_property = register_property
    logger.debug('Installed custom register_property function')
