"""
Console output test for all three sensors.
See values before main
"""

import time

from motion_sensor import MotionSensor
from light_sensor import LightSensor
from thermistor import Thermistor

# Sensors
motion = MotionSensor()   
light  = LightSensor()    
therm  = Thermistor()    
# Data refresh speed
PRINT_INTERVAL_MS = 1000

last_print = time.ticks_ms() #time.ticks_ms() checks time since raspberry pi started running dont forget 

print("Sensor Test Started")

while True:
    motion.update()
    if time.ticks_diff(time.ticks_ms(), last_print) >= PRINT_INTERVAL_MS: #if time since last print and time.ticks_ms longer than PRINT_INTERVAL_MS, do below.
        motion.update()
        light.update()
        therm.update()

        m = motion.get_data()
        l = light.get_data()
        t = therm.get_data()

        print("Sensor Reading")
        print(f"  Occupancy:   {m['occupancy']} occupancy")
        print(f"  Light:       {l['light_label']}  |  raw ADC: {l['light_raw']}")
        print(f"  Temperature: {t['temp_c']} C ")

        last_print = time.ticks_ms()

    time.sleep(0.01)
