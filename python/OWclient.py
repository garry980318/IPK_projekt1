#!/usr/bin/env python3
# author: Radoslav Grencik <xgrenc00@stud.fit.vutbr.cz>

################################################################################

import sys
import socket
import json
import time
import re

def Err(retval, msg):
    print("ERROR: {0}.".format(msg), file = sys.stderr)
    sys.exit(retval)
    
if len(sys.argv) != 3:
    Err(1, "bad args")

appid = sys.argv[1]
loc = sys.argv[2]

host = "api.openweathermap.org"
resource = "/data/2.5/weather?q=" + loc + "&APPID=" + appid +"&units=metric"

req = bytes("GET " + resource + " HTTP/1.1\r\n" + "Host: " + host + "\r\n\r\n", "utf-8") # HTTP request

soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # adress (and protocol) family = AF_INET, socket type = SOCK_STREAM
try:
    soc.connect((host, 80)) # HTTP port = 80
except:
    Err(1, "can't connect")

soc.send(req)
result = soc.recv(4096) # size of buffer shoul be a small power of 2 = 4096
soc.close()

result = str(result, "utf-8")

check = result.split(" ")[1]
if check != "200":
    Err(check, check)

result = result.split("\r\n\r\n")[1]
jres = json.loads(result)

if ("deg" in result) == False:
    jres["wind"]["deg"] = "-"

sunrise = re.search("(0[0-9]|1[0-9]|2[0-3]):[0-5][0-9]:[0-5][0-9]", time.ctime(jres["sys"]["sunrise"])).group()
sunset = re.search("(0[0-9]|1[0-9]|2[0-3]):[0-5][0-9]:[0-5][0-9]", time.ctime(jres["sys"]["sunset"])).group()

print(
"""Weather in {0}, {1}
{2}
temp:       {3} °C
pressure:   {4} hPa
humidity:   {5} %
visibility: {6} m
wind-speed: {7} m/s
wind-deg:   {8}
cloudiness: {9} %
sunrise:    {10}
sunset:     {11}"""
.format(
jres["name"],
jres["sys"]["country"],
jres["weather"][0]["description"],
jres["main"]["temp"],
jres["main"]["pressure"],
jres["main"]["humidity"],
jres["visibility"],
jres["wind"]["speed"],
jres["wind"]["deg"],
jres["clouds"]["all"],
sunrise,
sunset
))
