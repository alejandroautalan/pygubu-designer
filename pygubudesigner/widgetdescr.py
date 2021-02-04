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
import logging

from pygubu.builder import CLASS_MAP
from pygubu.builder.widgetmeta import WidgetMeta as WidgetMetaBase, BindingMeta
from .util.observable import Observable
from .properties import (WIDGET_PROPERTIES, PACK_PROPERTIES, PLACE_PROPERTIES,
                         GRID_PROPERTIES, LAYOUT_OPTIONS)

logger = logging.getLogger(__name__)


class WidgetMeta(WidgetMetaBase, Observable):
    
    def apply_layout_defaults(self):
        super(WidgetMeta, self).apply_layout_defaults()
        self.notify('LAYOUT_CHANGED', self)
        
    def widget_property(self, name, value=None):
        if value is None:
            if name == 'id':
                return self.identifier
            elif name == 'class':
                return self.classname
            else:
                return self.properties.get(name, '')
        else:
            # Setter
            if name == 'id':
                self.identifier = value
            elif name == 'class':
                self.classname = value
            else:
                if value:
                    self.properties[name] = value
                else:
                    # remove if no value set
                    self.properties.pop(name, None)
            self.notify('PROPERTY_CHANGED', self)
    
    def layout_property(self, name, value=None):
        if value is None:
            # Getter
            default = ''
            if name in ('row', 'column'):
                default = '0'
            return self.layout_properties.get(name, default)
        else:
            # Setter
            if value:
                self.layout_properties[name] = value
            else:
                # remove if no value set
                self.layout_properties.pop(name, None)
            self.notify('LAYOUT_CHANGED', self)
    
    def gridrc_property(self, type_, num, pname, value=None):
        if value is None:
            # Getter
            default = '0'
            if pname == 'uniform':
                default = ''
            pvalue = self.get_gridrc_value(type_, num, pname)
            pvalue = pvalue if pvalue is not None else default
            return pvalue
        else:
            # Setter
            self.set_gridrc_value(type_, num, pname, value)
            self.notify('LAYOUT_GRIDRC_CHANGED', self)

    
    @property
    def manager(self):
        return self._manager
    
    @manager.setter
    def manager(self, value):
        if self._manager != value:
            self._manager = value
            self.clear_layout()
        self.notify('LAYOUT_CHANGED', self)

    def get_bindings(self):
        blist = []
        for v in self.bindings:
            blist.append((v.sequence, v.handler, v.add))
        return blist

    def clear_bindings(self):
        self.bindings = []

    def add_binding(self, seq, handler, add):
        self.bindings.append(BindingMeta(seq, handler, add))

    def remove_unused_grid_rc(self):
        """Deletes unused grid row/cols"""
        pass
    
    def setup_defaults(self):
        propd, layoutd = WidgetMeta.get_widget_defaults(self, self.identifier)
        self.properties_defaults = propd
        self.layout_defaults = layoutd
    
    @staticmethod
    def get_widget_defaults(wclass, widget_id):
        properties = {}
        layout = {}
        
        if wclass in CLASS_MAP:
            # setup default values for properties
            for pname in CLASS_MAP[wclass].builder.properties:
                pdescription = {}
                if pname in WIDGET_PROPERTIES:
                    pdescription = WIDGET_PROPERTIES[pname]
                if wclass in pdescription:
                    pdescription = dict(pdescription, **pdescription[wclass])
                default_value = str(pdescription.get('default', ''))
                if default_value:
                    properties[pname] = default_value
                # default text for widgets with text prop:
                if pname in ('text', 'label'):
                    properties[pname] = widget_id
        
        # setup default values for layout
        groups = (
            ('pack', PACK_PROPERTIES),
            ('place', PLACE_PROPERTIES),
            ('grid', GRID_PROPERTIES),
        )
        for manager, manager_prop in groups:
            layout[manager] = {}
            for pname in manager_prop:
                pdescr = LAYOUT_OPTIONS[pname]
                if manager in pdescr:
                    pdescr = pdescr.copy()
                    pdescr = dict(pdescr, **pdescr[manager])
                default_value = pdescr.get('default', None)
                if default_value:
                    layout[manager][pname] = default_value
        return properties, layout

