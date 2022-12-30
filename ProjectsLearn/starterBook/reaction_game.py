import machine
import utime
import urandom


pressed = False
led = machine.Pin(15, machine.Pin.OUT)
right_button = machine.Pin(14, machine.Pin.IN, machine.Pin.PULL_DOWN)
left_button = machine.Pin(16, machine.Pin.IN, machine.Pin.PULL_DOWN)
fastest_button = None



def button_handler(pin):
    global pressed
    global timer_reaction
    if not pressed:
        pressed=True
        timer_reaction = utime.ticks_diff(utime.ticks_ms(), timer_start)
        global fastest_button
        fastest_button = pin


led.value(1)
utime.sleep(urandom.uniform(5, 10))
led.value(0)
timer_start = utime.ticks_ms()
right_button.irq(trigger=machine.Pin.IRQ_RISING, handler=button_handler)
left_button.irq(trigger=machine.Pin.IRQ_RISING, handler=button_handler)


while fastest_button is None:
    utime.sleep(1)
if fastest_button is left_button:
    print(f"{left_button} player wins in {timer_reaction} ms!")
elif fastest_button is right_button:
    print(f"{right_button} player wins in {timer_reaction} ms!")

