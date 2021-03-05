import requests
import json
from difflib import SequenceMatcher
import sys

uIdStore=list()
nameAlt100 = list()
name100 = list()
nameAlt90 = list()
name90 = list()
nameAlt80 = list()
name80 = list()
nameAlt70 = list()
name70 = list()
nameAlt60 = list()
name60 = list()
nameAlt50 = list()
name50 = list()
nameAlt40 = list()
name40 = list()
nameAlt30 = list()
name30 = list()
nameAlt20 = list()
name20 = list()
nameAlt10 = list()
name10 = list()
baseURL="https://g9b1fyald3.execute-api.eu-west-1.amazonaws.com/master"

with open("uIdSearch.dat", "r") as file:
	for line in file:
		currentPlace=line[:-1]
		if not currentPlace in uIdStore:
			uIdStore.append(currentPlace)

ct = 0
for i in uIdStore:
	requestURL=baseURL+"/users/"+i
	try:
		request = requests.get(requestURL).text
		jsonResponse = json.loads(request)['result']['username']
		lowName = jsonResponse
		if lowName not in nameAlt100:
			flag = True
			for z in nameAlt100:
				if SequenceMatcher(None, lowName, z).ratio() >= 1.00:
					flag = False
					break
			if flag:
				nameAlt100.append(lowName)
				name100.append(i)
		if lowName not in nameAlt90:
			flag = True
			for z in nameAlt90:
				if SequenceMatcher(None, lowName, z).ratio() >= 0.9:
					flag = False
					break
			if flag:
				nameAlt90.append(lowName)
				name90.append(i)
		if lowName not in nameAlt80:
			flag = True
			for z in nameAlt80:
				if SequenceMatcher(None, lowName, z).ratio() >= 0.8:
					flag = False
					break
			if flag:
				nameAlt80.append(lowName)
				name80.append(i)
		if lowName not in nameAlt70:
			flag = True
			for z in nameAlt70:
				if SequenceMatcher(None, lowName, z).ratio() >= 0.7:
					flag = False
					break
			if flag:
				nameAlt70.append(lowName)
				name70.append(i)
		if lowName not in nameAlt60:
			flag = True
			for z in nameAlt60:
				if SequenceMatcher(None, lowName, z).ratio() >= 0.6:
					flag = False
					break
			if flag:
				nameAlt60.append(lowName)
				name60.append(i)
		if lowName not in nameAlt50:
			flag = True
			for z in nameAlt50:
				if SequenceMatcher(None, lowName, z).ratio() >= 0.5:
					flag = False
					break
			if flag:
				nameAlt50.append(lowName)
				name50.append(i)
		if lowName not in nameAlt40:
			flag = True
			for z in nameAlt40:
				if SequenceMatcher(None, lowName, z).ratio() >= 0.4:
					flag = False
					break
			if flag:
				nameAlt40.append(lowName)
				name40.append(i)
		if lowName not in nameAlt30:
			flag = True
			for z in nameAlt30:
				if SequenceMatcher(None, lowName, z).ratio() >= 0.3:
					flag = False
					break
			if flag:
				nameAlt30.append(lowName)
				name30.append(i)
		if lowName not in nameAlt20:
			flag = True
			for z in nameAlt20:
				if SequenceMatcher(None, lowName, z).ratio() >= 0.2:
					flag = False
					break
			if flag:
				nameAlt20.append(lowName)
				name20.append(i)
		if lowName not in nameAlt10:
			flag = True
			for z in nameAlt10:
				if SequenceMatcher(None, lowName, z).ratio() >= 0.1:
					flag = False
					break
			if flag:
				nameAlt10.append(lowName)
				name10.append(i)
	except KeyboardInterrupt:
		sys.exit()
	except:
		a=1
	ct += 1
	if ct%100 == 0 and ct != 0:
		print(ct)

with open("./filters/filter100.dat", "w") as file:
	for item in name100:
		file.write('%s\n' % item)

with open("./filters/filter90.dat", "w") as file:
	for item in name90:
		file.write('%s\n' % item)

with open("./filters/filter80.dat", "w") as file:
	for item in name80:
		file.write('%s\n' % item)

with open("./filters/filter70.dat", "w") as file:
	for item in name70:
		file.write('%s\n' % item)

with open("./filters/filter60.dat", "w") as file:
	for item in name60:
		file.write('%s\n' % item)

with open("./filters/filter50.dat", "w") as file:
	for item in name50:
		file.write('%s\n' % item)

with open("./filters/filter40.dat", "w") as file:
	for item in name40:
		file.write('%s\n' % item)

with open("./filters/filter30.dat", "w") as file:
	for item in name30:
		file.write('%s\n' % item)

with open("./filters/filter20.dat", "w") as file:
	for item in name20:
		file.write('%s\n' % item)

with open("./filters/filter10.dat", "w") as file:
	for item in name10:
		file.write('%s\n' % item)