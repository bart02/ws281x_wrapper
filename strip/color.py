import colorsys


class Color:
    _rgb = None
    _hsv = None
    _dec = None
    _hex = None

    def __init__(self, p=None, rgb=None, hsv=None, dec=None, hex=None):
        if rgb is not None:
            self._rgb = rgb
            return
        elif hsv is not None:
            self._hsv = hsv
            return
        elif dec is not None:
            self._dec = dec
            return
        elif hex is not None:
            self._hex = hex
            return
        elif p is not None:
            if isinstance(p, str):
                self._hex = p
                return
            elif isinstance(p, int):
                self._dec = p
                return
            else:
                self._rgb = p
                return
        raise ValueError

    def __repr__(self):
        return '<Color {}>'.format(self.hex)
    __str__ = __repr__

    @property
    def rgb(self):
        if self._rgb is not None:
            pass
        elif self._dec is not None:
            self._rgb = dec2rgb(self._dec)
        elif self._hex is not None:
            self._rgb = dec2rgb(self.dec)
        elif self._hsv is not None:
            self._rgb = hsv2rgb(self._hsv)

        return self._rgb

    @property
    def hsv(self):
        if self._hsv is None:
            self._hsv = rgb2hsv(self.rgb)
        return self._hsv

    @property
    def dec(self):
        if self._dec is None:
            if self._hex is not None:
                self._dec = hex2dec(self._hex)
            else:
                self._dec = rgb2dec(self.rgb)
        return self._dec

    @property
    def hex(self):
        if self._hex is None:
            self._hex = dec2hex(self.dec)
        return self._hex


def rgb2dec(rgb):
    red, green, blue = rgb
    return (red << 16) | (green << 8) | blue


def dec2rgb(dec):
    return dec >> 16 & 0xff, dec >> 8 & 0xff, dec & 0xff


def dec2hex(dec):
    return '#' + hex(dec)[2:].zfill(6)


def hex2dec(hex):
    hex = hex.replace('#', '')
    return int(hex, 16)


def rgb2hsv(rgb):
    r, g, b = rgb
    return tuple(round(i * 255) for i in colorsys.rgb_to_hsv(r / 255, g / 255, b / 255))


def hsv2rgb(hsv):
    h, s, v = hsv
    return tuple(round(i * 255) for i in colorsys.hsv_to_rgb(h / 255, s / 255, v / 255))
