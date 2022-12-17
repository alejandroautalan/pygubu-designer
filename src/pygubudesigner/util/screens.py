import re
from screeninfo import get_monitors

# geometry format:  WxH+x+y
RE_GEOMETRY = (
    r"(?P<width>\d+)x(?P<heigth>\d+)(\+(?P<xpos>-?\d+)\+(?P<ypos>-?\d+))?"
)
RE_GEOMETRY = re.compile(RE_GEOMETRY)


def parse_geometry(geom: str):
    match = RE_GEOMETRY.match(geom)
    xpos, ypos, w, h = (0, 0, 0, 0)

    if match:
        groups = match.groups()
        w = int(match.group("width"))
        h = int(match.group("heigth"))
        if len(groups) > 1:
            xpos = int(match.group("xpos"))
            ypos = int(match.group("ypos"))
    return (w, h, xpos, ypos)


def is_visible_in_screens(geom: str):
    w, h, xpos, ypos = parse_geometry(geom)
    window_visible = False
    fh = 30
    x0 = xpos
    y0 = ypos
    x1 = xpos + w
    y1 = ypos + fh

    for m in get_monitors():
        cw = m.x + m.width
        ch = m.y + m.height
        # Is the window bar/menu visible in monitor?
        if (m.x <= x0 <= cw and m.y <= y0 + fh <= ch) or (
            m.x <= x1 <= cw and m.y <= y1 + fh < ch
        ):
            # print("I think the window is visible")
            window_visible = True
            break
    return window_visible
