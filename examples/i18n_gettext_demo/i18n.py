import gettext
import locale
import os
import sys
from pathlib import Path

# Change this variable to your app name!
#  The translation files will be under
#  @LOCALE_DIR@/@LANGUAGE@/LC_MESSAGES/@APP_NAME@.mo
#
APP_NAME = "demoapp"

# Not sure in a regular desktop:

DATA_DIR = Path(__file__).parent
LOCALE_DIR = DATA_DIR / "locale"

# Now we need to choose the language. We will provide a list, and gettext
# will use the first translation available in the list
#
#  In maemo it is in the LANG environment variable
#  (on desktop is usually LANGUAGES)
#
DEFAULT_LANGUAGES = os.environ.get("LANG", "").split(":")

# Try to get the languages from the default locale
languages = []
lc, encoding = locale.getdefaultlocale()
if lc:
    languages = [lc]

# Concat all languages (env + default locale),
#  and here we have the languages and location of the translations
#
languages = DEFAULT_LANGUAGES + languages + ["en_US"]
mo_location = LOCALE_DIR

# Lets tell those details to gettext
#  (nothing to change here for you)
gettext.install(True)
gettext.bindtextdomain(APP_NAME, mo_location)
gettext.textdomain(APP_NAME)
language = gettext.translation(
    APP_NAME, mo_location, languages=languages, fallback=True
)

_ = T = translator = language.gettext
