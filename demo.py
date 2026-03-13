from machine import Pin
import time

#RASPBERRY PI SLOTS
SENSOR_INSIDE_PIN = 14
SENSOR_OUTSIDE_PIN = 15


#GLOBAL VARIABLES
OCCUPANCY = 0
CHECK_WINDOW_MS = 1000 #How long to check sensors for if one is triggered

#RASPBERRY PI DATA
sensor_inside = Pin(SENSOR_INSIDE_PIN, Pin.IN)
sensor_outside = Pin(SENSOR_OUTSIDE_PIN, Pin.IN)
#TEST: COMMENT IN/OUT IF NEED RAW READINGS
#sensor_inside = Pin(14, Pin.IN)
#sensor_outside = Pin(15, Pin.IN)

#while True:
 #   print("Sensor1:", sensor_inside.value(),
  #        "Sensor2:", sensor_outside.value())
   # time.sleep(0.2)


#FUNCTIONS

def check_enter():
    global OCCUPANCY
    
    if sensor_outside.value() == 0:

        start_time = time.ticks_ms() #START CHECKING TIME HERE

        while time.ticks_diff(time.ticks_ms(), start_time) < CHECK_WINDOW_MS: #(if the difference between start time and time.ticks_ms() is less than 1 second.

            if sensor_inside.value() == 0:
                OCCUPANCY += 1
                print("Person entered the room.")
                print("Occupancy:", OCCUPANCY)

                wait_for_clear()
                return


def check_exit():
    global OCCUPANCY

    if sensor_inside.value() == 0:

        start_time = time.ticks_ms()

        while time.ticks_diff(time.ticks_ms(), start_time) < CHECK_WINDOW_MS: 

            if sensor_outside.value() == 0:

                OCCUPANCY -= 1
                if OCCUPANCY < 0: #SO IT DOESNT GO INTO -VE
                    OCCUPANCY = 0

                print("Person left the room.")
                print("Occupancy:", OCCUPANCY)

                wait_for_clear()
                return


def wait_for_clear():
    """
    Function that modifies sleep value (time between scans)
"""
    while sensor_inside.value() == 0 or sensor_outside.value() == 0:
        time.sleep(0.01)



while True:
    check_enter()
    check_exit()
    time.sleep(0.01)
    
    
    
    
"""Notes
neat function. global makes it update the variable instead.
Sensors 0 if motion detected.
Turn knob uptop of sensors to increase distance
ticks_ms():
Returns the time since raspberry started running
ticks_diff(new,old):
calculates the difference between old and new ticks_ms

"""

