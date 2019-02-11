#!/usr/bin/env python3
# author: Radoslav Grencik <xgrenc00@stud.fit.vutbr.cz>

################################################################################

import sys
import socket
import json

if len(sys.argv) != 3:
    print("Err: bad args.", file = sys.stderr)
    sys.exit(1)

appid = sys.argv[1]
loc = sys.argv[2]

host = "api.openweathermap.org"
resource = "/data/2.5/weather?q=" + loc + "&APPID=" + appid +"&units=metric"

req = bytes("GET " + resource + " HTTP/1.1\n" + "Host: " + host + "\r\n\r\n", "utf-8") # HTTP request

soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # AF_INET => type of connection, SOCK_STREAM => tcp
soc.connect((host, 80)) # HTTP port = 80
soc.send(req)
result = soc.recv(2048) # size of buffer = 2048
soc.close()

result = str(result, "utf-8")
wind = result.find("deg")

check = result.split("\r\n")[0]
if check != "HTTP/1.1 200 OK":
    print("Err: bad response.", file = sys.stderr)
    sys.exit(1)

result = result.split("\r\n\r\n")[1]
jres = json.loads(result)

if wind == -1:
    jres["wind"]["deg"] = "-"

print(
"""{0}
{1}
temp:       {2} °C
humidity:   {3} %
pressure:   {4} hPa
wind-speed: {5} m/s
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
