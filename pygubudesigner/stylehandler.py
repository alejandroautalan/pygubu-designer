# encoding: UTF-8
#
# Copyright 2012-2021 Alejandro Autalán
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
import json
import logging
from os import path, stat
from pygubu import builder
from pygubudesigner import preferences as pref
from pygubudesigner.widgets.ttkstyleentry import TtkStylePropertyEditor


logger = logging.getLogger(__name__)
CLASS_MAP = builder.CLASS_MAP

class StyleHandler:
    
    update_ttk_styles_func = None
    last_modified_definition_file = None
    last_modified_population_file = None

    def __init__(self, properties_editor):
        
        self.properties_editor = properties_editor
        self.style_property_editor = None
        self.after_token = None
        
    @staticmethod
    def _get_ttk_style_definition():
        """
        Return the ttk style code as a string.
        """
        contents = None
        
        # Get the path to the style definition file.
        style_definition_path = pref.get_option('v_style_definition_file')
        
        if path.isfile(style_definition_path):
        
            with open(style_definition_path) as f:
                contents = f.read()
                
            if not StyleHandler.last_modified_definition_file:
                file_info = stat(style_definition_path)
                StyleHandler.last_modified_definition_file = file_info.st_mtime
                
        return contents
        
    @staticmethod
    def _get_ttk_style_populate():
        """
        Return the style population code as a dictionary.
        """
        data = None
        
        # Get the path to the style population file.
        style_population_path = pref.get_option('v_style_population_file')        
        
        if path.isfile(style_population_path):
            with open(style_population_path) as f:
                contents = f.read()
                
                data = json.loads(contents)
                
            if not StyleHandler.last_modified_population_file:
                file_info = stat(style_population_path)
                StyleHandler.last_modified_population_file = file_info.st_mtime                
            
        return data

    def find_style_property_editor(self, pname, editor):
        """
        Find the style editor drop-down so we can populate it in a different method. 
        """

        # Look for the widget that contains a combobox.
        # The widget we're looking for is: TtkStylePropertyEditor
        for c in editor.winfo_children():
            if isinstance(c, TtkStylePropertyEditor):
                # We found the drop-down menu widget
                
                # Keep track of it so we can update populate it
                # with a list of styles.
                self.style_property_editor = c
                
                self.populate_ttk_style_list()
                
                
                if self.after_token:
                    self.style_property_editor.after_cancel(self.after_token)
                self.after_token = self.style_property_editor.after(1000, self.check_for_file_changes)
    
    def populate_ttk_style_list(self):

        style_names = []
        
        # Get the user-defined style definitions as a dictionary
        style_data = self._get_ttk_style_populate()
        
        # Get the current style that's selected in the Style combobox
        # because if the current style is not in the population list,
        # then the current style combobox text should be cleared.
        current_style = self.style_property_editor._combobox.get()
        
        style_exists_in_population_list = False
        
        # If the current widget that is selected is compatible
        # with one or more styles, list the compatible styles in the 'style'
        # drop-down.
        if style_data and isinstance(style_data, dict):
            for k, v in style_data.items():
                if self.properties_editor._current.classname in v:
                    if current_style and current_style == k:
                        style_exists_in_population_list = True
                    style_names.append(k)
        
        # Update 'style' drop-down menu.
        self.style_property_editor.parameters(values=style_names)     
        
        if not style_exists_in_population_list:
            # The user has a style selected that is not 
            # in the style population list. So clear the current style.
            self.style_property_editor._combobox.set('')

            self.reload_definition_file()
        
    def check_definition_file(self):
    
        # Get the path to the style definition file.
        style_definition_path = pref.get_option('v_style_definition_file')     
        
        if path.isfile(style_definition_path):
            file_info = stat(style_definition_path)
            
            if file_info.st_mtime != StyleHandler.last_modified_definition_file:
                StyleHandler.last_modified_definition_file = file_info.st_mtime
                self.reload_definition_file()
                
                print("Reloaded definition file")
                
    def check_population_file(self):
    
        # Get the path to the style population file.
        style_population_path = pref.get_option('v_style_population_file')     
        
        if path.isfile(style_population_path):
            file_info = stat(style_population_path)
            
            if file_info.st_mtime != StyleHandler.last_modified_population_file:
                StyleHandler.last_modified_population_file = file_info.st_mtime
                self.reload_population_file()
                

                print('Reloaded population file')
        
    def reload_definition_file(self):
        
        if StyleHandler.update_ttk_styles_func:
            StyleHandler.update_ttk_styles_func()
        
    def reload_population_file(self):
        
        self.populate_ttk_style_list()
        
    def check_for_file_changes(self):
        
        self.check_definition_file()
        self.check_population_file()
        self.after_token = self.style_property_editor.after(1000, self.check_for_file_changes)
        