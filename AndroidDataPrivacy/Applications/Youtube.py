import AndroidDataPrivacy.Flow as Flow
import AndroidDataPrivacy.Result as Result
import AndroidDataPrivacy.Applications.AppDefault as AppDefault

type = ''
info = ''

urls = []

partialURLs = ['https://youtubei.googleapis.com']

userAgents = []

partialUserAgents = ['com.google.android.youtube']

def checkBehavior(flow, results):
	if (flow.requestType == 'GET'):
		analyzeGetRequest(flow, results)
	if (flow.requestType == 'POST'):
		analyzePostRequest(flow, results)
	if (flow.requestType == 'HEAD'):
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

def analyzeHeadRequest(flow, results):
	checkHeadURL(flow, results)
	checkRequestHeaders(flow, flow.requestHeaders, results)
	AppDefault.checkRequestHeadersDefault(flow, flow.requestHeaders, results)
	checkResponseHeaders(flow, flow.responseHeaders, results)
	AppDefault.checkResponseHeadersDefault(flow, flow.responseHeaders, results)
	AppDefault.analyzeHeadRequestDefault(flow, results)

def checkRequestHeaders(flow, headers, results):
	if ('User-Agent' in headers.keys()):
		if (headers['User-Agent'][:26] == 'com.google.android.youtube'):
			flow.source = 'Youtube'

	if ('x-goog-device-auth' in headers.keys()):
		type = 'System Info: Google API Device Authentication'
		info = headers['x-goog-device-auth']
		results.append(Result.Result(flow, type, info))

	if ('x-goog-visitor-id' in headers.keys()):
		type = 'User Info: Google Visitor ID'
		info = headers['x-goog-visitor-id']
		results.append(Result.Result(flow, type, info))

def checkResponseHeaders(flow, headers, results):
	return None

def checkGetURL(flow, results):
	if (flow.url.find('https://www.googleadservices.com/pagead/conversion') == 0):
		type = 'System Info: Youtube App Version'
		info = AppDefault.findFormEntry(flow.requestContent, 'appversion')
		results.append(Result.Result(flow, type, info))

		type = 'System Info: Android Version'
		info = AppDefault.findFormEntry(flow.requestContent, 'osversion')
		results.append(Result.Result(flow, type, info))

		type = 'User Info: Youtube Screen Name'
		info = AppDefault.findFormEntry(flow.requestContent, 'data.screen_name')
		results.append(Result.Result(flow, type, info))

def checkPostURL(flow, results):
	if (flow.url.find('https://youtubei.googleapis.com/youtubei') == 0 and flow.url.find('key=') > -1):
		type = 'User Info: Google API Key'
		info = flow.url[flow.url.find('key=')+4:]
		if (info.find('&') > -1):
			info = info[:info.find('&')]
		results.append(Result.Result(flow, type, info))

def checkHeadURL(flow, results):
	return None