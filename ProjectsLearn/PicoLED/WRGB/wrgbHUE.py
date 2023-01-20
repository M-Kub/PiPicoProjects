import time
from libs.neopixel import Neopixel

numpix = 8
strip = Neopixel(numpix, 0, 15, "RGBW")

strip.brightness(80)
while True:
    color = (0, 0, 0, 255)
    strip.fill(color)
    strip.show()    


