import AndroidDataPrivacy.Flow as Flow
import AndroidDataPrivacy.Result as Result
import AndroidDataPrivacy.Applications.AppDefault as AppDefault

urls = ['http://www.google.com/gen_204', \
'https://www.google.com/generate_204', \
'http://connectivitycheck.gstatic.com/generate_204', \
'https://connectivitycheck.gstatic.com/generate_204', \
'https://android.clients.google.com/c2dm/register3', \
'https://android.googleapis.com/checkin', \
'https://android.clients.google.com/checkin', \
'https://android.googleapis.com/auth', \
'https://android.googleapis.com/auth/devicekey', \
'https://accounts.google.com/oauth/multilogin']

partialURLs = ['www.google.com/tg/fe/request?rqt=58', \
'https://www.googleapis.com/androidantiabuse/v1/x/create?', \
'https://www.googleapis.com/geolocation', \
'preloads?doc=android.autoinstalls.config.', \
'https://www.google.com/complete/search', \
'https://app-measurement.com', \
'https://www.googleapis.com/userlocation', \
'https://www.googleapis.com/calendar', \
'https://inbox.google.com/sync', \
'https://android.clients.google.com/fdfe/selfUpdate', \
'https://android.clients.google.com/fdfe/accountSync', \
'https://play.googleapis.com', \
'https://www.googleapis.com/experimentsandconfigs/v1/getExperimentsAndConfigs', \
'https://ssl.google-analytics.com']

userAgents = ['Android-GCM']

partialUserAgents = ['Android-GData', \
'Android-Gmail', \
'Android-Finsky', \
'AndroidDownloadManager']

appIds = {'1:1086610230652:android:131e4c3db28fca84':'com.google.android.googlequicksearchbox', \
'1:493454522602:android:4877c2b5f408a8b2':'com.google.android.apps.maps', \
'1:206908507205:android:167bd0ff59cd7d44':'com.google.android.apps.tachyon'}

def checkBehavior(flow, results):
	if (flow.requestType == 'GET'):
		analyzeGetRequest(flow, results)
	if (flow.requestType == 'POST'):
		analyzePostRequest(flow, results)

def analyzeGetRequest(flow, results):
	checkGetURL(flow, results)
	checkRequestHeaders(flow, flow.requestHeaders, results)
	AppDefault.checkRequestHeadersDefault(flow, flow.requestHeaders, results)
	checkResponseHeaders(flow, flow.responseHeaders, results)
	AppDefault.checkResponseHeadersDefault(flow, flow.responseHeaders, results)
	AppDefault.analyzeGetRequestDefault(flow, results)

def analyzePostRequest(flow, results):
	checkPostURL(flow, results)
	checkRequestHeaders(flow, flow.requestHeaders, results)
	AppDefault.checkRequestHeadersDefault(flow, flow.requestHeaders, results)
	checkResponseHeaders(flow, flow.responseHeaders, results)
	AppDefault.checkResponseHeadersDefault(flow, flow.responseHeaders, results)
	AppDefault.analyzePostRequestDefault(flow, results)

def checkRequestHeaders(flow, headers, results):
	if ('User-Agent' in headers.keys()):
		if (headers['User-Agent'][:22] == 'AndroidDownloadManager'):
			if (flow.url[:36] == 'https://play.googleapis.com/download' \
			or flow.url.find('play-apps-download') > -1):
				flow.source = 'Play Store Download'
			else:
				flow.source = 'File Download'
			type = 'IP Address'
			info = flow.address
			results.append(Result.Result(flow.app, flow.destination, flow.source, type, info, flow.all))
		if (headers['User-Agent'][:10] == 'DroidGuard'):
			flow.source = 'DroidGuard'
		if (headers['User-Agent'][:13] == 'Android-Gmail' and flow.source == ''):
			flow.source = 'GMail'
		if (headers['User-Agent'][:14] == 'Android-Finsky' and flow.source == ''):
			flow.source = 'Google Play Store'
	
	if ('authorization' in headers.keys()):
		type = 'User Info: Authorization Token'
		info = flow.requestHeaders['authorization']
		results.append(Result.Result(flow.app, flow.destination, flow.source, type, info, flow.all))

def checkResponseHeaders(flow, headers, results):
	return None

def checkGetURL(flow, results):
	#WiFi connectivity check
	if (flow.url == 'http://connectivitycheck.gstatic.com/generate_204' or flow.url == 'https://connectivitycheck.gstatic.com/generate_204'):
		flow.source = 'WiFi Connection'
		type = 'System Status'
		info = 'WiFi connection active'
		results.append(Result.Result(flow.app, flow.destination, flow.source, type, info, flow.all))
	
	#Google Ping
	elif (flow.url == 'https://www.google.com/generate_204'):
		flow.source = 'Google service ping'
	elif (flow.url == 'http://www.google.com/gen_204'):
		flow.source = 'Google service ping'
	
	elif (flow.url.find('https://android.clients.google.com/gsync') > -1):
		flow.source = 'Google Account Data Sync'
		type = 'System Info: GCM ID'
		info = flow.requestContent[flow.requestContent.find('gcm://?regId=')+13:flow.requestContent.find('&androidId=')]
		results.append(Result.Result(flow.app, flow.destination, flow.source, type, info, flow.all))
		
		type = 'System Info: Android ID'
		info = flow.requestContent[flow.requestContent.find('&androidId=')+11:flow.requestContent.find('\n')]
		results.append(Result.Result(flow.app, flow.destination, flow.source, type, info, flow.all))
	
	elif (flow.url.find('preloads?doc=android.autoinstalls.config.') > -1):
		flow.source = 'App Preloader'
		type = 'System Info: Build'
		info = flow.requestContent
		info = info[info.find('build_fingerprint:')+19:]
		info = info[:info.find('\n')]
		info = info.strip()
		results.append(Result.Result(flow.app, flow.destination, flow.source, type, info, flow.all))

	elif (flow.url.find('https://www.google.com/complete/search') > -1):
		flow.source = 'Google Search History Sync'

	elif (flow.url.find('https://app-measurement.com') == 0):
		flow.source = 'App Measurement'
		type = 'System Info: Application'
		info = flow.url[flow.url.find('app/')+4:flow.url.find('?')]
		info = AppDefault.fixUrlEncoding(info)
		if (info in appIds.keys()):
			info = appIds[info]
		results.append(Result.Result(flow.app, flow.destination, flow.source, type, info, flow.all))

		type = 'System Info: App Instance ID'
		info = flow.requestContent
		info = info[info.find('app_instance_id:')+17:]
		info = info[:info.find('\n')].strip()
		results.append(Result.Result(flow.app, flow.destination, flow.source, type, info, flow.all))
	
	elif (flow.url.find('https://www.googleapis.com/userlocation/v1/settings') == 0):
		flow.source = 'Android Location Settings Sync'
		type = 'System Info: Model'
		info = AppDefault.findFormEntry(flow.requestContent, 'brand') + ' ' + AppDefault.findFormEntry(flow.requestContent, 'model')
		results.append(Result.Result(flow.app, flow.destination, flow.source, type, info, flow.all))
		
		type = 'System Info: Build'
		info = AppDefault.findFormEntry(flow.requestContent, 'platform')
		results.append(Result.Result(flow.app, flow.destination, flow.source, type, info, flow.all))
	
	elif (flow.url.find('https://www.googleapis.com/calendar') == 0):
		flow.source = 'Google Calendar'
		
		if (flow.responseContent.find('notificationSettings') > -1):
			type = 'User Info: Notification Settings'
			info = AppDefault.findJSONSection(flow.responseContent, 'notificationSettings')
			results.append(Result.Result(flow.app, flow.destination, flow.source, type, info, flow.all))

		elif (flow.responseContent.find('"kind": "calendar#events"') > -1):
			type = 'User Info: Calendar Event'
			events = AppDefault.findJSONList(flow.responseContent, 'items')
			for info in events:
				results.append(Result.Result(flow.app, flow.destination, flow.source, type, info, flow.all))

	elif (flow.url[:27] == 'https://play.googleapis.com'):
		flow.source = 'Google Play Store'

def checkPostURL(flow, results):
	#Weather lookup
	if (flow.url.find('www.google.com/tg/fe/request?rqt=58') > -1):
		flow.source = 'Weather Lookup'
		#type = 'Location'
		#info = ''
		#results.append(Result.Result(flow.app, flow.destination, flow.source, type, info, flow.all))
	
	#Messages login
	elif (flow.url == 'https://android.clients.google.com/c2dm/register3'):
		flow.source = 'Messages Login'
		type = 'System Info: Device ID'
		info = flow.requestContent
		info = info[info.find('device:')+7:]
		info = info[:info.find('\n')]
		info = info.strip()
		results.append(Result.Result(flow.app, flow.destination, flow.source, type, info, flow.all))
		
		type = 'Token'
		info = flow.responseContent
		info = info[info.find('token=')+6:]
		info = info.strip()
		results.append(Result.Result(flow.app, flow.destination, flow.source, type, info, flow.all))
	
	elif (flow.url.find('https://www.googleapis.com/androidantiabuse/v1/x/create?') > -1):
		flow.source = 'DroidGuard'
		type = 'System Info: Bootloader'
		info = flow.requestContent[flow.requestContent.find('BOOTLOADER'):]
		info = info[:info.find('\n')]
		info = AppDefault.cleanEncoding(info)
		info = info.strip()
		info = info[10:]
		results.append(Result.Result(flow.app, flow.destination, flow.source, type, info, flow.all))
		
		type = 'System Info: Brand'
		info = flow.requestContent[flow.requestContent.find('BRAND'):]
		info = info[:info.find('\n')]
		info = AppDefault.cleanEncoding(info)
		info = info[5:]
		info = info.strip()
		results.append(Result.Result(flow.app, flow.destination, flow.source, type, info, flow.all))
		
		type = 'System Info: Model'
		info = flow.requestContent[flow.requestContent.find('MODEL'):]
		info = info[:info.find('\n')]
		info = AppDefault.cleanEncoding(info)
		info = info[5:]
		info = info.strip()
		results.append(Result.Result(flow.app, flow.destination, flow.source, type, info, flow.all))
		
		type = 'System Info: Serial Number'
		info = flow.requestContent[flow.requestContent.find('SERIAL'):]
		info = info[:info.find('\n')]
		info = AppDefault.cleanEncoding(info)
		info = info[6:]
		info = info.strip()
		results.append(Result.Result(flow.app, flow.destination, flow.source, type, info, flow.all))

	elif (flow.url[:27] == 'https://play.googleapis.com'):
		flow.source = 'Google Play Store'
	
	#Android Check-in
	elif (flow.url == 'https://android.googleapis.com/checkin' or flow.url == 'https://android.clients.google.com/checkin'):
		flow.source = 'Android Check-in'
		
		if (flow.responseContent.find('adwords:enable_primes_memory_monitoring') > -1):
			temp = flow.responseContent[flow.responseContent.find('1: adwords:enable_primes_memory_monitoring'):]
			temp = temp[temp.find('2:')+3:]
			temp = temp[:temp.find('\n')]
			if (temp == 'true'):
				type = 'System Status: Memory Monitoring'
				info = 'Android memory is being monitored'
				results.append(Result.Result(flow.app, flow.destination, flow.source, type, info, flow.all))
		if (flow.responseContent.find('adwords:enable_primes_network_monitoring') > -1):
			temp = flow.responseContent[flow.responseContent.find('1: adwords:enable_primes_network_monitoring'):]
			temp = temp[temp.find('2:')+3:]
			temp = temp[:temp.find('\n')]
			if (temp == 'true'):
				type = 'System Status: Network Monitoring'
				info = 'Android network activity is being monitored'
				results.append(Result.Result(flow.app, flow.destination, flow.source, type, info, flow.all))
		if (flow.responseContent.find('adwords:enable_primes_timing_monitoring') > -1):
			temp = flow.responseContent[flow.responseContent.find('1: adwords:enable_primes_timing_monitoring'):]
			temp = temp[temp.find('2:')+3:]
			temp = temp[:temp.find('\n')]
			if (temp == 'true'):
				type = 'System Status: Timing Monitoring'
				info = 'Android timing is being monitored'
				results.append(Result.Result(flow.app, flow.destination, flow.source, type, info, flow.all))
		if (flow.responseContent.find('adwords:enable_silent_feedback') > -1):
			temp = flow.responseContent[flow.responseContent.find('1: adwords:enable_silent_feedback'):]
			temp = temp[temp.find('2:')+3:]
			temp = temp[:temp.find('\n')]
			if (temp == 'true'):
				type = 'System Status: Silent Feedback'
				info = 'Silent feedback is enabled'
				results.append(Result.Result(flow.app, flow.destination, flow.source, type, info, flow.all))

	#Location pull
	elif (flow.url.find('https://www.googleapis.com/geolocation') > -1):
		flow.source = 'Google APIs'
		type = 'Location: Cell Towers'
		info = flow.requestContent
		info = info[info.find('"cellTowers": ['):]
		info = info[:info.find(']')+1]
		results.append(Result.Result(flow.app, flow.destination, flow.source, type, info, flow.all))
		
		type = 'Location: WiFi Access Points'
		info = flow.requestContent
		info = info[info.find('"wifiAccessPoints": ['):]
		info = info[:info.find(']')+1]
		results.append(Result.Result(flow.app, flow.destination, flow.source, type, info, flow.all))
		
		type = 'Location: Request Key'
		info = flow.url[flow.url.find('key=')+4:]
		results.append(Result.Result(flow.app, flow.destination, flow.source, type, info, flow.all))
	
	elif (flow.url.find('https://app-measurement.com') == 0):
		flow.source = 'App Measurement'

		if (flow.url == 'https://app-measurement.com/a'):
			cleaned = AppDefault.cleanEncoding(flow.requestContent)
			print(cleaned)
			if (cleaned.find('app_launched') > -1):
				type = 'User Action: App Launched'
				info = cleaned[cleaned.find('(1:')+1:]
				info = info[:40]
				if (info in appIds.keys()):
					info = appIds[info]
				results.append(Result.Result(flow.app, flow.destination, flow.source, type, info, flow.all))
	
	elif (flow.url == 'https://android.googleapis.com/auth'):
		flow.source = 'Google Login'
		if (AppDefault.findFormEntry(flow.requestContent, 'app') == 'com.google.android.gms'):
			flow.source = 'Google Mobile Services Login'
		if (AppDefault.findFormEntry(flow.requestContent, 'app') == 'com.google.android.gm'):
			flow.source = 'GMail Login'
		elif (AppDefault.findFormEntry(flow.requestContent, 'app') == 'com.google.android.googlequicksearchbox'):
			flow.source = 'Google Quick Search Login'
		elif (AppDefault.findFormEntry(flow.requestContent, 'app') == 'com.google.android.calendar'):
			flow.source = 'Google Calendar Login'
		elif (AppDefault.findFormEntry(flow.requestContent, 'app') == 'com.android.vending'):
			flow.source = 'Google Play Store Login'
		elif (AppDefault.findFormEntry(flow.requestContent, 'app') == 'com.google.android.contacts'):
			flow.source = 'Google Contacts Login'
		
		type = 'System Info: Android ID'
		info = AppDefault.findFormEntry(flow.requestContent, 'androidId')
		results.append(Result.Result(flow.app, flow.destination, flow.source, type, info, flow.all))
		
		type = 'System Info: Country'
		info = AppDefault.findFormEntry(flow.requestContent, 'device_country')
		results.append(Result.Result(flow.app, flow.destination, flow.source, type, info, flow.all))
		
		type = 'System Info: Language'
		info = AppDefault.findFormEntry(flow.requestContent, 'lang')
		results.append(Result.Result(flow.app, flow.destination, flow.source, type, info, flow.all))
		
		type = 'User Info: Email Address'
		info = AppDefault.findFormEntry(flow.requestContent, 'Email')
		results.append(Result.Result(flow.app, flow.destination, flow.source, type, info, flow.all))
		
		type = 'System Info: Android Client Signature'
		info = AppDefault.findFormEntry(flow.requestContent, 'client_sig')
		results.append(Result.Result(flow.app, flow.destination, flow.source, type, info, flow.all))
		
		type = 'System Info: Google Mobile Services Token'
		info = AppDefault.findFormEntry(flow.requestContent, 'Token')
		results.append(Result.Result(flow.app, flow.destination, flow.source, type, info, flow.all))
	
	elif (flow.url[:29] == 'https://inbox.google.com/sync'):
		flow.source = 'GMail Inbox Sync'

	elif (flow.url.find('https://www.googleapis.com/experimentsandconfigs/v1/getExperimentsAndConfigs') == 0):
		flow.source = 'Experimental Features Config Sync'

	elif (flow.url.find('https://ssl.google-analytics.com') == 0):
		flow.source = 'Google Analytics'

		if (AppDefault.findFormEntry(flow.requestContent, 'cd') == 'com.google.android.apps.contacts.activities.PeopleActivity' \
			and AppDefault.findFormEntry(flow.requestContent, 't') == 'screenview'):
			type = 'User Action: View Contact'
			info = AppDefault.findFormEntry(flow.requestContent, 'cid')
			results.append(Result.Result(flow.app, flow.destination, flow.source, type, info, flow.all))

	elif (flow.url == 'https://android.googleapis.com/auth/devicekey'):
		flow.source = 'Google Mobile Services'
		type = 'System Info: Device Key'
		info = flow.requestContent
		results.append(Result.Result(flow.app, flow.destination, flow.source, type, info, flow.all))

	elif (flow.url == 'https://accounts.google.com/oauth/multilogin'):
		flow.source == 'Google Account Login'
		temp = flow.responseContent[flow.responseContent.find('"accounts":[')+11:]
		temp = temp[:temp.find('}]+2')]
		print(temp)
		for account in temp.split('},{'):
			print(account)
			type = 'User Info: Name'
			info = account[account.find('"display_name":')+16:]
			info = info[:info.find('"')]
			results.append(Result.Result(flow.app, flow.destination, flow.source, type, info, flow.all))

			type = 'User Info: Email Address'
			info = account[account.find('"display_email":')+17:]
			info = info[:info.find('"')]
			results.append(Result.Result(flow.app, flow.destination, flow.source, type, info, flow.all))

			type = 'User Info: Account ID'
			info = account[account.find('"obfuscated_id":')+17:]
			info = info[:info.find('"')]
			results.append(Result.Result(flow.app, flow.destination, flow.source, type, info, flow.all))


def getURLs():
	return urls
