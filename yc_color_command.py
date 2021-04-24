import yescommander as yc
import re
from prompt_toolkit.formatted_text import FormattedText
import colorsys


def hex_to_rgb(h):
    h = h.lstrip("#")
    return tuple(int(h[i : i + 2], 16) / 255.0 for i in (0, 2, 4))


def rgb_to_hex(r):
    ...


def rgb_to_grey(r):
    return 0.2989 * r[0] + 0.5870 * r[1] + 0.1140 * r[2]


def rgb256_to_hex(r):
    return "#%02x%02x%02x" % r


to_256 = lambda c: tuple(int(i * 255) for i in c)
show_tuple = lambda c: " ".join([f"{i:.5f}" for i in c])
show_tuple_256 = lambda c: " ".join([str(i) for i in c])


def parse_triple(s):
    if "," not in s:
        s = ",".join(s.split())
    try:
        ans = eval(s)
        if len(ans) != 3:
            return None
    except:
        return None
    if all([isinstance(i, int) for i in ans]):
        ans = [i / 255.0 for i in ans]
    for i in ans:
        if i < 0 or i > 1:
            return None
    return ans


class ColorSoldier(yc.BaseCommand, yc.BaseCommander):
    def __init__(self):
        self.color = tuple()
        self._hex_regex = re.compile(r"^#(?:[0-9a-fA-F]{3}){2}$")
        self.score = 200

    def order(self, keywords):
        if len(keywords) == 0:
            return

        s = " ".join(keywords)
        if re.search(self._hex_regex, s):
            self.color = hex_to_rgb(s)
            return

        if keywords[0] not in ["rgb", "RGB", "hsv", "HSV", "hls", "HLS"]:
            return
        s = parse_triple(" ".join(keywords[1:]))
        if s is None:
            return
        if keywords[0] in ["rgb", "RGB"]:
            self.color = s
        elif keywords[0] in ["hsv", "HSV"]:
            self.color = colorsys.hsv_to_rgb(*s)
        elif keywords[0] in ["hls", "HLS"]:
            self.color = colorsys.hls_to_rgb(*s)
        yield self

    def __str__(self):
        if self.color != "":
            fg = "black" if rgb_to_grey(self.color) > 0.5 else "white"
            hex_color = rgb256_to_hex(to_256(self.color))
            return FormattedText([(f"bg:{hex_color} fg:{fg}", hex_color)])
        return "Wrong"

    def result(self):
        for k, v in self.preview().items():
            print("---", k)
            print(v)

    def preview(self):
        rgb = self.color
        hls = colorsys.rgb_to_hls(*rgb)
        hsv = colorsys.rgb_to_hls(*rgb)
        return {
            "rgb": show_tuple(rgb),
            "rgb 256": show_tuple_256(to_256(rgb)),
            "hsv": show_tuple(hsv),
            "hsv 256": show_tuple_256(to_256(hsv)),
            "hls": show_tuple(hls),
            "hls 256": show_tuple_256(to_256(hls)),
        }
