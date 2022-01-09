#!/bin/bash

<<comment
tree  -L 1
.
├── pygubu
├── pygubu-designer
└── venv
comment

# Use virtualenv 'venv' if exists
if [[ -f "../venv/bin/activate" ]];then
    source ../venv/bin/activate
fi

args=("$@") # All parameters from terminal.

install_r(){
    pip3 install -U -r ./requirements/development.txt
}

auto_sort_pep8(){
    isort -v ./setup.py
    isort -v ./pygubudesigner/
    autopep8 -i -a -a -r -v ./setup.py
    autopep8 -i -a -a -r -v ./pygubudesigner/

    isort -v ../pygubu/setup.py
    isort -v ../pygubu/pygubu/
    autopep8 -v -i -a -a -r  ../pygubu/setup.py
    autopep8 -v -i -a -a -r  ../pygubu/pygubu/
}

auto_sort_pep8_commit(){
    auto_sort_pep8

    git_commit_m='sort imports and autopep8'
    cd ../pygubu/
    git add . ; git commit -m "$git_commit_m"
    cd ../pygubu-designer/
    git add . ; git commit -m "$git_commit_m"
}

_xgettext(){
    xgettext -L glade --output=pygubudesigner/locale/pygubu.pot \
    $(find ./pygubudesigner/ui -name "*.ui")

    xgettext --join-existing --language=Python --keyword=_ \
    --output=pygubudesigner/locale/pygubu.pot --from-code=UTF-8 \
    `find ./pygubudesigner -name "*.py"`

    for _po in $(find ./pygubudesigner/locale -name "*.po"); do
        msgmerge $_po ./pygubudesigner/locale/pygubu.pot -U
    done

}

_msgfmt(){
    for _po in $(find ./pygubudesigner/locale -name "*.po"); do
        msgfmt -o ${_po/.po/.mo}  $_po
    done
}

_build(){
    _msgfmt # compile .po files
    cd ../pygubu
    rm -rf ./dist/* ./build/*
    python3 setup.py sdist bdist_wheel
    
    cd ../pygubu-designer
    rm -rf ./dist/* ./build/*
    cp -r ../pygubu/dist/ .
    python3 setup.py sdist bdist_wheel
}

_serve(){
    # default port is 8080
    _port=`[[ -z ${args[1]} ]] && echo "8080" || echo ${args[1]}`
    python3 -m http.server $_port
}

build_and_serve(){
    _build
    cd dist
    _serve
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

ir(){   install_r; }
p8(){   auto_sort_pep8; }
p8c(){  auto_sort_pep8_commit; }
po(){   _xgettext; }
msgf(){ _msgfmt; }
_b(){   _build; }
_s(){   _serve; }
bs(){   build_and_serve; }
bup(){  build_and_upload; }
bi(){   build_and_install; }
ts(){   _test; }

if [ $# -eq 0 ]
  then
    echo "Bash utility to facilitate development."
    echo "usage: pygubudesigner.sh [option] [args]"
    echo "Available options:"
    echo "  ts: test"
    echo "  bi: build and install."
    echo "  bs: build and serve."
    echo "  bup: build and upload."
else
    $1
fi