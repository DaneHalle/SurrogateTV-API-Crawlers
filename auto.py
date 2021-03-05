import requests
import json
import argparse
import time
import threading
import logging
import math
import os.path
from os import path
from datetime import datetime
now = datetime.now()
current_time = now.strftime("%H:%M:%S")
print("Started Overall at ", current_time)
parser = argparse.ArgumentParser()
parser.add_argument('-w', '--web', help='Start a webCrawl on the known User IDs',
                    action='store_true')
parser.add_argument('-n', '--name', help='Add a username to the list',
                    type=str)
parser.add_argument('-l', '--loop', help='Loop over known games to get more usernames for given minutes. Default=1',
                    type=int, default=1)
parser.add_argument('-t', '--thread', help='Number of threads to run',
					type=int, default=150)
args = parser.parse_args()

WEBCRAWL = args.web
NAMES = args.name
LOOP = args.loop
THREAD = args.thread

baseURL="https://g9b1fyald3.execute-api.eu-west-1.amazonaws.com/master"

toCheck=[]
uIdStore=[]
shortIdResult=[]

if not path.exists("uIdSearch.dat"):
	open("uIdSearch.dat", "w")
if not path.exists("shortId.dat"):
	open("shortId.dat", "w")


with open("uIdSearch.dat", "r") as file:
	for line in file:
		currentPlace=line[:-1]
		if not currentPlace in uIdStore:
			uIdStore.append(currentPlace)

with open("shortId.dat", "r") as file:
	for line in file:
		currentPlace=line[:-1]
		if not currentPlace in shortIdResult:
			shortIdResult.append(currentPlace)

shortIdResult.sort()
uIdStore.sort()

def webCrawl(lower=0, upper=len(uIdStore)):
	print("Checking range "+str(lower)+" - "+str(upper))
	for uId in range(lower, upper):
		requestURL=baseURL+"/scores?userId="+uIdStore[uId]+"&order=bestPointsPerGame&limit=50"
		try:
			response=requests.get(requestURL).text
			data=json.loads(response)
		except:
			print("Issue with "+uIdStore[uId])
			continue
		for score in data['result']['Items']:
			try:
				shortIdRes=score['gameObject']['shortId']
				if not shortIdRes in shortIdResult:
					print("Found "+shortIdRes+" from "+score['userObject']['username'])
					shortIdResult.append(shortIdRes)
				shortURL=baseURL+"/games/?shortId="+shortIdRes
				shortResponse=requests.get(shortURL).text
				shortUUID=json.loads(shortResponse)['result']['uuid']
				newUsersURL=baseURL+"/scores?gameId="+shortUUID+"&order=&limit=50"
				newResponse=requests.get(newUsersURL).text
				newData=json.loads(newResponse)
			except:
				print("Issue with "+shortIdRes)
				continue
			for new in newData['result']['Items']:
				if not new['userId'] in uIdStore:
					print("Added "+new['userObject']['username']+" from "+shortIdRes)
					uIdStore.append(new['userId'])
			inGameURL=baseURL+"/games/"+shortUUID+"/ingameGamestate"
			try:
				inGameResponse=requests.get(inGameURL).text
			except:
				print("Issue with "+shortIdRes)
				continue
			try:
				inGameData=json.loads(inGameResponse)['result'][0]['payload']['gameSpecificState']['players']
				for payload in inGameData:
					payloadUserURL=baseURL+"/users?search="+payload['username']
					payloadResponse=requests.get(payloadUserURL).text
					payloadData=json.loads(payloadResponse)['result'][0]['userId']
					if not payloadData in uIdStore:
						print("Added "+payload['username']+" from inGameState of "+shortIdRes)
						uIdStore.append(payloadData)
			except:
					a=0
		recentURL=baseURL+"/scores?userId="+uIdStore[uId]+"&order=&limit=50"
		try:
			recentResponse=requests.get(recentURL).text
			recentData=json.loads(recentResponse)['result']['Items']
		except:
			a=0
		for recent in recentData:
			shortIdRes=recent['gameObject']['shortId']
			if not shortIdRes in shortIdResult:
				print("Found "+shortIdRes+" from "+recent['userObject']['username'])
				shortIdResult.append(shortIdRes)
				shortURL=baseURL+"/games/?shortId="+shortIdRes
				shortResponse=requests.get(shortURL).text
				shortUUID=json.loads(shortResponse)['result']['uuid']
				newUsersURL=baseURL+"/scores?gameId="+shortUUID+"&order=&limit=50"
				newResponse=requests.get(newUsersURL).text
				newData=json.loads(newResponse)
				for new in newData['result']['Items']:
					if not new['userId'] in uIdStore:
						print("Added "+new['userObject']['username']+" from "+shortIdRes)
						uIdStore.append(new['userId'])
				inGameURL=baseURL+"/games/"+shortUUID+"/ingameGamestate"
				inGameResponse=requests.get(inGameURL).text
				try:
					inGameData=json.loads(inGameResponse)['result'][0]['payload']['gameSpecificState']['players']
					for payload in inGameData:
						payloadUserURL=baseURL+"/users?search="+payload['username']
						payloadResponse=requests.get(payloadUserURL).text
						payloadData=json.loads(payloadResponse)['result'][0]['userId']
						if not payloadData in uIdStore:
							print("Added "+payload['username']+" from inGameState of "+shortIdRes)
							uIdStore.append(payloadData)
				except:
					a=0



def nameCrawl():
	for name in toCheck:
		requestURL=baseURL+"/users?search="+name
		response=requests.get(requestURL).text
		data=json.loads(response)
		try:
			if not data['result'][0]['userId'] in uIdStore:
				print("Added "+name)
				uIdStore.append(data['result'][0]['userId'])
				with open("uIdSearch.dat", "w") as file:
					for item in uIdStore:
						file.write('%s\n' % item)
		except:
			a=0

def loopCrawl():
	print(shortIdResult)
	t_end = time.time()+LOOP*60
	while time.time()<t_end:
		for short in shortIdResult:
			shortURL=baseURL+"/games/?shortId="+short
			shortResponse=requests.get(shortURL).text
			try:
				shortUUID=json.loads(shortResponse)['result']['uuid']
				inGameURL=baseURL+"/games/"+shortUUID+"/ingameGamestate"
				leaderboardURL=baseURL+"/scores?gameId="+shortUUID+"&order=&limit=50"
				inGameResponse=requests.get(inGameURL).text
				leaderboardResponse=requests.get(leaderboardURL).text
			except:
				a=0
			try:
				inGameData=json.loads(inGameResponse)['result'][0]['payload']['gameSpecificState']['players']
				for payload in inGameData:
					payloadUserURL=baseURL+"/users?search="+payload['username']
					payloadResponse=requests.get(payloadUserURL).text
					payloadData=json.loads(payloadResponse)['result'][0]['userId']
					if not payloadData in uIdStore:
						print("Added "+payload['username']+" from "+short)
						uIdStore.append(payloadData)
						with open("uIdSearch.dat", "w") as file:
							for item in uIdStore:
								file.write('%s\n' % item)
						with open("New Players.txt", "a") as file:
							item = "Added "+payload['username']+" from "+short
							file.write('%s\n' % item)
				leaderboardData=json.loads(leaderboardResponse)['result']['Items']
				for player in leaderboardData:
					if not player['userObject']['userId'] in uIdStore:
						print("Added "+player['userObject']['username']+" from leaderboard of "+short)
						uIdStore.append(player['userObject']['userId'])
						with open("uIdSearch.dat", "w") as file:
							for item in uIdStore:
								file.write('%s\n' % item)		
						with open("New Players.txt", "a") as file:
							item = "Added "+player['userObject']['username']+" from leaderboard of "+short
							file.write('%s\n' % item)
			except:
				a=0
		time.sleep(12)

def creatorCrawl(lower=0, upper=len(uIdStore)):
	for uId in range(lower, upper):
		creatorURL=baseURL+"/games/ids?creatorId="+uIdStore[uId]
		creatorResponse=requests.get(creatorURL).text
		creatorData=json.loads(creatorResponse)['result']
		for gameId in creatorData:
			gameURL=baseURL+"/games/"+gameId
			gameResposne=requests.get(gameURL).text
			gameData=json.loads(gameResposne)['result']
			if not gameData['shortId'] in shortIdResult:
				print("Found "+gameData['shortId']+" from creator "+gameData['userObject']['username'])
				shortIdResult.append(gameData['shortId'])
				with open("shortId.dat", "w") as file:
					for item in shortIdResult:
						file.write('%s\n' % item)

def categoryCrawl():
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
				if not gameData in shortIdResult and ":" not in gameData:
					print("Found "+gameData)
					shortIdResult.append(gameData)
					with open("shortId.dat", "w") as file:
						for item in shortIdResult:
							file.write('%s\n' % item)
		except:
			a=1

def confirmCreator():
	for sId in shortIdResult:
		time.sleep(1)
		try:
			URL=baseURL+"/games/?shortId="+sId
			request=requests.get(URL).text
			data=json.loads(request)['result']['userObject']
			if not data['userId'] in uIdStore:
				print("Added "+data['username']+" from "+sId)
				uIdStore.append(data['userId'])
				with open("uIdSearch.dat", "w") as file:
					for item in uIdStore:
						file.write('%s\n' % item)
		except:
			print("Issue with "+sId)
	
if(NAMES):
	now = datetime.now()
	current_time = now.strftime("%H:%M:%S")
	print("Checking Usernames at ", current_time)
	toCheck.extend(NAMES.split("|"))
	nameCrawl()
	now = datetime.now()
	current_time = now.strftime("%H:%M:%S")
	print("Finished Checking Usernames at ", current_time)

if(WEBCRAWL):
	now = datetime.now()
	current_time = now.strftime("%H:%M:%S")
	print("Checking User IDs at ", current_time)
	threads=list()
	amountPer=math.floor(len(uIdStore)/(THREAD))+1
	highest=0
	for i in range(THREAD):
		logging.info("Main	: create and start thread %d", i)
		lower=i*amountPer
		upper=(i+1)*amountPer
		if i!=0:
			lower+=1
		if lower >= len(uIdStore):
			continue
		if upper >= len(uIdStore):
			upper=len(uIdStore)
		highest=upper
		x=threading.Thread(target=webCrawl, args=(lower, upper,))
		threads.append(x)
		x.start()
	for a, thread in enumerate(threads):
		logging.info("Main 	: before joining thread %d", a)
		thread.join()
		logging.info("Main 	: thread %d done", a)
	print("Finished main threads")
	if highest+1 < len(uIdStore):
		webCrawl(highest+1, len(uIdStore))

	with open("shortId.dat", "w") as file:
		for item in shortIdResult:
			file.write('%s\n' % item)

	with open("uIdSearch.dat", "w") as file:
		for item in uIdStore:
			file.write('%s\n' % item)

	now = datetime.now()
	current_time = now.strftime("%H:%M:%S")
	print("Finished Checking User IDs at ", current_time)

if(LOOP):
	now = datetime.now()
	current_time = now.strftime("%H:%M:%S")
	print("Crawling through games at ", current_time)
	loopCrawl()
	now = datetime.now()
	current_time = now.strftime("%H:%M:%S")
	print("Finished Crawling through games at ", current_time)

time.sleep(5)

now = datetime.now()
current_time = now.strftime("%H:%M:%S")
print("Crawling for Game Creators at ", current_time)
cThreads=list()
cAmountPer=math.floor(len(uIdStore)/THREAD)+1
cHighest=0
for z in range(THREAD):
	logging.info("Main 	: create and start thread %d", z)
	cLower=z*cAmountPer
	cUpper=(z+1)*cAmountPer
	if z != 0:
		cLower+=1
	if cLower >= len(uIdStore):
		continue
	if cUpper >= len(uIdStore):
		cUpper=len(uIdStore)
	cHighest=cUpper
	c=threading.Thread(target=creatorCrawl, args=(cLower, cUpper,))
	cThreads.append(c)
	c.start()
for q, thread in enumerate(cThreads):
	logging.info("Main 	: before joining thread %d", q)
	thread.join()
	logging.info("Main 	: thread %d done", q)
print("Finished main threads")
if cHighest+1 < len(uIdStore):
	creatorCrawl(cHighest+1, len(uIdStore))
now = datetime.now()
current_time = now.strftime("%H:%M:%S")
print("Finished Crawling for Game Creators at ", current_time)

time.sleep(5)

now = datetime.now()
current_time = now.strftime("%H:%M:%S")
print("Crawling for Category Games at ", current_time)
categoryCrawl()
now = datetime.now()
current_time = now.strftime("%H:%M:%S")
print("Finished Crawling for Category Games at ", current_time)

# time.sleep(5)

# now = datetime.now()
# current_time = now.strftime("%H:%M:%S")
# print("Confirming Creators of Games at ", current_time)
# confirmCreator()
# now = datetime.now()
# current_time = now.strftime("%H:%M:%S")
# print("Finished Confirming Creators of Games at ", current_time)

shortIdResult.sort()
uIdStore.sort()

with open("shortId.dat", "w") as file:
	for item in shortIdResult:
		file.write('%s\n' % item)

with open("uIdSearch.dat", "w") as file:
	for item in uIdStore:
		file.write('%s\n' % item)

now = datetime.now()
current_time = now.strftime("%H:%M:%S")
print("Finished Overall at ", current_time)