import AndroidDataPrivacy.Flow as Flow
import AndroidDataPrivacy.Result as Result
import AndroidDataPrivacy.Applications.AppDefault as AppDefault

urls = []

partialURLs = ['https://play.hulu.com', \
'https://vortex.hulu.com', \
'https://auth.hulu.com', \
'https://home.hulu.com', \
'https://discover.hulu.com', \
'https://cws-hulu.conviva.com', \
'https://hulu.hb.omtrdc.net', \
'https://manifest.hulustream.com', \
'https://license.hulu.com', \
'https://ads-e-darwin.hulustream.com', \
'https://http-e-darwin.hulustream.com', \
'https://assetshuluimcom-a.akamaihd.net']

userAgents = []

partialUserAgents = ['Hulu']

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
	return None

def checkResponseHeaders(flow, headers, results):
	return None

def checkGetURL(flow, results):
	flow.source = 'Hulu'

	if (flow.url.find('https://home.hulu.com/v1/users/self') == 0):
		type = 'User Action: Hulu'
		info = AppDefault.findFormEntry(flow.requestContent, 'action')
		results.append(Result.Result(flow, type, info))

		type = 'User Info: Hulu Token'
		info = AppDefault.findFormEntry(flow.requestContent, 'user_token')
		results.append(Result.Result(flow, type, info))

	elif (flow.url.find('https://discover.hulu.com/content/v4/hubs/series') == 0):
		type = 'User Action: Viewed Series'
		info = flow.url[flow.url.find('series/')+7:]
		info = info[:info.find('/')]
		results.append(Result.Result(flow, type, info))

		if (flow.url.find('season/') > -1):
			type = 'User Action: Viewed Season'
			info = flow.url[flow.url.find('season/')+7:]
			info = info[:info.find('?')]
			results.append(Result.Result(flow, type, info))

	elif (flow.url.find('https://discover.hulu.com/content/v4/search') == 0):
		type = 'User Action: Hulu Search'
		info = AppDefault.findFormEntry(flow.requestContent, 'search_query')
		results.append(Result.Result(flow, type, info))

	elif (flow.url.find('https://discover.hulu.com/content/v4/hubs') == 0):
		type = 'User Action: Viewed Hub'
		info = flow.url[flow.url.find('hubs/')+5:]
		info = info[:info.find('?')]
		results.append(Result.Result(flow, type, info))

	elif (flow.url.find('https://hulu.hb.omtrdc.net') == 0):
		if (flow.requestContent.find('s:event:type') > -1):
			type = 'Hulu Event'
			info = AppDefault.findFormEntry(flow.requestContent, 's:event:type')
			results.append(Result.Result(flow, type, info))

		if (flow.requestContent.find('s:asset:name') > -1):
			type = 'User Action: Hulu Asset Name'
			info = AppDefault.findFormEntry(flow.requestContent, 's:asset:name')
			results.append(Result.Result(flow, type, info))

		if (flow.requestContent.find('s:meta:a.media.show') > -1):
			type = 'User Action: Hulu Show'
			info = AppDefault.findFormEntry(flow.requestContent, 's:meta:a.media.show')
			results.append(Result.Result(flow, type, info))

	elif (flow.url.find('https://manifest.hulustream.com/dash') == 0):
		if (flow.requestContent.find('user_id') > -1):
			type = 'User Info: Hulu User ID'
			info = AppDefault.findFormEntry(flow.requestContent, 'user_id')
			results.append(Result.Result(flow, type, info))

	elif (flow.url.find('https://ag.innovid.com') == 0 or flow.url.find('https://s.innovid.com') == 0):
		type = 'Innovid Client ID'
		info = AppDefault.findFormEntry(flow.requestContent, 'client_id')
		results.append(Result.Result(flow, type, info))

		type = 'Innovid Video ID'
		info = AppDefault.findFormEntry(flow.requestContent, 'video_id')
		results.append(Result.Result(flow, type, info))


def checkPostURL(flow, results):
	flow.source = 'Hulu'

	if (flow.url == 'https://play.hulu.com/config'):
		type = 'System Info: Hulu Device ID'
		info = AppDefault.findFormEntry(flow.requestContent, 'device_id')
		results.append(Result.Result(flow, type, info))

		type = 'System Info: Model'
		info = AppDefault.findFormEntry(flow.requestContent, 'device_model')
		results.append(Result.Result(flow, type, info))

	elif (flow.url == 'https://vortex.hulu.com/api/v3/event'):
		if (flow.requestContent.find('app_session_id') > -1):
			type = 'Hulu Session ID'
			info = AppDefault.findJSONItem(flow.requestContent, 'app_session_id')
			results.append(Result.Result(flow, type, info))

		if (flow.requestContent.find('app_visit_count') > -1):
			type = 'User Action: Hulu Visit Count'
			info = AppDefault.findJSONItem(flow.requestContent, 'app_visit_count')
			results.append(Result.Result(flow, type, info))

		if (flow.requestContent.find('application_instance_id') > -1):
			type = 'System Info: Hulu App ID'
			info = AppDefault.findJSONItem(flow.requestContent, 'application_instance_id')
			results.append(Result.Result(flow, type, info))

		if (flow.requestContent.find('device_ad_id') > -1):
			type = 'Ad ID'
			info = AppDefault.findJSONItem(flow.requestContent, 'device_ad_id')
			results.append(Result.Result(flow, type, info))

		if (flow.requestContent.find('device_manufacturer') > -1):
			type = 'System Info: Brand'
			info = AppDefault.findJSONItem(flow.requestContent, 'device_manufacturer')
			results.append(Result.Result(flow, type, info))

		if (flow.requestContent.find('device_model') > -1):
			type = 'System Info: Model'
			info = AppDefault.findJSONItem(flow.requestContent, 'device_model')
			results.append(Result.Result(flow, type, info))

		if (flow.requestContent.find('device_os') > -1):
			type = 'System Info: OS Version'
			info = AppDefault.findJSONItem(flow.requestContent, 'device_os')
			results.append(Result.Result(flow, type, info))

		if (flow.requestContent.find('manufacturer_device_id') > -1):
			type = 'System Info: Serial Number'
			info = AppDefault.findJSONItem(flow.requestContent, 'manufacturer_device_id')
			results.append(Result.Result(flow, type, info))

		if (flow.requestContent.find('network_mode') > -1):
			type = 'System Info: Connection Type'
			info = AppDefault.findJSONItem(flow.requestContent, 'network_mode')
			results.append(Result.Result(flow, type, info))

		if (flow.requestContent.find('screen_resolution') > -1):
			type = 'System Info: Screen Size'
			info = AppDefault.findJSONItem(flow.requestContent, 'screen_resolution')
			results.append(Result.Result(flow, type, info))

		if (flow.requestContent.find('screen_orientation') > -1):
			type = 'System Info: Screen Orientation'
			info = AppDefault.findJSONItem(flow.requestContent, 'screen_orientation')
			results.append(Result.Result(flow, type, info))

		if (flow.requestContent.find('event') > -1):
			type = 'Hulu Event'
			info = AppDefault.findJSONItem(flow.requestContent, 'event')
			results.append(Result.Result(flow, type, info))

	elif (flow.url == 'https://auth.hulu.com/v1/device/code/register'):
		type = 'System Info: Serial Number'
		info = AppDefault.findFormEntry(flow.requestContent, 'serial_number')
		results.append(Result.Result(flow, type, info))

	elif (flow.url == 'https://auth.hulu.com/v1/device/password/authenticate'):
		type = 'User Info: Email Address'
		info = AppDefault.findFormEntry(flow.requestContent, 'user_email')
		results.append(Result.Result(flow, type, info))

		type = 'User Info: Hulu Password'
		info = AppDefault.findFormEntry(flow.requestContent, 'password')
		results.append(Result.Result(flow, type, info))

		type = 'System Info: Serial Number'
		info = AppDefault.findFormEntry(flow.requestContent, 'serial_number')
		results.append(Result.Result(flow, type, info))

		type = 'System Info: Timezone'
		info = AppDefault.findFormEntry(flow.requestContent, 'time_zone')
		results.append(Result.Result(flow, type, info))

	elif (flow.url == 'https://auth.hulu.com/v1/device/profiles/switch'):
		type = 'User Action: Profile Switch'
		info = AppDefault.findFormEntry(flow.requestContent, 'profile_id')
		results.append(Result.Result(flow, type, info))

	elif (flow.url.find('https://home.hulu.com/v1/users/self/profiles/self/asset_view_progress') == 0):
		type = 'User Action: Video Progress'
		info = AppDefault.findJSONItem(flow.requestContent, 'position')
		results.append(Result.Result(flow, type, info))


def checkHeadURL(flow, results):
	return None

def checkPutURL(flow, results):
	flow.source = 'Hulu'

	if (flow.url.find('https://home.hulu.com/v2/users/self/profiles/self/saves') == 0):
		type = flow.requestContent[flow.requestContent.find('"entity_type":')+16:]
		type = type[:type.find('"')]
		type = 'User Action: Saved ' + type
		info = flow.requestContent[flow.requestContent.find('"entity_id":')+14:]
		info = info[:info.find('"')]
		results.append(Result.Result(flow, type, info))


def checkDeleteURL(flow, results):
	flow.source = 'Hulu'

	if (flow.url.find('https://home.hulu.com/v1/users/self/profiles/self/viewed_entities') == 0):
		type = 'User Action: Delete Watch History'
		info = flow.url[flow.url.find('viewed_entities/')+16:]
		info = info[:info.find('?')]
		results.append(Result.Result(flow, type, info))
