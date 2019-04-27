import AndroidDataPrivacy.Flow as Flow
import AndroidDataPrivacy.Result as Result
import AndroidDataPrivacy.Applications.AppDefault as AppDefault

urls = ['http://www.google.com/gen_204', \
'https://www.google.com/generate_204', \
'http://connectivitycheck.gstatic.com/generate_204', \
'https://connectivitycheck.gstatic.com/generate_204', \
'https://android.googleapis.com/checkin', \
'https://android.clients.google.com/checkin', \
'https://android.googleapis.com/auth', \
'https://android.googleapis.com/auth/devicekey', \
'https://accounts.google.com/oauth/multilogin', \
'https://www.googleapis.com/cryptauth/v1/deviceSync/getmydevices', \
'https://www.google.com/tg/fe/request?rqt=98&bq=0', \
'https://clients3.google.com/generate_204']

partialURLs = ['www.google.com/tg/fe/request?rqt=58', \
'https://www.googleapis.com/androidantiabuse/v1/x/create?', \
'https://www.googleapis.com/geolocation', \
'preloads?doc=android.autoinstalls.config.', \
'https://www.google.com/complete/search', \
'https://app-measurement.com', \
'https://www.googleapis.com/userlocation', \
'https://android.clients.google.com/fdfe/selfUpdate', \
'https://android.clients.google.com/fdfe/accountSync', \
'https://play.googleapis.com', \
'https://www.googleapis.com/experimentsandconfigs/v1/getExperimentsAndConfigs', \
'https://ssl.google-analytics.com', \
'https://g.tenor.com/v1/categories?key=', \
'https://www.google.com/m/voice-search/down?pair=', \
'https://www.google.com/m/voice-search/up?pair=', \
'https://playatoms-pa.googleapis.com/v1/archiveDownload', \
'https://www.google.com/complete/search', \
'https://mobilenetworkscoring-pa.googleapis.com/v1/GetWifiQuality', \
'https://www.googleapis.com/plus/v2whitelisted/people/me', \
'https://www.gstatic.com/android/keyboard', \
'https://firebaseremoteconfig.googleapis.com']

userAgents = ['Android-GCM']

partialUserAgents = ['Android-GData', \
'Android-Finsky', \
'AndroidDownloadManager', \
'Chrome', \
'GoogleMobile', \
'Crashlytics', \
'com.android.vending']

appIds = {'1:1086610230652:android:131e4c3db28fca84':'com.google.android.googlequicksearchbox', \
'1:493454522602:android:4877c2b5f408a8b2':'com.google.android.apps.maps', \
'1:206908507205:android:167bd0ff59cd7d44':'com.google.android.apps.tachyon', \
'1:531457836147:android:0fb36a1600ce546b':'com.google.android.apps.photos', \
'1:933360113277:android:2918df7f0aab10ef':'com.reddit.frontpage', \
'1:508767403424:android:7c2619785291111d':'com.slack', \
'1:162066849712:android:db38e83be74de1b6':'com.discord', \
'1:494597445014:android:779d79f75183bf65':'com.spotify.music', \
'1:966004744864:android:23a3da72f34a80d2':'com.venmo', \
'1:191083992402:android:b773719be4662429':'com.instructure.candroid', \
'1:227709821840:android:581824269584ae5c':'com.hulu.plus', \
'1:484286080282:android:7eb516d49bb4ad11':'com.netflix.mediaclient'}

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
			results.append(Result.Result(flow, type, info))
		elif (headers['User-Agent'][:10] == 'DroidGuard'):
			flow.source = 'DroidGuard'
		elif (headers['User-Agent'][:14] == 'Android-Finsky' and flow.source == ''):
			flow.source = 'Google Play Store'
		elif (headers['User-Agent'].find('Chrome') > -1 and flow.source == ''):
			if ('referer' in headers.keys() and headers['referer'].find('android-app://com.google.android.googlequicksearchbox') == 0):
				flow.source = 'News Feed Article'
			else:
				flow.source = 'Google Chrome'
		elif (headers['User-Agent'][:11] == 'Crashlytics'):
			flow.source = 'Crashlytics'
	
	if ('authorization' in headers.keys()):
		type = 'User Info: Authorization Token'
		info = flow.requestHeaders['authorization']
		results.append(Result.Result(flow, type, info))

	if ('X-CRASHLYTICS-DEVICE-MODEL' in headers.keys()):
		type = 'System Info: Model'
		info = headers['X-CRASHLYTICS-DEVICE-MODEL']
		results.append(Result.Result(flow, type, info))

	if ('X-CRASHLYTICS-OS-DISPLAY-VERSION' in headers.keys()):
		type = 'System Info: OS Version'
		info = headers['X-CRASHLYTICS-OS-DISPLAY-VERSION']
		results.append(Result.Result(flow, type, info))

	if ('X-CRASHLYTICS-INSTALLATION-ID' in headers.keys()):
		type = 'System Info: Crashlytics ID'
		info = headers['X-CRASHLYTICS-INSTALLATION-ID']
		results.append(Result.Result(flow, type, info))

def checkResponseHeaders(flow, headers, results):
	return None

def checkGetURL(flow, results):
	#WiFi connectivity check
	if (flow.url == 'http://connectivitycheck.gstatic.com/generate_204' or flow.url == 'https://connectivitycheck.gstatic.com/generate_204'):
		flow.source = 'WiFi Connection'
		type = 'System Status'
		info = 'WiFi connection active'
		results.append(Result.Result(flow, type, info))
	
	#Google Ping
	elif (flow.url == 'https://www.google.com/generate_204'):
		flow.source = 'Google service ping'
	elif (flow.url == 'http://www.google.com/gen_204'):
		flow.source = 'Google service ping'
	
	elif (flow.url.find('https://android.clients.google.com/gsync') > -1):
		flow.source = 'Google Account Data Sync'
		type = 'System Info: GCM ID'
		info = flow.requestContent[flow.requestContent.find('gcm://?regId=')+13:flow.requestContent.find('&androidId=')]
		results.append(Result.Result(flow, type, info))
		
		type = 'System Info: Android ID'
		info = flow.requestContent[flow.requestContent.find('&androidId=')+11:flow.requestContent.find('\n')]
		results.append(Result.Result(flow, type, info))
	
	elif (flow.url.find('preloads?doc=android.autoinstalls.config.') > -1):
		flow.source = 'App Preloader'
		type = 'System Info: Build'
		info = flow.requestContent
		info = info[info.find('build_fingerprint:')+19:]
		info = info[:info.find('\n')]
		info = info.strip()
		results.append(Result.Result(flow, type, info))

	elif (flow.url.find('https://www.google.com/complete/search') > -1):
		flow.source = 'Google Search History Sync'

	elif (flow.url.find('https://app-measurement.com') == 0):
		flow.source = 'App Measurement'
		type = 'System Info: Application'
		info = flow.url[flow.url.find('app/')+4:flow.url.find('?')]
		info = AppDefault.fixUrlEncoding(info)
		if (info in appIds.keys()):
			info = appIds[info]
		results.append(Result.Result(flow, type, info))

		type = 'System Info: App Instance ID'
		info = flow.requestContent
		info = info[info.find('app_instance_id:')+17:]
		info = info[:info.find('\n')].strip()
		results.append(Result.Result(flow, type, info))
	
	elif (flow.url.find('https://www.googleapis.com/userlocation/v1/settings') == 0):
		flow.source = 'Android Location Settings Sync'
		type = 'System Info: Model'
		info = AppDefault.findFormEntry(flow.requestContent, 'brand') + ' ' + AppDefault.findFormEntry(flow.requestContent, 'model')
		results.append(Result.Result(flow, type, info))
		
		type = 'System Info: Build'
		info = AppDefault.findFormEntry(flow.requestContent, 'platform')
		results.append(Result.Result(flow, type, info))

	elif (flow.url.find('https://www.googleapis.com/userlocation/v1/reports') == 0):
		flow.source = 'Location Report'
		type = 'Location Info'
		info = flow.requestContent
		results.append(Result.Result(flow, type, info))

	elif (flow.url[:27] == 'https://play.googleapis.com'):
		flow.source = 'Google Play Store'

	elif (flow.url[:38] == 'https://g.tenor.com/v1/categories?key='):
		flow.source = 'Tenor GIF Keyboard'

	elif (flow.url.find('https://playatoms-pa.googleapis.com/v1/archiveDownload') == 0):
		flow.source = 'Google Play Store Download'

	elif (flow.url.find('https://www.google.com/complete/search') == 0):
		flow.source = 'Google Search History Sync'

	elif (flow.url == 'https://clients3.google.com/generate_204'):
		flow.source = 'Google Connectivity Check'

	elif (flow.url.find('https://www.googleapis.com/plus/v2whitelisted/people/me') == 0):
		flow.source = 'Google Friends Lookup'

	elif (flow.url.find('https://www.gstatic.com/android/keyboard') == 0):
		flow.source = 'Android Keyboard'

def checkPostURL(flow, results):
	#Weather lookup
	if (flow.url.find('www.google.com/tg/fe/request?rqt=58') > -1):
		flow.source = 'Weather/News Update'
		#type = 'Location'
		#info = ''
		#results.append(Result.Result(flow, type, info))
	
	elif (flow.url.find('https://www.googleapis.com/androidantiabuse/v1/x/create?') > -1):
		flow.source = 'DroidGuard'
		type = 'System Info: Bootloader'
		info = flow.requestContent[flow.requestContent.find('BOOTLOADER'):]
		info = info[:info.find('\n')]
		info = AppDefault.cleanEncoding(info)
		info = info.strip()
		info = info[10:]
		results.append(Result.Result(flow, type, info))
		
		type = 'System Info: Brand'
		info = flow.requestContent[flow.requestContent.find('BRAND'):]
		info = info[:info.find('\n')]
		info = AppDefault.cleanEncoding(info)
		info = info[5:]
		info = info.strip()
		results.append(Result.Result(flow, type, info))
		
		type = 'System Info: Model'
		info = flow.requestContent[flow.requestContent.find('MODEL'):]
		info = info[:info.find('\n')]
		info = AppDefault.cleanEncoding(info)
		info = info[5:]
		info = info.strip()
		results.append(Result.Result(flow, type, info))
		
		type = 'System Info: Serial Number'
		info = flow.requestContent[flow.requestContent.find('SERIAL'):]
		info = info[:info.find('\n')]
		info = AppDefault.cleanEncoding(info)
		info = info[6:]
		info = info.strip()
		results.append(Result.Result(flow, type, info))

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
				results.append(Result.Result(flow, type, info))
		if (flow.responseContent.find('adwords:enable_primes_network_monitoring') > -1):
			temp = flow.responseContent[flow.responseContent.find('1: adwords:enable_primes_network_monitoring'):]
			temp = temp[temp.find('2:')+3:]
			temp = temp[:temp.find('\n')]
			if (temp == 'true'):
				type = 'System Status: Network Monitoring'
				info = 'Android network activity is being monitored'
				results.append(Result.Result(flow, type, info))
		if (flow.responseContent.find('adwords:enable_primes_timing_monitoring') > -1):
			temp = flow.responseContent[flow.responseContent.find('1: adwords:enable_primes_timing_monitoring'):]
			temp = temp[temp.find('2:')+3:]
			temp = temp[:temp.find('\n')]
			if (temp == 'true'):
				type = 'System Status: Timing Monitoring'
				info = 'Android timing is being monitored'
				results.append(Result.Result(flow, type, info))
		if (flow.responseContent.find('adwords:enable_silent_feedback') > -1):
			temp = flow.responseContent[flow.responseContent.find('1: adwords:enable_silent_feedback'):]
			temp = temp[temp.find('2:')+3:]
			temp = temp[:temp.find('\n')]
			if (temp == 'true'):
				type = 'System Status: Silent Feedback'
				info = 'Silent feedback is enabled'
				results.append(Result.Result(flow, type, info))

	#Location pull
	elif (flow.url.find('https://www.googleapis.com/geolocation') > -1):
		flow.source = 'Google APIs'
		type = 'Location: Cell Towers'
		info = flow.requestContent
		info = info[info.find('"cellTowers": ['):]
		info = info[:info.find(']')+1]
		results.append(Result.Result(flow, type, info))
		
		type = 'Location: WiFi Access Points'
		info = flow.requestContent
		info = info[info.find('"wifiAccessPoints": ['):]
		info = info[:info.find(']')+1]
		results.append(Result.Result(flow, type, info))
		
		type = 'Location: Request Key'
		info = flow.url[flow.url.find('key=')+4:]
		results.append(Result.Result(flow, type, info))
	
	elif (flow.url.find('https://app-measurement.com') == 0):
		flow.source = 'App Measurement'

		if (flow.url == 'https://app-measurement.com/a'):
			cleaned = AppDefault.cleanEncoding(flow.requestContent)
			if (cleaned.find('app_launched') > -1):
				type = 'User Action: App Launched'
				info = cleaned[cleaned.find('(1:')+1:]
				info = info[:40]
				if (info in appIds.keys()):
					info = appIds[info]
				results.append(Result.Result(flow, type, info))
			if (cleaned.find('app_open') > -1):
				type = 'System Info: App Open'
				info = cleaned[cleaned.find(':android:')-14:]
				info = info[:39]
				if (info in appIds.keys()):
					info = appIds[info]
				results.append(Result.Result(flow, type, info))

			if (flow.requestContent.find('com.instructure.candroid') > -1):
				if (flow.requestContent.find('FindSchoolActivity') > -1):
					type = 'User Action: Canvas'
					info = 'School Search'
					results.append(Result.Result(flow, type, info))

				if (flow.requestContent.find('SignInActivity') > -1):
					type = 'User Action: Canvas'
					info = 'Sign In'
					results.append(Result.Result(flow, type, info))

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
		elif (AppDefault.findFormEntry(flow.requestContent, 'app') == 'com.google.android.apps.tachyon'):
			flow.source = 'Google Duo Login'
		
		type = 'System Info: Android ID'
		info = AppDefault.findFormEntry(flow.requestContent, 'androidId')
		results.append(Result.Result(flow, type, info))
		
		type = 'System Info: Country'
		info = AppDefault.findFormEntry(flow.requestContent, 'device_country')
		results.append(Result.Result(flow, type, info))
		
		type = 'System Info: Language'
		info = AppDefault.findFormEntry(flow.requestContent, 'lang')
		results.append(Result.Result(flow, type, info))
		
		type = 'User Info: Email Address'
		info = AppDefault.findFormEntry(flow.requestContent, 'Email')
		results.append(Result.Result(flow, type, info))
		
		type = 'System Info: Android Client Signature'
		info = AppDefault.findFormEntry(flow.requestContent, 'client_sig')
		results.append(Result.Result(flow, type, info))
		
		type = 'System Info: Google Mobile Services Token'
		info = AppDefault.findFormEntry(flow.requestContent, 'Token')
		results.append(Result.Result(flow, type, info))

	elif (flow.url.find('https://www.googleapis.com/experimentsandconfigs/v1/getExperimentsAndConfigs') == 0):
		flow.source = 'Experimental Features Config Sync'

	elif (flow.url.find('https://ssl.google-analytics.com') == 0):
		flow.source = 'Google Analytics'

		if (AppDefault.findFormEntry(flow.requestContent, 'cd').find('com.google.android.apps.contacts') > -1 \
			and AppDefault.findFormEntry(flow.requestContent, 't') == 'screenview'):
			type = 'User Action'
			info = 'Viewing Contacts'
			results.append(Result.Result(flow, type, info))

		elif (AppDefault.findFormEntry(flow.requestContent, 'utc') == 'Create reminder'):
			type = 'User Action'
			info = 'Google Calendar Reminder Created'
			results.append(Result.Result(flow, type, info))

	elif (flow.url == 'https://android.googleapis.com/auth/devicekey'):
		flow.source = 'Google Mobile Services'
		type = 'System Info: Device Key'
		info = flow.requestContent
		results.append(Result.Result(flow, type, info))

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
			results.append(Result.Result(flow, type, info))

			type = 'User Info: Email Address'
			info = account[account.find('"display_email":')+17:]
			info = info[:info.find('"')]
			results.append(Result.Result(flow, type, info))

			type = 'User Info: Account ID'
			info = account[account.find('"obfuscated_id":')+17:]
			info = info[:info.find('"')]
			results.append(Result.Result(flow, type, info))

	elif (flow.url == 'https://www.googleapis.com/cryptauth/v1/deviceSync/getmydevices'):
		flow.source = 'Google Account Device Lookup'

	elif (flow.url.find('https://www.google.com/m/voice-search/down?pair=') == 0 \
		or flow.url.find('https://www.google.com/m/voice-search/up?pair=') == 0):
		flow.source = 'Google Assistant'
		type = 'System Info: Assistant Pair ID'
		info = AppDefault.findFormEntry(flow.requestContent, 'pair')
		results.append(Result.Result(flow, type, info))

	elif (flow.url == 'https://www.google.com/tg/fe/request?rqt=98&bq=0'):
		flow.source = 'Assistant Weather Card'
		type = 'Location'
		info = AppDefault.cleanEncoding(flow.responseContent)
		info = info[info.find(' in ')+4:]
		info = info[:info.find('\\')-1]
		results.append(Result.Result(flow, type, info))

	elif (flow.url == 'https://www.google.com/loc/m/api'):
		flow.source = 'Google Location API'
		type = 'Location'
		info = 'Location'
		results.append(Result.Result(flow, type, info))

	elif (flow.url.find('https://mobilenetworkscoring-pa.googleapis.com/v1/GetWifiQuality') == 0):
		flow.source = 'WiFi Strength Query'
		type = 'System Info: WiFi Strength'
		info = 'Key: ' + flow.url[flow.url.find('key=')+4:]
		results.append(Result.Result(flow, type, info))

	elif (flow.url.find('https://firebaseremoteconfig.googleapis.com') == 0):
		flow.source = 'Firebase'
		if (flow.requestContent.find('"packageName":') > -1):
			appName = flow.requestContent[flow.requestContent.find('"packageName":')+16:]
			appName = appName[:appName.find('"')]
			flow.source = flow.source + ' ' + appName

			type = 'Firebase ' + appName + ' Instance ID'
			info = flow.requestContent[flow.requestContent.find('"appInstanceId":')+18:]
			info = info[:info.find('"')]
			results.append(Result.Result(flow, type, info))


def getURLs():
	return urls

