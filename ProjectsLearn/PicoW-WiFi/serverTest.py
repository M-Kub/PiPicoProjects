import machine
import socket
import network
import rp2
import utime
from libs import stuff
from libs.neopixel import Neopixel


# Pico Setup
piLED = machine.Pin('LED', machine.Pin.OUT)

# Neopixel setup
numpix = 8
strip = Neopixel(numpix, 0, 15, "RGBW")
strip.brightness(80)
ledOn = (0, 0, 0, 255)
ledOff = (0, 0, 0, 0)
strip_state = 0

# WiFi setup
wifiSSID = stuff.wifiSSID
wifiPW = stuff.wifiPW
rp2.country('DE')

# Setup for the Webpage
page = open("libs/index.html", "r")
html = page.read()
page.close()


def wifiConnect():
    wifi = network.WLAN(network.STA_IF)
    if not wifi.isconnected():
        print("Please establish WIFI connection")
        wifi.active(True)
        wifi.connect(wifiSSID, wifiPW)
        for i in range(10):
            if wifi.status() < 0 or wifi.status() >= 3:
                break
            print("@@@")
            utime.sleep(0.5)
    if wifi.isconnected():
        print("Connection established, congratulations!")
        piLED.value(1)
        netConfig = wifi.ifconfig()
        print(f"Your IP address is: {netConfig[0]}\n")
        return netConfig[0]
    else:
        print(f"No WIFI connection. WIFI status is {wifi.status()}.\n")
        piLED.value(0)
        return ""


# Establish WIFI-Connection
ipv4 = wifiConnect()

# Starting the server
if ipv4 != "":
    print("Starting the server")
    addr = socket.getaddrinfo(ipv4, 80)[0][-1]
    server = socket.socket()
    server.bind(addr)
    server.listen(1)
    print(f"Server is listening on {addr}")
    
# Waitiing for connections
while True:
    try:
        conn, addr = server.accept()
        print(f"HTTP request from {addr} !")
        request = conn.recv(1024)
        request = str(request)
        request = request.split()
        print(f"URL: {request[1]}")
        if request[1] == "/light/on":
            print("Turning on LED!")
            strip_state = 1
            strip.fill(ledOn)
            strip.show()  
        elif request[1] == "/light/off":
            print('Turning off LED')
            strip_state = 0
            strip.fill(ledOff)
            strip.show()  
            
        # Evaluate LED status
        state_is = ""
        if strip_state == 1:
            state_is += "<p align='center'><b>LED is ON</b> <a href='/light/off'><button>OFF</button></a></p>"
        if strip_state == 0:
            state_is += "<p align='center'><b>LED is OFF</b> <a href='/light/on'><button>ON</button></a></p>"
        # Create the HTTP-Response
        response = html
        conn.send("HTTP/1.0 200 OK\r\nContent-type: text/html\r\n\r\n")
        conn.send(response)
        conn.close()
        print("HTTP-Response was send\n")
        print()
    except OSError as e:
        break
    except (KeyboardInterrupt):
        break

try: conn.close()
except NameError: pass
try: server.close()
except NameError: pass
piLED.value(0)
print("Server shut down")
