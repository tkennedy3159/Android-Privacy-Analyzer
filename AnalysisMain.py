#!/usr/bin/python3

import AndroidDataPrivacy.syslog_client as syslog_client

import AndroidDataPrivacy.Flow as Flow
import AndroidDataPrivacy.Result as Result
import AndroidDataPrivacy.AppFinder as AppFinder

import AndroidDataPrivacy.Applications.AppDefault as AppDefault
import AndroidDataPrivacy.Applications.AndroidNative as AndroidNative
import AndroidDataPrivacy.Applications.GSuite as GSuite
import AndroidDataPrivacy.Applications.Youtube as Youtube
import AndroidDataPrivacy.Applications.Reddit as Reddit
import AndroidDataPrivacy.Applications.CertInstaller as CertInstaller

testNum = 3
filename = "backup.txt"
file = open(filename, "r")
newFlowFileName = 'newflows.txt'
capture = file.readlines()
flows = []
results = []
appList = ['AppDefault','AndroidNative','GSuite','Youtube', 'Reddit', 'CertInstaller']
log = syslog_client.Syslog()

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
	count = 0
	for line in capture:
		if (count > 0):
			flow = flow + line
			count = count - 1
		elif (line[0:1] == ' ' or line[1:2] == '' or line[0:6] == '<0x00>' or line[:21] == 'cd=com.google.android'):
			flow = flow + line
		elif (line[0:15] == 'generic profile'):
			flow = flow + line
			count = 2
		else:
			if (checkForUseless(flow)):
				flow = line
			else:
				flows.append(Flow.Flow(flow))
				flow = line
	if (len(flow.strip()) > 1 and checkForUseless(flow) == False):
		flows.append(Flow.Flow(flow))

def checkForUseless(flow):
	if (flow[0:14] == 'Loading script' or \
		flow[0:22] == 'Proxy server listening' or \
		flow[0:9] == 'Traceback' or \
		flow[0:1] == '<' or \
		flow[0:12] == 'Auto Content' or \
		flow[0:10] == 'ValueError' or \
		flow[0:15] == 'During handling' or \
		flow[0:18] == 'UnicodeDecodeError' or \
		flow[0:17] == 'Initiating HTTP/2' or \
		flow[0:19] == 'EOFError: requested' or \
		flow[0:54] == 'TypeError: don\'t know how to handle UnicodeDecodeError' or \
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
		flow[0:flow.find('\n')].find(': HTTP/2 connection terminated by server: error code:') > -1 or \
		flow[0:flow.find('\n')].find('Establish TLS') > -1 or \
		flow[0:].find('Cannot establish TLS with client') > -1 or \
		flow[0:flow.find('\n')].find('server communication error:') > -1 or \
		flow[0:flow.find('\n')].find('Connection killed') > -1 or \
		flow[0:flow.find('\n')].find('NotImplementedError') > -1):
		return True
	else:
		return False

def findNewFlows():
	newFlowFile = open(newFlowFileName, "w")
	newFlows = []
	analyzeAll()
	for flow in flows:
		if (flow.source == '' \
		or flow.source == 'App Measurement' \
		or flow.url == 'https://play.googleapis.com/log/batch'):
			if (flow.all.find('[Errno -3] Temporary failure in name resolution') == -1 \
			and flow.all.find('[Errno -2] Name or service not known') == -1 \
			and flow.url.find('https://www.google.com/tg/fe/request?rqt=3&bq=1') == -1 \
			and flow.url.find('https://android.googleapis.com/auth/lookup/account_state?rt=b') == -1 \
			and flow.url.find('https://www.googleapis.com/androidcheck/v1/attestations/adAttest?key=') == -1):
				newFlows.append(flow)
				newFlowFile.write(flow.all)


def checkFlow(flow):
	results = []
	flow.app = AppFinder.findApp(flow, appList)
	print('App: ' + flow.app)
	
	if (flow.app == 'CertInstaller' and 'CertInstaller' in appList):
		CertInstaller.checkBehavior(flow, results)
	if (flow.app == 'GSuite' and 'GSuite' in appList):
		GSuite.checkBehavior(flow, results)
	if (flow.app == 'Youtube' and 'Youtube' in appList):
		Youtube.checkBehavior(flow, results)
	if (flow.app == 'Reddit' and 'Reddit' in appList):
		Reddit.checkBehavior(flow, results)
	if (flow.app == 'AndroidNative' and 'AndroidNative' in appList):
		AndroidNative.checkBehavior(flow, results)
	if (flow.app == 'AppDefault' and 'AppDefault' in appList):
		AppDefault.checkBehavior(flow, results)
	AppDefault.syncSource(flow, results)
	print(flow.all)
	printLogs(results)
	#sendLogs(results)

def sendLogs(results):
	for result in results:
		log.send(result.logFull, syslog_client.Level.INFO)

def printLogs(results):
	print('\n')
	for result in results:
		lines = result.log.split(';;;;;')
		print('Source: ' + lines[0])
		print('Destination: ' + lines[1])
		print('Type: ' + lines[2])
		print('Info: ' + lines[3])
		#print(lines[4])
		print()

def testFlow(num):
	#print(flows[num].all)
	#print(AppDefault.cleanEncoding(flows[num].responseContent))
	checkFlow(flows[num])

def analyzeAll():
	count = 0
	for flow in flows:
		print(count)
		checkFlow(flow)
		count = count + 1

separateFlows()
#printFlows()
#analyzeAll()
testFlow(testNum)
#findNewFlows()
