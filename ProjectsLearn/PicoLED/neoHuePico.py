import time
from neopixel import Neopixel

numpix = 60
pixels = Neopixel(numpix, 0, 0, "GRB")



red = pixels.colorHSV(0, 255, 255)
green = pixels.colorHSV(21845, 255, 255)
blue = pixels.colorHSV(43691, 255, 255)

hue_offset = 4096

while True:
    for hue in range(0, 65535, 1000):
        for led in range(numpix):
            color = pixels.colorHSV(hue + (led * hue_offset), 128, 125)
            pixels.set_pixel(led, color)
        pixels.show()
        time.sleep(0.05)