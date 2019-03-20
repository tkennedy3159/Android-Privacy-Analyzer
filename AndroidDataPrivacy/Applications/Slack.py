import base64
import AndroidDataPrivacy.Flow as Flow
import AndroidDataPrivacy.Result as Result
import AndroidDataPrivacy.Applications.AppDefault as AppDefault

urls = ['https://sessions.bugsnag.com/', \
'https://slack.com/beacon/track/']

partialURLs = ['https://slack.com/api', \
'https://wss-mobile.slack.com']

userAgents = ['']

partialUserAgents = ['slack']

def checkBehavior(flow, results):
	if (flow.requestType == 'GET'):
		analyzeGetRequest(flow, results)
	if (flow.requestType == 'POST'):
		analyzePostRequest(flow, results)
	if (flow.requestType == 'HEAD'):
		analyzePostRequest(flow, results)
	if (flow.requestType == 'PUT'):
		analyzePutRequest(flow, results)
	if (flow.requestType == 'DELETE'):
		analyzeDeleteRequest(flow, results)

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

def analyzeHeadRequest(flow, results):
	checkHeadURL(flow, results)
	checkRequestHeaders(flow, flow.requestHeaders, results)
	AppDefault.checkRequestHeadersDefault(flow, flow.requestHeaders, results)
	checkResponseHeaders(flow, flow.responseHeaders, results)
	AppDefault.checkResponseHeadersDefault(flow, flow.responseHeaders, results)
	AppDefault.analyzeHeadRequestDefault(flow, results)

def analyzePutRequest(flow, results):
	checkPutURL(flow, results)
	checkRequestHeaders(flow, flow.requestHeaders, results)
	AppDefault.checkRequestHeadersDefault(flow, flow.requestHeaders, results)
	checkResponseHeaders(flow, flow.responseHeaders, results)
	AppDefault.checkResponseHeadersDefault(flow, flow.responseHeaders, results)
	AppDefault.analyzePutRequestDefault(flow, results)

def analyzeDeleteRequest(flow, results):
	checkDeleteURL(flow, results)
	checkRequestHeaders(flow, flow.requestHeaders, results)
	AppDefault.checkRequestHeadersDefault(flow, flow.requestHeaders, results)
	checkResponseHeaders(flow, flow.responseHeaders, results)
	AppDefault.checkResponseHeadersDefault(flow, flow.responseHeaders, results)
	AppDefault.analyzeDeleteRequestDefault(flow, results)

def checkRequestHeaders(flow, headers, results):
	if ('User-Agent' in headers.keys()):
		if (headers['User-Agent'][:5] == 'slack' and flow.source == ''):
			flow.source = 'Slack'

	if ('uuid' in headers.keys()):
		type = 'Slack UUID'
		info = headers['uuid']
		results.append(Result.Result(flow, type, info))

def checkResponseHeaders(flow, headers, results):
	if ('x-slack-req-id' in headers.keys()):
		type = 'Slack Req ID'
		info = flow.responseHeaders['x-slack-req-id']
		results.append(Result.Result(flow, type, info))

def checkGetURL(flow, results):
	if (flow.url.find('https://wss-mobile.slack.com') == 0):
		flow.source = 'Slack'

		if (len(AppDefault.findFormEntry(flow.requestContent, 'token')) > 25):
			type = 'Slack Token'
			info = AppDefault.findFormEntry(flow.requestContent, 'token')
			#results.append(Result.Result(flow, type, info))

		if (len(AppDefault.findFormEntry(flow.requestContent, 'push_token')) > 25):
			type = 'Slack Push Token'
			info = AppDefault.findFormEntry(flow.requestContent, 'push_token')
			#results.append(Result.Result(flow, type, info))

def checkPostURL(flow, results):
	if (flow.url.find('https://slack.com/api') == 0):
		flow.source = 'Slack'

		if (len(AppDefault.findFormEntry(flow.requestContent, 'token')) > 25):
			type = 'Slack Token'
			info = AppDefault.findFormEntry(flow.requestContent, 'token')
			results.append(Result.Result(flow, type, info))

		if (len(AppDefault.findFormEntry(flow.requestContent, 'push_token')) > 25):
			type = 'Slack Push Token'
			info = AppDefault.findFormEntry(flow.requestContent, 'push_token')
			results.append(Result.Result(flow, type, info))

	if (flow.url == 'https://slack.com/api/experiments.getByVisitor'):
		type = 'System Info: Slack Experiments'
		info = flow.responseContent
		results.append(Result.Result(flow, type, info))

	elif (flow.url == 'https://sessions.bugsnag.com/'):
		if ('Bugsnag-Api-Key' in flow.requestHeaders.keys()):
			type = 'Bugsnag API Key'
			info = flow.requestHeaders['Bugsnag-Api-Key']
			results.append(Result.Result(flow, type, info))

		if (AppDefault.findJSONItem(flow.requestContent, 'packageName') == 'com.Slack'):
			flow.source = 'Slack Bugsnag'

			type = 'Current Slack Screen'
			info = AppDefault.findJSONItem(flow.requestContent, 'activeScreen')
			results.append(Result.Result(flow, type, info))

			type = 'Slack Foreground Status'
			info = AppDefault.findJSONItem(flow.requestContent, 'inForeground')
			results.append(Result.Result(flow, type, info))

			type = 'Slack Session ID'
			info = AppDefault.findJSONItem(AppDefault.findJSONGroup(flow.requestContent, 'sessions'), 'id')
			results.append(Result.Result(flow, type, info))

			type = 'User Info: Slack User ID'
			info = AppDefault.findJSONItem(AppDefault.findJSONGroup(AppDefault.findJSONGroup(flow.requestContent, 'sessions'), 'user'), 'id')
			results.append(Result.Result(flow, type, info))

			type = 'Session Start Time'
			info = AppDefault.findJSONItem(AppDefault.findJSONGroup(flow.requestContent, 'sessions'), 'startedAt') + ' UTC'
			results.append(Result.Result(flow, type, info))

			type = 'System Info: Model'
			make = AppDefault.findJSONItem(flow.requestContent, 'manufacturer')
			model = AppDefault.findJSONItem(flow.requestContent, 'model')
			info = make + ' ' + model
			results.append(Result.Result(flow, type, info))

			type = 'System Info: OS Version'
			info = AppDefault.findJSONItem(flow.requestContent, 'osName') + ' ' + AppDefault.findJSONItem(flow.requestContent, 'osVersion')
			results.append(Result.Result(flow, type, info))

	elif (flow.url == 'https://slack.com/api/auth.findTeam'):
		type = 'User Action: Domain Lookup'
		info = AppDefault.findFormEntry(flow.requestContent, 'domain')
		results.append(Result.Result(flow, type, info))

	elif (flow.url == 'https://slack.com/api/auth.findUser'):
		type = 'User Action: Login'
		info = AppDefault.findFormEntry(flow.requestContent, 'email')
		results.append(Result.Result(flow, type, info))

		type = 'User Info: Slack User ID'
		info = AppDefault.findJSONItem(flow.responseContent, 'user_id')
		results.append(Result.Result(flow, type, info))

	elif (flow.url == 'https://slack.com/api/auth.signin'):
		type = 'User Info: Password'
		info = AppDefault.findFormEntry(flow.requestContent, 'password')
		results.append(Result.Result(flow, type, info))

		type = 'User Info: Slack User ID'
		info = AppDefault.findJSONItem(flow.responseContent, 'user')
		results.append(Result.Result(flow, type, info))

		type = 'User Info: Team ID'
		info =  AppDefault.findFormEntry(flow.requestContent, 'team')
		results.append(Result.Result(flow, type, info))

		type = 'Slack Token'
		info = AppDefault.findJSONItem(flow.responseContent, 'token')
		results.append(Result.Result(flow, type, info))

		type = 'User Info: Email'
		info = AppDefault.findJSONItem(flow.responseContent, 'user_email')
		results.append(Result.Result(flow, type, info))

	elif (flow.url == 'https://slack.com/api/users.counts'):
		channels = AppDefault.findJSONListNonSpaced(flow.responseContent, 'channels')
		channels = channels[2:]
		for channel in channels.split('},'):
			type = 'Slack Channel Info'
			info = channel
			results.append(Result.Result(flow, type, info))

	elif (flow.url == 'https://slack.com/api/conversations.history'):
		type = 'Channel Messages Sync'
		info = 'Channel: ' + AppDefault.findFormEntry(flow.requestContent, 'channel')
		results.append(Result.Result(flow, type, info))

	elif (flow.url == 'https://slack.com/beacon/track/'):
		type = 'System Info: Performance Tracking'
		info = AppDefault.findFormEntry(flow.requestContent, 'data')
		info = base64.b64decode(info)
		info = info.decode("UTF-8")
		results.append(Result.Result(flow, type, info))

	elif (flow.url == 'https://slack.com/api/chat.postMessage'):
		type = 'User Action: Send Message'
		info = 'Message "' + AppDefault.findFormEntry(flow.requestContent, 'text') + '" sent to channel ' + AppDefault.findFormEntry(flow.requestContent, 'channel')
		results.append(Result.Result(flow, type, info))

	elif (flow.url == 'https://slack.com/api/conversations.mark'):
		type = 'User Action: Viewed Channel'
		info = 'Viewed channel ' + AppDefault.findFormEntry(flow.requestContent, 'channel') + ' at ' + AppDefault.findFormEntry(flow.requestContent, 'ts')
		results.append(Result.Result(flow, type, info))

def checkHeadURL(flow, results):
	return None

def checkPutURL(flow, results):
	return None

def checkDeleteURL(flow, results):
	return None
