import AndroidDataPrivacy.Flow as Flow
import AndroidDataPrivacy.Result as Result
import AndroidDataPrivacy.Applications.AppDefault as AppDefault

urls = ['https://gql.reddit.com/']

partialURLs = ['https://www.reddit.com']

userAgents = []

partialUserAgents = ['Reddit']

appIds = {'1:933360113277:android:2918df7f0aab10ef':'com.reddit.frontpage'}

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
		if (headers['User-Agent'][:6] == 'Reddit' and flow.source == ''):
			flow.source = 'Reddit'

	if ('x-reddit-device-id' in headers.keys()):
		type = 'User Info: Reddit Device ID'
		info = headers['x-reddit-device-id']
		results.append(Result.Result(flow, type, info))

	if ('x-dev-ad-id' in headers.keys()):
		type = 'User Info: Ad ID'
		info = headers['x-dev-ad-id']
		results.append(Result.Result(flow, type, info))

def checkResponseHeaders(flow, headers, results):
	if ('x-reddit-loid' in headers.keys()):
		type = 'User Info: Reddit LOID'
		info = headers['x-reddit-loid']
		results.append(Result.Result(flow, type, info))

	if ('x-reddit-session' in headers.keys()):
		type = 'User Info: Reddit Session ID'
		info = headers['x-reddit-session']
		results.append(Result.Result(flow, type, info))

def checkGetURL(flow, results):
	if (flow.url.find('https://oauth.reddit.com/api/v1/me') == 0):
		flow.source = 'Reddit Login'

def checkPostURL(flow, results):
	if (flow.url == 'https://www.reddit.com/api/v1/access_token'):
		type = 'System Info: Access Token'
		info = flow.responseContent[flow.responseContent.find('"access_token":')+15:]
		info = info[info.find('"')+1:]
		info = info[:info.find('"')]
		results.append(Result.Result(flow, type, info))

	if (flow.url.find('https://api.branch.io/') == 0):
		flow.source = 'Branch.io'
		content = flow.requestContent

		type = 'System Info: Model'
		brand = content[content.find('"brand":')+10:]
		brand = brand[:brand.find('"')]
		model = content[content.find('"model":')+10:]
		model = model[:model.find('"')]
		info = brand + ' ' + model
		results.append(Result.Result(flow, type, info))

		type = 'User Info: Ad ID'
		info = content[content.find('"google_advertising_id":')+26:]
		info = info[:info.find('"')]
		results.append(Result.Result(flow, type, info))

		type = 'System Info: Hardware ID'
		info = content[content.find('"hardware_id":')+16:]
		info = info[:info.find('"')]
		results.append(Result.Result(flow, type, info))

		type = 'System Info: Local IP Address'
		info = content[content.find('"local_ip":')+13:]
		info = info[:info.find('"')]
		results.append(Result.Result(flow, type, info))

		type = 'System Info: Screen Size'
		width = content[content.find('"screen_width":')+16:]
		width = width[:width.find(',')]
		height = content[content.find('"screen_height":')+17:]
		height = height[:height.find(',')]
		info = width + ' x ' + height
		results.append(Result.Result(flow, type, info))

		type = 'System Info: WiFi Connection Status'
		info = content[content.find('"wifi":')+8:]
		info = info[:info.find('"')]
		results.append(Result.Result(flow, type, info))

		type = 'Branch.io Key'
		info = content[content.find('"branch_key":')+15:]
		info = info[:info.find('"')]
		results.append(Result.Result(flow, type, info))

		type = 'System Info: First Install Time'
		info = content[content.find('"first_install_time":')+22:]
		info = info[:info.find(',')]
		results.append(Result.Result(flow, type, info))

		type = 'System Info: Latest Install Time'
		info = content[content.find('"latest_install_time":')+23:]
		info = info[:info.find(',')]
		results.append(Result.Result(flow, type, info))

		type = 'System Info: Latest Update Time'
		info = content[content.find('"latest_update_time":')+22:]
		info = info[:info.find(',')]
		results.append(Result.Result(flow, type, info))

		if (flow.url[len(flow.url)-4:] == 'open'):
			type = 'User Action: Opened App'
			info = 'Reddit'
			results.append(Result.Result(flow, type, info))

			type = 'User info: Branch ID'
			info = content[content.find('"identity_id":')+16:]
			info = info[:info.find('"')]
			results.append(Result.Result(flow, type, info))

			type = 'System Info: Device Fingerprint ID'
			info = content[content.find('"device_fingerprint_id":')+26:]
			info = info[:info.find('"')]
			results.append(Result.Result(flow, type, info))

		elif (flow.url[len(flow.url)-7:] == 'install'):
			type = 'User Action: Installed App'
			info = 'Reddit'
			results.append(Result.Result(flow, type, info))

	elif (flow.url == 'https://gql.reddit.com/'):
		if (flow.responseContent.find('experimentVariants') > -1):
			type = 'Experimental Features Config'
			info = AppDefault.findJSONListNonSpaced(flow.responseContent, 'experimentVariants')
			results.append(Result.Result(flow, type, info))

	elif (flow.url.find('https://gateway.reddit.com/redditmobile/1/android/config') == 0):
		type = 'Experimental Features Config'
		info = AppDefault.findFormEntry(flow.requestContent, 'experiments')
		results.append(Result.Result(flow, type, info))
		info = AppDefault.findJSONListNonSpaced(flow.responseContent, 'buckets')
		results.append(Result.Result(flow, type, info))

	elif (flow.url.find('https://gateway.reddit.com/redditmobile') == 0):
		type = 'Reddit Client ID'
		info = AppDefault.findFormEntry(flow.requestContent, 'client_id')
		results.append(Result.Result(flow, type, info))

		type = 'System Info: Timezone'
		info = AppDefault.findFormEntry(flow.requestContent, 'tz_name')
		results.append(Result.Result(flow, type, info))

	elif (flow.url == 'https://events.redditmedia.com/v1'):
		event = flow.requestContent[flow.requestContent.find('"event_type":')+14:]
		event = event[:event.find('"')]
		time = flow.requestContent[flow.requestContent.find('"event_ts":')+11:]
		time = time[:time.find(',')]
		if (event == 'cs.app_launch_android'):
			type = 'User Action: Reddit Opened'
			info = 'Reddit Opened @ ' + time
			results.append(Result.Result(flow, type, info))

def checkHeadURL(flow, results):
	return None

def checkPutURL(flow, results):
	return None

def checkDeleteURL(flow, results):
	return None
