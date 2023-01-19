import machine
import socket
import network
import rp2
import utime
from libs import stuff


# PiPico Setup
led = machine.Pin("LED", machine.Pin.OUT)

# WiFi setup
wifiSSID = stuff.wifiSSID
wifiPW = stuff.wifiPW
rp2.country('DE')

html = """<!doctype html><html lang="en"> <head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><link rel="shortcut icon" href="data:"> \
<title>PicoW ServerTest</title> </head> \
<body><h1 align="center">HiHo, what is going on?</h1><hr>TEXT<hr><p align="center">What's up everybody?</p></body></html>"""


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
        netConfig = wifi.ifconfig()
        print(f"Your IP address is: {netConfig[0]}\n")
        return netConfig[0]
    else:
        print(f"No WIFI connection. WIFI status is {wifi.status()}.\n")
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
            led.value(1)
        elif request[1] == "/light/off":
            print('Turning off LED')
            led.value(0)
        elif request[1] == "/light/toggle":
            print("Toggle LED")
            led.toggle()
        # Evaluate LED status
        state_is = ""
        if led.value() == 1:
            state_is += "<p align='center'><b>LED is ON</b> <a href='/light/off'><button>OFF</button></a></p>"
        if led.value() == 0:
            state_is += '<p align="center"><b>LED is OFF</b> <a href="/light/on"><button>ON</button></a></p>'
        # Create the HTTP-Response
        response = html.replace("TEXT", state_is)
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
print("Server shut down")
            
        
            
        
        

