import requests
import json
import argparse
import time
import threading
import logging
import time
import math
import os.path
from os import path
from datetime import datetime
now = datetime.now()
current_time = now.strftime("%H:%M:%S")
print("Started Overall at ", current_time)
epoch = datetime.utcfromtimestamp(0)

def week(dt):
    return math.floor((dt - epoch).total_seconds() * 1000.0)-604800000

uIdStore=list()

with open("uIdSearch.dat", "r") as file:
# with open("filters/filter100.dat", "r") as file:
	for line in file:
		currentPlace=line[:-1]
		if not currentPlace in uIdStore:
			uIdStore.append(currentPlace)

baseURL="https://g9b1fyald3.execute-api.eu-west-1.amazonaws.com/master"

result=list()
bad=list()

for uid in uIdStore:
	requestURL=baseURL+"/scores?userId="+uid
	try:
		request = requests.get(requestURL).text
		jsonResponse = json.loads(request)
		data = jsonResponse['result']['Items'][0]['timestamp']
		result.append(str(uid)+"|"+str(data)+"|"+str(jsonResponse['result']['Count']))
	except:
		bad.append(uid)

with open("retention.dat", "w") as file:
	for item in result:
		file.write('%s\n' % item)

with open("bad.dat", "w") as file:
	for item in bad:
		file.write('%s\n' % item)


g=0
b=0

with open("retention.dat", "r") as file:
	for line in file:
		currentPlace=line[:-1]
		x = currentPlace.split("|")
		curTime=week(datetime.now())
		if int(x[1]) >= curTime and int(x[2]) >=10:
			g+=1
		else:
			b+=1

print("Retained: "+str(g))
print("Not Retained: "+str(b)) 

now = datetime.now()
current_time = now.strftime("%H:%M:%S")
print("Finished Overall at ", current_time)