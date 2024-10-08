""" uSGP30-test.py
Tests the uSGP30 library. Uses test values for temperature and humidity for
triggering humidity compensation.
Does not check < 7 day validity of stored baseline, nor does it enforce
12 hour early operation phase if no baseline is found (just a warning is
displayed).
"""

import uSGP30
import machine
import ujson
import utime

from ST7735_80x160 import TFT
from sysfont import sysfont
from machine import SPI

BASELINE_FILE = "sgp30_iaq_baseline.txt"
I2C_SCL_GPIO = const(39)
I2C_SDA_GPIO = const(40)
I2C_FREQ = const(400000)
MEASURE_INTERVAL_MS = const(2000)  # Minutely measurements
BASELINE_INTERVAL_MS = const(3600000)  # Hourly baseline commits
SGP30_INIT_TIME_MS = const(15000)
# Made-up test values
TEST_TEMP_C = const(25)
TEST_R_HUMIDITY_PERC = const(50)

#=== prepare ST7735 SPI 80x160
spi = SPI(2, baudrate=20000000, polarity=0, phase=0, sck=7, mosi=11, miso=12)
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
tft.text((0, 0), 'SGP30 Test', TFT.WHITE, sysfont, 1)


def run():
    """ Runs test application """
    print("Warning: Test uses ficticious temperature and humidity values!")
#    i2c = machine.I2C(scl=machine.Pin(I2C_SCL_GPIO, machine.Pin.OUT), sda=machine.Pin(I2C_SDA_GPIO, machine.Pin.OUT), freq=I2C_FREQ,)
    i2c = machine.I2C(1, scl=39, sda=40, freq=400000)
    sgp30 = uSGP30.SGP30(i2c)
    # Sensor initialisation time
    utime.sleep_ms(SGP30_INIT_TIME_MS)
    try:
        with open(BASELINE_FILE, "r") as file:
            current_baseline = ujson.loads(file.read())
    except OSError as exception:
        print(exception)
        print(
            "No valid baseline found. You should wait 12 hours for calibration before use."
        )
    else:
        print("Baseline found:", current_baseline)
        sgp30.set_iaq_baseline(current_baseline[0], current_baseline[1])
    finally:
        # Set absolute humidity
        a_humidity_perc = uSGP30.convert_r_to_a_humidity(
            TEST_TEMP_C, TEST_R_HUMIDITY_PERC
        )
        sgp30.set_absolute_humidity(a_humidity_perc)
    # Main application loop
    last_baseline_commit_ms = utime.ticks_ms()
    while True:
        last_iaq_check_ms = utime.ticks_ms()
        co2eq_ppm, tvoc_ppb = sgp30.measure_iaq()
        print("BaseLine=", sgp30.get_iaq_baseline())
        print("CO2 ppm = ", str(co2eq_ppm))
        print("TVOC ppb = ", tvoc_ppb)
        print()
        
        tft.fill(TFT.BLACK);
        v = 0
        tft.text((0, v), 'CO2 ppm = ' + str(co2eq_ppm), TFT.WHITE, sysfont, 1, nowrap=True)
        v += (sysfont["Height"] + 2)
        tft.text((0, v), 'VOC ppb = ' + str(tvoc_ppb), TFT.WHITE, sysfont, 1, nowrap=True)
        v += (sysfont["Height"] + 2)
        tft.text((0, v), 'BaseLine = ' + str(sgp30.get_iaq_baseline()), TFT.WHITE, sysfont, 1, nowrap=True)
        
        # Set absolute humidity
        a_humidity_perc = uSGP30.convert_r_to_a_humidity(
            TEST_TEMP_C, TEST_R_HUMIDITY_PERC
        )
        sgp30.set_absolute_humidity(a_humidity_perc)
        if utime.ticks_ms() - last_baseline_commit_ms > BASELINE_INTERVAL_MS:
            # Get current baseline and store on flash
            current_baseline = sgp30.get_iaq_baseline()
            with open(BASELINE_FILE, "w") as file:
                file.write(str(current_baseline))
            print("Baseline commited:", str(current_baseline))
            last_baseline_commit_ms = utime.ticks_ms()
        utime.sleep_ms(MEASURE_INTERVAL_MS - (utime.ticks_ms() - last_iaq_check_ms))

run()