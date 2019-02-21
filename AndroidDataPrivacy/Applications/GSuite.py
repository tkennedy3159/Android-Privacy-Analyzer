import AndroidDataPrivacy.Flow as Flow
import AndroidDataPrivacy.Result as Result
import AndroidDataPrivacy.Applications.AppDefault as AppDefault

urls = []

partialURLs = ['https://www.googleapis.com/drive/v2internal/files?']

userAgents = []

partialUserAgents = []

appIds = {'1:493454522602:android:4877c2b5f408a8b2':'com.google.android.apps.maps', \
#Google Maps
'1:206908507205:android:167bd0ff59cd7d44':'com.google.android.apps.tachyon'}
#Google Duo

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
	if ('referer' in headers.keys()):
		if (headers['referer'] == 'android-app://com.google.android.gm'):
			flow.source = 'Gmail'

def checkResponseHeaders(flow, headers, results):
	return None

def checkGetURL(flow, results):
	if (flow.url.find('https://www.googleapis.com/drive/v2internal/files?') == 0):
		flow.source = 'Google Drive File Lookup'

def checkPostURL(flow, results):
	if (flow.url == 'https://android.clients.google.com/c2dm/register3'):
		if (flow.requestHeaders['app'] == 'com.google.android.apps.tachyon'):
			flow.source = 'Google Duo Login'
		elif (flow.requestHeaders['app'] == 'com.google.android.apps.maps'):
			flow.source = 'Google Maps Login'
		type = 'System Info: Device ID'
		info = flow.requestContent
		info = info[info.find('device:')+7:]
		info = info[:info.find('\n')]
		info = info.strip()
		results.append(Result.Result(flow.app, flow.destination, flow.source, type, info, flow.all))
		
		type = 'Token'
		info = flow.responseContent
		info = info[info.find('token=')+6:]
		info = info.strip()
		results.append(Result.Result(flow.app, flow.destination, flow.source, type, info, flow.all))

def checkHeadURL(flow, results):
	return None
