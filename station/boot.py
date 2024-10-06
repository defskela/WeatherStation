# boot.py -- run on boot-up
import network
from machine import Pin
from station.security import SSID, PASSWORD

# Replace the following with your WIFI Credentials
SSID = SSID
SSI_PASSWORD = PASSWORD

def do_connect():
    import network
    sta_if = network.WLAN(network.STA_IF)
    if not sta_if.isconnected():
        print('connecting to network...')
        sta_if.active(True)
        sta_if.connect(SSID, SSI_PASSWORD)
        while not sta_if.isconnected():
            pass
    # sta_if.ifconfig(('192.168.1.150', '255.255.255.0', '192.168.1.1', '192.168.1.1'))
    sta_if.ifconfig((need address))
    print('network config:', sta_if.ifconfig())
    led.on()
do_connect()