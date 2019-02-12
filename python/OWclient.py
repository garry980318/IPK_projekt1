#!/usr/bin/env python3
# author: Radoslav Grencik <xgrenc00@stud.fit.vutbr.cz>

################################################################################

import sys
import socket
import json
import time

if len(sys.argv) != 3:
    print("ERROR: bad args.", file = sys.stderr)
    sys.exit(1)

appid = sys.argv[1]
loc = sys.argv[2]

host = "api.openweathermap.org"
resource = "/data/2.5/weather?q=" + loc + "&APPID=" + appid +"&units=metric"

req = bytes("GET " + resource + " HTTP/1.1\n" + "Host: " + host + "\r\n\r\n", "utf-8") # HTTP request

soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # adress (and protocol) family = AF_INET, socket type = SOCK_STREAM
soc.connect((host, 80)) # HTTP port = 80
soc.send(req)
result = soc.recv(4096) # size of buffer shoul be a small power of 2 = 4096
soc.close()

result = str(result, "utf-8")

check = result.split(" ")[1]
if check != "200":
    print("ERROR: {0}.".format(check), file = sys.stderr)
    sys.exit(1)

result = result.split("\r\n\r\n")[1]
jres = json.loads(result)

if ("deg" in result) == False:
    jres["wind"]["deg"] = "-"

sunrise = time.ctime(jres["sys"]["sunrise"]).split(" ")[3]
sunset = time.ctime(jres["sys"]["sunset"]).split(" ")[3]

print(
"""Weather in {0}, {7}
{1}
temp:       {2} °C
pressure:   {4} hPa
humidity:   {3} %
visibility: {8} m
wind-speed: {5} m/s
wind-deg:   {6}
cloudiness: {9} %
sunrise:    {10}
sunset:     {11}"""
.format(
jres["name"], jres["weather"][0]["description"], jres["main"]["temp"],
jres["main"]["humidity"], jres["main"]["pressure"], jres["wind"]["speed"],
jres["wind"]["deg"], jres["sys"]["country"], jres["visibility"],
jres["clouds"]["all"], sunrise, sunset
))
