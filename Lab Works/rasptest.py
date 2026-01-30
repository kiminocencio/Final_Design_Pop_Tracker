import machine
import utime

VOLT_RAW = machine.ADC(26) #Initializes pin 31
CONVERSION_FACTOR = 3.3/65535
LIGHT_RAW = machine.ADC(27)
TEMP_RAW = machine.ADC(4) #4 because the ADC is in the chip itself
#LIGHT_ON = VOLTAGE HERE. Measure first


def read_volts():
    """
    Just reads the volts and prints
    
    can probably return voltage for other stuff by using return?
    
    """
    
    while True:
        raw= VOLT_RAW.read_u16()
        voltage = raw * CONVERSION_FACTOR
        print(raw)
        
        utime.sleep(2)


def read_light():
    """
    reads the light levels of light sensor, prints if exposed to light or not
    """
    while True:
        raw = LIGHT_RAW.read_u16()         # can use first function maybe.      
        voltage = raw * CONVERSION_FACTOR        

        print("Raw ADC:", raw, "Voltage:", voltage)

        if voltage > LIGHT_ON:
            print("Light sensor is exposed to light")
        else:
            print("Light sensor is not exposed to light")

        utime.sleep(2)
        
        
def read_temp():
    """
    Should read the temp of sensor and give it in Celcius
    """
    while True:
        raw = TEMP_RAW.read_u16()
        reading =  raw * CONVERSION_FACTOR
        temperature = 27 - (reading - 0.706)/0.001721
        print(temperature)
        utime.sleep(2)
        
        

    

