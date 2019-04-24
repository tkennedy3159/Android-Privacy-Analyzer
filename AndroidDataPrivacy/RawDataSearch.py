#!/usr/bin/python3

import AndroidDataPrivacy.Flow as Flow
import AndroidDataPrivacy.Result as Result

filename = 'searchitems.txt'
ignoredInfos = ['test', \
'WiFi connection active']

ignoredTypes = ['System Info: Performance Tracking', \
'User Info: Opened App Count', \
'System Info: Android Version', \
'Location: WiFi Access Points', \
'Location: Cell Towers' \
'User Info: Calendar Events', \
'Slack Channel Info', \
'User Info: Notification Settings', \
'System Info: Cookie', \
'User Action', \
'User Action: Youtube', \
'User Action: Youtube Browsing', \
'User Action: App Installation Time', \
'Youtube Playlist', \
'User Action: Add Video to Playlist', \
'User Action: Create Playlist', \
'Youtube Video Status', \
'Youtube Search Suggestion', \
'User Action: Search Query', \
'User Action: Discord', \
'User Action: Discord User Search', \
'User Action: View Discord User Profile', \
'Messsage', \
'Reddit Activity & Info Dump', \
'User Action: Input Field', \
'User Info: Youtube Screen Opened', \
'Event Time', \
'Spotify Event', \
'User Info: 2FA Device', \
'LinkedIn Client Event', \
'LinkedIn Client Event Stats', \
'User Info: Contact', \
'User Info: Calendar Events', \
'LinkedIn Tracking Token', \
'System Info: LinkedIn App State', \
'System Info: Battery Level']

def checkRawData(flow, results):
	file = open(filename, "r")
	itemsList = file.readlines()
	file.close()
	items = separateSearchItems(itemsList)

	addNewResults(results, items)
	searchFlow(flow, results, items)

def searchFlow(flow, results, items):
	infos = []
	content = flow.all

	for result in results:
		infos.append(result.info)

	while len(content) > 1:
		for key, value in items.items():
			if (content[0:len(key)] == key and key not in infos):
				type = value + ' (RAWDATASEARCH)'
				info = key
				results.append(Result.Result(flow, type, info))
				infos.append(key)
		content = content[1:]

def addNewResults(results, items):
	file = open(filename, "w")
	for key, value in items.items():
		file.write(key + '\n' + '----' + '\n' + value + '\n' + '---------------' + '\n')

	for result in results:
		if len(result.info) > 3 and result.info not in items.keys() and result.info not in ignoredInfos and result.type.find('User Action') == -1 and result.type not in ignoredTypes:
			items[result.info] = result.type
			file.write(result.info + '\n' + '----' + '\n' + result.type + '\n' + '---------------' + '\n')

	file.close()

def separateSearchItems(itemsList):
	items = {}
	temp = ''
	for line in itemsList:
		if (line.strip() == '---------------'):
			items[temp.split('----')[0].strip()] = temp.split('----')[1].strip()
			temp = ''
		else:
			temp = temp + line
	return items