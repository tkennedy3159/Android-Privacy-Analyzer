import AndroidDataPrivacy.Flow as Flow
import AndroidDataPrivacy.Result as Result
import AndroidDataPrivacy.Applications.AppDefault as AppDefault

urls = []

partialURLs = ['https://venmopics.appspot.com', \
'https://api.venmo.com']

userAgents = []

partialUserAgents = ['Venmo']

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
		if (headers['User-Agent'].find('Venmo') == 0 and flow.source == ''):
			flow.source = 'Venmo'

	if ('device-id' in headers.keys()):
		type = 'Venmo Device ID'
		info = headers['device-id']
		results.append(Result.Result(flow, type, info))

	if 'VENMO-OTP-SECRET' in headers.keys():
		type = 'Venmo OTP Secret'
		info = headers['VENMO-OTP-SECRET']
		results.append(Result.Result(flow, type, info))

def checkResponseHeaders(flow, headers, results):
	return None

def checkGetURL(flow, results):
	if (flow.url.find('https://api.venmo.com/v1/stories/target-or-actor') == 0):
		flow.source = 'Venmo Stories Sync'

	elif (flow.url.find('https://api.venmo.com/v1/stories') == 0 and flow.url.find('target-or-actor') == -1):
		type = 'User Action: Viewed Story'
		info = flow.url[flow.url.find('stories/')+8:]
		results.append(Result.Result(flow, type, info))

	elif (flow.url == 'https://api.venmo.com/v1/account/two-factor/token'):
		flow.source = 'Venmo Login'

		type = 'User Info: 2FA Device'
		info = AppDefault.findJSONListNonSpaced(flow.responseContent, 'devices')
		results.append(Result.Result(flow, type, info))

	elif (flow.url == 'https://api.venmo.com/v1/account'):
		flow.source = 'Venmo Account Sync'

		type = 'User Info: Venmo ID'
		info = flow.responseContent[flow.responseContent.find('"id":')+7:]
		info = info[:info.find('"')]
		results.append(Result.Result(flow, type, info))

		type = 'User Info: Venmo Account Creation Time'
		info = flow.responseContent[flow.responseContent.find('"date_joined":')+16:]
		info = info[:info.find('"')]
		results.append(Result.Result(flow, type, info))

		type = 'System Info: Phone Number'
		info = flow.responseContent[flow.responseContent.find('"phone":')+10:]
		info = info[:info.find('"')]
		results.append(Result.Result(flow, type, info))

		type = 'User Info: Email Address'
		info = flow.responseContent[flow.responseContent.find('"email":')+10:]
		info = info[:info.find('"')]
		results.append(Result.Result(flow, type, info))

		type = 'User Info: Venmo Zendesk ID'
		info = flow.responseContent[flow.responseContent.find('"zendesk_identifier":')+23:]
		info = info[:info.find('"')]
		results.append(Result.Result(flow, type, info))

	elif (flow.url.find('https://api.venmo.com/v1/notifications') == 0):
		type = 'User Action: Venmo'
		info = 'Checked Notifications'
		results.append(Result.Result(flow, type, info))

	elif (flow.url.find('https://api.venmo.com/v1/users?query=') == 0):
		type = 'User Action: Venmo Search'
		info = AppDefault.findFormEntry(flow.requestContent, 'query')
		results.append(Result.Result(flow, type, info))

	elif (flow.url.find('https://api.venmo.com/v1/users') == 0 and flow.url.find('/friends') == -1):
		type = 'User Action: Viewed Profile'
		info = flow.responseContent[flow.responseContent.find('"display_name":')+17:]
		info = info[:info.find('"')]
		results.append(Result.Result(flow, type, info))

	elif (flow.url.find('https://api.venmo.com/v1/users') == 0 and flow.url.find('/friends') > -1):
		type = 'User Action: Viewed Friends of Profile'
		info = flow.url[flow.url.find('/users/')+7:]
		info = info[:info.find('/')]
		results.append(Result.Result(flow, type, info))


def checkPostURL(flow, results):
	if (flow.url.find('https://api.venmo.com') == 0):
		flow.source = 'Venmo'

	if (flow.url == 'https://api.venmo.com/v1/oauth/access_token'):
		flow.source = 'Venmo Login'

		if (flow.requestContent.find('phone_email_or_username:') > -1):
			type = 'Venmo Username'
			info = AppDefault.findFormEntry(flow.requestContent, 'phone_email_or_username')
			results.append(Result.Result(flow, type, info))

		if (flow.requestContent.find('password:') > -1):
			type = 'Venmo Password'
			info = AppDefault.findFormEntry(flow.requestContent, 'password')
			results.append(Result.Result(flow, type, info))

		if (flow.responseContent.find('"access_token":') > -1):
			type = 'Venmo Access Token'
			info = flow.responseContent[flow.responseContent.find('"access_token":')+17:]
			info = info[:info.find('"')]
			results.append(Result.Result(flow, type, info))

		if (flow.responseContent.find('"id":') > -1):
			type = 'Venmo Access Token'
			info = flow.responseContent[flow.responseContent.find('"id":')+7:]
			info = info[:info.find('"')]
			results.append(Result.Result(flow, type, info))

	elif (flow.url == 'https://api.venmo.com/v1/account/two-factor/token'):
		flow.source = 'Venmo Login'
		type = 'User Action: 2FA Sent'
		info = AppDefault.findFormEntry(flow.requestContent, 'via')
		results.append(Result.Result(flow, type, info))

	elif (flow.url == 'https://api.venmo.com/v1/users/devices'):
		type = 'User Info: Location'
		info = flow.responseContent[flow.responseContent.find('"location":')+13:]
		info = info[:info.find('"')]
		results.append(Result.Result(flow, type, info))

		type = 'User Info: Venmo Client'
		info = flow.responseContent[flow.responseContent.find('"browser":')+12:]
		info = info[:info.find('"')]
		results.append(Result.Result(flow, type, info))

		type = 'System Info: Venmo ID'
		info = flow.responseContent[flow.responseContent.find('"id":')+7:]
		info = info[:info.find(',')]
		results.append(Result.Result(flow, type, info))

		type = 'User Action: Venmo Device Login Time'
		info = flow.responseContent[flow.responseContent.find('"created_at":')+15:]
		info = info[:info.find('"')]
		results.append(Result.Result(flow, type, info))

	elif (flow.url == 'https://api.venmo.com/v1/device-tokens/android'):
		type = 'System Info: Venmo Token'
		info = AppDefault.findFormEntry(flow.requestContent, 'device_token')
		results.append(Result.Result(flow, type, info))

	elif (flow.url == 'https://api.venmo.com/v1/contacts'):
		type = 'User Info: Contact'
		contacts = AppDefault.findJSONListNonSpaced(flow.requestContent, 'contacts')

		for info in contacts.split('            },\n            {'):
			results.append(Result.Result(flow, type, info))

	elif (flow.url == 'https://api.venmo.com/v1/payments'):
		type = 'User Action: Venmo Payment'
		info = flow.requestContent
		results.append(Result.Result(flow, type, info))

	elif (flow.url.find('https://api.venmo.com/v1/stories') == 0 and flow.url.find('/likes') > -1):
		type = 'User Action: Liked Story'
		info = flow.url[flow.url.find('stories/')+8:]
		info = info[:info.find('/')]
		results.append(Result.Result(flow, type, info))

	elif (flow.url.find('https://api.venmo.com/v1/stories') == 0 and flow.url.find('/comments') > -1):
		type = 'User Action: Commented on Story'
		info = flow.url[flow.url.find('stories/')+8:]
		info = info[:info.find('/')]
		info = info + ': ' + AppDefault.findFormEntry(flow.requestContent, 'message')
		results.append(Result.Result(flow, type, info))


def checkHeadURL(flow, results):
	return None

def checkPutURL(flow, results):
	return None

def checkDeleteURL(flow, results):
	if (flow.url.find('https://api.venmo.com/v1/requests') == 0):
		type = 'User Action: Delete Request'
		info = flow.url[flow.url.find('requests/')+9:]
		info = info[:info.find('/')]
		results.append(Result.Result(flow, type, info)) 
