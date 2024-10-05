import mhz19
from time import sleep

mhz = mhz19.MHZ19(17, 18) # TX=GPIO17 RX=GPIO18

# detection range 0-5000PPM
mhz.set_detection_range(5000)

# read co2 once
co2 = mhz.read_co2()

# read co2 continuously every 5 secs
mhz.read_co2_continuous(10000)

while True:
#    sleep(0.05)

    mhz.update()
    
    # get co2 measured in the continuous mode
    if (mhz.measure_co2 == 1):
        co2 = mhz.get_co2()
        print("CO2 =", co2)
        mhz.measure_co2 = 0