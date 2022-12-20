import uos
import machine
import random
import utime
import sdcard
import st7789py as st7789
from fonts import vga2_8x8 as font1
from fonts import vga1_16x32 as font2
from bmx280 import BMX280
import ds1302


# DS1302 RTC setup
ds = ds1302.DS1302(machine.Pin(6, machine.Pin.OUT, machine.Pin.PULL_DOWN), machine.Pin(5), machine.Pin(4))
ds.date_time() # returns the current datetime.

# BMP280 I2C
sda=machine.Pin(20)
scl=machine.Pin(21, machine.Pin.OUT, machine.Pin.PULL_DOWN)
i2c=machine.I2C(0,sda=sda, scl=scl, freq=400000)
bus = machine.I2C(0, sda=sda, scl=scl)
bmp = BMX280(bus, 0x76)

# Assign SD-Reader chip select (CS) pin (and start it high)
cs = machine.Pin(1, machine.Pin.OUT, machine.Pin.PULL_DOWN)

# Intialize SD-Reader SPI(0) peripheral (start with 1 MHz)
spi_SD = machine.SPI(0,
                  baudrate=1000000,
                  polarity=0,
                  firstbit=machine.SPI.MSB,
                  sck=machine.Pin(2),
                  mosi=machine.Pin(3),
                  miso=machine.Pin(0))

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
                          dc=machine.Pin(st7789_dc, machine.Pin.OUT, machine.Pin.PULL_DOWN),
                          xstart=0, ystart=0, rotation=1)

# Initialize SD card
sd = sdcard.SDCard(spi_SD, cs)

# Mount filesystem
vfs = uos.VfsFat(sd)
uos.mount(vfs, "/sd")

while True:
    cur_date = f"{ds.day():02d}.{ds.month():02d}.{ds.year()} - {ds.hour():02d}:{ds.minute():02d}:{ds.second():02d}"
    pressure = bmp.pressure
    temperature = bmp.temperature
    
    display.fill(st7789.MAGENTA)
    display.text(font1, f"{cur_date}", 30, 10)
    display.text(font2, f"Temperature", 10, 70, st7789.BLACK, st7789.MAGENTA)
    display.text(font2, f"{temperature:>10.2f}", 60, 100, st7789.BLACK, st7789.MAGENTA)
    display.text(font2, f"Pressure", 10, 130, st7789.BLACK, st7789.MAGENTA)
    display.text(font2, f"{pressure:>10.2f}", 60, 160, st7789.BLACK, st7789.MAGENTA)

    with open("/sd/temp.txt", "a") as file:
        file.write(f"Date: {cur_date}, Temp: {temperature}, Pres: {pressure}" + "\n")
        utime.sleep_ms(5)
        file.flush()
    utime.sleep(5)



