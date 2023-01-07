from libs.neopixel import Neopixel
from time import sleep, ticks_ms
from machine import Pin,Timer
import utime
 
## Setup
NUM_LEDS = 60
LED_PIN = 0
BTN_PIN = 10
SENSOR_PIN = 14 #For later feature
pixels = Neopixel(NUM_LEDS, 0, LED_PIN, "GRB")
pixels.brightness(30)
btn = Pin(BTN_PIN, Pin.IN, Pin.PULL_DOWN)

red = pixels.colorHSV(0, 255, 255)
green = pixels.colorHSV(21845, 255, 255)
blue = pixels.colorHSV(43691, 255, 255)
hue = 0
debounce_time = 0
led_state = 0


def button_handler(btn):
    global led_state, debounce_time
    if (utime.ticks_ms()-debounce_time) > 500:
        led_state = 1
        debounce_time=utime.ticks_ms()
    return led_state
btn.irq(trigger=machine.Pin.IRQ_FALLING, handler=button_handler)

while True:
    hue += 50
    color = pixels.colorHSV(hue, 255, 255)
    if led_state is 1:
        led_state = 0
        pixels.fill(color)
        pixels.show()
        print(f"Interrupt Detected {led_state}")