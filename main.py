import time

from motion_sensor import MotionSensor
from light_sensor import LightSensor
from thermistor import Thermistor

motion = MotionSensor()   
light  = LightSensor()    
therm  = Thermistor()     

# Data refresh speed
UPDATE_INTERVAL_MS = 500 #every half a second

last_update = time.ticks_ms()

while True:
    motion.update()

    if time.ticks_diff(time.ticks_ms(), last_update) >= UPDATE_INTERVAL_MS:
        light.update()
        therm.update()

        m = motion.get_data()
        l = light.get_data()
        t = therm.get_data()

        last_update = time.ticks_ms()

    time.sleep(0.01)