import uos
import machine
import st7789py as st7789
from fonts import vga2_8x8 as font1
from fonts import vga1_16x32 as font2
from fonts import vga3_8x8 as font3
from fonts import vga4_16x16 as font4
import random
import utime
from bmx280 import BMX280
import ds1302


# DS1302 RTC setup
ds = ds1302.DS1302(machine.Pin(6, machine.Pin.OUT,
                   machine.Pin.PULL_DOWN), machine.Pin(5), machine.Pin(4))
# ds.date_time([2022, 9, 9, 5, 20, 10, 10, 0]) # Change time on setup

# BMP280 I2C
sda = machine.Pin(0)
scl = machine.Pin(1)
i2c = machine.I2C(0, sda=sda, scl=scl, freq=400000)
bus = machine.I2C(0, sda=sda, scl=scl)
bmp = BMX280(bus, 0x76)

# Initialize 7789-Display SPI(1) default pins
spi1_sck = 10
spi1_mosi = 11
spi1_miso = 13  # not use
st7789_res = 12
st7789_dc = 8
disp_width = 240
disp_height = 240
CENTER_Y = int(disp_width / 2)
CENTER_X = int(disp_height / 2)

print(uos.uname())
spi1 = machine.SPI(1, baudrate=40000000, polarity=1)
print(spi1)
display = st7789.ST7789(spi1, disp_width, disp_width,
                        reset=machine.Pin(st7789_res, machine.Pin.OUT),
                        dc=machine.Pin(st7789_dc, machine.Pin.OUT,
                                       machine.Pin.PULL_DOWN),
                        xstart=0, ystart=0, rotation=1)

display.fill(st7789.BLACK)
file = open("temps.txt", "a")


while True:
    cur_date = f"{ds.day():02d}.{ds.month():02d}.{ds.year()} - {ds.hour():02d}:{ds.minute():02d}:{ds.second():02d}"

    pressure = bmp.pressure
    temperature = bmp.temperature - 4

    display.text(font3, f"{cur_date}", 30, 10)
    display.text(font2, "Temperatur", 10, 70, st7789.WHITE, st7789.BLACK)
    display.text(font2, f"{temperature:>10.2f}", 30,
                 100, st7789.WHITE, st7789.BLACK)
    display.text(font2, "Luftdruck", 10, 130, st7789.WHITE, st7789.BLACK)
    display.text(font2, f"{pressure:>10.2f}", 30,
                 160, st7789.WHITE, st7789.BLACK)

    file.write(
        f"Date: {cur_date}, Temp: {temperature}, Pres: {pressure}" + "\n")
    utime.sleep_ms(5)
    file.flush()

    utime.sleep(5)
