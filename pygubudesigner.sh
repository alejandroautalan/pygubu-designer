#!/bin/sh

install_r(){
    pip3 install -U -r requirements.txt
}

auto_sort_pep8(){
    isort ./setup.py
    isort ./pygubudesigner/
    autopep8 -i -a -a -r  ./setup.py
    autopep8 -i -a -a -r  ./pygubudesigner/
}

_xgettext(){
    xgettext -L glade --output=po/pygubu.pot \
    $(find ./pygubudesigner/ui -name "*.ui")

    xgettext --join-existing --language=Python --keyword=_ \
    --output=po/pygubu.pot --from-code=UTF-8 \
    `find ./pygubudesigner -name "*.py"`

    for _po in $(find ./pygubudesigner/locale -name "*.po"); do
        msgmerge $_po po/pygubu.pot -U
    done

}

ir(){
    install_r; 
}
p8(){ 
    auto_sort_pep8; 
}
po(){
    _xgettext;
}


$1