import AndroidDataPrivacy.Flow as Flow
import AndroidDataPrivacy.Result as Result

def findApp(flow, appList):
	app = ''
	if ('app' in flow.requestHeaders.keys()):
		app = flow.requestHeaders['app']
	if (app == '' and 'User-Agent' in flow.requestHeaders.keys()):
		app = identifyUserAgent(flow.requestHeaders['User-Agent'], appList)
	if (app == ''):
		app = identifyURL(flow.url, appList)
	app = translate(app)
	return app

def identifyUserAgent(agent, appList):
	if 'AndroidNative' in appList:
		import AndroidDataPrivacy.Applications.AndroidNative as AndroidNative
		if agent in AndroidNative.userAgents:
			return 'AndroidNative'
		for item in AndroidNative.partialUserAgents:
			if (agent.find(item) > -1):
				return 'AndroidNative'

	if 'Youtube' in appList:
		import AndroidDataPrivacy.Applications.Youtube as Youtube
		if agent in Youtube.userAgents:
			return 'Youtube'
		for item in Youtube.partialUserAgents:
			if (agent.find(item) > -1):
				return 'Youtube'

	return ''

def identifyURL(url, appList):
	if 'AndroidNative' in appList:
		import AndroidDataPrivacy.Applications.AndroidNative as AndroidNative
		if url in AndroidNative.urls:
			return 'AndroidNative'
		for item in AndroidNative.partialURLs:
			if (url.find(item) > -1):
				return 'AndroidNative'

	if 'Youtube' in appList:
		import AndroidDataPrivacy.Applications.Youtube as Youtube
		if url in Youtube.urls:
			return 'Youtube'
		for item in Youtube.partialURLs:
			if (url.find(item) > -1):
				return 'Youtube'

	return ''

def translate(app):
	if (app == 'com.google.android.apps.messaging' \
	or app == 'com.google.android.googlequicksearchbox' \
	or app == 'com.google.android.calendar' \
	or app == 'com.google.android.gms' \
	or app == 'com.google.android.gm' \
	or app == 'com.android.vending'):
		app = 'AndroidNative'
	if (app == ''):
		app = 'AppDefault'
	return app

