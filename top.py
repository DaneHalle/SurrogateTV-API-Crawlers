import requests
import json
from datetime import datetime
now = datetime.now()
current_time = now.strftime("%H:%M:%S")
print("Started at ", current_time)

def takeSecond(elem):
    return elem[1]

userId=list()
with open("uIdSearch.dat", "r") as file:
	for line in file:
		currentPlace=line[:-1]
		userId.append(currentPlace)

bigBoiList=list()
baseURL="Not going to be that easy"

for obj in userId:
	url=baseUrl+obj
	request=requests.get(url).text
	jsonRequest=json.loads(request)
	try:
		data=jsonRequest['result']
	except:
		print("Issue with "+str(obj))
		continue
	try:
		bigBoiList.append([data['username'], data['experience']])
	except:
		bigBoiList.append([data['username'], 0])

bigBoiList.sort(key=takeSecond, reverse=True)

for i in range(len(bigBoiList)):
	print(str((i+1))+")\t"+bigBoiList[i][0]+"\t|\t"+str(bigBoiList[i][1]))


now = datetime.now()
current_time = now.strftime("%H:%M:%S")
print("Ended at ", current_time)