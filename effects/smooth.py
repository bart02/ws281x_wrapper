from strip.color import Color
from strip.strip import Effect


def rng(start, end, kol):
    tek = start
    rzn = (end - start) / kol
    for _ in range(kol):
        tek += rzn
        yield int(tek)


class Smooth(Effect):
    def __init__(self, strip, leds, color, pers, delay=0.01):
        self.delay = delay
        self.stages = pers

        if isinstance(leds, int):
            leds = [leds]
        for i in leds:
            tek = strip[i].rgb
            need = color.rgb

            stages = [rng(tek[0], need[0], pers),
                      rng(tek[1], need[1], pers),
                      rng(tek[2], need[2], pers)]
            stages = list(map(Color, zip(*stages)))

            self.__setitem__(i, stages)
