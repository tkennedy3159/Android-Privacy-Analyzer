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

def checkResponseHeaders(flow, headers, results):
	return None

def checkGetURL(flow, results):
	if (flow.url.find('https://www.linkedin.com') == 0):
		flow.source = 'LinkedIn'

def checkPostURL(flow, results):
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
			info = AppDefault.findJSONSection(body, 'eventBody')
			results.append(Result.Result(flow, type, info))
			body = body[20:]


def checkHeadURL(flow, results):
	return None

def checkPutURL(flow, results):
	return None

def checkDeleteURL(flow, results):
	return None
