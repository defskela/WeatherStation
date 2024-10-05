# Complete project details at https://RandomNerdTutorials.com

from machine import Pin, I2C
from time import sleep
import BME280
import adafruit_sgp30
import ssd1306

# ESP32 - Pin assignment
i2c = I2C(1, scl=Pin(39), sda=Pin(40), freq=400000)
sgp30 = adafruit_sgp30.Adafruit_SGP30(i2c)
bme = BME280.BME280(i2c=i2c)
display = ssd1306.SSD1306_I2C(128, 64, i2c)
display.text('Hello, World!', 0, 0, 1)
display.show()
while True:
  
  tempC = bme.temperatureD
  humC = bme.humidityD
  presC = bme.pressureD
  co2eq, tvoc = sgp30.iaq_measure()
  print('Temperature °C: ', tempC)
  print('Humidity %: ', humC)
  print('Pressure hPa: ', presC)
  print("CO2eq ppm", co2eq)
  print("TVOC ppb", tvoc)
  print(' ')
  tempC_str = str(tempC)
  humC_str = str(humC)
  presC_str = str(presC)
  co2eq_str = str(co2eq)
  tvoc_str = str(tvoc)
  display.fill(0)
  display.text('Temp C: ' + tempC_str, 0, 0, 1)
  display.text('Hum %: ' + humC_str, 0, 10, 1)
  display.text('Pres hPa: ' + presC_str, 0, 20, 1)
  display.text('CO2eq ppm: ' + co2eq_str, 0, 30, 1)
  display.text('TVOC ppb: ' + tvoc_str, 0, 40, 1)
  display.show()
  sleep(1)
