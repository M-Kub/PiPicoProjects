import machine
from libs.neopixel import Neopixel
import utime


# Setup
piPin = 0
numpix = 59

strip = Neopixel(numpix, 0, piPin, "RGBW")
button = machine.Pin(15, machine.Pin.IN, machine.Pin.PULL_UP)

strip_state = 0
debounce_time = 0
button_pushes = 0

def button_handler(button):
    global strip_state, debounce_time
    if strip_state == 0 and (utime.ticks_ms()-debounce_time) > 100:
        strip_state = 1
        debounce_time=utime.ticks_ms()
    if strip_state == 1 and (utime.ticks_ms()-debounce_time) > 100:
        strip_state = 0
        debounce_time=utime.ticks_ms()
        
        
    
button.irq(trigger=machine.Pin.IRQ_FALLING, handler=button_handler)

while True:
    if strip_state is 1:
        button_pushes += 1
        color = (0, 0, 0, 255)
        strip.fill(color)
        strip.show()
        print(f"Interrupt Detected {button_pushes}")
    elif strip_state is 0:
        color = (0, 0, 0, 0)
        strip.fill(color)
        strip.show()
        