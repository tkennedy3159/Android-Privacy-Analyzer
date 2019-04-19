import AndroidDataPrivacy.Flow as Flow
import AndroidDataPrivacy.Result as Result
import AndroidDataPrivacy.Applications.AppDefault as AppDefault

urls = []

partialURLs = ['https://graph.facebook.com']

userAgents = []

partialUserAgents = ['FBAndroidSDK']

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
		if (headers['User-Agent'].find('FBAndroidSDK') == 0):
			flow.source = 'Facebook'

def checkResponseHeaders(flow, headers, results):
	return None

def checkGetURL(flow, results):
	if (flow.url.find('https://graph.facebook.com') == 0):
		if (flow.requestContent.find('advertiser_id:') > -1):
			type = 'Ad ID'
			info = AppDefault.findFormEntry(flow.requestContent, 'advertiser_id')
			results.append(Result.Result(flow, type, info))
		elif (flow.requestContent.find('device_id:') > -1):
			type = 'Ad ID'
			info = AppDefault.findFormEntry(flow.requestContent, 'device_id')
			results.append(Result.Result(flow, type, info))


def checkPostURL(flow, results):
	if (flow.url.find('https://graph.facebook.com') == 0):
		if (flow.requestContent.find('anon_id:') > -1):
			type = 'Facebook Anonymous ID'
			info = AppDefault.findFormEntry(flow.requestContent, 'anon_id')
			results.append(Result.Result(flow, type, info))

		if (flow.requestContent.find('advertiser_id:') > -1):
			type = 'Ad ID'
			info = AppDefault.findFormEntry(flow.requestContent, 'advertiser_id')
			results.append(Result.Result(flow, type, info))

		if (flow.requestContent.find('installer_package:') > -1):
			type = 'App Installer'
			info = AppDefault.findFormEntry(flow.requestContent, 'installer_package')
			results.append(Result.Result(flow, type, info))

		if (flow.url.find('/activities') > -1):
			type = 'User Action: ' + AppDefault.findFormEntry(flow.requestContent, 'application_package_name')
			if (AppDefault.findFormEntry(flow.requestContent, 'event') == 'CUSTOM_APP_EVENTS'):
				info = AppDefault.findFormEntry(flow.requestContent, 'custom_events')
			else:
				info = AppDefault.findFormEntry(flow.requestContent, 'event')
			results.append(Result.Result(flow, type, info))


def checkHeadURL(flow, results):
	return None

def checkPutURL(flow, results):
	return None

def checkDeleteURL(flow, results):
	return None
