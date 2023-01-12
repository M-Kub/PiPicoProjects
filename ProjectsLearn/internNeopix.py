import machine
from neopixel import NeoPixel
import utime


# Setup
piPin = machine.Pin(0, machine.Pin.OUT)
numpix = 59

strip = NeoPixel(piPin, numpix, bpp=4, timing=1)
button = machine.Pin(15, machine.Pin.IN, machine.Pin.PULL_UP)

strip_state = 0
debounce_time = 0
button_pushes = 0

def button_handler(button):
    global strip_state, debounce_time
    if (utime.ticks_ms()-debounce_time) > 100:
        strip_state = 1
        debounce_time=utime.ticks_ms()
button.irq(trigger=machine.Pin.IRQ_FALLING, handler=button_handler)

while True:
    if strip_state is 1:
        strip_state = 0
        button_pushes += 1
        color = (0, 0, 0, 255)
        strip.fill(color)
        strip.write()
        print(f"Interrupt Detected {button_pushes}")

        
    
