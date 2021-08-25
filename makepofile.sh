#!/bin/sh

xgettext -L glade --output=po/pygubu.pot $(find ./pygubudesigner/ui -name "*.ui")
xgettext --join-existing --language=Python --keyword=_ --output=po/pygubu.pot --from-code=UTF-8 `find ./pygubudesigner -name "*.py"`

for _po in $(find ./pygubudesigner/locale -name "*.po"); do
    msgmerge $_po po/pygubu.pot -U
done
