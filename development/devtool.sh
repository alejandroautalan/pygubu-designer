#!/bin/bash

[[ -n $project_dir_path ]] || \
project_dir_path="pygubudesigner"

activate_venv(){
    # Use virtualenv 'venv' if exists
    echo "virtualenv is used, enter 'deactivate' to exit."
    for v in \
        "./venv/bin/activate" \
        "./venv/local/bin/activate" # python 3.10
    do
        [[ -f $v ]] && . $v
    done
}

# Echo requirements for development environment, write the requirements of 
# product environment in 'pygubudesigner/__init__.py' file.
get_dev_requirements(){
    echo "\
    'isort>=5.9.2'          'setuptools>=57.3.0' \
    'wheel>=0.37.0'         'twine>=4.0.0' \
    'pip>=22.1.1' \
    "
}

get_dev_req(){  get_dev_requirements;     }

install_req(){
    [[ -f ./pygubudesigner_.py ]] && \
    eval "pip3 install \
    $(python3 pygubudesigner_.py prt_req) \
    $(get_dev_req)"
}

blk(){
    black -l 80 --exclude="venv/" --verbose \
    $([[ $# -eq 0 ]] && echo '.' || echo $*)
}

sort_imports(){
    isort -v ./setup.py
    [[ -d ./pygubudesigner ]]   && isort -v ./pygubudesigner/
    [[ -d ./pygubu ]]           && isort -v ./pygubu/
}

style(){
    sort_imports; blk
}

_xgettext(){
    pot_path=${project_dir_path}/locale/pygubu-designer.pot
    [[ -d ./${project_dir_path}/ui ]] && \
        xgettext -L glade \
            --verbose \
            --output=${pot_path} \
            $(find ./${project_dir_path}/ui -name "*.ui")
    xgettext --join-existing \
        --verbose \
        --language=Python \
        --keyword=_ \
        --output=${pot_path} \
        --from-code=UTF-8 \
        `find ./${project_dir_path} -name "*.py"`
    for _po in $(find ./${project_dir_path}/locale -name "*.po")
    do
        msgmerge --verbose $_po ${pot_path} -U
    done
}

_msgfmt(){
    for _po in $(find ./${project_dir_path}/locale -name "*.po")
    do
        msgfmt --verbose -o ${_po/.po/.mo}  $_po
    done
}

_build(){
    _msgfmt
    rm -rf ./dist/* ./build/*
    python3 setup.py sdist bdist_wheel
}

_serve(){   # default port is 8080
    _port=`[[ -z $1 ]] && echo "8080" || echo $1`
    python3 -m http.server $_port
}

build_and_serve(){
    _build
    cd dist
    _serve $1
    cd ..
}

build_and_upload(){
    _build
    twine upload dist/*
}

_install(){
    pip3 install ./dist/*.whl
}

build_and_install(){
    _build
    _install
}

_test(){
    # uninstall all
    pip3 uninstall pygubu pygubu-designer appdirs Mako -y
    build_and_install
    pygubu-designer
}

start(){
    style
    [[ -f ./pygubudesigner_.py ]] && \
    python3 pygubudesigner_.py start
}

if [[ \
    $PATH != *"${PWD}/venv/local/bin"* && \
    $PATH != *"${PWD}/venv/bin"* ]]
then
    if [[ -d "${PWD}/venv" ]];then
        activate_venv
    elif [[ -x $(which virtualenv) ]]
    then 
        virtualenv venv
        activate_venv
    else
        echo "virtualenv is not installed, cancel virtual environment."
    fi

fi

ir(){   install_req;            }
po(){   _xgettext;              }
msgf(){ _msgfmt;                }

_b(){   _build;                 }
_s(){   _serve;                 }
bs(){   build_and_serve $1;     }

bup(){  build_and_upload;       }
bi(){   build_and_install;      }
ts(){   _test;                  }

if [ $# -eq 0 ]
  then
    echo "Bash utility to facilitate development."
    echo "usage: ${project_dir_path}.sh [option] [args]"
    echo "Available options:"
    echo "  start : start pygubudesigner use development environment."
    echo "     ir : install all development requirements."
    echo "     ts : test."
    echo "     bi : build and install."
    echo "     bs : build and serve."
    echo "    bup : build and upload."
    echo "     po : update po file."
    echo "  style : format all *.py files."
    echo "   msgf : compile message catalog to binary format."
else
    # './devtool.sh' is approved, 
    # if enter '. devtool.sh', '$0' gets 'bash'.
    [[ $0 == *"devtool.sh" ]] && $*
fi
