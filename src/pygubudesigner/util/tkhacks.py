import sys
import tkinter as tk


def filedialog_hack(master: tk.Widget):
    # Customize OpenFiledialog window
    if sys.platform == "linux":
        scaling_cmd = f"tk scaling -displayof {master}"
        tk_scaling = float(master.tk.eval(scaling_cmd))
        fd_width = int(tk_scaling * 510)
        fd_height = int(tk_scaling * 262)
        # print(f"{tk_scaling} {dialog_width} {dialog_height}")

        file_dialog_hack = """
# Show button and hide hidden files
catch {tk_getOpenFile -badoption}
set ::tk::dialog::file::showHiddenBtn 1
set ::tk::dialog::file::showHiddenVar 0

# Make dialog window bigger
rename ::tk::dialog::file::Create ::tk::dialog::file::_CreateOriginal
proc ::tk::dialog::file::Create {w class} {
    eval ::tk::dialog::file::_CreateOriginal $w $class
    wm geometry $w {dialog_geometry}
}"""
        file_dialog_hack = file_dialog_hack.replace(
            "{dialog_geometry}", f"{fd_width}x{fd_height}"
        )
        master.tk.eval(file_dialog_hack)
