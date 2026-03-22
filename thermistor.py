from machine import Pin
from machine import ADC
import math

THERMISTOR_PIN = 27  # ADC 1

#VALUES
SERIES_RESISTOR = 10000  # The resistor connecting to thermistor
BETA = 3960              # Beta value from lecture


class Thermistor:
    """
    Thermistor temperature connected to ADC1
    Usage:
    therm = Thermistor()
    therm.update()       # Read and compute temperature
    print(therm.celsius)     # Temperature in celcius
    """

    def __init__(self, pin=THERMISTOR_PIN):
        self.adc = ADC(Pin(pin))
        self.raw_value = 0
        self.celsius = 0.0
        #self.fahrenheit = 0.0 #SEE COMMENT IN UPDATE

    def update(self):
        """
        Read the ADC and convert to temperature using the Beta equation.
        """
        self.raw_value = self.adc.read_u16()  # 0-65535

        if self.raw_value <= 0 or self.raw_value >= 65535: #if outside of (0,65535) return nothing because it doesnt WORKRRKAORKSORKAORK
            return

        temp_k = 1 / (1/298 + (1/3960) * math.log(65535 / self.raw_value - 1)) #KELVIN FROM DEADLOCK. LOOK HIM UP
        self.celsius = round((temp_k - 273) * 1, 1)
        #self.fahrenheit = round(self.celsius * 9 / 5 + 32, 1) #NOTE, WE CAN DO FARENHEIT BUT I HATE AMERICANS. PLEASE DO CELCIUS. (JOKES)

    def get_data(self):
        """
        Return sensor data for website
        """
        return {"temp_c": self.celsius}