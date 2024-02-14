# i18n example using gettext

The pygubu builder allows you to pass a callable named translator
used to process translatable strings from the ui file.

```python
# ...
class Builder(object):
    def __init__(self, translator=None, *, on_first_object=None):
# ...
```

In this example I will use the translator function from the [gettext](https://docs.python.org/3/library/gettext.html) module.

You will need the gettext console utilities installed in your system.

The i18n.py file is used to setup gettext.

This file is imported on every module that has strings marked for translation.

The common marker used is a _ .  This marker is used later with the console utilities to extract
the translatable strings from source files.

Example:

```python
# ...
from i18n import translator

# Set translatable strings marker
_ = translator

# ...

self.countries = [
            _("Argentina"),
            _("Brazil"),
            _("Peru"),
            _("Spain"),
            _("Germany"),
            _("Belgium"),
            _("Finland"),
            _("Other"),
        ]
# ...

if __name__ == "__main__":
    app = DemoI18NApp(translator=translator)
    app.run()
```


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

    ./locale/es/LC_MESSAGES/demoapp.po

using a text editor or install [poedit](https://poedit.net/) application to make the process easier.

Once the translation is finished it is necessary to compile the file to a format required by gettext.

    msgfmt --verbose -o ./locale/es/LC_MESSAGES/demoapp.mo ./locale/es/LC_MESSAGES/demoapp.po

You can use poedit to compile also.

## Testing

If you are on a linux system you can test translations setting up the LANG environment variable.

Spanish translation test:

    LANG=es; python3 demoapp.py

English translation test:

    LANG=en; python3 demoapp.py
