import AndroidDataPrivacy.Flow as Flow
import AndroidDataPrivacy.Result as Result
import AndroidDataPrivacy.Applications.AppDefault as AppDefault

type = ''
info = ''
#results = []

urls = ['http://www.google.com/gen_204', \
'https://www.google.com/generate_204', \
'http://connectivitycheck.gstatic.com/generate_204', \
'https://connectivitycheck.gstatic.com/generate_204', \
'https://android.clients.google.com/c2dm/register3', \
'https://android.googleapis.com/checkin', \
'https://android.clients.google.com/checkin']

partialURLs = ['www.google.com/tg/fe/request?rqt', \
'https://www.googleapis.com/androidantiabuse/v1/x/create?', \
'https://www.googleapis.com/geolocation', \
'preloads?doc=android.autoinstalls.config.']

userAgents = ['AndroidDownloadManager', \
'Android-GCM']

partialUserAgents = ['Android-GData']

def checkBehavior(flow, results):
	if (flow.requestType == 'GET'):
		analyzeGetRequest(flow, results)
	if (flow.requestType == 'POST'):
		analyzePostRequest(flow, results)
	AppDefault.syncSource(flow, results)

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

def checkResponseHeaders(flow, headers, results):
	return None

def checkGetURL(flow, results):
	#WiFi connectivity check
	if (flow.url == 'http://connectivitycheck.gstatic.com/generate_204' or flow.url == 'https://connectivitycheck.gstatic.com/generate_204'):
		flow.source = 'WiFi Connection'
		type = 'System Status'
		info = 'Phone connected to a WiFi network. IP address: ' + flow.address
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

def getURLs():
	return urls

