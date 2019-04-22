import AndroidDataPrivacy.Flow as Flow
import AndroidDataPrivacy.Result as Result
import AndroidDataPrivacy.Applications.AppDefault as AppDefault

urls = []

partialURLs = ['https://www.linkedin.com', \
'https://platform.linkedin.com']

userAgents = []

partialUserAgents = ['com.linkedin.android']

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
	if 'User-Agent' in headers.keys():
		if (headers['User-Agent'].find('com.linkedin.android') > -1 and flow.source == ''):
			flow.source = 'LinkedIn'

	if ('x-li-track' in headers.keys()):
		type = 'System Info: OS Version'
		info = headers['x-li-track'][headers['x-li-track'].find('"osVersion":')+13:]
		info = info[:info.find('"')]
		results.append(Result.Result(flow, type, info))

		type = 'System Info: Model'
		info = headers['x-li-track'][headers['x-li-track'].find('"model":')+9:]
		info = info[:info.find('"')]
		results.append(Result.Result(flow, type, info))

		type = 'System Info: LinkedIn Version'
		info = headers['x-li-track'][headers['x-li-track'].find('"clientVersion":')+17:]
		info = info[:info.find('"')]
		results.append(Result.Result(flow, type, info))

	if ('x-udid' in headers.keys()):
		type = 'System Info: Device ID'
		info = headers['x-udid']
		results.append(Result.Result(flow, type, info))

	if ('csrf-token' in headers.keys()):
		type = 'LinkedIn Session ID'
		info = headers['csrf-token']
		results.append(Result.Result(flow, type, info))


def checkResponseHeaders(flow, headers, results):
	return None

def checkGetURL(flow, results):
	if (flow.url.find('https://www.linkedin.com') == 0 or flow.url.find('https://platform.linkedin.com') == 0):
		flow.source = 'LinkedIn'

	if (flow.url.find('https://www.linkedin.com/voyager/api/feed/updates') == 0):
		flow.source = 'LinkedIn Feed Update'
		type = 'System Info: Battery Level'
		info = AppDefault.findFormEntry(flow.requestContent, 'battery')
		results.append(Result.Result(flow, type, info))

		type = 'System Info: Connection Type'
		info = AppDefault.findFormEntry(flow.requestContent, 'connectionType')
		results.append(Result.Result(flow, type, info))


def checkPostURL(flow, results):
	if (flow.url.find('https://www.linkedin.com') == 0):
		flow.source = 'LinkedIn'

	if (flow.url.find('https://www.linkedin.com/li/track') == 0):
		flow.source = 'LinkedIn Tracker'

		if (flow.requestContent.find('"advertiserId":') > -1):
			type = 'Ad ID'
			info = flow.requestContent[flow.requestContent.find('"advertiserId":')+17:]
			info = info[:info.find('"')]
			results.append(Result.Result(flow, type, info))

		if (flow.requestContent.find('"appState":') > -1):
			type = 'System Info: LinkedIn App State'
			info = flow.requestContent[flow.requestContent.find('"appState":')+13:]
			info = info[:info.find('"')]
			results.append(Result.Result(flow, type, info))

		if (flow.requestContent.find('"connectionType":') > -1):
			type = 'System Info: Connection Type'
			info = flow.requestContent[flow.requestContent.find('"connectionType":')+19:]
			info = info[:info.find('"')]
			results.append(Result.Result(flow, type, info))

		if (flow.requestContent.find('"deviceModel":') > -1):
			type = 'System Info: Model'
			info = flow.requestContent[flow.requestContent.find('"deviceModel":')+16:]
			info = info[:info.find('"')]
			results.append(Result.Result(flow, type, info))

		if (flow.requestContent.find('"osVersion":') > -1):
			type = 'System Info: OS Version'
			info = flow.requestContent[flow.requestContent.find('"osVersion":')+14:]
			info = info[:info.find('"')]
			results.append(Result.Result(flow, type, info))

		if (flow.requestContent.find('clientEventStats') > -1):
			type = 'LinkedIn Client Event Stats'
			for info in AppDefault.findJSONListNonSpaced(flow.requestContent, 'clientEventStats').split('                    },\n                    {'):
				results.append(Result.Result(flow, type, info))

		body = flow.requestContent
		type = 'LinkedIn Client Event'
		while body.find('"eventBody":') > -1:
			body = body[body.find('"eventBody":'):]
			#info = AppDefault.findJSONSection(body, 'eventBody')
			info = body[:body.find('        {\n            "eventBody":')]
			results.append(Result.Result(flow, type, info))
			body = body[20:]

	elif (flow.url.find('https://www.linkedin.com/uas/authenticate') == 0):
		flow.source = 'LinkedIn Login'

		type = 'User Info: Username'
		info = AppDefault.findFormEntry(flow.requestContent, 'session_key')
		results.append(Result.Result(flow, type, info))

		type = 'User Info: Password'
		info = AppDefault.findFormEntry(flow.requestContent, 'session_password')
		results.append(Result.Result(flow, type, info))

		type = 'LinkedIn Session ID'
		info = AppDefault.findFormEntry(flow.requestContent, 'JSESSIONID')
		results.append(Result.Result(flow, type, info))

	elif (flow.url.find('https://www.linkedin.com/voyager/api/pushRegistration') == 0):
		if (flow.requestContent.find('"pushNotificationTokens":') > -1):
			type = 'LinkedIn Push Notification Token'
			if (AppDefault.findJSONListNonSpaced(flow.requestContent, 'pushNotificationTokens').find(',') > -1):
				for info in AppDefault.findJSONListNonSpaced(flow.requestContent, 'pushNotificationTokens').split(','):
					info = info.strip()
					info = info[1:len(info)-1]
			else:
				info = AppDefault.findJSONListNonSpaced(flow.requestContent, 'pushNotificationTokens')
				info = info[1:len(info)-1]
				info = info.strip()
				info = info[1:len(info)-1]
			results.append(Result.Result(flow, type, info))

	elif (flow.url.find('https://www.linkedin.com/voyager/api/growth/contacts?action=uploadContacts') == 0):
		flow.source = 'LinkedIn Contacts Upload'

		type = 'User Info: Contact'
		for info in flow.requestContent.split('            },\n            {'):
			if (info.find('"fullName":') > -1):
				results.append(Result.Result(flow, type, info))


def checkHeadURL(flow, results):
	return None

def checkPutURL(flow, results):
	return None

def checkDeleteURL(flow, results):
	return None
