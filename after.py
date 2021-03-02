import json
import requests
import time
import sys

baseURL="Not going to be that easy"

shortIdResult=[]
with open("shortId.dat", "r") as file:
	for line in file:
		currentPlace=line[:-1]
		if not currentPlace in shortIdResult:
			shortIdResult.append(currentPlace)

with open("gameIdShort.dat", "w") as file:
	for shortGameId in shortIdResult:
		try:
			time.sleep(2)
			gameUUIDrequest = requests.get(baseURL+"/games/?shortId="+str(shortGameId)).text
			gameUUID = json.loads(gameUUIDrequest)['result']['uuid']
			toFile = gameUUID+"|"+shortGameId.replace("/", "_").replace(".", "_").replace("\\", "_").replace(" ", "_")
			file.write('%s\n' % toFile)
		except KeyboardInterrupt:
			sys.exit()
		except:
			print(shortGameId)