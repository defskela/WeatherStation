# boot.py -- run on boot-up
import network
from machine import Pin

led = Pin(12, Pin.OUT)
led_work = Pin(13, Pin.OUT)

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
    sta_if.ifconfig(('192.168.0.150', '255.255.255.0', '192.168.0.1', '255.255.255.0'))
    print('network config:', sta_if.ifconfig())
    led.on()
do_connect()