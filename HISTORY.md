History
=======

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
