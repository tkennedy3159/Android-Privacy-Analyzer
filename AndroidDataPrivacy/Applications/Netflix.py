import AndroidDataPrivacy.Flow as Flow
import AndroidDataPrivacy.Result as Result
import AndroidDataPrivacy.Applications.AppDefault as AppDefault

urls = []

partialURLs = ['https://android.prod.cloud.netflix.com', \
'https://assets.nflxext.com']

userAgents = []

partialUserAgents = ['com.netflix.mediaclient']

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
		if (headers['User-Agent'].find('com.netflix.mediaclient') == 0):
			flow.source = 'Netflix'

	if ('x-netflix.request.client.user.guid' in headers.keys()):
		type = 'User Info: Netflix UUID'
		info = headers['x-netflix.request.client.user.guid']
		results.append(Result.Result(flow, type, info))


def checkResponseHeaders(flow, headers, results):
	return None

def checkGetURL(flow, results):
	flow.source = 'Netflix'

	if (flow.url.find('https://android.prod.cloud.netflix.com/android/samurai/config') == 0):
		type = 'System Info: Build'
		info = AppDefault.findFormEntry(flow.requestContent, 'osDisplay')
		results.append(Result.Result(flow, type, info))

		type = 'System Info: Chipset'
		info = AppDefault.findFormEntry(flow.requestContent, 'chipsetHardware')
		results.append(Result.Result(flow, type, info))


def checkPostURL(flow, results):
	flow.source = 'Netflix'

	if (flow.url.find('https://android-appboot.netflix.com/appboot') == 0):
		type = 'User Action: App Launch'
		info = 'Netflix opened'
		results.append(Result.Result(flow, type, info))

	elif (flow.url.find('https://android.prod.cloud.netflix.com/ichnaea/log') == 0):
		type = 'Netflix Event'
		info = flow.requestContent[flow.requestContent.find('"event_type":')+15:]
		info = info[:info.find('"')]
		results.append(Result.Result(flow, type, info))

		type = 'Ad ID'
		info = flow.requestContent[flow.requestContent.find('"advdevtag_id":')+17:]
		info = info[:info.find('"')]
		results.append(Result.Result(flow, type, info))

	elif (flow.url.find('https://android.prod.cloud.netflix.com/aui/pathEvaluator') == 0):
		type = 'Secure Netflix ID'
		info = AppDefault.findFormEntry(flow.requestContent, 'secureNetflixId')
		results.append(Result.Result(flow, type, info))

		type = 'Netflix ID'
		info = AppDefault.findFormEntry(flow.requestContent, 'netflixId')
		results.append(Result.Result(flow, type, info))

		type = 'Netflix FLWSSN'
		info = AppDefault.findFormEntry(flow.requestContent, 'flwssn')
		results.append(Result.Result(flow, type, info))

	elif (flow.url.find('https://android.prod.cloud.netflix.com/android') == 0):
		if (flow.requestContent.find('path:') > -1 and AppDefault.findFormEntry(flow.requestContent, 'path').find('"logBillboardActivity"') == -1):
			type = 'Netflix Browsing Path'
			info = AppDefault.findFormEntry(flow.requestContent, 'path')
			results.append(Result.Result(flow, type, info))


def checkHeadURL(flow, results):
	return None

def checkPutURL(flow, results):
	return None

def checkDeleteURL(flow, results):
	return None
