from machine import I2C, Pin
from dht import DHT11, InvalidChecksum
from lcd_api import LcdApi
from pico_i2c_lcd import I2cLcd
import utime


I2C_ADDR     = 0x27
I2C_NUM_lines = 2
I2C_NUM_columns = 16

i2c = I2C(0, sda=Pin(0), scl=Pin(1), freq=200000)
lcd = I2cLcd(i2c, I2C_ADDR, I2C_NUM_lines, I2C_NUM_columns)

pin = 15
sensor = DHT11(Pin(pin, Pin.OUT, Pin.PULL_DOWN))
utime.sleep(1)

while True:
    lcd.backlight_on()
    temp = sensor.temperature
    humidity = sensor.humidity
    lcd.putstr(f"Temp: {temp}C \nHumidity: {humidity:.0f}% ")
    utime.sleep(5)
    lcd.clear()
