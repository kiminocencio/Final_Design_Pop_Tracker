import network
import socket
import time

try:
    import ujson as json
except ImportError:
    import json

from motion_sensor import MotionSensor
from light_sensor import LightSensor
from thermistor import Thermistor


# ---------------------------------------------------------
# Wi-Fi Access Point
# ---------------------------------------------------------
SSID = "b15g03"
PASSWORD = "teamthermostat"

ap = network.WLAN(network.AP_IF)
ap.active(True)
ap.config(essid=SSID, password=PASSWORD)

print("Starting Pico WiFi access point...")

while not ap.active():
    time.sleep(0.1)

ip = ap.ifconfig()[0]
print("Access Point active")
print("WiFi name:", SSID)
print("Password:", PASSWORD)
print("Pico IP address:", ip)


# ---------------------------------------------------------
# Sensor objects
# ---------------------------------------------------------
motion = MotionSensor()
light = LightSensor()
therm = Thermistor()

UPDATE_INTERVAL_MS = 500
last_update = time.ticks_ms()


def update_sensors_if_needed():
    global last_update

    motion.update()

    if time.ticks_diff(time.ticks_ms(), last_update) >= UPDATE_INTERVAL_MS:
        light.update()
        therm.update()
        last_update = time.ticks_ms()


def get_system_data():
    update_sensors_if_needed()

    m = motion.get_data()
    l = light.get_data()
    t = therm.get_data()

    occupancy = m["occupancy"]
    temp_c = t["temp_c"]
    light_label = l["light_label"]
    light_raw = l["light_raw"]

    if occupancy > 0:
        occupancy_status = "Room Occupied"
        light_status = "Lights ON"
        heating_state = "Active"
        alert_text = "Room occupied. Lighting and heating systems active."
    else:
        occupancy_status = "Room Empty"
        light_status = "Lights OFF"
        heating_state = "Idle"
        alert_text = "Room empty. Lighting and heating systems reduced."

    return {
        "occupancy": occupancy,
        "occupancy_status": occupancy_status,
        "temp_c": temp_c,
        "light_label": light_label,
        "light_raw": light_raw,
        "light_status": light_status,
        "heating_state": heating_state,
        "alert_text": alert_text
    }


def build_html():
    return """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Occupancy-Aware Room Dashboard</title>
<style>
body {
    font-family: Arial, sans-serif;
    margin: 0;
    padding: 20px;
    background: #f4f6f8;
    color: #222;
}
h1 {
    text-align: center;
    margin-bottom: 24px;
}
.dashboard {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
    gap: 16px;
    max-width: 1000px;
    margin: 0 auto;
}
.card {
    background: white;
    border-radius: 12px;
    padding: 18px;
    box-shadow: 0 2px 8px rgba(0,0,0,0.08);
}
.card h2 {
    font-size: 1.1rem;
    margin-top: 0;
    margin-bottom: 10px;
}
.value {
    font-size: 1.8rem;
    font-weight: bold;
    margin-bottom: 8px;
}
.status {
    font-size: 1rem;
    padding: 8px 10px;
    border-radius: 8px;
    display: inline-block;
    background: #e9eef3;
}
.alert-box {
    background: #fff3cd;
    border-left: 5px solid #f0ad4e;
    padding: 12px;
    border-radius: 8px;
    margin-top: 6px;
}
.small {
    font-size: 0.9rem;
    color: #555;
    margin-top: 8px;
}
</style>
</head>
<body>

<h1>Room Monitoring Dashboard</h1>

<div class="dashboard">

    <div class="card">
        <h2>Occupancy</h2>
        <div class="value" id="occupancy">--</div>
        <div class="status" id="occupancy_status">Loading...</div>
    </div>

    <div class="card">
        <h2>Temperature</h2>
        <div class="value" id="temp_c">-- °C</div>
        <div class="status">Live sensor reading</div>
    </div>

    <div class="card">
        <h2>Light Level</h2>
        <div class="value" id="light_label">--</div>
        <div class="status" id="light_status">Loading...</div>
        <div class="small">Raw ADC: <span id="light_raw">--</span></div>
    </div>

    <div class="card">
        <h2>Heating</h2>
        <div class="value" id="heating_state">--</div>
        <div class="status">System responding to occupancy</div>
    </div>

    <div class="card">
        <h2>System Alerts</h2>
        <div class="alert-box" id="alert_text">
            Waiting for sensor data...
        </div>
    </div>

</div>

<script>
async function updateDashboard() {
    try {
        const response = await fetch('/data');
        const data = await response.json();

        document.getElementById('occupancy').textContent = data.occupancy;
        document.getElementById('occupancy_status').textContent = data.occupancy_status;
        document.getElementById('temp_c').textContent = data.temp_c + " °C";
        document.getElementById('light_label').textContent = data.light_label;
        document.getElementById('light_status').textContent = data.light_status;
        document.getElementById('light_raw').textContent = data.light_raw;
        document.getElementById('heating_state').textContent = data.heating_state;
        document.getElementById('alert_text').textContent = data.alert_text;
    } catch (error) {
        console.log("Update failed:", error);
    }
}

updateDashboard();
setInterval(updateDashboard, 1000);
</script>

</body>
</html>
"""


# ---------------------------------------------------------
# Web server
# ---------------------------------------------------------
addr = socket.getaddrinfo("0.0.0.0", 80)[0][-1]
server = socket.socket()
server.bind(addr)
server.listen(1)

print("Server running.")
print("Connect your device to:", SSID)
print("Then open in browser:", ip)

while True:
    client, address = server.accept()
    print("Request received from", address)

    request = client.recv(1024)
    request_str = request.decode("utf-8")

    first_line = request_str.split("\r\n")[0]
    print("First line:", first_line)

    if "GET /data" in first_line:
        data = get_system_data()
        response_body = json.dumps(data)

        client.send("HTTP/1.1 200 OK\r\n")
        client.send("Content-Type: application/json\r\n")
        client.send("Cache-Control: no-cache\r\n")
        client.send("Connection: close\r\n\r\n")
        client.sendall(response_body.encode())

    else:
        html = build_html()
        client.send("HTTP/1.1 200 OK\r\n")
        client.send("Content-Type: text/html\r\n")
        client.send("Connection: close\r\n\r\n")
        client.sendall(html.encode())

    client.close()