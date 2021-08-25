#!/bin/sh

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

install_r(){
    pip3 install -U -r requirements.txt
}

auto_sort_pep8(){
    isort ./setup.py
    isort ./pygubudesigner/
    autopep8 -i -a -a -r  ./setup.py
    autopep8 -i -a -a -r  ./pygubudesigner/

    isort ../pygubu/setup.py
    isort ../pygubu/pygubu/
    autopep8 -i -a -a -r  ../pygubu/setup.py
    autopep8 -i -a -a -r  ../pygubu/pygubu/
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

build_and_serve(){
    _build
    cd dist
    python3 -m http.server 8080
    cd ..
}
build_and_upload(){
    _build
    twine upload dist/*
    twine upload ../pygubu/dist/*
}
_install(){
    pip3 install ./dist/*.whl
}

build_and_install(){
    _build
    _install
}

test(){
    pip3 uninstall pygubu pygubu-designer -y
    bi
    pygubu-designer
}

ir(){   install_r; }
p8(){   auto_sort_pep8; }
po(){   _xgettext;}
msgf(){ _msgfmt;}
_b(){   _build;}
bs(){   build_and_serve;}
bup(){  build_and_upload;}
bi(){   build_and_install;}
ts(){   test;}


$1