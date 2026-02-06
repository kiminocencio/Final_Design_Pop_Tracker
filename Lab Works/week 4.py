import machine
import utime

# Choose which part to run
RUN_IR = False   # False = 4.4.2 blink, True = 4.4.3 IR control

# 4.4.2 LED on GP16
led = machine.Pin(16, machine.Pin.OUT)

# 4.4.3 IR receiver on ADC1 (GP27)
ir = machine.ADC(27)

threshold = 30000  # tune this after the readings

if RUN_IR == False:
    # ---------- Activity 4.4.2: blink every 2 seconds ----------
    while True:
        led.value(1)
        utime.sleep(2)
        led.value(0)
        utime.sleep(2)

else:
    # ---------- Activity 4.4.3: IR controls LED ----------
    while True:
        x = ir.read_u16()
        print(x)

        # If IR is NOT received -> LED OFF
        # This assumes "blocked" gives a LOWER reading.
        if x < threshold:
            led.value(0)
        else:
            led.value(1)

        utime.sleep(0.2)
