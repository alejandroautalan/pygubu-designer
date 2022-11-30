import os
import shlex
import pathlib
import subprocess as sp


PROJECT_DIR = pathlib.Path(__file__).parent.parent
SRC_DIR = PROJECT_DIR / "src"
DATA_DIR = SRC_DIR / "pygubudesigner" / "data"
PYGUBU_SRC_DIR = pathlib.Path("..") / PROJECT_DIR.parent / "pygubu" / "src"

locale_dir = DATA_DIR / "locale"


def create_pot():
    pot_path = locale_dir / "pygubu-designer.pot"
    ui_dir = DATA_DIR / "ui"
    uifiles = [f.relative_to(PROJECT_DIR) for f in ui_dir.glob("**/*.ui")]
    uifiles = " ".join([str(f) for f in uifiles])
    options = "--package-name pygubudesigner -L glade"
    cmd = f"""xgettext {options} --output={pot_path} {uifiles}"""
    sp.run(shlex.split(cmd))

    pyfiles = [f.relative_to(PROJECT_DIR) for f in SRC_DIR.glob("**/*.py")]
    pyfiles = " ".join([str(f) for f in pyfiles])
    options = (
        "--package-name pygubudesigner --join-existing -L Python --keyword=_ "
    )
    cmd = f"xgettext {options} --output={pot_path} --from-code=UTF-8 {pyfiles}"
    sp.run(shlex.split(cmd))

    pot_path = DATA_DIR / "locale" / "pygubu.pot"
    pyfiles = [
        os.path.relpath(f, PROJECT_DIR) for f in PYGUBU_SRC_DIR.glob("**/*.py")
    ]
    pyfiles = " ".join([str(f) for f in pyfiles])
    options = "--package-name pygubu -L Python --keyword=_"
    cmd = f"xgettext {options} --output={pot_path} --from-code=UTF-8 {pyfiles}"
    sp.run(shlex.split(cmd))


def update_po():
    pot_path = locale_dir / "pygubu-designer.pot"
    # update designer po files
    for f in locale_dir.glob("*/*/pygubu-designer.po"):
        cmd = f"msgmerge --verbose {f} {pot_path} -U"
        sp.run(shlex.split(cmd))

    pot_path = DATA_DIR / "locale" / "pygubu.pot"
    # update pygubu po files
    for f in locale_dir.glob("*/*/pygubu.po"):
        cmd = f"msgmerge --verbose {f} {pot_path} -U"
        sp.run(shlex.split(cmd))


def compile_po():
    for pofile in locale_dir.glob("*/*/*.po"):
        mofile = pofile.with_suffix(".mo")
        cmd = f"msgfmt --verbose -o {mofile} {pofile}"
        sp.run(shlex.split(cmd))


def main():
    # create_pot()
    # update_po()
    compile_po()


if __name__ == "__main__":
    main()
