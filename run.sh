#!/bin/bash
#
# usage: ./run.sh command [argument ...]
#
# Commands used during development / CI.
# Also, executable documentation for project dev practices.
#
# See https://death.andgravity.com/run-sh
# for an explanation of how it works and why it's useful.


# First, set up the environment.
# (Check the notes at the end when changing this.)

set -o nounset
set -o pipefail
set -o errexit

# Change the current directory to the project root.
PROJECT_ROOT=${0%/*}
if [[ $0 != $PROJECT_ROOT && $PROJECT_ROOT != "" ]]; then
    cd "$PROJECT_ROOT"
fi
readonly PROJECT_ROOT=$( pwd )

# Store the absolute path to this script (useful for recursion).
readonly SCRIPT="$PROJECT_ROOT/$( basename "$0" )"



# Commands follow.

# System requirements:
# apt install python3-build twine
#

DESIGNER_MODULE_ROOT_DIR="./src/pygubudesigner"

python3bin=$(which python3)

function tests {
    cd tests; $python3bin -W default -m unittest -v; cd ..;
}

function build {
    $python3bin -m build
}

function upload_testpypi {
    build
    twine upload --skip-existing -r test_pygubu_designer dist/*
}

function upload_pypi {
    build
    twine upload --skip-existing -r pygubu_designer_project dist/*
}

function create_pot {
    # Pygubu designer
    pkg_name="pygubudesigner"
    pot_path="$DESIGNER_MODULE_ROOT_DIR/data/locale/pygubu-designer.pot"
    ui_files=$(find ${DESIGNER_MODULE_ROOT_DIR}/data/ui -name "*.ui" | sort | paste -d " ")
    # echo $ui_files
    xgettext \
        --package-name $pkg_name \
        --language=Glade \
        --verbose \
        --output=${pot_path} \
        $ui_files
    py_files=$(find ${DESIGNER_MODULE_ROOT_DIR} -name "*.py" | sort | paste -d " ")
    # echo $py_files
    xgettext \
        --package-name $pkg_name \
        --join-existing \
        --language=Python \
        --keyword=_ \
        --verbose \
        --output=${pot_path} \
        --from-code=UTF-8 \
        $py_files

    #
    # Pygubu
    pkg_name="pygubu"
    pot_path="$DESIGNER_MODULE_ROOT_DIR/data/locale/pygubu.pot"
    PYGUBU_SRC_DIR="../pygubu/src/pygubu"
    py_files=$(find ${PYGUBU_SRC_DIR} -name "*.py" | sort | paste -d " ")
    # echo $py_files
    xgettext \
        --package-name $pkg_name \
        --language=Python \
        --keyword=_ \
        --verbose \
        --output=${pot_path} \
        --from-code=UTF-8 \
        $py_files
}

function update_po {
    pot_designer="$DESIGNER_MODULE_ROOT_DIR/data/locale/pygubu-designer.pot"
    pot_pygubu="$DESIGNER_MODULE_ROOT_DIR/data/locale/pygubu.pot"

    po_files=$(find $DESIGNER_MODULE_ROOT_DIR/data/locale -name "pygubu-designer.po")
    for _po in $po_files
    do
        msgmerge --verbose $_po ${pot_designer} -U
    done

    po_files=$(find $DESIGNER_MODULE_ROOT_DIR/data/locale -name "pygubu.po")
    for _po in $po_files
    do
        msgmerge --verbose $_po ${pot_pygubu} -U
    done
}

function compile_po {
    for _po in $(find ./src/pygubudesigner/data/locale -name "*.po")
    do
        msgfmt --verbose -o ${_po/.po/.mo}  $_po
    done
}

function install_from_testpypi {
    VENV_DIR=$PROJECT_ROOT"/../venv_testpypi";
    if [ -d "$VENV_DIR" ]; then
        rm -rf $VENV_DIR;
    fi
    echo "Creating venv."
    python3 -m venv $VENV_DIR
    source $VENV_DIR/bin/activate
    pip install -i https://test.pypi.org/simple/ --extra-index-url https://pypi.org/simple/ pygubu
    pip install -i https://test.pypi.org/simple/ --extra-index-url https://pypi.org/simple/ pygubu-designer
    pygubu-designer
    deactivate
}

# Commands end. Dispatch to command.

"$@"


# Some dev notes for this script.
#
# The commands *require*:
#
# * The current working directory is the project root.
# * The shell options and globals are set as they are.
#
# Inspired by http://www.oilshell.org/blog/2020/02/good-parts-sketch.html
#
