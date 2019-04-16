#!/usr/bin/python3

import AndroidDataPrivacy.syslog_client as syslog_client

import AndroidDataPrivacy.Flow as Flow
import AndroidDataPrivacy.Result as Result
import AndroidDataPrivacy.AppFinder as AppFinder
import AndroidDataPrivacy.RawDataSearch as RawDataSearch

import AndroidDataPrivacy.Applications.AppDefault as AppDefault
import AndroidDataPrivacy.Applications.AndroidNative as AndroidNative
import AndroidDataPrivacy.Applications.GSuite as GSuite
import AndroidDataPrivacy.Applications.Youtube as Youtube
import AndroidDataPrivacy.Applications.Reddit as Reddit
import AndroidDataPrivacy.Applications.Slack as Slack
import AndroidDataPrivacy.Applications.Discord as Discord
import AndroidDataPrivacy.Applications.Spotify as Spotify
import AndroidDataPrivacy.Applications.CertInstaller as CertInstaller

testNumList = list(range(1,20))
#filename = 'capturefixed.txt'
filename = 'backup.txt'
#filename = 'newflows.txt'
file = open(filename, "r")
newFlowFileName = 'newflows.txt'
capture = file.readlines()
flows = []
results = []
appList = ['AppDefault','AndroidNative','GSuite','Youtube', \
'Reddit', 'Slack', 'Discord', 'Spotify', 'CertInstaller', 'RawDataSearch']
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
		elif (line[0:1] == ' ' or line[1:2] == '' or line[:21] == 'cd=com.google.android'):
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
		flow[0:flow.find('\n')].find('StreamClosedError') > -1 or \
		flow[0:flow.find('\n')].find('HEADERS frame suppressed') > -1 or \
		flow[0:flow.find('\n')].find('HTTP/2 PRIORITY frame suppressed') > -1 or \
		flow[0:flow.find('\n')].find('ALPN') > -1 or \
		flow[0:flow.find('\n')].find('HTTP2 Event') > -1 or \
		flow[0:flow.find('\n')].find('clientconnect') > -1 or \
		flow[0:flow.find('\n')].find('serverconnect') > -1 or \
		flow[0:flow.find('\n')].find('clientdisconnect') > -1 or \
		flow[0:flow.find('\n')].find('serverdisconnect') > -1 or \
		flow[0:flow.find('\n')].find('Error in WebSocket connection') > -1 or \
		flow[0:flow.find('\n')].find('WebSocket connection closed') > -1 or \
		flow[flow.find('\n'):].find('-> Request') > -1 or \
		flow[flow.find('\n'):].find('-> Response') > -1 or \
		flow[0:flow.find('\n')].find(': CONNECT') > -1 or \
		flow[0:flow.find('\n')].find('Set new server address:') > -1 or \
		flow[0:flow.find('\n')].find('WebSocket 2 message') > -1 or \
		flow[0:flow.find('\n')].find('WebSocket 1 message') > -1 or \
		flow[0:flow.find('\n')].find('Failed to send error response to client:') > -1 or \
		flow[0:flow.find('\n')].find(': HTTP/2 connection terminated by server: error code:') > -1 or \
		flow[0:flow.find('\n')].find('Establish TLS') > -1 or \
		flow[0:].find('Cannot establish TLS with client') > -1 or \
		flow[0:].find('Error connecting to') > -1 or \
		flow[0:].find('SourceFile:') > -1 or \
		flow[0:].find('at java.') > -1 or \
		flow[0:flow.find('\n')].find('server communication error:') > -1 or \
		flow[0:flow.find('\n')].find('Connection killed') > -1 or \
		flow[0:flow.find('\n')].find('NotImplementedError') > -1):
		return True
	else:
		return False

def findNewFlows():
	newFlowFile = open(newFlowFileName, "w")
	newFlows = []
	oldURLs = ['https://googleads.g.doubleclick.net/pagead', \
	'https://www.youtube.com/pagead', \
	'https://s.youtube.com/api/stats', \
	'https://www.youtube.com/ptracking', \
	'https://www.google.com/pagead', \
	'https://www.youtube.com/csi_204', \
	'https://youtubei.googleapis.com/youtubei/v1/next?key=', \
	'https://i.ytimg.com', \
	'https://yt3.ggpht.com', \
	'https://securepubads.g.doubleclick.net', \
	'https://www.youtube.com/pcs/activeview', \
	'https://www.youtube.com/api/stats', \
	'https://www.gstatic.com/images', \
	'https://pagead2.googlesyndication.com/pcs/activeview', \
	'https://suggestqueries.google.com/complete/search', \
	'http://192.168.0.30', \
	'https://i9.ytimg.com', \
	'https://redirector.googlevideo.com', \
	'https://youtubei.googleapis.com/youtubei/v1/log_event', \
	'https://ad.doubleclick.net', \
	'https://s0.2mdn.net/viewad', \
	'https://spclient.wg.spotify.com/ads/v2/config', \
	'https://spclient.wg.spotify.com/abba-service/v1/resolve', \
	'https://pl.scdn.co/images/pl/default', \
	'https://i.scdn.co/image', \
	'https://spclient.wg.spotify.com/metadata/4']

	oldURLparts = ['googlevideo.com/initplayback', \
	'googlevideo.com/videoplayback']

	old = False
	analyzeAll()
	for flow in flows:
		for oldURL in oldURLs:
			if (flow.url.find(oldURL) == 0):
				old = True
		if (old == False):
			for oldURLpart in oldURLparts:
				if (flow.url.find(oldURLpart) > -1):
					old = True
		if (old == False):
			newFlows.append(flow)
			newFlowFile.write(flow.all)
		old = False


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
	if (flow.app == 'Slack' and 'Slack' in appList):
		Slack.checkBehavior(flow, results)
	if (flow.app == 'Discord' and 'Discord' in appList):
		Discord.checkBehavior(flow, results)
	if (flow.app == 'Spotify' and 'Spotify' in appList):
		Spotify.checkBehavior(flow, results)
	if (flow.app == 'AndroidNative' and 'AndroidNative' in appList):
		AndroidNative.checkBehavior(flow, results)
	if (flow.app == 'AppDefault' and 'AppDefault' in appList):
		AppDefault.checkBehavior(flow, results)
	AppDefault.syncSource(flow, results)
	if ('RawDataSearch' in appList):
		RawDataSearch.checkRawData(flow, results)
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

def testFlows(numList):
	for num in numList:
		print(num)
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
#testFlows(testNumList)
findNewFlows()
