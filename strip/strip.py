from rpi_ws281x import PixelStrip

from strip.color import Color
from os import getuid
from time import sleep


class Strip:
    def __init__(self, num, gpio, **kwargs):
        if getuid() != 0:
            raise PermissionError('Only `root` can use Strip. Try `sudo python <name>`.')
        self.num = num
        self.gpio = gpio
        self.strip = PixelStrip(self.num, self.gpio, **kwargs)
        self.strip.begin()

    def __setitem__(self, key, color):
        if not isinstance(color, Color):
            color = Color(color)

        if isinstance(key, slice):
            key = range(key.start if key.start is not None else 0,
                        key.stop if key.stop is not None else self.num,
                        key.step if key.step is not None else 1)
            for i in key:
                if i in range(0, self.num):
                    self.strip.setPixelColor(i, color.dec)
        elif isinstance(key, int):
            if key in range(0, self.num):
                self.strip.setPixelColor(key, color.dec)
        else:
            TypeError("Invalid argument type")

    def __getitem__(self, key):
        if isinstance(key, slice):
            key = range(key.start if key.start is not None else 0,
                        key.stop if key.stop is not None else self.num,
                        key.step if key.step is not None else 1)
            return [Color(self.strip.getPixelColor(i)) for i in key]
        elif isinstance(key, int):
            return Color(self.strip.getPixelColor(key))
        else:
            raise TypeError("Invalid argument type")

    def __iter__(self):
        for i in range(self.num):
            yield self.__getitem__(i)

    # Deprecated. Use slices `Strip[:] = Color()`.
    def set_strip_color(self, color):
        self.__setitem__(slice(None), color)
    setStripColor = set_strip_color

    def clean(self):
        self.__setitem__(slice(None), Color(0))

    def show(self):
        self.strip.show()

    def do_effect(self, effect):
        for st in range(effect.stages):
            for i in effect:
                self.__setitem__(i, effect[i][st])
            self.show()
            sleep(effect.delay)


class Effect(dict):
    delay = None
    stages = None

    def __add__(self, other):
        if self.delay == other.delay and self.stages == other.stages:
            new = Effect()
            new.delay = self.delay
            new.stages = self.stages
            new.update(self)
            new.update(other)
            return new
