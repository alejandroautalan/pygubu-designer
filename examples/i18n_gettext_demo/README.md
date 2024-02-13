# i18n example using gettext

## String extraction to a .pot file template

From ui file

    xgettext --package-name demoapp -L glade --output=./locale/demoapp.pot ./demo-i18n.ui

Add strings from source file

    xgettext --package-name demoapp --join-existing -L Python --keyword=_  --output=./locale/demoapp.pot --from-code=UTF-8 ./demoapp.py

## Translate to a specific language

Prepare a translation for spanish language

    mkdir -p ./locale/es/LC_MESSAGES

    cp ./locale/demoapp.pot  ./locale/es/LC_MESSAGES/demoapp.po

Translate the file:

    ./locale/es/LC_MESSAGES/demoapp.pot

using a text editor or install [poedit](https://poedit.net/) application to make the process easier.

Once the translation is finished it is necessary to compile the file to a format required by gettext.

    msgfmt --verbose -o ./locale/es/LC_MESSAGES/demoapp.mo ./locale/es/LC_MESSAGES/demoapp.po

You can use poedit to compile also.
