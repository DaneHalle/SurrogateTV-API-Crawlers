import requests
import json
import time
import logging
import os.path
from os import path
from datetime import datetime

baseURL="Not going to be that easy"
uuid = "Game UUID"
inGameURL = baseURL + "/games/" + uuid + "/ingameGamestate"

inGame = False

while True:	
	request = requests.get(inGameURL).text
	toJson = json.loads(request)

	topData = toJson['result'][0]
	payload = topData['payload']
	if payload['state'] == "endGame":
		inGame = False
	elif not inGame:
		inGame = True
		now = datetime.now()
		current_time = now.strftime("%H:%M:%S")
		print(str(current_time) + "\t|\t" + str(payload['gameSpecificState']['players']))
