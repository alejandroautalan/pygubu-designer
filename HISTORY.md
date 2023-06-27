History
=======

Changes for version 0.37 (next)

  * Customize open file dialog on Gnu/Linux.
  * New format for ttk style definition file. #204, #211
  * New settings to auto generate code in Code Tab. (BloodyRain2k)
  * Fix scrolling in toolbar frame (BloodyRain2k)
  * New option to render widget palette as a single section widget toolbar.
    Changes the widget toolbar to contain all chosen widgets instead of grouping them with tabs.
    Useful for wide monitors. (BloodyRain2k)
  * Type hints for tk variables in code generation. (BloodyRain2k)
  * Add template code to center window at start. (BloodyRain2k)

Changes for version 0.36

  * Add option to auto generate code when code template is changed. refs #208
  * Fix event names, refs #197
  * Changed template code to call ttk styles on first object created. refs alejandroautalan/pygubu#282

Changes for version 0.35

  * Quick fix to allow tkinter dark themes on designer. refs #195
  * Fix error when font is not correctly defined in option database (by the user).
  * Container Layout Fix remove hover on widget leave.

Changes for version 0.34

  * Check main window visibility at start. refs #145
  * Show log info when using --loglevel debug
  * Code generator: Import tk when creating variable.
  * Updated pathchooser demo example.
  * Use method str.isidentifier() for identifiers.
  * Internal tkvariable editor: Allow to specify default type of tkvariable.

Changes for version 0.33

  * Show dimension of preview in pixels.
  * Fix issue when working with Notebook tabs.
  * Fix validation of classname. closes #159
  * Added support for ttk.OptionMenu and ttk.LabeledScale
  * Update tooltip text. Closes #162
  * Respect background of current style. closes #166
  * Update Chinese Translations. PR  #168 larryw3i

Changes for version 0.32

  * Added support for customtkinter and tkintermapview.
  * Removed property groups in Appearance tab (needed for plugins and future tooltip property).

Changes for version 0.31.3

 * Fix for issues #154, #155
 * Update zh_CN translations #158 (larryw3i).

Changes for version 0.31.2

 * Hotfix, reset code tab on load file.

Changes for version 0.31

 * Use a lighter code formatter. Removed black, use autopep8. refs #152
 * Fix AttributeError: 'Dialog' object has no attribute 'update_idletasks' when pressing F5
 * Add example integration with python zipapp module. refs alejandroautalan/pygubu#269

Changes for version 0.30

  * New selected indicator in preview.
  * Completed menu support for code generator (issue #103)
  * Decluttering for widget IDs (issue #117)

Changes for version 0.29.1

  * Hotfix:  Fix template path in preferences window #147 (jrezai)
  
Changes for version 0.29

  * Changed project structure to use src folder.
  * Added internal cursor property editor.
  * Adapted code to use pygubu plugin engine
  * Merged pull request #138 from jrezai/master

Changes for version 0.28

  * Added more examples
  * Fix: 'filedialog.askopenfilename' is blocked by 'preferences.dialog' (larryw3i).
  * Translations for pygubu strings in pygubu-designer (larryw3i)

Changes for version 0.27

  * Add option to center the toplevel preview window. PR #124 @jrezai
  * Fix error loading ui file. issue #123
  * Added option for i18n support in code generated. issue #120
  * Added option for select main menu for generated app. issue #103 (partially fixed)

Changes for version 0.26.1

  * Hot fix: Error when loading old UI files. issue #123

Changes for version 0.26

  * Fix name collisions between widget ids, variables and commands. #115
  * Fix issue with Delete key in macOS. #119
  * Fix wiki links. #118

Changes for version 0.25

  * Make more intuitive design screen labels. #87
  * Fix options of wrap property for ScrolledText. #98
  * Improve style of generated code. #84, #85, #89, #92
  * Use black as formatter for generated code.
  * Add a new context command menu to select the current item's parent. #97, @jrezai
  * Fix Toplevel preview issues. @jrezai
  * Fix issue when changing geometry manager. #77, #80, @jrezai
  * Examples updated.

Changes for version 0.24

  * Removed Python 2.7 support, Minimum Python version required is now 3.6
  * New layout editor for container widgets. Added support to configure grid with 'all' index (issue #76)

Changes for version 0.23

  * Add support to use custom ttk styles defined by the user. Thanks to @jrezai
  * This is the last version with python 2.7 support
  * Other minor bug fixes.
