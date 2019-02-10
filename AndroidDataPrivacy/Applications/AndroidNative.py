import AndroidDataPrivacy.Flow as Flow
import AndroidDataPrivacy.Result as Result
import AndroidDataPrivacy.Applications.AppDefault as AppDefault

type = ''
info = ''

urls = ['http://www.google.com/gen_204', \
'https://www.google.com/generate_204', \
'http://connectivitycheck.gstatic.com/generate_204', \
'https://connectivitycheck.gstatic.com/generate_204', \
'https://android.clients.google.com/c2dm/register3', \
'https://android.googleapis.com/checkin', \
'https://android.clients.google.com/checkin', \
'https://android.googleapis.com/auth']

partialURLs = ['www.google.com/tg/fe/request?rqt', \
'https://www.googleapis.com/androidantiabuse/v1/x/create?', \
'https://www.googleapis.com/geolocation', \
'preloads?doc=android.autoinstalls.config.', \
'https://www.google.com/complete/search', \
'https://app-measurement.com', \
'https://www.googleapis.com/userlocation', \
'https://www.googleapis.com/calendar', \
'https://inbox.google.com/sync']

userAgents = ['AndroidDownloadManager', \
'Android-GCM']

partialUserAgents = ['Android-GData', \
'Android-Gmail']

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
			flow.source = 'File Download'
			type = 'IP Address'
			info = flow.address
			results.append(Result.Result(flow.app, flow.destination, flow.source, type, info))
		if (headers['User-Agent'][:10] == 'DroidGuard'):
			flow.source = 'DroidGuard'
		if (headers['User-Agent'][:13] == 'Android-Gmail'):
			if (flow.source == ''):
				flow.source = 'GMail'
			print(AppDefault.cleanEncoding(flow.responseContent))
	
	if ('authorization' in headers.keys()):
		type = 'User Info: Authorization Token'
		info = flow.requestHeaders['authorization']
		results.append(Result.Result(flow.app, flow.destination, flow.source, type, info))

def checkResponseHeaders(flow, headers, results):
	return None

def checkGetURL(flow, results):
	#WiFi connectivity check
	if (flow.url == 'http://connectivitycheck.gstatic.com/generate_204' or flow.url == 'https://connectivitycheck.gstatic.com/generate_204'):
		flow.source = 'WiFi Connection'
		type = 'System Status'
		info = 'WiFi connection active'
		results.append(Result.Result(flow.app, flow.destination, flow.source, type, info))
	
	#Google Ping
	elif (flow.url == 'https://www.google.com/generate_204'):
		flow.source = 'Google service ping'
	elif (flow.url == 'http://www.google.com/gen_204'):
		flow.source = 'Google service ping'
	
	elif (flow.url.find('https://android.clients.google.com/gsync') > -1):
		flow.source = 'Google Account Data Sync'
		type = 'System Info: GCM ID'
		info = flow.requestContent[flow.requestContent.find('gcm://?regId=')+13:flow.requestContent.find('&androidId=')]
		results.append(Result.Result(flow.app, flow.destination, flow.source, type, info))
		
		type = 'System Info: Android ID'
		info = flow.requestContent[flow.requestContent.find('&androidId=')+11:flow.requestContent.find('\n')]
		results.append(Result.Result(flow.app, flow.destination, flow.source, type, info))
	
	elif (flow.url.find('preloads?doc=android.autoinstalls.config.') > -1):
		flow.source = 'App Preloader'
		type = 'System Info: Build'
		info = flow.requestContent
		info = info[info.find('build_fingerprint:')+19:]
		info = info[:info.find('\n')]
		info = info.strip()
		results.append(Result.Result(flow.app, flow.destination, flow.source, type, info))

	elif (flow.url.find('https://www.google.com/complete/search') > -1):
		flow.source = 'Google Search History Sync'

	elif (flow.url.find('https://app-measurement.com') == 0):
		flow.source = 'App Measurement'
		type = 'System Info: App ID'
		info = flow.url[flow.url.find('app/')+4:flow.url.find('?')]
		info = AppDefault.fixUrlEncoding(info)
		results.append(Result.Result(flow.app, flow.destination, flow.source, type, info))

		type = 'System Info: App Instance ID'
		info = flow.requestContent
		info = info[info.find('app_instance_id:')+17:]
		info = info[:info.find('\n')].strip()
		results.append(Result.Result(flow.app, flow.destination, flow.source, type, info))
	
	elif (flow.url.find('https://www.googleapis.com/userlocation/v1/settings') == 0):
		flow.source = 'Android Location Settings Sync'
		type = 'System Info: Model'
		info = AppDefault.findFormEntry(flow.requestContent, 'brand') + ' ' + AppDefault.findFormEntry(flow.requestContent, 'model')
		results.append(Result.Result(flow.app, flow.destination, flow.source, type, info))
		
		type = 'System Info: Build'
		info = AppDefault.findFormEntry(flow.requestContent, 'platform')
		results.append(Result.Result(flow.app, flow.destination, flow.source, type, info))
	
	elif (flow.url.find('https://www.googleapis.com/calendar') == 0):
		flow.source = 'Google Calendar'
		
		if (flow.responseContent.find('notificationSettings') > -1):
			type = 'User Info: Notification Settings'
			info = AppDefault.findJSONSection(flow.responseContent, 'notificationSettings')
			results.append(Result.Result(flow.app, flow.destination, flow.source, type, info))

def checkPostURL(flow, results):
	#Weather lookup
	if (flow.url.find('www.google.com/tg/fe/request?rqt') > -1):
		flow.source = 'Weather Lookup'
		type = 'Location'
		info = 'Your location was collected'
		results.append(Result.Result(flow.app, flow.destination, flow.source, type, info))
	
	#Messages login
	elif (flow.url == 'https://android.clients.google.com/c2dm/register3'):
		flow.source = 'Messages Login'
		type = 'System Info: Device ID'
		info = flow.requestContent
		info = info[info.find('device:')+7:]
		info = info[:info.find('\n')]
		info = info.strip()
		results.append(Result.Result(flow.app, flow.destination, flow.source, type, info))
		
		type = 'Token'
		info = flow.responseContent
		info = info[info.find('token=')+6:]
		info = info.strip()
		results.append(Result.Result(flow.app, flow.destination, flow.source, type, info))
	
	elif (flow.url.find('https://www.googleapis.com/androidantiabuse/v1/x/create?') > -1):
		flow.source = 'DroidGuard'
		type = 'System Info: Bootloader'
		info = flow.requestContent[flow.requestContent.find('BOOTLOADER'):]
		info = info[:info.find('\n')]
		info = AppDefault.cleanEncoding(info)
		info = info.strip()
		info = info[10:]
		results.append(Result.Result(flow.app, flow.destination, flow.source, type, info))
		
		type = 'System Info: Brand'
		info = flow.requestContent[flow.requestContent.find('BRAND'):]
		info = info[:info.find('\n')]
		info = AppDefault.cleanEncoding(info)
		info = info[5:]
		info = info.strip()
		results.append(Result.Result(flow.app, flow.destination, flow.source, type, info))
		
		type = 'System Info: Model'
		info = flow.requestContent[flow.requestContent.find('MODEL'):]
		info = info[:info.find('\n')]
		info = AppDefault.cleanEncoding(info)
		info = info[5:]
		info = info.strip()
		results.append(Result.Result(flow.app, flow.destination, flow.source, type, info))
		
		type = 'System Info: Serial Number'
		info = flow.requestContent[flow.requestContent.find('SERIAL'):]
		info = info[:info.find('\n')]
		info = AppDefault.cleanEncoding(info)
		info = info[6:]
		info = info.strip()
		results.append(Result.Result(flow.app, flow.destination, flow.source, type, info))
	
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
				results.append(Result.Result(flow.app, flow.destination, flow.source, type, info))
		if (flow.responseContent.find('adwords:enable_primes_network_monitoring') > -1):
			temp = flow.responseContent[flow.responseContent.find('1: adwords:enable_primes_network_monitoring'):]
			temp = temp[temp.find('2:')+3:]
			temp = temp[:temp.find('\n')]
			if (temp == 'true'):
				type = 'System Status: Network Monitoring'
				info = 'Android network activity is being monitored'
				results.append(Result.Result(flow.app, flow.destination, flow.source, type, info))
		if (flow.responseContent.find('adwords:enable_primes_timing_monitoring') > -1):
			temp = flow.responseContent[flow.responseContent.find('1: adwords:enable_primes_timing_monitoring'):]
			temp = temp[temp.find('2:')+3:]
			temp = temp[:temp.find('\n')]
			if (temp == 'true'):
				type = 'System Status: Timing Monitoring'
				info = 'Android timing is being monitored'
				results.append(Result.Result(flow.app, flow.destination, flow.source, type, info))
		if (flow.responseContent.find('adwords:enable_silent_feedback') > -1):
			temp = flow.responseContent[flow.responseContent.find('1: adwords:enable_silent_feedback'):]
			temp = temp[temp.find('2:')+3:]
			temp = temp[:temp.find('\n')]
			if (temp == 'true'):
				type = 'System Status: Silent Feedback'
				info = 'Silent feedback is enabled'
				results.append(Result.Result(flow.app, flow.destination, flow.source, type, info))

	#Location pull
	elif (flow.url.find('https://www.googleapis.com/geolocation') > -1):
		flow.source = 'Google APIs'
		type = 'Location: Cell Towers'
		info = flow.requestContent
		info = info[info.find('"cellTowers": ['):]
		info = info[:info.find(']')+1]
		results.append(Result.Result(flow.app, flow.destination, flow.source, type, info))
		
		type = 'Location: WiFi Access Points'
		info = flow.requestContent
		info = info[info.find('"wifiAccessPoints": ['):]
		info = info[:info.find(']')+1]
		results.append(Result.Result(flow.app, flow.destination, flow.source, type, info))
		
		type = 'Location: Request Key'
		info = flow.url[flow.url.find('key=')+4:]
		results.append(Result.Result(flow.app, flow.destination, flow.source, type, info))
	
	elif (flow.url.find('https://app-measurement.com') == 0):
		flow.source = 'App Measurement'
	
	elif (flow.url == 'https://android.googleapis.com/auth'):
		flow.source = 'Google Login'
		if (AppDefault.findFormEntry(flow.requestContent, 'app') == 'com.google.android.gms'):
			flow.source = 'Google Mobile Services Login'
			temp = AppDefault.findFormEntry(flow.requestContent, 'service')
			if (temp.find('auth/plus') > -1):
				flow.source = 'Google Plus Login'
		if (AppDefault.findFormEntry(flow.requestContent, 'app') == 'com.google.android.gm'):
			flow.source = 'GMail Login'
		elif (AppDefault.findFormEntry(flow.requestContent, 'app') == 'com.google.android.googlequicksearchbox'):
			flow.source = 'Google Quick Search Login'
		elif (AppDefault.findFormEntry(flow.requestContent, 'app') == 'com.google.android.calendar'):
			flow.source = 'Google Calendar Login'
		
		type = 'System Info: Android ID'
		info = AppDefault.findFormEntry(flow.requestContent, 'androidId')
		results.append(Result.Result(flow.app, flow.destination, flow.source, type, info))
		
		type = 'System Info: Country'
		info = AppDefault.findFormEntry(flow.requestContent, 'device_country')
		results.append(Result.Result(flow.app, flow.destination, flow.source, type, info))
		
		type = 'System Info: Language'
		info = AppDefault.findFormEntry(flow.requestContent, 'lang')
		results.append(Result.Result(flow.app, flow.destination, flow.source, type, info))
		
		type = 'User Info: Email Address'
		info = AppDefault.findFormEntry(flow.requestContent, 'Email')
		results.append(Result.Result(flow.app, flow.destination, flow.source, type, info))
		
		type = 'System Info: Android Client Signature'
		info = AppDefault.findFormEntry(flow.requestContent, 'client_sig')
		results.append(Result.Result(flow.app, flow.destination, flow.source, type, info))
		
		type = 'System Info: Google Mobile Services Token'
		info = AppDefault.findFormEntry(flow.requestContent, 'Token')
		results.append(Result.Result(flow.app, flow.destination, flow.source, type, info))
	
	elif (flow.url[:29] == 'https://inbox.google.com/sync'):
		flow.source = 'GMail Inbox Sync'
		

def getURLs():
	return urls

