import math
import time
from time import sleep
import uasyncio as asyncio
import BME280
import mhz19
import ujson
#import adafruit_sgp30
import uSGP30
import uwebsockets.client as websocket_client
from machine import I2C, SPI, Pin
from ST7735_80x160 import TFT
#import ssd1306
from sysfont import sysfont

from security import HOST

# Подключаемся к WebSocket серверу
websocket = websocket_client.connect(HOST)

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
#tft.text((0, 23), 'WEATHER STATION', TFT.BLUE, sysfont, 2)
tft.text((40, 18), 'WEATHER', TFT.BLUE, sysfont, 2)
tft.text((40, 18 + 2 * sysfont["Height"] + 4), 'STATION', TFT.BLUE, sysfont, 2)
#display.text('Hello, World!', 0, 0, 1)
#display.show()

# waiting MHZ19
sleep(20)
# init MHZ19
mhz = mhz19.MHZ19(17, 18) # TX=GPIO17 RX=GPIO18
mhz.set_detection_range(5000) # detection range 0-5000PPM
mhz.read_co2_continuous(10000) # read co2 continuously every 10 secs
co2 = mhz.read_co2() # read co2 once

send_data = {
    "temperature": 0,
    "humidity": 0,
    "pressure": 0,
    "co2": 0,
    "co2eq": 0,
    "tvoc": 0
}



# Подключение к WebSocket серверу
async def websocket_connection():
    while True:
        try:
            print("Connecting to server...")
            websocket = websocket_client.connect(HOST)
            print("Connected!")

            while True:
                mhz.update()
  
                if (mhz.measure_co2 == 1):
                    # Обработка сенсорных данных
                    send_data = get_sensor_data()

                    # Отправка данных на сервер
                    ws_data = ujson.dumps(send_data)
                    websocket.send(ws_data)
                    print("ws data:", ws_data)
                    print('Temperature °C: ', send_data["temperature"])
                    print('Humidity %: ', send_data["humidity"])
                    print('Pressure mmHg: ', send_data["pressure"])
                    print("CO2 ppm", send_data["co2"])
                    print("CO2eq ppm", send_data["co2eq"])
                    print("TVOC ppb", send_data["tvoc"])
                    print(' ')
                    tempC_str = str(send_data["temperature"])
                    humC_str = str(send_data["humidity"])
                    presC_str = str(send_data["pressure"])
                    co2_str = str(send_data["co2"])
                    co2eq_str = str(send_data["co2eq"])
                    tvoc_str = str(send_data["tvoc"])
     
                    tft.fill(TFT.BLACK)
                    v = 0
                    tft.text((0, v), 'Temp C: ' + tempC_str, TFT.WHITE, sysfont, 1, nowrap=True)
                    v += sysfont["Height"] + 4
                    tft.text((0, v), 'Hum %: ' + humC_str, TFT.WHITE, sysfont, 1, nowrap=True)
                    v += sysfont["Height"] + 4
                    tft.text((0, v), 'Pres mmHg: ' + presC_str, TFT.WHITE, sysfont, 1, nowrap=True)
                    v += sysfont["Height"] + 4
                    tft.text((0, v), 'CO2: ' + co2_str + 'ppm', TFT.GREEN, sysfont, 1, nowrap=True)
                    v += sysfont["Height"] + 4
                    tft.text((0, v), 'CO2eq ppm: ' + co2eq_str, TFT.WHITE, sysfont, 1, nowrap=True)
                    v += sysfont["Height"] + 4
                    tft.text((0, v), 'TVOC ppb: ' + tvoc_str, TFT.WHITE, sysfont, 1, nowrap=True)

                    mhz.measure_co2 = 0 # wait set measure_co2

                # Отправляем ping-запрос для поддержания соединения
                try:
                    websocket.send("ping")  # Отправляем пинг
                    pong = websocket.recv()  # Ожидаем ответ от сервера
                    if pong != "pong":
                        raise Exception("No pong received!")
                    print("Received pong:", pong)
                    if pong is None:
                        raise Exception("No pong received!")
                except Exception as e:
                    print("Ping error or no pong:", e)
                    raise  # Закрываем соединение и переподключаемся

                # Ожидание перед следующей отправкой данных
                await asyncio.sleep(5)

        except Exception as e:
            print("Connection error:", e)
            await asyncio.sleep(5)  # Ждем и пробуем снова подключиться

def get_sensor_data():
    tempC = int(bme.temperatureD)
    humC = int(bme.humidityD)
    presC = int(bme.pressureD)
    co2eq, tvoc = sgp30.measure_iaq()
    co2 = mhz.get_co2()

    send_data = {
        "temperature": tempC,
        "humidity": humC,
        "pressure": presC,
        "co2": co2,
        "co2eq": co2eq,
        "tvoc": tvoc
    }
    return send_data


asyncio.run(websocket_connection())