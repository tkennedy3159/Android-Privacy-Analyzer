#!/usr/bin/python3

import AndroidDataPrivacy.Flow as Flow
import AndroidDataPrivacy.Result as Result
import AndroidDataPrivacy.AppFinder as AppFinder

import AndroidDataPrivacy.Applications.AppDefault as AppDefault
import AndroidDataPrivacy.Applications.AndroidNative as AndroidNative

filename = "startup.txt"
file = open(filename, "r")
capture = file.readlines()
flows = []
results = []
appList = ['AppDefault','AndroidNative']


def printFlows():
	counter = 0
	for flow in flows:
		print(counter)
		print(flow.all)
		print('')
		counter = counter + 1

def printFlow(num):
	print(flows[num].all)

def separateFlows():
	flow = ''
	for line in capture:
		if (line[0:1] == ' ' or line[1:2] == ''):
			flow = flow + line
		else:
			if (checkForUseless(flow)):
				flow = line
			else:
				flows.append(Flow.Flow(flow))
				flow = line

def checkForUseless(flow):
	if (flow[0:14] == 'Loading script' or \
		flow[0:22] == 'Proxy server listening' or \
		flow[0:9] == 'Traceback' or \
		flow[0:12] == 'Auto Content' or \
		flow[0:10] == 'ValueError' or \
		flow[0:15] == 'During handling' or \
		flow[0:18] == 'UnicodeDecodeError' or \
		flow[0:17] == 'Initiating HTTP/2' or \
		flow[0:flow.find('\n')].find('HEADERS frame suppressed') > -1 or \
		flow[0:flow.find('\n')].find('HTTP/2 PRIORITY frame suppressed') > -1 or \
		flow[0:flow.find('\n')].find('ALPN') > -1 or \
		flow[0:flow.find('\n')].find('HTTP2 Event') > -1 or \
		flow[0:flow.find('\n')].find('clientconnect') > -1 or \
		flow[0:flow.find('\n')].find('serverconnect') > -1 or \
		flow[0:flow.find('\n')].find('clientdisconnect') > -1 or \
		flow[0:flow.find('\n')].find('serverdisconnect') > -1 or \
		flow[flow.find('\n'):].find('-> Request') > -1 or \
		flow[flow.find('\n'):].find('-> Response') > -1 or \
		flow[0:flow.find('\n')].find('Set new server address:') > -1 or \
		flow[0:flow.find('\n')].find('Establish TLS') > -1 or \
		flow[0:flow.find('\n')].find('Connection killed') > -1 or \
		flow[0:flow.find('\n')].find('NotImplementedError') > -1):
		return True
	else:
		return False

def checkFlow(flow):
	flow.app = AppFinder.findApp(flow, appList)
	print('App: ' + flow.app)
	
	if (flow.app == 'AndroidNative' and 'AndroidNative' in appList):
		AndroidNative.checkBehavior(flow, results)
	if (flow.app == 'AppDefault' and 'AppDefault' in appList):
		AppDefault.checkBehavior(flow, results)

def sendLogs():
	print('\n')
	for result in results:
		print(result.log, end='\n\n')

def testFlow(num):
	print(flows[num].all)
	checkFlow(flows[num])
	sendLogs()

separateFlows()
#printFlows()
testFlow(35)