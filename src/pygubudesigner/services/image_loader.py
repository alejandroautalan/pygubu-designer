from pygubu.stockimage import StockImage, StockImageException
from pygubu.theming.iconset.iconset import ThemeType
from pygubu.theming.iconset.loader import IconSetLoader, HAS_SVG_SUPPORT
from pygubu.theming.bootstrap.themes import STANDARD_THEMES as PBS_THEMES


def image_loader(master, image_id):
    return StockImage.get(image_id)


iconset_loader = IconSetLoader("pygubudesigner.data.iconset", "pygubu.json")


def match_icons_with_theme(theme_name: str):
    """For now use a table with harcoded know styles.
    In future releases use a better method.
    """
    theme_type = None
    dark = ThemeType.DARK
    light = ThemeType.LIGHT

    known_themes = dict(
        alt=light,
        clam=light,
        classic=light,
        default=light,
    )

    if theme_name in known_themes:
        theme_type = known_themes[theme_name]
    elif theme_name.startswith("pbs_") and theme_name in PBS_THEMES:
        theme_def = PBS_THEMES[theme_name]
        theme_type = light if theme_def["type"] == "light" else dark
        if HAS_SVG_SUPPORT:
            color = theme_def["colors"]["primary"]
            if theme_type == light:
                iconset_loader.iconset.color_onlight = color
            else:
                iconset_loader.iconset.color_ondark = color
    else:
        theme_type = light

    iconset_loader.theme = theme_type
