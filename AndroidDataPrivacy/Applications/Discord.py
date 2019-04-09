import AndroidDataPrivacy.Flow as Flow
import AndroidDataPrivacy.Result as Result
import AndroidDataPrivacy.Applications.AppDefault as AppDefault

urls = []

partialURLs = ['https://dl.discordapp.net', \
'https://gateway.discord.gg', \
'https://cdn.discordapp.com']

userAgents = []

partialUserAgents = ['Discord-Android']

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
		if (headers['User-Agent'].find('Discord-Android') == 0 and flow.source == ''):
			flow.source = 'Discord'

	if ('x-fingerprint' in headers.keys()):
		type = 'Discord Fingerprint'
		info = headers['x-fingerprint']
		results.append(Result.Result(flow, type, info))

	if ('Sec-WebSocket-Key' in headers.keys()):
		type = 'Discord Web Socket Key'
		info = headers['Sec-WebSocket-Key']
		results.append(Result.Result(flow, type, info))

def checkResponseHeaders(flow, headers, results):
	return None

def checkGetURL(flow, results):
	if (flow.url.find('https://dl.discordapp.net') == 0):
		flow.source = 'Discord'

	elif (flow.url.find('https://discordapp.com') == 0):
		flow.source = 'Discord'

	elif (flow.url.find('https://gateway.discord.gg') == 0):
		flow.source = 'Discord'

	if (flow.url.find('https://discordapp.com/api/v6/channels') == 0):
		if (flow.url.find('messages') > -1):
			flow.source = 'Discord Messages Sync'
			type = 'Discord Channel'
			info = flow.url[flow.url.find('channels/')+9:]
			info = info[:info.find('/messages')]
			results.append(Result.Result(flow, type, info))
		elif (flow.url.find('pins') > -1):
			flow.source = 'Discord Pins Lookup'
			type = 'Discord Channel'
			info = flow.url[flow.url.find('channels/')+9:]
			info = info[:info.find('/pins')]
			results.append(Result.Result(flow, type, info))

	elif (flow.url.find('https://discordapp.com/api/v6/users') == 0 and flow.url.find('profile') > -1):
		type = 'User Action: View Discord User Profile'
		temp = flow.responseContent[flow.responseContent.find('"username":')+13:]
		temp = temp[:temp.find('"')]
		info = temp
		temp = flow.responseContent[flow.responseContent.find('"discriminator":')+18:]
		temp = temp[:temp.find('"')]
		info = info + '#' + temp
		results.append(Result.Result(flow, type, info))

	elif (flow.url.find('https://discordapp.com/api/v6/guilds') == 0 and flow.url.find('search') > -1):
		flow.source = 'Discord Channel Search'
		type = 'Discord Channel'
		info = flow.url[flow.url.find('guilds/')+7:]
		info = info[:info.find('/messages')]
		results.append(Result.Result(flow, type, info))

def checkPostURL(flow, results):
	if (flow.url == 'https://discordapp.com/api/v6/track'):
		type = 'User Action: Discord'
		temp = flow.requestContent[flow.requestContent.find('"events": [')+11:]
		for info in temp.split('},\n            {'):
			results.append(Result.Result(flow, type, info))

	elif (flow.url == 'https://discordapp.com/api/v6/auth/login'):
		type = 'User Info: Discord Username'
		info = AppDefault.findJSONItem(flow.requestContent, '"email"')
		results.append(Result.Result(flow, type, info))

		type = 'User Info: Discord Password'
		info = AppDefault.findJSONItem(flow.requestContent, '"password"')
		results.append(Result.Result(flow, type, info))

	elif (flow.url == 'https://discordapp.com/api/v6/users/@me/relationships'):
		type = 'User Action: Discord User Search'
		info = AppDefault.findJSONItem(flow.requestContent, '"username"') + '#' + AppDefault.findJSONItem(flow.requestContent, '"discriminator"')
		results.append(Result.Result(flow, type, info))

	elif (flow.url == 'https://discordapp.com/api/v6/guilds'):
		type = 'User Action: Create Discord Channel'
		info = AppDefault.findJSONItem(flow.requestContent, '"name"')
		results.append(Result.Result(flow, type, info))

	elif (flow.url.find('https://discordapp.com/api/v6/guilds') == 0 and flow.url.find('delete') > -1):
		flow.source = 'Discord Server Delete'
		type = 'Discord Channel'
		info = flow.url[flow.url.find('guilds/')+7:]
		info = info[:info.find('/delete')]
		results.append(Result.Result(flow, type, info))

	elif (flow.url.find('https://discordapp.com/api/v6/channels') == 0 and flow.url.find('typing') > -1):
		flow.source = 'Discord Message Typing'
		type = 'Discord Channel'
		info = flow.url[flow.url.find('channels/')+9:]
		info = info[:info.find('/typing')]
		results.append(Result.Result(flow, type, info))

	elif (flow.url.find('https://discordapp.com/api/v6/channels') == 0 and flow.url.find('messages') > -1):
		flow.source = 'Discord Message Sent'
		type = 'Discord Channel'
		info = flow.url[flow.url.find('channels/')+9:]
		info = info[:info.find('/messages')]
		results.append(Result.Result(flow, type, info))

		if (flow.requestContent.find('content:') > -1):
			type = 'Message'
			info = AppDefault.findFormEntry(flow.requestContent, 'content')
			results.append(Result.Result(flow, type, info))

	elif (flow.url.find('https://discordapp.com/api/v6/invite') == 0):
		flow.source = 'Discord Server Invite'
		type = 'Discord Channel'
		info = flow.responseContent[flow.responseContent.find('"guild"'):]
		info = info[info.find('"id":')+7:]
		info = info[:info.find('"')]
		results.append(Result.Result(flow, type, info))

def checkHeadURL(flow, results):
	return None

def checkPutURL(flow, results):
	return None

def checkDeleteURL(flow, results):
	if (flow.url.find('https://discordapp.com/api/v6/channels') == 0):
		flow.source = 'Discord Channel Delete'
		type = 'Discord Channel'
		info = flow.url[flow.url.find('channels/')+9:]
		results.append(Result.Result(flow, type, info))

	elif (flow.url.find('https://discordapp.com/api/v6/users/@me/guilds') == 0):
		flow.source = 'Discord Server Delete'
		type = 'Discord Channel'
		info = flow.url[flow.url.find('guilds/')+7:]
		results.append(Result.Result(flow, type, info))
