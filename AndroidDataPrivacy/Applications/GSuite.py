import AndroidDataPrivacy.Flow as Flow
import AndroidDataPrivacy.Result as Result
import AndroidDataPrivacy.Applications.AppDefault as AppDefault

urls = ['https://www.googleapis.com/plusdatamixer/v1/mutate']

partialURLs = ['https://www.googleapis.com/drive/v2internal/files', \
'https://inbox.google.com/sync', \
'https://mail.google.com/mail', \
'https://www.googleapis.com/discussions/v1', \
'https://docs.google.com/document', \
'https://docs.google.com/spreadsheets', \
'https://photosdata-pa.googleapis.com', \
'https://photos.googleapis.com/data/upload']

userAgents = []

partialUserAgents = ['Android-Gmail', \
'Cakemix', \
'com.google.android.apps.photos']

appIds = {'1:493454522602:android:4877c2b5f408a8b2':'com.google.android.apps.maps', \
'1:206908507205:android:167bd0ff59cd7d44':'com.google.android.apps.tachyon'}

def checkBehavior(flow, results):
	if (flow.requestType == 'GET'):
		analyzeGetRequest(flow, results)
	if (flow.requestType == 'POST'):
		analyzePostRequest(flow, results)
	if (flow.requestType == 'HEAD'):
		analyzeHeadRequest(flow, results)
	if (flow.requestType == 'PUT'):
		analyzePutRequest(flow, results)

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

def checkRequestHeaders(flow, headers, results):
	if ('referer' in headers.keys()):
		if (headers['referer'] == 'android-app://com.google.android.gm'):
			flow.source = 'Gmail'

	elif ('User-Agent' in headers.keys()):
		if (headers['User-Agent'][:13] == 'Android-Gmail' and flow.source == ''):
			flow.source = 'GMail'

		elif (headers['User-Agent'][:7] == 'Cakemix' and flow.source == ''):
			if (headers['User-Agent'].find('Google.Docs') > -1):
				flow.source = 'Google Docs'
			elif (headers['User-Agent'].find('Google.Sheets') > -1):
				flow.source = 'Google Sheets'
			elif (headers['x-google-drive-feature-label'][:5] == 'cello' and flow.source == ''):
				flow.source = 'Google Drive Sync'
			else:
				flow.source = 'Google Drive'

		elif (headers['User-Agent'][:30] == 'com.google.android.apps.photos' and flow.source == ''):
			flow.source = 'Google Photos'

def checkResponseHeaders(flow, headers, results):
	if ('Content-Type' in headers.keys() and headers['Content-Type'][:5] == 'image'):
		if ('User-Agent' in flow.requestHeaders.keys() and flow.requestHeaders['User-Agent'][:30] == 'com.google.android.apps.photos'):
			flow.source = 'Google Photos'
			if (flow.url.find('https://ap2.googleusercontent.com') == 0):
				if (AppDefault.findFormEntry(flow.responseContent, 'Size').strip() == '246 x 328 px' or \
					AppDefault.findFormEntry(flow.responseContent, 'Size').strip() == '38 x 50 px'):
					flow.source = 'Google Photos Thumbnail'
				type = 'Possible User Action'
				picName = flow.responseHeaders['content-disposition'][flow.responseHeaders['content-disposition'].find('filename=')+10:]
				picName = picName[:picName.find('"')]
				info = 'Image Viewed: ' + picName
				results.append(Result.Result(flow.app, flow.destination, flow.source, type, info, flow.all))

def checkGetURL(flow, results):
	if (flow.url.find('https://www.googleapis.com/drive/v2internal/files') == 0):
		flow.source = 'Google Drive File Lookup'
	elif (flow.url.find('https://www.googleapis.com/drive/v2internal/changes') == 0):
		flow.source = 'Google Drive File Sync'
	elif (flow.url.find('https://www.googleapis.com/discussions/v1/authors') == 0):
		flow.source = 'Google Drive Comments'
	elif (flow.url.find('https://docs.google.com/document/d') == 0):
		flow.source = 'Google Docs'
		if (flow.url.find('leave') > -1):
			type = 'User Action'
			info = 'Document Deleted: '
			docID = flow.url[35:]
			docID = docID[:docID.find('/')]
			info = info + docID
			results.append(Result.Result(flow.app, flow.destination, flow.source, type, info, flow.all))
		else:
			type = 'User Action'
			info = 'Document Opened: '
			docID = flow.url[35:]
			docID = docID[:docID.find('/')]
			info = info + docID
			if (flow.responseContent.find('":"') > -1 and flow.url.find('edit') > -1):
				name = flow.responseContent[flow.responseContent.find('"t":"')+5:]
				name = name[:name.find('"')]
				info = info + ' (' + name + ')'
			results.append(Result.Result(flow.app, flow.destination, flow.source, type, info, flow.all))
	elif (flow.url.find('https://docs.google.com/spreadsheets/d') == 0):
		flow.source = 'Google Sheets'
		if (flow.url.find('leave') > -1):
			type = 'User Action'
			info = 'Document Deleted: '
			docID = flow.url[39:]
			docID = docID[:docID.find('/')]
			info = info + docID
			results.append(Result.Result(flow.app, flow.destination, flow.source, type, info, flow.all))
		else:
			type = 'User Action'
			info = 'Spreadsheet Opened: '
			docID = flow.url[39:]
			docID = docID[:docID.find('/')]
			info = info + docID
			if (flow.responseContent.find('":"') > -1 and (flow.url.find('edit') > -1 or flow.url.find('model') > -1)):
				name = flow.responseContent[flow.responseContent.find('"t":"')+5:]
				name = name[:name.find('"')]
				info = info + ' (' + name + ')'
			results.append(Result.Result(flow.app, flow.destination, flow.source, type, info, flow.all))

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

	elif (flow.url.find('https://inbox.google.com/sync') == 0):
		flow.source = 'Gmail Inbox Sync'

	elif (flow.url.find('https://mail.google.com/mail/ads') == 0):
		flow.source = 'Gmail Ads'

	elif (flow.url == 'https://www.googleapis.com/plusdatamixer/v1/mutate'):
		flow.source = 'Google Drive'

	elif (flow.url.find('https://www.googleapis.com/discussions/v1/targets') == 0):
		flow.source = 'Google Drive Comments'

	elif (flow.url.find('https://docs.google.com/document/create') == 0):
		flow.source = 'Google Docs'
		type = "User Action"
		info = 'Create New Document: ' + AppDefault.findFormEntry(flow.requestContent, 'title')
		results.append(Result.Result(flow.app, flow.destination, flow.source, type, info, flow.all))

	elif (flow.url.find('https://docs.google.com/document/d') == 0):
		flow.source = 'Google Docs'
		if (flow.url.find('/save?') > -1):
			type = 'User Action: Edit Document'
			temp = AppDefault.findFormEntry(flow.requestContent, 'bundles')
			temp = AppDefault.findJSONListNonSpaced(flow.requestContent, 'commands')
			temp = temp[2:len(temp)-2]
			commands = []
			print(flow.requestContent)
			for item in temp.split('},{'):
				commands.append(item)
			for item in commands:
				entries = {}
				print(item)
				for i in item.split(','):
					#print(i.split(':'))
					temp = i.split(':')[0]
					temp2 = i.split(':')[1]
					entries[temp] = temp2
				print(entries)
				if ('"s"' in entries.keys()):
					type = 'User Action'
					info = 'Inserted ' + entries['"s"']
					results.append(Result.Result(flow.app, flow.destination, flow.source, type, info, flow.all))
				if ('"si"' in entries.keys()):
					type = 'User Action'
					info = 'Deleted Index: ' + entries['"si"']
					results.append(Result.Result(flow.app, flow.destination, flow.source, type, info, flow.all))

	elif (flow.url == 'https://www.googleapis.com/batch/drive/v2internal'):
		if (flow.requestContent.find('{"additionalRoles":') > -1):
			flow.source = 'Google Drive'
			type = 'User Action'
			info = flow.requestContent[flow.requestContent.find('{"additionalRoles":'):]
			info = info[:info.find('}')+1]
			info = 'File Role Change: ' + info
			results.append(Result.Result(flow.app, flow.destination, flow.source, type, info, flow.all))
		elif (flow.requestContent.find('GET https://www.googleapis.com/drive/v2internal/files') > -1):
			flow.source = 'Google Drive File Lookup'

	elif (flow.url.find('https://photosdata-pa.googleapis.com') == 0):
		flow.source = 'Google Photos'

	elif (flow.url.find('https://photos.googleapis.com/data/upload') == 0):
		flow.source = 'Google Photos Upload'
		type = 'User Action'
		info = 'Photo Uploaded: ' + flow.requestHeaders['x-goog-upload-file-name']
		results.append(Result.Result(flow.app, flow.destination, flow.source, type, info, flow.all))

def checkHeadURL(flow, results):
	return None

def checkPutURL(flow, results):
	if (flow.url.find('https://www.googleapis.com/drive/v2internal/files') == 0):
		flow.source = 'Google Drive'
		if (flow.requestContent.find('"title":') > -1):
			type = 'User Action'
			info = flow.requestContent[flow.requestContent.find('"title":')+8:]
			info = info[:info.find('\n')].strip()
			info = info[1:len(info)-1]
			docID = flow.url[50:]
			docID = docID[:docID.find('?')]
			info = 'Rename File: ' + docID + ' (' + info + ')'
			results.append(Result.Result(flow.app, flow.destination, flow.source, type, info, flow.all))

		elif (flow.requestContent.find('"lastViewedByMeDate":')):
			type = 'User Action'
			info = flow.requestContent[flow.requestContent.find('"lastViewedByMeDate":'):]
			info = info[:info.find('\n')]
			info = info.split(' ')[1]
			info = info[1:len(info)-1]
			docID = flow.url[50:]
			docID = docID[:docID.find('?')]
			info = "Document Opened: " + docID + ' @ ' + info
			results.append(Result.Result(flow.app, flow.destination, flow.source, type, info, flow.all))

	elif (flow.url.find('https://photos.googleapis.com/data/upload') == 0):
		flow.source = 'Google Photos Upload'
