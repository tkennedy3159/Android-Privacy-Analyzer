import AndroidDataPrivacy.Flow as Flow
import AndroidDataPrivacy.Result as Result
import AndroidDataPrivacy.Applications.AppDefault as AppDefault

urls = []

partialURLs = ['https://cloud.rocket.chat', \
'https://open.rocket.chat']

userAgents = []

partialUserAgents = []

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
	if ('referer' in headers.keys()):
		type = 'Referer'
		info = headers['referer']
		results.append(Result.Result(flow, type, info))

def checkResponseHeaders(flow, headers, results):
	return None

def checkGetURL(flow, results):
	flow.source = 'RocketChat'

	if (flow.url.find('https://certify.alexametrics.com/atrk') == 0):
		type = 'RocketChat AlexaMetrics Session Cookie'
		info = AppDefault.findFormEntry(flow.requestContent, 'sess_cookie')
		results.append(Result.Result(flow, type, info))

	elif (flow.url.find('https://q.stripe.com/?event') == 0):
		type = 'Stripe Key'
		info = AppDefault.findFormEntry(flow.requestContent, 'key')
		results.append(Result.Result(flow, type, info))

		type = 'Stripe JS ID'
		info = AppDefault.findFormEntry(flow.requestContent, 'stripe_js_id')
		results.append(Result.Result(flow, type, info))

		type = 'Stripe Event'
		info = AppDefault.findFormEntry(flow.requestContent, 'event')
		results.append(Result.Result(flow, type, info))

	elif (flow.url.find('https://open.rocket.chat/api/v1/settings.public') == 0 and flow.url.find('RegistrationForm') > -1):
		type = 'User Action: RocketChat Screen View'
		info = 'Viewed Registration Form'
		results.append(Result.Result(flow, type, info))

	elif (flow.url == 'https://open.rocket.chat/api/v1/me'):
		type = 'User Action: Viewed Profile'
		info = 'Viewed own profile'
		results.append(Result.Result(flow, type, info))

		type = 'RocketChat ID'
		info = flow.responseContent[flow.responseContent.find('id":')+6:]
		info = info[:info.find('"')]
		results.append(Result.Result(flow, type, info))

	elif (flow.url.find('https://open.rocket.chat/api/v1/spotlight') == 0):
		type = 'User Action: RocketChat Search'
		info = AppDefault.findFormEntry(flow.requestContent, 'query')
		results.append(Result.Result(flow, type, info))

	elif (flow.url.find('https://open.rocket.chat/api/v1/channels.getAllUserMentionsByChannel') == 0):
		type = 'User Action: Viewed Channel Mentions'
		info = AppDefault.findFormEntry(flow.requestContent, 'roomId')
		results.append(Result.Result(flow, type, info))

	elif (flow.url.find('https://open.rocket.chat/api/v1/channels.files') == 0):
		type = 'User Action: Viewed Channel Files'
		info = AppDefault.findFormEntry(flow.requestContent, 'roomId')
		results.append(Result.Result(flow, type, info))


def checkPostURL(flow, results):
	flow.source = 'RocketChat'

	if (flow.url == 'https://open.rocket.chat/api/v1/users.register'):
		type = 'User Info: Email Address'
		info = AppDefault.findJSONItem(flow.requestContent, 'email')
		results.append(Result.Result(flow, type, info))

		type = 'User Info: RocketChat Name'
		info = AppDefault.findJSONItem(flow.requestContent, 'name')
		results.append(Result.Result(flow, type, info))

		type = 'User Info: RocketChat Password'
		info = AppDefault.findJSONItem(flow.requestContent, 'pass')
		results.append(Result.Result(flow, type, info))

		type = 'User Info: RocketChat Username'
		info = AppDefault.findJSONItem(flow.requestContent, 'username')
		results.append(Result.Result(flow, type, info))

	elif (flow.url == 'https://open.rocket.chat/api/v1/login'):
		type = 'User Info: RocketChat Password'
		info = AppDefault.findJSONItem(flow.requestContent, 'pass')
		results.append(Result.Result(flow, type, info))

		type = 'User Info: RocketChat Username'
		info = AppDefault.findJSONItem(flow.requestContent, 'username')
		results.append(Result.Result(flow, type, info))

	elif (flow.url == 'https://open.rocket.chat/api/v1/push.token'):
		type = 'RocketChat GCM Token'
		info = AppDefault.findJSONItem(flow.requestContent, 'value')
		results.append(Result.Result(flow, type, info))

	elif (flow.url == 'https://open.rocket.chat/api/v1/channels.create'):
		type = 'User Action: Create Channel'
		info = flow.requestContent[flow.requestContent.find('"name":')+9:]
		info = info[:info]
		results.append(Result.Result(flow, type, info))

	elif (flow.url == 'https://open.rocket.chat/api/v1/chat.sendMessage'):
		type = 'User Action: Send Message'
		info = flow.requestContent[flow.requestContent.find('"msg":')+8:]
		info = info[:info.find('"')]
		results.append(Result.Result(flow, type, info))

	elif (flow.url.find('https://open.rocket.chat/api/v1/chat.search') == 0):
		type = 'User Action: Chat Search'
		info = AppDefault.findFormEntry(flow.requestContent, 'searchText')
		results.append(Result.Result(flow, type, info))

	elif (flow.url == 'https://open.rocket.chat/api/v1/users.deleteOwnAccount'):
		type = 'User Action: Delete Account'
		info = 'Deleted RocketChat Account'
		results.append(Result.Result(flow, type, info))

	elif (flow.url == 'https://open.rocket.chat/api/v1/logout'):
		type = 'User Action: Logout'
		info = 'Logged Out'
		results.append(Result.Result(flow, type, info))


def checkHeadURL(flow, results):
	return None

def checkPutURL(flow, results):
	return None

def checkDeleteURL(flow, results):
	return None
