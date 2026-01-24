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
PYGUBU_DIR=$(realpath "$PROJECT_ROOT/../pygubu")
DESIGNER_MODULE_ROOT_DIR="./src/pygubudesigner"

python3bin=$(which python3)

fades_bin=/opt/py-3.13.8-tk-8.6.17/bin/fades
fades_tk9_bin=/opt/py-3.14.2-tk-9.0.3/bin/fades


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
    #
    # all widgets converted to code so, no ui files needed
    #
    #ui_files=$(find ${DESIGNER_MODULE_ROOT_DIR}/data/ui -name "*.ui" | sort | paste -d " ")
    # echo $ui_files
    #xgettext \
    #    --package-name $pkg_name \
    #    --language=Glade \
    #    --verbose \
    #    --output=${pot_path} \
    #    $ui_files
    py_files=$(find ${DESIGNER_MODULE_ROOT_DIR} -name "*.py" | sort | paste -d " ")
    # echo $py_files
    xgettext \
        --package-name $pkg_name \
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
    if [[ -d ${PYGUBU_SRC_DIR} ]];then
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
    fi
}

function update_po {
    pot_designer="$DESIGNER_MODULE_ROOT_DIR/data/locale/pygubu-designer.pot"
    pot_pygubu="$DESIGNER_MODULE_ROOT_DIR/data/locale/pygubu.pot"

    po_files=$(find $DESIGNER_MODULE_ROOT_DIR/data/locale -name "pygubu-designer.po")
    for _po in $po_files
    do
        echo "Merging ${pot_designer} to ${_po}"
        msgmerge --verbose $_po ${pot_designer} -U
    done

    po_files=$(find $DESIGNER_MODULE_ROOT_DIR/data/locale -name "pygubu.po")
    for _po in $po_files
    do
        echo "Merging ${pot_pygubu} to ${_po}"
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

function designer {
    reqfile="/tmp/pygubu-designertk8-editable.txt"
    cat << EOF > $reqfile
platformdirs
-e file://$PYGUBU_DIR#egg=pygubu
-e file://$PROJECT_ROOT#egg=pygubu-designer
EOF

    $fades_bin -r $reqfile -x pygubu-designer ${@:1}

}

function designertk9 {
    reqfile="/tmp/pygubu-designer-tk9-editable.txt"
    cat << EOF > $reqfile
platformdirs
-e file://$PYGUBU_DIR#egg=pygubu
-e file://$PROJECT_ROOT#egg=pygubu-designer
EOF

    $fades_tk9_bin -r $reqfile -x pygubu-designer ${@:1}

}

function all-examples {
    declare -a arr=(
        "helloworld/helloworld.py"
        "7guis/01_counter/counterapp.py"
        "7guis/02_temperature_converter/tempconvapp.py"
        "7guis/03_flight_Booker/flightbookerapp.py"
        "7guis/04_timer/timerapp.py"
        "canvas/canvas-scrollregion/myapp.py"
        "command_properties/command_properties.py"
        "control_variables/controlvariables.py"
        "dialogs/demo1/demo.py"
        "dialogs/demo2/demo.py"
        "dialogs/demo3/demo.py"
        "dialogs/demo4/settingsdemoapp.py"
        "dialogs/demo5/mainapp.py"
        "forms/formsdemo1app.py"
        "i18n_gettext_demo/demoapp.py"
        "image_property/image_property.py"
        #"jpg_image_on_canvas/demoapp.py"
        "menubutton/menubutton_demo.py"
        "notebook/demo1app.py"
        "pathchooserdemo/demo1/pathchooserdemo.py"
        "pathchooserdemo/demo2/pathchooserdemo.py"
        "pbs_themes/demo01/demoapp.py"
        "scrolledframe/demoapp.py"
        "scrolledtext/scrolledtextdemoapp.py"
        "static_image/demoapp.py"
        "text/logwindowdemo/demo1app.py"
        "tk_window/tkdemoapp.py"
        "toplevel_centered/centered_demo1.py"
        "toplevel_centered/centered_demo2.py"
        "toplevel_menu/menu.py"
        "treeview/demo1/treeview.py"
        "treeview/demo2/columnsstretchingdemo.py"
        "treeview_editable/demo1/demoapp.py"
        "treeview_editable/demo2/demo2app.py"
        "treeview_editable/demo3/demo3app.py"
        "treeview_filterable/demoapp.py"
        "user_input/userinputapp.py"
        "windowdeleteevent/demo1.py"
        "windowdeleteevent/demo2.py"
        )
    
    EXAMPLES_DIR=$PROJECT_ROOT"/examples";
    for i in "${arr[@]}"
    do
       echo "Running: $EXAMPLES_DIR/$i"
       $python3bin $EXAMPLES_DIR/$i
    done
}

# Commands end. Dispatch to command.

if [[ -z "$@" ]]; then
  echo "No subcommand provided."
  echo "Available commands:"
  compgen -A function | sed -e $'s/^/    /'
  exit 1
else
  "$@"
fi


# Some dev notes for this script.
#
# The commands *require*:
#
# * The current working directory is the project root.
# * The shell options and globals are set as they are.
#
# Inspired by http://www.oilshell.org/blog/2020/02/good-parts-sketch.html
#
