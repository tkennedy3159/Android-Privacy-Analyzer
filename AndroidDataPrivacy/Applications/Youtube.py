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
		if (headers['User-Agent'][:26] == 'com.google.android.youtube' and flow.source == ''):
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
	if (flow.url.find('youtube.com') > -1):
		if (flow.requestContent.find('plid:') > -1):
			type = 'Youtube PLID'
			info = AppDefault.findFormEntry(flow.requestContent, 'plid')
			results.append(Result.Result(flow, type, info))

		if (flow.requestContent.find('cos:') > -1):
			type = 'System Info: OS'
			info = AppDefault.findFormEntry(flow.requestContent, 'cos')
			results.append(Result.Result(flow, type, info))

		if (flow.requestContent.find('docid:') > -1):
			type = 'Youtube Video ID'
			info = AppDefault.findFormEntry(flow.requestContent, 'docid')
			results.append(Result.Result(flow, type, info))
		elif (flow.requestContent.find('video_id:') > -1):
			type = 'Youtube Video ID'
			info = AppDefault.findFormEntry(flow.requestContent, 'video_id')
			results.append(Result.Result(flow, type, info))
		elif (flow.requestContent.find('content_v:') > -1):
			type = 'Youtube Video ID'
			info = AppDefault.findFormEntry(flow.requestContent, 'content_v')
			results.append(Result.Result(flow, type, info))

	if (flow.url.find('https://www.googleadservices.com/pagead/conversion') == 0):
		type = 'System Info: Youtube App Version'
		info = AppDefault.findFormEntry(flow.requestContent, 'appversion')
		results.append(Result.Result(flow, type, info))

		type = 'System Info: Android Version'
		info = AppDefault.findFormEntry(flow.requestContent, 'osversion')
		results.append(Result.Result(flow, type, info))

		type = 'User Info: Youtube Screen Opened'
		info = AppDefault.findFormEntry(flow.requestContent, 'data.screen_name')
		results.append(Result.Result(flow, type, info))

		type = 'User Info: Ad ID'
		info = AppDefault.findFormEntry(flow.requestContent, 'rdid')
		results.append(Result.Result(flow, type, info))

	elif (flow.url.find('upnphost/udhisapi.dll?content=uuid:') > -1):
		type = 'User Info: Youtube UUID'
		info = flow.requestContent[flow.requestContent.find('uuid:')+5:]
		info = info[:info.find('\n')]
		results.append(Result.Result(flow, type, info))

	elif (flow.url.find('https://www.youtube.com/csi_204') == 0):
		type = 'User Action: Youtube'
		info = AppDefault.findFormEntry(flow.requestContent, 'action')
		results.append(Result.Result(flow, type, info))

		type = 'System Info: Brand'
		info = AppDefault.findFormEntry(flow.requestContent, 'cbrand')
		results.append(Result.Result(flow, type, info))

		type = 'System Info: Model'
		info = AppDefault.findFormEntry(flow.requestContent, 'cmodel')
		results.append(Result.Result(flow, type, info))

	elif (flow.url.find('https://s.youtube.com/api/stats') == 0):
		if (flow.requestContent.find('state:') > -1):
			type = 'Youtube Video Status'
			info = AppDefault.findFormEntry(flow.requestContent, 'state')
			results.append(Result.Result(flow, type, info))

		if (flow.requestContent.find('referrer:') > -1):
			type = 'Youtube Video Referrer'
			info = AppDefault.findFormEntry(flow.requestContent, 'referrer')
			results.append(Result.Result(flow, type, info))

	elif (flow.url.find('https://www.youtube.com/api/stats/ads') == 0):
		type = 'Youtube Ad Video'
		info = AppDefault.findFormEntry(flow.requestContent, 'ad_v')
		results.append(Result.Result(flow, type, info))

	elif (flow.url.find('https://www.youtube.com/gen_204') == 0):
		type = 'Youtube Ad Video'
		info = AppDefault.findFormEntry(flow.requestContent, 'ad_vid')
		results.append(Result.Result(flow, type, info))

	elif (flow.url.find('https://suggestqueries.google.com/complete/search') == 0):
		type = 'User Action: Search Query'
		info = AppDefault.findFormEntry(flow.requestContent, 'q')
		results.append(Result.Result(flow, type, info))

		type = 'Youtube Search Suggestion'
		query = info
		if (len(info) > 0):
			for item in flow.responseContent.split('],['):
				info = item[item.find('\\\\u003e')+7:]
				info = info[:info.find('\\\\')]
				if (len(info) > 0):
					info = query + info
					results.append(Result.Result(flow, type, info))
		else:
			for item in flow.responseContent.split('}],['):
				info = item[item.find('youtube-android'):]
				info = info[info.find('\\\\u003d')+7:]
				info = info[:info.find('\\\\')]
				if (len(info) > 0):
					info = query + info
					results.append(Result.Result(flow, type, info))

	elif (flow.url.find('https://www.youtube.com/player_204') == 0):
		if (flow.requestContent.find('event:') > -1 and AppDefault.findFormEntry(flow.requestContent, 'event') == 'iv'):
			type = 'User Action: Youtube'
			info = 'Opened Video Info'
			results.append(Result.Result(flow, type, info))

def checkPostURL(flow, results):
	if (flow.url.find('https://youtubei.googleapis.com/youtubei') == 0 and flow.url.find('key=') > -1):
		type = 'User Info: Google API Key'
		info = flow.url[flow.url.find('key=')+4:]
		if (info.find('&') > -1):
			info = info[:info.find('&')]
		results.append(Result.Result(flow, type, info))

	if (flow.url.find('https://youtubei.googleapis.com/youtubei/v1/search') == 0):
		type = 'User Action: Youtube Search'
		info = AppDefault.findJSONGroup(flow.requestContent, '16')
		info = info[info.find('4: ')+3:]
		info = info[:info.find('\n')]
		results.append(Result.Result(flow, type, info))

	elif (flow.url.find('https://www.youtube.com/error_204') == 0):
		source = 'Youtube Error'
		type = 'Youtube Error Message'
		info = AppDefault.findFormEntry(requestContent, 'exception.message')
		results.append(Result.Result(flow, type, info))

	elif (flow.url.find('https://youtubei.googleapis.com/youtubei/v1/browse/edit_playlist') == 0):
		flow.source = 'Youtube Playlist Edit'
		type = 'Youtube Video ID'
		if (flow.requestContent.find('2 {\n      2: ') > -1):
			info = flow.requestContent[flow.requestContent.find('2 {\n      2: '):]
			info = info[info.find('2: ')+3:]
			info = info[:info.find('\n')]
			results.append(Result.Result(flow, type, info))
		elif (flow.requestContent.find('2 {\n      6: ') > -1):
			info = flow.requestContent[flow.requestContent.find('2 {\n      6: '):]
			info = info[info.find('17: ')+4:]
			info = info[:info.find('\n')]
			results.append(Result.Result(flow, type, info))

		if (flow.requestContent.find('        }\n      }\n    }\n    2 {') > -1):
			type = 'Youtube Playlist'
			info = flow.requestContent[flow.requestContent.find('        }\n      }\n    }\n    2 {')+40:]
			info = info[info.find('3: ')+3:]
			info = info[:info.find('\n')]
			results.append(Result.Result(flow, type, info))

	elif (flow.url.find('https://youtubei.googleapis.com/youtubei/v1/browse') == 0):
		if (flow.requestContent.find('        }\n      }\n    }\n    2: ') > -1):
			type = 'User Action: Youtube Browsing'
			info = flow.requestContent[flow.requestContent.find('        }\n      }\n    }\n    2: ')+31:]
			info = info[:info.find('\n')]
			results.append(Result.Result(flow, type, info))

	elif (flow.url.find('https://youtubei.googleapis.com/youtubei/v1/share/get_share_panel') == 0):
		type = 'User Action: Youtube'
		info = 'Opened share panel'
		results.append(Result.Result(flow, type, info))

	elif (flow.url.find('https://youtubei.googleapis.com/youtubei/v1/playlist/get_add_to_playlist') == 0):
		if (flow.requestContent.find('        }\n      }\n    }\n    2: ') > -1):
			type = 'User Action: Add Video to Playlist'
			info = flow.requestContent[flow.requestContent.find('        }\n      }\n    }\n    2: ')+31:]
			info = info[:info.find('\n')]
			results.append(Result.Result(flow, type, info))

	elif (flow.url.find('https://youtubei.googleapis.com/youtubei/v1/playlist/create') == 0):
		if (flow.requestContent.find('        }\n      }\n    }\n    2: ') > -1):
			type = 'User Action: Create Playlist'
			info = flow.requestContent[flow.requestContent.find('        }\n      }\n    }\n    2: ')+31:]
			info = info[:info.find('\n')]
			results.append(Result.Result(flow, type, info))

	elif (flow.url.find('https://youtubei.googleapis.com/youtubei/v1/playlist/delete') == 0):
		if (flow.requestContent.find('        }\n      }\n    }\n    2: ') > -1):
			type = 'User Action: Delete Playlist'
			info = flow.requestContent[flow.requestContent.find('        }\n      }\n    }\n    2: ')+31:]
			info = info[:info.find('\n')]
			results.append(Result.Result(flow, type, info))

def checkHeadURL(flow, results):
	return None