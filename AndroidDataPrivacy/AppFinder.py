import AndroidDataPrivacy.Flow as Flow
import AndroidDataPrivacy.Result as Result

def findApp(flow, appList):
	app = ''
	if ('app' in flow.requestHeaders.keys()):
		app = flow.requestHeaders['app']
	if (app == '' and 'User-Agent' in flow.requestHeaders.keys()):
		app = identifyUserAgent(flow.requestHeaders['User-Agent'], appList)
	if (app == ''):
		app = identifyURL(flow, flow.url, appList)
	if (app == '' and 'referer' in flow.requestHeaders):
		app = identifyReferer(flow.requestHeaders['referer'], appList)
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

	if 'GSuite' in appList:
		import AndroidDataPrivacy.Applications.GSuite as GSuite
		if agent in GSuite.userAgents:
			return 'GSuite'
		for item in GSuite.partialUserAgents:
			if (agent.find(item) > -1):
				return 'GSuite'

	if 'Youtube' in appList:
		import AndroidDataPrivacy.Applications.Youtube as Youtube
		if agent in Youtube.userAgents:
			return 'Youtube'
		for item in Youtube.partialUserAgents:
			if (agent.find(item) > -1):
				return 'Youtube'

	if 'Reddit' in appList:
		import AndroidDataPrivacy.Applications.Reddit as Reddit
		if agent in Reddit.userAgents:
			return 'Reddit'
		for item in Reddit.partialUserAgents:
			if (agent.find(item) > -1):
				return 'Reddit'

	if 'Slack' in appList:
		import AndroidDataPrivacy.Applications.Slack as Slack
		if agent in Slack.userAgents:
			return 'Slack'
		for item in Slack.partialUserAgents:
			if (agent.find(item) > -1):
				return 'Slack'

	if 'CertInstaller' in appList:
		import AndroidDataPrivacy.Applications.CertInstaller as CertInstaller
		if agent in CertInstaller.userAgents:
			return 'CertInstaller'
		for item in CertInstaller.partialUserAgents:
			if (agent.find(item) > -1):
				return 'CertInstaller'

	return ''

def identifyURL(flow, url, appList):
	if 'AndroidNative' in appList:
		import AndroidDataPrivacy.Applications.AndroidNative as AndroidNative
		if url in AndroidNative.urls:
			return 'AndroidNative'
		for item in AndroidNative.partialURLs:
			if (url.find(item) > -1):
				return 'AndroidNative'

	if 'GSuite' in appList:
		import AndroidDataPrivacy.Applications.GSuite as GSuite
		if url in GSuite.urls:
			return 'GSuite'
		for item in GSuite.partialURLs:
			if (url.find(item) > -1):
				return 'GSuite'

	if 'Youtube' in appList:
		import AndroidDataPrivacy.Applications.Youtube as Youtube
		if url in Youtube.urls:
			return 'Youtube'
		for item in Youtube.partialURLs:
			if (url.find(item) > -1):
				return 'Youtube'

	if 'Reddit' in appList:
		import AndroidDataPrivacy.Applications.Reddit as Reddit
		if url in Reddit.urls:
			return 'Reddit'
		for item in Reddit.partialURLs:
			if (url.find(item) > -1):
				return 'Reddit'

	if 'Slack' in appList:
		import AndroidDataPrivacy.Applications.Slack as Slack
		if url in Slack.urls:
			return 'Slack'
		for item in Slack.partialURLs:
			if (url.find(item) > -1):
				return 'Slack'

	if 'CertInstaller' in appList:
		import AndroidDataPrivacy.Applications.CertInstaller as CertInstaller
		if url in CertInstaller.urls:
			return 'CertInstaller'
		for item in CertInstaller.partialURLs:
			if (url.find(item) > -1):
				return 'CertInstaller'

	if (url[:21] == 'https://api.branch.io'):
		temp = flow.requestContent
		temp = temp[temp.find('"cd": {'):]
		temp = temp[:temp.find('}')]
		temp = temp[temp.find('"pn": "')+7:]
		temp = temp[:temp.find('"')]
		if (temp[:10] == 'com.reddit'):
			return 'Reddit'

	return ''

def identifyReferer(referer, appList):
	if (referer == 'android-app://com.google.android.gm'):
		return 'com.google.android.gm'
	return ''

def translate(app):
	if (app == 'com.google.android.apps.messaging' \
	or app == 'com.google.android.googlequicksearchbox' \
	or app == 'com.google.android.gms' \
	or app == 'com.google.android.gm' \
	or app == 'com.android.vending'):
		app = 'AndroidNative'

	elif (app == 'com.google.android.apps.tachyon' \
	or app == 'com.google.android.calendar' \
	or app == 'com.google.android.contacts' \
	or app == 'com.google.android.apps.maps' \
	or app == 'com.google.android.apps.photos' \
	or app == 'com.google.android.talk' \
	or app == 'com.google.android.apps.docs'):
		app = 'GSuite'

	elif (app == 'com.reddit.frontpage'):
		app = 'Reddit'

	elif (app == 'com.google.android.youtube'):
		app = 'Youtube'

	if (app == ''):
		app = 'AppDefault'
	return app
