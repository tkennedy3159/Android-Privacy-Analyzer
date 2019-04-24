import AndroidDataPrivacy.Flow as Flow
import AndroidDataPrivacy.Result as Result
import AndroidDataPrivacy.Applications.AppDefault as AppDefault

urls = []

partialURLs = ['https://canvas.instructure.com', \
'https://champlain.instructure.com', \
'https://instructure-uploads.s3.amazonaws.com']

userAgents = []

partialUserAgents = ['candroid']

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
		if (headers['User-Agent'].find('candroid') == 0):
			flow.source = 'Canvas'

def checkResponseHeaders(flow, headers, results):
	return None

def checkGetURL(flow, results):
	flow.source = 'Canvas'

	if (flow.url.find('https://canvas.instructure.com//api/v1/accounts/search') == 0):
		type = 'User Action: School Search'
		info = AppDefault.findFormEntry(flow.requestContent, 'search_term')
		results.append(Result.Result(flow, type, info))

	elif (flow.url.find('https://canvas.instructure.com/api/v1/mobile_verify.json') == 0):
		type = 'System Info: Canvas API Key'
		info = AppDefault.findJSONItem(flow.responseContent, 'api_key')
		results.append(Result.Result(flow, type, info))

		type = 'System Info: Canvas Client ID'
		info = AppDefault.findJSONItem(flow.responseContent, 'client_id')
		results.append(Result.Result(flow, type, info))

		type = 'System Info: Canvas Client Secret'
		info = AppDefault.findJSONItem(flow.responseContent, 'client_secret')
		results.append(Result.Result(flow, type, info))

	elif (flow.url.find('https://champlain.instructure.com/login/oauth2/auth') == 0):
		type = 'System Info: Canvas Client ID'
		info = AppDefault.findFormEntry(flow.requestContent, 'client_id')
		results.append(Result.Result(flow, type, info))

	elif (flow.url.find('https://champlain.instructure.com/api/v1/courses') == 0):
		if (flow.url.find('front_page') > -1):
			type = 'User Action: View Course Front Page'
			info = flow.url[flow.url.find('courses/')+8:]
			info = info[:info.find('/')]
			results.append(Result.Result(flow, type, info))

		elif (flow.url.find('announcements') > -1):
			type = 'User Action: View Course Announcements'
			info = flow.url[flow.url.find('courses/')+8:]
			info = info[:info.find('/')]
			results.append(Result.Result(flow, type, info))

		elif (flow.url.find('discussion_topics') > -1 and flow.url.find('view') > -1):
			type = 'User Action: View Discussion Topic'
			info = flow.url[flow.url.find('discussion_topics/')+18:]
			info = info[:info.find('/')]
			results.append(Result.Result(flow, type, info))

		elif (flow.url.find('modules') > -1):
			type = 'User Action: View Course Modules'
			info = flow.url[flow.url.find('courses/')+8:]
			info = info[:info.find('/')]
			results.append(Result.Result(flow, type, info))

			if (flow.url.find('/items') > -1):
				type = 'User Action: View Module'
				info = flow.url[flow.url.find('modules/')+8:]
				info = info[:info.find('/')]
				results.append(Result.Result(flow, type, info))

		elif (flow.url.find('pages/') > -1):
			type = 'User Action: View Course Page'
			info = flow.url[flow.url.find('pages/')+6:]
			results.append(Result.Result(flow, type, info))

		elif (flow.url.find('assignments') > -1):
			if (flow.url.find('submissions') > -1):
				type = 'User Action: View Assignment Submission'
				info = flow.url[flow.url.find('submissions/')+12:]
				info = info[:info.find('?')]
				results.append(Result.Result(flow, type, info))
			else:
				type = 'User Action: View Assignment'
				info = flow.url[flow.url.find('assignments/')+12:]
				info = info[:info.find('?')]
				results.append(Result.Result(flow, type, info))

		elif (flow.url.find('users') > -1):
			if (flow.url.find('users/') > -1):
				type = 'User Action: View Canvas User'
				info = flow.url[flow.url.find('users/')+6:]
				info = info[:info.find('?')]
				name = flow.responseContent[flow.responseContent.find('"name":')+9:]
				name = name[:name.find('"')]
				info = info + ': ' + name
				results.append(Result.Result(flow, type, info))
			else:
				type = 'User Action: View Course People'
				info = flow.url[flow.url.find('courses/')+8:]
				info = info[:info.find('/')]
				results.append(Result.Result(flow, type, info))

	elif (flow.url.find('https://champlain.instructure.com/api/v1/calendar_events') == 0):
		type = 'User Action: View Calendar'
		info = AppDefault.findFormEntry(flow.requestContent, 'start_date') + ' - ' + AppDefault.findFormEntry(flow.requestContent, 'end_date')
		results.append(Result.Result(flow, type, info))

		if (flow.url.find('context_codes[]=course_') > -1):
			type = 'User Action: Course Calendar Viewed'
			info = AppDefault.findFormEntry(flow.requestContent, 'context_codes[]')
			info = info[7:]
			results.append(Result.Result(flow, type, info))

	elif (flow.url.find('https://champlain.instructure.com/api/v1/users/self/todo') == 0):
		type = 'User Action: View To-Do\'s'
		info = 'Viewed To Do\'s'
		results.append(Result.Result(flow, type, info))

	elif (flow.url.find('https://champlain.instructure.com/api/v1/users/self/activity_stream') == 0):
		type = 'User Action: View Notifications'
		info = 'Viewed Notifications'
		results.append(Result.Result(flow, type, info))

	elif (flow.url.find('https://champlain.instructure.com/api/v1/conversations') == 0):
		if (flow.url.find('conversations/?') == -1 and flow.url.find('unread_count') == -1):
			type = 'User Action: Viewed Message'
			info = flow.url[flow.url.find('conversations/')+14:]
			info = info[:info.find('?')]
			results.append(Result.Result(flow, type, info))
		else:
			type = 'User Action: Viewed Inbox'
			info = 'Viewed Inbox'
			results.append(Result.Result(flow, type, info))

	elif (flow.url.find('https://champlain.instructure.com/api/v1/users/self/folders') == 0):
		type = 'User Action: Viewed Files'
		info = flow.url[flow.url.find('folders/')+8:]
		results.append(Result.Result(flow, type, info))

	elif (flow.url.find('https://champlain.instructure.com/api/v1/folders') == 0):
		type = 'User Action: Viewed Folder'
		info = flow.url[flow.url.find('folders/')+8:]
		info = info[:info.find('/')]
		results.append(Result.Result(flow, type, info))

	elif (flow.url.find('https://champlain.instructure.com/files') == 0):
		type = 'User Action: Viewed File'
		info = flow.url[flow.url.find('files/')+6:]
		info = info[:info.find('/')]
		results.append(Result.Result(flow, type, info))

	elif (flow.url.find('https://champlain.instructure.com/api/v1/users') == 0 and flow.url.find('files?search_term=') > -1):
		type = 'User Action: Search Files'
		info = AppDefault.findFormEntry(flow.requestContent, 'search_term')
		results.append(Result.Result(flow, type, info))


def checkPostURL(flow, results):
	flow.source = 'Canvas'

	if (flow.url == 'https://my.champlain.edu/auth/login'):
		flow.source = 'Canvas Login'
		type = 'User Info: Canvas Username'
		info = AppDefault.findFormEntry(flow.requestContent, 'username')
		results.append(Result.Result(flow, type, info))

		#type = 'User Info: Canvas Password'
		#info = AppDefault.findFormEntry(flow.requestContent, 'password')
		#results.append(Result.Result(flow, type, info))

	elif (flow.url.find('https://champlain.instructure.com/login/oauth2/token') == 0):
		type = 'System Info: Canvas Client ID'
		info = AppDefault.findFormEntry(flow.requestContent, 'client_id')
		results.append(Result.Result(flow, type, info))

		type = 'System Info: Canvas Client Secret'
		info = AppDefault.findFormEntry(flow.requestContent, 'client_secret')
		results.append(Result.Result(flow, type, info))

	elif (flow.url.find('https://champlain.instructure.com/api/v1/calendar_events/?calendar_event') == 0):
		type = 'User Action: Created Calendar Event'
		info = flow.responseContent
		results.append(Result.Result(flow, type, info))


def checkHeadURL(flow, results):
	return None

def checkPutURL(flow, results):
	return None

def checkDeleteURL(flow, results):
	if (flow.url.find('https://champlain.instructure.com/api/v1/calendar_events') == 0):
		type = 'User Action: Delete Calendar Event'
		info = flow.url[flow.url.find('calendar_events/')+16:]
		info = info[:info.find('?')]
		results.append(Result.Result(flow, type, info))
