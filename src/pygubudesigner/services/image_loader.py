from pygubu.stockimage import StockImage, StockImageException
from pygubu.theming.iconset.loader import IconSetLoader


def image_loader(master, image_id):
    return StockImage.get(image_id)


iconset_loader = IconSetLoader("pygubudesigner.data.iconset", "pygubu.json")
