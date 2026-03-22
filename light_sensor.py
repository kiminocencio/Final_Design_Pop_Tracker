from machine import Pin
from machine import ADC
import time

LIGHT_SENSOR_PIN = 26

# VARIABLES
DARK_THRESHOLD = 35000   # Below this = dark
BRIGHT_THRESHOLD = 50000 # Above this = bright


class LightSensor:
    """
    Ambient light sensor using an phototransistor connected to ADC 0

    Usage:
    light = LightSensor()
    light.update()                  # Read a new value
    print(light.raw_value)          # Raw 16-bit ADC reading (0–65535)
    print(light.label)              # "dark", "moderate", or "bright" 
    """

    def __init__(self, pin=LIGHT_SENSOR_PIN):
        self.adc = ADC(Pin(pin))
        self.raw_value = 0
        self.label = "blergh"

    def update(self):
        """
        Read a fresh value from the ADC and update all properties
        """
        self.raw_value = self.adc.read_u16()  # 0–65535
        self.label = self._classify(self.raw_value)

    def _classify(self, raw):
        """
        Tells light levels of raspberry
        """
        if raw < DARK_THRESHOLD:
            return "dark"
        elif raw < BRIGHT_THRESHOLD:
            return "moderate"
        else:
            return "bright"

    def get_data(self):
        """
        Return sensor data as variable for webpage
        """
        return {
            "light_raw": self.raw_value,
            "light_label": self.label }
