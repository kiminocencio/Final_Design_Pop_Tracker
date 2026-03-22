from machine import Pin
import time

# PIN CONFIGURATION
SENSOR_INSIDE_PIN = 14
SENSOR_OUTSIDE_PIN = 15

#TIMING
CHECK_WINDOW_MS = 1000  # How long to check sensors after one is triggered. INCREASE IF UVIC IS FULL OF SLOW WALKERS.


class MotionSensor:
    """
    Occupancy counter using gikfun motion sensor
    Sensor reads 0 when motion is detected, 1 if none.

    Usage:
    sensor = MotionSensor() 
    sensor.update()           # Call repeatedly in your main loop
    count = sensor.occupancy  # Get current occupancy count
    
    
    
    
    
    """

    def __init__(self, inside_pin=SENSOR_INSIDE_PIN, outside_pin=SENSOR_OUTSIDE_PIN):
        self.sensor_inside = Pin(inside_pin, Pin.IN)
        self.sensor_outside = Pin(outside_pin, Pin.IN)
        self.occupancy = 0

    def wait_for_clear(self):
        """
        Wait until both sensors stop detecting motion before resuming. For when retards stand in doorways.
        """
        while self.sensor_inside.value() == 0 or self.sensor_outside.value() == 0:
            time.sleep(0.01)

    def check_enter(self):
        """
        Detect if a person has entered (sensor farthest from raspberry pi triggers last).
        """
        if self.sensor_outside.value() == 0:
            start_time = time.ticks_ms()
            while time.ticks_diff(time.ticks_ms(), start_time) < CHECK_WINDOW_MS: #If time 
                if self.sensor_inside.value() == 0:
                    self.occupancy += 1
                    self.wait_for_clear()
                    return

    def check_exit(self):
        """
        Detect if a person has exited (sensor closest to raspberry pi triggers first)
        """
        if self.sensor_inside.value() == 0:
            start_time = time.ticks_ms()
            while time.ticks_diff(time.ticks_ms(), start_time) < CHECK_WINDOW_MS:
                if self.sensor_outside.value() == 0:
                    self.occupancy -= 1
                    if self.occupancy < 0:
                        self.occupancy = 0
                    self.wait_for_clear()
                    return

    def update(self):
        """
        Run one cycle of enter/exit detection. Call this in main. call whenever.
        """
        self.check_enter()
        self.check_exit()

    def get_data(self):
        """
        Return sensor data as value for website
        """
        return {
            "occupancy": self.occupancy
        }
