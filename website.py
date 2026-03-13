# ---------------------------------------------------------
# Libraries
# ---------------------------------------------------------
# network: allows the Pico W to connect to Wi-Fi
# socket: allows the Pico to create a web server
# time: used for delays while connecting to Wi-Fi
# machine: used to access hardware pins and analog sensors
import network
import socket
import time
from machine import Pin, ADC


# ---------------------------------------------------------
# Wi-Fi Access Point Information
# ---------------------------------------------------------
# These credentials allow the Pico W to connect to the team's
# Wi-Fi network so the webpage can be accessed from a browser.
SSID = "b15g03"
PASSWORD = "teamthermostat"


# ---------------------------------------------------------
# Sensor Setup
# ---------------------------------------------------------
# These pins correspond to sensors connected to the Pico.

# IR sensor used to detect occupancy (digital input)
ir_sensor = Pin(14, Pin.IN)

# Thermistor connected to an ADC pin for temperature readings
thermistor = ADC(26)

# Light sensor (phototransistor or photoresistor) using ADC
light_sensor = ADC(27)


# ---------------------------------------------------------
# Output Setup
# ---------------------------------------------------------
# Built-in LED on the Pico can be used for testing or status
led = Pin("LED", Pin.OUT)


# ---------------------------------------------------------
# Function: get_temperature()
# ---------------------------------------------------------
# Reads the analog thermistor value and converts it to an
# approximate temperature in Celsius.
# NOTE: This is a placeholder conversion for demonstration.
def get_temperature():
    raw = thermistor.read_u16()   # read ADC value (0-65535)

    # Convert raw sensor reading into approximate temperature
    temp_c = 20 + (raw / 65535) * 10

    # Round to one decimal place for display on dashboard
    return round(temp_c, 1)


# ---------------------------------------------------------
# Function: get_light_level()
# ---------------------------------------------------------
# Reads the analog light sensor and categorizes the brightness
# into qualitative levels for easier display on the dashboard.
def get_light_level():

    raw = light_sensor.read_u16()

    # Threshold ranges determine brightness category
    if raw < 20000:
        return "Low"
    elif raw < 45000:
        return "Moderate"
    else:
        return "Bright"


# ---------------------------------------------------------
# Function: get_occupancy()
# ---------------------------------------------------------
# Reads the IR motion sensor to determine if the room is
# occupied. Returns both a count and a text label.
# (Currently simple placeholder logic.)
def get_occupancy():

    if ir_sensor.value() == 0:
        return 1, "Room Occupied"
    else:
        return 0, "Room Empty"


# ---------------------------------------------------------
# Function: build_html()
# ---------------------------------------------------------
# Creates the HTML webpage that will be sent to the browser.
# Sensor values are inserted dynamically using Python
# variables so the webpage reflects real-time data.
def build_html():

    # Get latest sensor readings
    current_temp = get_temperature()
    light_level = get_light_level()
    occupancy_count, occupancy_status = get_occupancy()

    # Determine system state based on occupancy
    if occupancy_count > 0:
        light_status = "Lights ON"
        heating_state = "Active"
        alert_text = "Room occupied. Lighting and heating systems active."
    else:
        light_status = "Lights OFF"
        heating_state = "Idle"
        alert_text = "Room empty. Lighting and heating systems reduced."

    # HTML webpage sent to the user’s browser
    # f-string allows Python variables to appear inside the page
    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Occupancy-Aware Room Dashboard</title>

<style>

body {{
font-family: Arial, sans-serif;
margin: 0;
padding: 20px;
background: #f4f6f8;
color: #222;
}}

h1 {{
text-align: center;
margin-bottom: 24px;
}}

.dashboard {{
display: grid;
grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
gap: 16px;
max-width: 1000px;
margin: 0 auto;
}}

.card {{
background: white;
border-radius: 12px;
padding: 18px;
box-shadow: 0 2px 8px rgba(0,0,0,0.08);
}}

.card h2 {{
font-size: 1.1rem;
margin-top: 0;
margin-bottom: 10px;
}}

.value {{
font-size: 1.8rem;
font-weight: bold;
margin-bottom: 8px;
}}

.status {{
font-size: 1rem;
padding: 8px 10px;
border-radius: 8px;
display: inline-block;
background: #e9eef3;
}}

.alert-box {{
background: #fff3cd;
border-left: 5px solid #f0ad4e;
padding: 12px;
border-radius: 8px;
margin-top: 6px;
}}

</style>
</head>


<body>

<h1>Room Monitoring Dashboard</h1>

<div class="dashboard">

<div class="card">
<h2>Occupancy</h2>
<div class="value">{occupancy_count}</div>
<div class="status">{occupancy_status}</div>
</div>

<div class="card">
<h2>Temperature</h2>
<div class="value">{current_temp}°C</div>
<div class="status">Live sensor reading</div>
</div>

<div class="card">
<h2>Light Level</h2>
<div class="value">{light_level}</div>
<div class="status">{light_status}</div>
</div>

<div class="card">
<h2>Heating</h2>
<div class="value">{heating_state}</div>
<div class="status">System responding to occupancy</div>
</div>

<div class="card">
<h2>System Alerts</h2>
<div class="alert-box">
{alert_text}
</div>
</div>

</div>

</body>
</html>
"""

    return html


# ---------------------------------------------------------
# Wi-Fi Connection
# ---------------------------------------------------------
# Connect the Pico W to the specified Wi-Fi network
wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect(SSID, PASSWORD)

print("Connecting to WiFi...")

# Wait until connection is successful
while not wlan.isconnected():
    time.sleep(1)

# Get IP address assigned by the router
ip = wlan.ifconfig()[0]

print("Connected!")
print("Pico IP address:", ip)


# ---------------------------------------------------------
# Web Server Setup
# ---------------------------------------------------------
# Create a socket server that listens for browser requests
addr = socket.getaddrinfo("0.0.0.0", 80)[0][-1]

server = socket.socket()
server.bind(addr)
server.listen(1)

print("Server running. Open this in browser:", ip)


# ---------------------------------------------------------
# Main Server Loop
# ---------------------------------------------------------
# Waits for a browser to connect, then sends the webpage
while True:

    # Accept incoming browser connection
    client, address = server.accept()

    # Receive request from browser
    request = client.recv(1024)
    print("Request received from", address)

    # Build the webpage with latest sensor values
    html = build_html()

    # Send HTTP response header
    client.send("HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n\r\n")

    # Send webpage content
    client.sendall(html.encode())

    # Close connection
    client.close()