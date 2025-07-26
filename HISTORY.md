History
=======

Changes for version 0.41.3

  * Fix for issue #302, missing .gif images for tk 8.5

Changes for version 0.41.2

  * Treeview, fix incorrect editor for xscroll command.

Changes for version 0.41.1

  * Allow to specify screen units for width/height/x/y place manager properties and other widgets. refs #295

Changes for version 0.41

  * Use point instead of pixels in designer UI. Fix glitches on high dpi screens.
  * Enable image auto scaling for high dpi screens.
  * Fix filedialog size in high dpi screens (Linux)
  * Fix for issue #284
  * Improved container layout editor for grid manager.
  * Fix window centerig code in code templates.

Changes for version 0.40.2

  * Fix python 3.8, 3.9 compatibility.

Changes for version 0.40.1

  * Fix: Treeview rows overlap in high dpi screen. refs #283
  * Sticky editor: Draw widget bigger on high dpi screen.
  * GridSelector: Draw widget bigger on high dpi screen.

Changes for version 0.40

  * Add backspace key to trigger delete action. (#269 @Tweety24655)
  * Set menu tearoff to false by default.
  * In style property editor: show Toolbutton ttk class for Button, Checkbutton and Radiobutton widgets.
  * Add builder data_pool parameter in templates.
  * Add min and max options to number editors.
  * New json_entry property editor.

Changes for version 0.39.3

  * Fix for issues #251 and #253
  * Drop support for python 3.6 and 3.7 (was already not working)

Changes for version 0.39.2

  * Fix issue with project path with windows junction link. refs #249
  * Fix code template error.
  * Fix error when "live" updating preview properties
  * Added new example for EditableTreeview

Changes for version 0.39.1

  * Add option to reset window layout. (#244 @jrezai)

Changes for version 0.39

  * New UI Layout. Removed code generation Tab.
  * New project settings dialog.
  * Cleaned designer settings dialog.

Changes for version 0.38

  * Update to support customtkinter 5.2.2

Changes for version 0.37

  * Customize open file dialog on Gnu/Linux.
  * New format for ttk style definition file. alejandroautalan/pygubu-designer#204, alejandroautalan/pygubu-designer#211
  * New settings to auto generate code in Code Tab. (BloodyRain2k)
  * Fix scrolling in toolbar frame (BloodyRain2k)
  * New option to render widget palette as a single section widget toolbar.
    Changes the widget toolbar to contain all chosen widgets instead of grouping them with tabs.
    Useful for wide monitors. (BloodyRain2k)
  * Type hints for tk variables in code generation. (BloodyRain2k)
  * Add template code to center window at start. (BloodyRain2k)
  * New Vietnamese translation for README.md (lebao3105)
  * Update Chinese Translation (littlewhitecloud)

Changes for version 0.36

  * Add option to auto generate code when code template is changed. refs alejandroautalan/pygubu-designer#208
  * Fix event names, refs alejandroautalan/pygubu-designer#197
  * Changed template code to call ttk styles on first object created. refs alejandroautalan/pygubu#282

Changes for version 0.35

  * Quick fix to allow tkinter dark themes on designer. refs alejandroautalan/pygubu-designer#195
  * Fix error when font is not correctly defined in option database (by the user).
  * Container Layout Fix remove hover on widget leave.

Changes for version 0.34

  * Check main window visibility at start. refs alejandroautalan/pygubu-designer#145
  * Show log info when using --loglevel debug
  * Code generator: Import tk when creating variable.
  * Updated pathchooser demo example.
  * Use method str.isidentifier() for identifiers.
  * Internal tkvariable editor: Allow to specify default type of tkvariable.

Changes for version 0.33

  * Show dimension of preview in pixels.
  * Fix issue when working with Notebook tabs.
  * Fix validation of classname. closes alejandroautalan/pygubu-designer#159
  * Added support for ttk.OptionMenu and ttk.LabeledScale
  * Update tooltip text. Closes alejandroautalan/pygubu-designer#162
  * Respect background of current style. closes alejandroautalan/pygubu-designer#166
  * Update Chinese Translations. PR  alejandroautalan/pygubu-designer#168 larryw3i

Changes for version 0.32

  * Added support for customtkinter and tkintermapview.
  * Removed property groups in Appearance tab (needed for plugins and future tooltip property).

Changes for version 0.31.3

 * Fix for issues alejandroautalan/pygubu-designer#154, alejandroautalan/pygubu-designer#155
 * Update zh_CN translations alejandroautalan/pygubu-designer#158 (larryw3i).

Changes for version 0.31.2

 * Hotfix, reset code tab on load file.

Changes for version 0.31

 * Use a lighter code formatter. Removed black, use autopep8. refs alejandroautalan/pygubu-designer#152
 * Fix AttributeError: 'Dialog' object has no attribute 'update_idletasks' when pressing F5
 * Add example integration with python zipapp module. refs alejandroautalan/pygubu#269

Changes for version 0.30

  * New selected indicator in preview.
  * Completed menu support for code generator (issue alejandroautalan/pygubu-designer#103)
  * Decluttering for widget IDs (issue alejandroautalan/pygubu-designer#117)

Changes for version 0.29.1

  * Hotfix:  Fix template path in preferences window alejandroautalan/pygubu-designer#147 (jrezai)

Changes for version 0.29

  * Changed project structure to use src folder.
  * Added internal cursor property editor.
  * Adapted code to use pygubu plugin engine
  * Merged pull request alejandroautalan/pygubu-designer#138 from jrezai/master

Changes for version 0.28

  * Added more examples
  * Fix: 'filedialog.askopenfilename' is blocked by 'preferences.dialog' (larryw3i).
  * Translations for pygubu strings in pygubu-designer (larryw3i)

Changes for version 0.27

  * Add option to center the toplevel preview window. PR alejandroautalan/pygubu-designer#124 @jrezai
  * Fix error loading ui file. issue alejandroautalan/pygubu-designer#123
  * Added option for i18n support in code generated. issue alejandroautalan/pygubu-designer#120
  * Added option for select main menu for generated app. issue alejandroautalan/pygubu-designer#103 (partially fixed)

Changes for version 0.26.1

  * Hot fix: Error when loading old UI files. issue alejandroautalan/pygubu-designer#123

Changes for version 0.26

  * Fix name collisions between widget ids, variables and commands. alejandroautalan/pygubu-designer#115
  * Fix issue with Delete key in macOS. alejandroautalan/pygubu-designer#119
  * Fix wiki links. alejandroautalan/pygubu-designer#118

Changes for version 0.25

  * Make more intuitive design screen labels. alejandroautalan/pygubu-designer#87
  * Fix options of wrap property for ScrolledText. alejandroautalan/pygubu-designer#98
  * Improve style of generated code. alejandroautalan/pygubu-designer#84, alejandroautalan/pygubu-designer#85, alejandroautalan/pygubu-designer#89, alejandroautalan/pygubu-designer#92
  * Use black as formatter for generated code.
  * Add a new context command menu to select the current item's parent. alejandroautalan/pygubu-designer#97, @jrezai
  * Fix Toplevel preview issues. @jrezai
  * Fix issue when changing geometry manager. alejandroautalan/pygubu-designer#77, alejandroautalan/pygubu-designer#80, @jrezai
  * Examples updated.

Changes for version 0.24

  * Removed Python 2.7 support, Minimum Python version required is now 3.6
  * New layout editor for container widgets. Added support to configure grid with 'all' index (issue alejandroautalan/pygubu-designer#76)

Changes for version 0.23

  * Add support to use custom ttk styles defined by the user. Thanks to @jrezai
  * This is the last version with python 2.7 support
  * Other minor bug fixes.
