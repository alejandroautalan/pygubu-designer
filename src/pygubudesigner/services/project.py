import sys
import pathlib
import logging
import importlib

from pygubu.component.uidefinition import UIDefinition
from ..widgetdescr import WidgetMeta
from ..i18n import translator


logger = logging.getLogger(__name__)
_ = translator


def load_definition(filename):
    uidef = UIDefinition(wmetaclass=WidgetMeta)
    uidef.load_file(filename)

    uidir = pathlib.Path(filename).parent.resolve()
    path_list = []
    notfound_list = []
    # Xml will have relative paths to UI file directory
    for cw in uidef.custom_widgets:
        cw_path: pathlib.Path = pathlib.Path(uidir, cw).resolve()
        if cw_path.exists():
            path_list.append(cw_path)
        else:
            notfound_list.append(cw_path)
    if notfound_list:
        # Notify user some path does not exits
        # raise exception
        msg = "Custom widgets not found:\n" + "\n".join(
            (str(f) for f in notfound_list)
        )
        raise Exception(msg)
    else:
        # Load builders
        for path in path_list:
            load_custom_widget(path)
    return uidef


def load_custom_widget(path: pathlib.Path):
    print("LOading ", path)
    if not path.match("*.py"):
        return

    dirname = str(path.parent)
    modulename = path.name[:-3]
    if dirname not in sys.path:
        sys.path.append(dirname)

    try:
        importlib.import_module(modulename)
    except Exception as e:
        logger.exception(e)
        raise e
