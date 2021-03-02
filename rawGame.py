import requests
import json
import sys

baseURL="Not going to be that easy"

shortIdResult=[]
with open("shortId.dat", "r") as file:
	for line in file:
		currentPlace=line[:-1]
		if not currentPlace in shortIdResult:
			shortIdResult.append(currentPlace)

categoryURL=baseURL+"/categories"
categoryResponse=requests.get(categoryURL).text
catDat=json.loads(categoryResponse)['result']
for catId in catDat:
	try:
		shortData=catId['categoryId']
		categoryURL=baseURL+"/games/ids?category="+shortData
		categoryResponse=requests.get(categoryURL).text
		categoryData=json.loads(categoryResponse)
		for gameId in categoryData['result']:
			gameURL=baseURL+"/games/"+gameId
			gameResposne=requests.get(gameURL).text
			gameData=json.loads(gameResposne)['result']['shortId']
			if not gameData in shortIdResult:
				print("Found "+gameData)
				print("\t"+baseURL+"/games/"+gameId)
	except KeyboardInterrupt:
		sys.exit()
	except:
		a=1