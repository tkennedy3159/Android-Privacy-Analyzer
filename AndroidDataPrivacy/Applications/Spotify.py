import AndroidDataPrivacy.Flow as Flow
import AndroidDataPrivacy.Result as Result
import AndroidDataPrivacy.Applications.AppDefault as AppDefault

urls = []

partialURLs = ['https://spclient.wg.spotify.com']

userAgents = []

partialUserAgents = ['Spotify']

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
		if (headers['User-Agent'].find('Spotify') == 0 and flow.source == ''):
			flow.source = 'Spotify'

def checkResponseHeaders(flow, headers, results):
	return None

def checkGetURL(flow, results):
	if (flow.url.find('https://spclient.wg.spotify.com/v1/pses/featureflags') == 0):
		flow.source = 'Spotify Features Sync'
	
	elif (flow.url.find('https://spclient.wg.spotify.com/abba-service/v1/resolve') == 0):
		flow.source = 'Spotify Features Sync'
	
	elif (flow.url.find('https://spclient.wg.spotify.com/ads/v2/config') == 0):
		type = 'Spotify Session ID'
		info = flow.requestHeaders['vnd.spotify.ads-payload']
		info = info[info.find('"session_id":')+14:]
		info = info[:info.find('"')]
		results.append(Result.Result(flow, type, info))

	elif (flow.url.find('https://spclient.wg.spotify.com/storage-resolve/files/audio/interactive/') == 0):
		type = 'User Action: Song Opened'
		info = flow.url[flow.url.find('audio/interactive/')+18:]
		info = info[:info.find('?')]
		results.append(Result.Result(flow, type, info))

	elif (flow.url.find('https://spclient.wg.spotify.com/storage-resolve/files/audio/interactive_prefetch') == 0):
		type = 'User Action: Song Opened'
		info = flow.url[flow.url.find('interactive_prefetch/')+21:]
		info = info[:info.find('?')]
		results.append(Result.Result(flow, type, info))

	elif (flow.url.find('https://audio-sp-dca.pscdn.co/audio') == 0):
		type = 'User Action: Song Opened'
		info = flow.url[flow.url.find('audio/')+6:]
		info = info[:info.find('?')]
		results.append(Result.Result(flow, type, info))

	elif (flow.url.find('https://audio4-ak-spotify-com.akamaized.net/audio') == 0):
		type = 'User Action: Song Opened'
		info = flow.url[flow.url.find('audio/')+6:]
		info = info[:info.find('?')]
		results.append(Result.Result(flow, type, info))

	elif (flow.url.find('https://spclient.wg.spotify.com/searchview/android/v4/assisted-curation') == 0):
		type = 'User Info: Spotify Username'
		info = AppDefault.findFormEntry(flow.requestContent, 'username')
		results.append(Result.Result(flow, type, info))

		type = 'User Action: Spotify Search'
		info = flow.url[flow.url.find('assisted-curation/')+18:]
		info = info[:info.find('?')]
		info = AppDefault.fixUrlEncoding(info)
		results.append(Result.Result(flow, type, info))

	elif (flow.url.find('https://spclient.wg.spotify.com/searchview/android/v4/search') == 0):
		type = 'User Info: Spotify Username'
		info = AppDefault.findFormEntry(flow.requestContent, 'username')
		results.append(Result.Result(flow, type, info))

		type = 'User Action: Spotify Search'
		info = flow.url[flow.url.find('search/')+7:]
		info = info[:info.find('?')]
		info = AppDefault.fixUrlEncoding(info)
		results.append(Result.Result(flow, type, info))

	elif (flow.url.find('https://spclient.wg.spotify.com/quicksilver/v2/cards') == 0):
		if (flow.requestContent.find('trigger:') > -1):
			type = 'User Action: Click'
			info = AppDefault.findFormEntry(flow.requestContent, 'trigger')
			results.append(Result.Result(flow, type, info))

	elif (flow.url.find('megaphone.fm') > -1):
		type = 'User Action: Podcast Opened'
		info = flow.url[flow.url.find('megaphone.fm/')+13:]
		info = info[:info.find('.mp3')]
		results.append(Result.Result(flow, type, info))

def checkPostURL(flow, results):
	if (flow.url.find('https://spclient.wg.spotify.com/remote-config-resolver') == 0):
		type = 'System Info: Spotify Installation ID'
		info = AppDefault.findFormEntry(flow.requestContent, 'installation_id')
		results.append(Result.Result(flow, type, info))

def checkHeadURL(flow, results):
	return None

def checkPutURL(flow, results):
	return None

def checkDeleteURL(flow, results):
	return None
