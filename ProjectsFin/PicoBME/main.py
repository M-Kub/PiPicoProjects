import uos
import machine
import st7789py as st7789
from pycom_bme680 import *
import utime
from fonts import vga2_8x8 as font1
from fonts import vga1_16x32 as font2


sda=machine.Pin(0)
scl=machine.Pin(1)
i2c=machine.I2C(0,sda=sda, scl=scl)
bme=BME680_I2C(i2c)

temperature_offset = -5
bme.sea_level_pressure = 1013.25


#Initialize 7789-Display SPI(1) default pins
spi1_sck=10
spi1_mosi=11
spi1_miso=13    #not use
st7789_res = 12
st7789_dc  = 8
disp_width = 240
disp_height = 240
CENTER_Y = int(disp_width/2)
CENTER_X = int(disp_height/2)


print(uos.uname())
spi1 = machine.SPI(1, baudrate=40000000, polarity=1)
print(spi1)
display = st7789.ST7789(spi1, disp_width, disp_width,
                          reset=machine.Pin(st7789_res, machine.Pin.OUT),
                          dc=machine.Pin(st7789_dc, machine.Pin.OUT),
                          xstart=0, ystart=0, rotation=1)


while True:

    temperature = bme.temperature
    humidity = bme.humidity
    pressure = bme.pressure
    altitude = bme.altitude
    gas = bme.gas / 1000
    
    display.fill(st7789.BLACK)
    display.text(font2, f"Temp:{temperature + temperature_offset:.2f}", 10, 50)
    display.text(font2, f"Humi:{humidity:.2f}", 10, 80)
    display.text(font2, f"Pres:{pressure:.2f}", 10, 110)
    display.text(font2, f"Gas:{gas:.2f}", 10, 140)
    display.text(font2, f"Alti:{altitude:.0f}", 10, 170)
    utime.sleep(5)
