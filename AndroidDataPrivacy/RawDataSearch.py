#!/usr/bin/python3

import AndroidDataPrivacy.Flow as Flow
import AndroidDataPrivacy.Result as Result

def searchFlow(flow, results):
	filename = "searchitems.txt"
	file = open(filename, "r")
	itemsList = file.readlines()
	file.close()
	items = {}
	infos = []
	content = flow.all

	for line in itemsList:
		line = line.strip()
		if (len(line) > 5):
			items[line.split(':::::')[0]] = line.split(':::::')[1]

	for result in results:
		infos.append(result.info)

	while len(content) > 1:
		for key, value in items.items():
			if (content[0:len(key)] == key and key not in infos):
				type = 'RAWDATASEARCH: ' + value
				info = key
				results.append(Result.Result(flow, type, info))
				infos.append(key)
		content = content[1:]

def addNewResults(results):
	filename = "searchitems.txt"
	file = open(filename, "r")
	itemsList = file.readlines()
	file.close()
	items = {}
	for line in itemsList:
		line = line.strip()
		if (len(line) > 5):
			items[line.split(':::::')[0]] = line.split(':::::')[1]

	file = open(filename, "w")
	for key, value in items.items():
		file.write(key + ':::::' + value + '\n')

	for result in results:
		if result.info not in items.keys():
			items[result.info] = result.type
			file.write(result.info + ':::::' + result.type + '\n')

	file.close()