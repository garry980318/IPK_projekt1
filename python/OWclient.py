#!/usr/bin/env python3
# author: Radoslav Grencik <xgrenc00@stud.fit.vutbr.cz>

################################################################################

import sys
import socket
import json

if len(sys.argv) != 3:
    print("Err: bad args.")
    sys.exit(1)

appid = sys.argv[1]
loc = sys.argv[2]

host = "api.openweathermap.org"
resource = "/data/2.5/weather?q=" + loc + "&APPID=" + appid +"&units=metric"

req = bytes("GET " + resource + " HTTP/1.1\n" + "Host: " + host + "\r\n\r\n", "utf-8")

soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
soc.connect((host, 80))
soc.send(req)
result = soc.recv(10000)
soc.close()

result = str(result, "utf-8")

check = result.split("\r\n")[0]
if check != "HTTP/1.1 200 OK":
    print("Err: bad response.")
    sys.exit(1)

result = result.split("\r\n\r\n")[1]
jres = json.loads(result)

print(
"""{0}
overcast:   {1}
temp:       {2} °C
humidity:   {3} %
pressure:   {4} hPa
wind-speed: {5} km/h
wind-deg:   {6}"""
.format(
jres["name"],
jres["weather"][0]["description"],
jres["main"]["temp"],
jres["main"]["humidity"],
jres["main"]["pressure"],
jres["wind"]["speed"],
jres["wind"]["deg"]
))
