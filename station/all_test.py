from ST7735_80x160 import TFT
#import ssd1306
from sysfont import sysfont

import BME280

#import adafruit_sgp30
import uSGP30

import mhz19

import time
from time import sleep
import math
from machine import SPI,Pin, I2C

# ESP32 - Pin assignment I2C
i2c = I2C(1, scl=Pin(39), sda=Pin(40), freq=400000)
# Connect SGP30
sgp30 = uSGP30.SGP30(i2c)
# Connect BME280
bme = BME280.BME280(i2c=i2c)
# Connect OLED
#display = ssd1306.SSD1306_I2C(128, 64, i2c)
# SPI for TFT ST7735 80x160
spi = SPI(2, baudrate=20000000, polarity=0, phase=0, sck=Pin(7), mosi=Pin(11), miso=Pin(12))
pin_DC = 3
pin_RESET = 9
pin_CS = 5
# init TFT
tft=TFT(spi, pin_DC, pin_RESET, pin_CS)
tft.initr()
tft.rgb(False)
tft.invertcolor(True)
tft.rotation(1)
tft.setStart(1, 26)

# Welcome print displays
tft.fill(TFT.BLACK)
tft.text((0, 0), 'Hello, World!', TFT.WHITE, sysfont, 1)
#display.text('Hello, World!', 0, 0, 1)
#display.show()

# waiting MHZ19
sleep(20)
# init MHZ19
mhz = mhz19.MHZ19(17, 18) # TX=GPIO17 RX=GPIO18
mhz.set_detection_range(5000) # detection range 0-5000PPM
mhz.read_co2_continuous(10000) # read co2 continuously every 10 secs
co2 = mhz.read_co2() # read co2 once


while True:
  
  mhz.update()
  
  if (mhz.measure_co2 == 1): # wait read_co2_continuous
    tempC = int(bme.temperatureD)
    humC = int(bme.humidityD)
    presC = int(bme.pressureD)
    co2eq, tvoc = sgp30.measure_iaq()
    co2 = mhz.get_co2()
    print('Temperature °C: ', tempC)
    print('Humidity %: ', humC)
    print('Pressure hPa: ', presC)
    print("CO2 ppm", co2)
    print("CO2eq ppm", co2eq)
    print("TVOC ppb", tvoc)
    print(' ')
    tempC_str = str(tempC)
    humC_str = str(humC)
    presC_str = str(presC)
    co2_str = str(co2)
    co2eq_str = str(co2eq)
    tvoc_str = str(tvoc)
 
    tft.fill(TFT.BLACK);
    v = 0
    tft.text((0, v), 'Temp C: ' + tempC_str, TFT.WHITE, sysfont, 1, nowrap=True)
    v += sysfont["Height"] + 2
    tft.text((0, v), 'Hum %: ' + humC_str, TFT.WHITE, sysfont, 1, nowrap=True)
    v += sysfont["Height"] + 2
    tft.text((0, v), 'Pres hPa: ' + presC_str, TFT.WHITE, sysfont, 1, nowrap=True)
    v += sysfont["Height"] + 2
    tft.text((0, v), 'CO2: ' + co2_str, TFT.GREEN, sysfont, 1, nowrap=True)
    v += sysfont["Height"] + 2
    tft.text((0, v), 'CO2eq ppm: ' + co2eq_str, TFT.WHITE, sysfont, 1, nowrap=True)
    v += sysfont["Height"] + 2
    tft.text((0, v), 'TVOC ppb: ' + tvoc_str, TFT.WHITE, sysfont, 1, nowrap=True)

    mhz.measure_co2 = 0 # wait set measure_co2
