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
import AndroidDataPrivacy.Applications.Venmo as Venmo
import AndroidDataPrivacy.Applications.Facebook as Facebook
import AndroidDataPrivacy.Applications.LinkedIn as LinkedIn
import AndroidDataPrivacy.Applications.Canvas as Canvas
import AndroidDataPrivacy.Applications.RocketChat as RocketChat
import AndroidDataPrivacy.Applications.Hulu as Hulu
import AndroidDataPrivacy.Applications.Netflix as Netflix
import AndroidDataPrivacy.Applications.KeeperSecurity as KeeperSecurity
import AndroidDataPrivacy.Applications.CertInstaller as CertInstaller

testNumList = list(range(41,53))
filename = 'capturefixed.txt'
#filename = 'backup.txt'
#filename = 'newflows.txt'
file = open(filename, "r")
newFlowFileName = 'newflows.txt'
capture = file.readlines()
flows = []
results = []
appList = ['AppDefault','AndroidNative','GSuite','Youtube', 'Reddit', 'Slack', 'Discord', 'Spotify', \
'Venmo', 'Facebook', 'LinkedIn', 'Canvas', 'RocketChat', 'Hulu', 'Netflix', 'KeeperSecurity', \
'CertInstaller', 'RawDataSearch']
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
	block = False
	for line in capture:
		if (count > 0):
			flow = flow + line
			count = count - 1
		elif (line[0:1] == ' ' or line[1:2] == '' or line[:21] == 'cd=com.google.android' or block == True):
			flow = flow + line
			if (block == True):
				if (line[0:1] == ' ' or line[1:2] == ''):
					block = False
		elif (line[0:15] == 'generic profile'):
			flow = flow + line
			count = 2
		elif (line[0:3] == 'icc'):
			block = True
			count = 1
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
	'https://spclient.wg.spotify.com/metadata/4', \
	'https://inbox.google.com/sync', \
	'https://www.google.com/complete/search', \
	'https://audio-sp-dca.pscdn.co/audio', \
	'https://scannables.scdn.co/uri/800/spotify', \
	'https://events.redditmedia.com', \
	'https://audio4-ak-spotify-com.akamaized.net/audio', \
	'https://spclient.wg.spotify.com', \
	'https://e.crashlytics.com', \
	'https://venmopics.appspot.com', \
	'https://venmo-merchant-images.s3.amazonaws.com', \
	'https://api.venmo.com/v1/account/settings/social', \
	'https://api.venmo.com/v1/alerts', \
	'https://platform-lookaside.fbsbx.com', \
	'https://api.venmo.com/v1/stories/target-or-actor', \
	'https://api.venmo.com/v1/users/merchant-payments-activation-views', \
	'https://api.venmo.com/v1/account', \
	'https://api.venmo.com/v1/venmo-card/settings', \
	'https://api.venmo.com/v1/payment-methods', \
	'https://api.venmo.com/v1/checkpoints', \
	'https://media.licdn.com/dms/image', \
	'https://www.linkedin.com/realtime/realtimeFrontendTimestamp', \
	'https://www.linkedin.com/li/track', \
	'https://static.licdn.com', \
	'https://www.linkedin.com/voyager/api/jobs/jobSeekerPreferences', \
	'https://www.linkedin.com/voyager/api/voyagerIdentityMarketplaceRoles', \
	'https://www.linkedin.com/voyager/api/voyagerIdentityProfileActionsV2?ids=', \
	'https://www.linkedin.com/voyager/api/legoWidgetImpressionEvents', \
	'https://www.linkedin.com/voyager/api/voyagerIdentityProfiles', \
	'https://www.linkedin.com/voyager/api/messaging/presenceStatuses', \
	'https://www.linkedin.com/voyager/api/typeahead/hits', \
	'https://www.linkedin.com/voyager/api/voyagerIdentityDashPrivacySettings', \
	'https://www.linkedin.com/voyager/api/premium/featureAccess', \
	'https://www.linkedin.com/voyager/api/feed/updates', \
	'https://www.linkedin.com/voyager/api/voyagerIdentitySearchAppearances', \
	'https://www.linkedin.com/voyager/api/identity/ge', \
	'https://www.linkedin.com/voyager/api/voyagerGrowthPageContent', \
	'https://www.linkedin.com/voyager/api/feed/packageRecommendations', \
	'https://media.licdn.com/media-proxy', \
	'https://dms.licdn.com/playback', \
	'https://dms.licdn.com/video-thumbs', \
	'https://www.linkedin.com/voyager/api/feed/richRecommendedEntities', \
	'https://www.linkedin.com/voyager/api/messaging/badge?action=markAllItemsAsSeen', \
	'https://www.linkedin.com/csp/simt', \
	'https://www.linkedin.com/voyager/api/growth/emailConfirmationTask', \
	'https://www.linkedin.com/voyager/api/messaging/badge?action=markAllItemsAsSeen', \
	'https://www.linkedin.com/voyager/api/messaging/conversations', \
	'https://www.linkedin.com/voyager/api/messaging/typeahead/hits', \
	'https://www.linkedin.com/voyager/api/messaging/peripheral/messagingSearchHistory', \
	'https://www.linkedin.com/cross-promo-fe/api/promo', \
	'https://www.linkedin.com/voyager/api/feed/badge', \
	'https://www.linkedin.com/voyager/api/search/history', \
	'https://js.stripe.com', \
	'https://play.googleapis.com/log/batch', \
	'https://mobilenetworkscoring-pa.googleapis.com/v1/GetWifiQuality', \
	'https://play.googleapis.com/log/batch', \
	'https://android.googleapis.com/auth', \
	'http://b.scorecardresearch.com', \
	'https://graph.facebook.com', \
	'https://vortex.hulu.com/api/v3/event', \
	'https://t.appsflyer.com/api', \
	'https://img.hulu.com', \
	'https://img1.hulu.com', \
	'https://img2.hulu.com', \
	'https://img3.hulu.com', \
	'https://img4.hulu.com', \
	'https://img5.hulu.com', \
	'https://img6.hulu.com', \
	'https://img7.hulu.com', \
	'https://img8.hulu.com', \
	'https://discover.hulu.com/content/v4/search', \
	'https://discover.hulu.com/content/v4/me/state', \
	'https://play.googleapis.com/play/log', \
	'https://stats.appsflyer.com/stats', \
	'https://play.hulu.com/v4/playlist', \
	'https://license.hulu.com', \
	'https://ads-e-darwin.hulustream.com', \
	'https://manifest.hulustream.com', \
	'https://ib.hulu.com/thumb', \
	'https://hulu.hb.omtrdc.net', \
	'https://t2.hulu.com', \
	'https://mb.moatads.com', \
	'https://http-e-darwin.hulustream.com', \
	'https://geo.moatads.com', \
	'https://px.moatads.com', \
	'https://z.moatads.com', \
	'https://ag.innovid.com', \
	'https://s.innovid.com', \
	'https://cws-hulu.conviva.com/0/wsg', \
	'https://settings.crashlytics.com/spi/v2/platforms/android/apps', \
	'https://android-appboot.netflix.com/appboot', \
	'https://android.prod.cloud.netflix.com/msl', \
	'https://android.prod.cloud.netflix.com/ichnaea', \
	'https://cast.google.com/cast/nearby/search', \
	'https://android.clients.google.com/c2dm/register3', \
	'https://keepersecurity.com/api/rest/vault/execute_v2_command']

	oldURLparts = ['googlevideo.com/initplayback', \
	'googlevideo.com/videoplayback', \
	'com/generate_204', \
	'/recommendations?', \
	'/recommendationRequests?', \
	'/marketplacePreferences?', \
	'/memberConnections?', \
	'/profilePromotions?', \
	'/following?', \
	'/profileContactInfo?', \
	'/positionGroups?', \
	'/posts?', \
	'/volunteerCauses?', \
	'/skills?', \
	'/suggestedSkills', \
	'/suggestedTopSkills', \
	'/networkinfo?', \
	'.png', \
	'.webp', \
	'.jpg', \
	'-ix.1.oca.nflxvideo.net']

	old = False
	count = 0
	#analyzeAll()
	for flow in flows:
		print(count)
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
		count = count + 1


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
	if (flow.app == 'Venmo' and 'Venmo' in appList):
		Venmo.checkBehavior(flow, results)
	if (flow.app == 'Facebook' and 'Facebook' in appList):
		Facebook.checkBehavior(flow, results)
	if (flow.app == 'LinkedIn' and 'LinkedIn' in appList):
		LinkedIn.checkBehavior(flow, results)
	if (flow.app == 'Canvas' and 'Canvas' in appList):
		Canvas.checkBehavior(flow, results)
	if (flow.app == 'RocketChat' and 'RocketChat' in appList):
		RocketChat.checkBehavior(flow, results)
	if (flow.app == 'Hulu' and 'Hulu' in appList):
		Hulu.checkBehavior(flow, results)
	if (flow.app == 'Netflix' and 'Netflix' in appList):
		Netflix.checkBehavior(flow, results)
	if (flow.app == 'KeeperSecurity' and 'KeeperSecurity' in appList):
		KeeperSecurity.checkBehavior(flow, results)
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
analyzeAll()
#testFlows(testNumList)
#findNewFlows()
