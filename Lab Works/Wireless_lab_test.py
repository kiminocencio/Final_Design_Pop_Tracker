#libraries
import network
import socket
import time  #note utime same as time

# access point details, change if u want different name
ssid= 'wireless_lab_test'
password= 'teamthermostat'

ap = network.WLAN(network.AP_IF)
ap.config(essid=ssid, password= password)
ap.active(False) #turns on/off accesspoint when true/false

while ap.active() == False:
    pass
print ('Connection is successful')
print(ap.ifconfig()) # print ip address of pico board

# create socket sercer
s= socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(('',80))
s.listen(5) # max num of requests that can be qued


def web_page():
    html = """
          <!DOCTYPE html>
          <html>
          <head>
          <style>

          h1{ color:red; postition:absolute; left: 100px; top:50px;}

          p{ color:blue; position: absolute; left: 25px; top:200px;}

          </head>
          </style>



          <body>
          <h1>Welcome</h1>
          <p>ENGR 120 Lab</p>
          </body>
          </html>




           """
    return html


while True:
    conn, addr= s.accept()
    print('Got a connection from %s' % str(addr))
    request = conn.recv(1024)
    response = web_page() # indicate when response connection was recieved
    conn.send("HTTP/1.1 200 OK\n")
    conn.send("Content-Type: text/html\n")
    conn.send("Connection: close\n\n")
    conn.sendall(response)
    conn.close()
