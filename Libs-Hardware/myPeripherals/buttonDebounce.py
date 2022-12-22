import machine
import utime

led_state = 0
debounce_time = 0
button_pushes = 0
led_ext = machine.Pin(15, machine.Pin.OUT)
button = machine.Pin(14, machine.Pin.IN, machine.Pin.PULL_UP)


def button_handler(button):
    global led_state, debounce_time
    if (utime.ticks_ms()-debounce_time) > 500:
        led_state = 1
        debounce_time=utime.ticks_ms()
button.irq(trigger=machine.Pin.IRQ_FALLING, handler=button_handler)


while True:
    if led_state is 1:
        led_state = 0
        button_pushes += 1
        print(f"Interrupt Detected {button_pushes}")
        led_ext.toggle()
