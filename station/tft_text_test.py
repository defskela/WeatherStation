from ST7735_80x160 import TFT
from sysfont import sysfont
from machine import SPI,Pin, I2C
import BME280
import adafruit_sgp30
import mhz19
import time
from time import sleep
import math

# ESP32 - Pin assignment
i2c = I2C(1, scl=Pin(39), sda=Pin(40), freq=400000)
sgp30 = adafruit_sgp30.Adafruit_SGP30(i2c)
bme = BME280.BME280(i2c=i2c)
#=== prepare ST7735 SPI 80x160
spi = SPI(2, baudrate=20000000, polarity=0, phase=0, sck=Pin(7), mosi=Pin(11), miso=Pin(12))
pin_DC = 3
pin_RESET = 9
pin_CS = 5
tft=TFT(spi, pin_DC, pin_RESET, pin_CS)
tft.initr()
tft.rgb(False)
tft.invertcolor(True)
#===

tft.rotation(1)
tft.setStart(1, 26)
tft.fill(TFT.BLACK)
tft.text((0, 0), 'Hello, World!', TFT.WHITE, sysfont, 1)
sleep(1)

mhz = mhz19.MHZ19(17, 18) # TX=GPIO17 RX=GPIO18
mhz.set_detection_range(5000) # detection range 0-5000PPM
mhz.read_co2_continuous(10000) # read co2 continuously every 10 secs
co2 = mhz.read_co2() # read co2 once



def tftprinttest():
    tft.fill(TFT.BLACK);
    v = 0
    tft.text((0, v), "Hello World!", TFT.RED, sysfont, 1, nowrap=True)
    time.sleep_ms(1500)
    v += sysfont["Height"]
    tft.text((0, v), "WETHER STATION", TFT.YELLOW, sysfont, 2)
    time.sleep_ms(1500)
    v += sysfont["Height"] * 2
    tft.text((0, v), "Hello World!", TFT.GREEN, sysfont, 3, nowrap=True)
    time.sleep_ms(1500)
    v += sysfont["Height"] * 3
    tft.text((0, v), str(1234.567), TFT.BLUE, sysfont, 4, nowrap=True)
    time.sleep_ms(1500)
    tft.fill(TFT.BLACK);
    v = 0
    tft.text((0, v), "Hello World!", TFT.RED, sysfont, 2)
    v += sysfont["Height"] * 2
    tft.text((0, v), str(math.pi), TFT.GREEN, sysfont, 2)
    v += sysfont["Height"] * 2
    tft.text((0, v), " Want pi?", TFT.GREEN, sysfont, 2)
    v += sysfont["Height"] * 2
    tft.text((0, v), hex(8675309), TFT.GREEN, sysfont, 2)
    v += sysfont["Height"]
    tft.text((0, v), " Print HEX!", TFT.GREEN, sysfont, 2)
    v += sysfont["Height"] * 2
    tft.text((0, v), "Sketch has been", TFT.WHITE, sysfont)
    v += sysfont["Height"]
    tft.text((0, v), "running for: ", TFT.WHITE, sysfont)
    v += sysfont["Height"]
    tft.text((0, v), str(time.ticks_ms() / 1000), TFT.PURPLE, sysfont)
    v += sysfont["Height"]
    tft.text((0, v), " seconds.", TFT.WHITE, sysfont)

def test_main():
    tft.fill(TFT.BLACK)
    tft.text((0, 0), "PRIVET", TFT.WHITE, sysfont, 1)
    time.sleep_ms(1000)

    tftprinttest()
    time.sleep_ms(4000)


'''
test_main()

tft.rotation(1)
tft.setStart(1, 26)
test_main()
'''
test_main()
while True:
  
  mhz.update()
  
  if (mhz.measure_co2 == 1):
    tempC = bme.temperatureD
    humC = bme.humidityD
    presC = bme.pressureD
    co2eq, tvoc = sgp30.iaq_measure()
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
    v += sysfont["Height"]
    tft.text((0, v), 'Hum %: ' + humC_str, TFT.WHITE, sysfont, 1, nowrap=True)
    v += sysfont["Height"]
    tft.text((0, v), 'Pres hPa: ' + presC_str, TFT.WHITE, sysfont, 1, nowrap=True)
    v += sysfont["Height"]
    tft.text((0, v), 'CO2: ' + co2_str, TFT.WHITE, sysfont, 1, nowrap=True)
    v += sysfont["Height"]
    tft.text((0, v), 'CO2eq ppm: ' + co2eq_str, TFT.WHITE, sysfont, 1, nowrap=True)
    v += sysfont["Height"]
    tft.text((0, v), 'TVOC ppb: ' + tvoc_str, TFT.WHITE, sysfont, 1, nowrap=True)

    mhz.measure_co2 = 0
