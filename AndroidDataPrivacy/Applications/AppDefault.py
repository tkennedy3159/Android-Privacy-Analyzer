import AndroidDataPrivacy.Flow as Flow
import AndroidDataPrivacy.Result as Result

def checkBehavior(flow, results):
	if (flow.requestType == 'GET'):
		analyzeGetRequestDefault(flow, results)
	if (flow.requestType == 'POST'):
		analyzePostRequestDefault(flow, results)
	if (flow.requestType == 'HEAD'):
		analyzeHeadRequestDefault(flow, results)
	if (flow.requestType == 'PUT'):
		analyzePutRequestDefault(flow, results)
	checkRequestHeadersDefault(flow, flow.requestHeaders, results)
	checkResponseHeadersDefault(flow, flow.responseHeaders, results)

def analyzeGetRequestDefault(flow, results):
	if (checkFlowResults('IP Address', results) == False):
		info = flow.address
		type = 'IP Address'
		results.append(Result.Result(flow, type, info))

def analyzePostRequestDefault(flow, results):
	if (checkFlowResults('IP Address', results) == False):
		info = flow.address
		type = 'IP Address'
		results.append(Result.Result(flow, type, info))

	if (flow.url == 'https://android.clients.google.com/c2dm/register3'):
		flow.source = flow.requestHeaders['app'] + ' GCM Login'
		type = 'System Info: Device ID'
		info = flow.requestContent
		info = info[info.find('device:')+7:]
		info = info[:info.find('\n')]
		info = info.strip()
		results.append(Result.Result(flow, type, info))
		
		type = 'Token'
		info = flow.responseContent
		info = info[info.find('token=')+6:]
		info = info.strip()
		results.append(Result.Result(flow, type, info))

		type = 'Certificate'
		info = findFormEntry(flow.requestContent, 'cert')
		results.append(Result.Result(flow, type, info))
	
	elif (flow.url.find('appsflyer.com/api') > -1):
		content = flow.requestContent
		if (flow.url.find('https://t.appsflyer.com/api') == 0):
			flow.source = flow.url[flow.url.find('app_id=')+7:]
			flow.source = 'AppsFlyer ' + flow.source

		if (flow.url.find('https://register.appsflyer.com/api') == 0):
			flow.source = content[content.find('"app_name":')+13:]
			flow.source = flow.source[:flow.source.find('"')] + ' AppsFlyer'

		if (flow.url.find('https://events.appsflyer.com/api') == 0):
			flow.source = flow.url[flow.url.find('app_id=')+7:]
			if (flow.source.find('&') > -1):
				flow.source = flow.source[:flow.source.find('&')]
			flow.source = flow.source + ' AppsFlyer'

		type = 'Ad ID'
		info = content[content.find('"advertiserId":')+17:]
		info = info[:info.find('"')]
		results.append(Result.Result(flow, type, info))

		if (flow.requestContent.find('"android_id":') > -1):
			type = 'Android ID'
			info = content[content.find('"android_id":')+15:]
			info = info[:info.find('"')]
			results.append(Result.Result(flow, type, info))

		type = 'AppsFlyer Key'
		info = content[content.find('"appsflyerKey":')+17:]
		info = info[:info.find('"')]
		results.append(Result.Result(flow, type, info))

		if (flow.requestContent.find('"counter":') > -1):
			type = 'User Info: Opened App Count'
			info = content[content.find('"counter":')+12:]
			info = info[:info.find('"')]
			results.append(Result.Result(flow, type, info))

		if (flow.requestContent.find('"batteryLevel":') > -1):
			type = 'System Info: Battery Level'
			info = content[content.find('"batteryLevel":')+17:]
			info = info[:info.find('"')] + '%'
			results.append(Result.Result(flow, type, info))

		type = 'System Info: Brand'
		info = content[content.find('"brand":')+10:]
		info = info[:info.find('"')]
		results.append(Result.Result(flow, type, info))

		type = 'System Info: Build'
		info = content[content.find('"build_display_id":')+21:]
		info = info[:info.find('"')]
		results.append(Result.Result(flow, type, info))

		type = 'System Info: Screen Size'
		width = content[content.find('"x_px":')+9:]
		width = width[:width.find('"')]
		height = content[content.find('"y_px":')+9:]
		height = height[:height.find('"')]
		info = width + ' x ' + height
		results.append(Result.Result(flow, type, info))

		if (flow.requestContent.find('sensors') > -1):
			type = 'System Info: Sensor Data'
			info = findJSONListNonSpaced(flow.requestContent, 'sensors')
			results.append(Result.Result(flow, type, info))

		if (flow.requestContent.find('"af_gcm_token":') > -1):
			type = 'AppFlyer GCM Token'
			info = content[content.find('"af_gcm_token":')+17:]
			info = info[:info.find('"')]
			results.append(Result.Result(flow, type, info))

		type = 'System Info: App Version'
		info = content[content.find('"app_version_name":')+21:]
		info = info[:info.find('"')]
		results.append(Result.Result(flow, type, info))

		type = 'System Info: App Install Date'
		info = content[content.find('"installDate":')+16:]
		info = info[:info.find('"')]
		results.append(Result.Result(flow, type, info))

		if (flow.requestContent.find('"launch_counter":') > -1):
			type = 'User Info: App Launch Count'
			info = content[content.find('"launch_counter":')+19:]
			info = info[:info.find('"')]
			results.append(Result.Result(flow, type, info))

		type = 'System Info: Model'
		brand = content[content.find('"brand":')+10:]
		brand = brand[:brand.find('"')]
		model = content[content.find('"model":')+10:]
		model = model[:model.find('"')]
		info = brand + ' ' + model
		results.append(Result.Result(flow, type, info))

		type = 'System Info: Network Connection'
		info = content[content.find('"network":')+12:]
		info = info[:info.find('"')]
		results.append(Result.Result(flow, type, info))

		type = 'System Info: AppsFlyer UID'
		info = content[content.find('"uid":')+8:]
		info = info[:info.find('"')]
		results.append(Result.Result(flow, type, info))

	elif (flow.url == 'https://api.branch.io/v1/close'):
		flow.source = 'Branch.io'
		type = 'User Action: Closed App'
		branchkey = flow.requestContent[flow.requestContent.find('"branch_key":')+15:]
		branchkey = branchkey[:branchkey.find('"')]
		sessionkey = flow.requestContent[flow.requestContent.find('"session_id":')+15:]
		sessionkey = sessionkey[:sessionkey.find('"')]
		info = 'Closed App with Branch Key ' + branchkey + ' and session ID ' + sessionkey
		results.append(Result.Result(flow, type, info))

def analyzeHeadRequestDefault(flow, results):
	if (checkFlowResults('IP Address', results) == False):
		info = flow.address
		type = 'IP Address'
		results.append(Result.Result(flow.source, flow.destination, flow.source, type, info, flow.all))

def analyzePutRequestDefault(flow, results):
	if (checkFlowResults('IP Address', results) == False):
		info = flow.address
		type = 'IP Address'
		results.append(Result.Result(flow, type, info))

def analyzeDeleteRequestDefault(flow, results):
	return None

def checkRequestHeadersDefault(flow, headers, results):
	if ('User-Agent' in headers.keys() and checkFlowResults('System Info: User-Agent', results) == False):
		info = headers['User-Agent']
		type = 'System Info: User-Agent'
		results.append(Result.Result(flow, type, info))
	if ('Cookie' in headers.keys() and checkFlowResults('System Info: Cookie', results) == False):
		info = headers['Cookie']
		type = 'System Info: Cookie'
		results.append(Result.Result(flow, type, info))
	if ('x-dfe-device-id' in headers.keys() and checkFlowResults('System Info: Device ID', results) == False):
		info = headers['x-dfe-device-id']
		type = 'System Info: Device ID'
		results.append(Result.Result(flow, type, info))
	if ('x-dfe-device-config-token' in headers.keys() and checkFlowResults('System Info: Config Token', results) == False):
		info = headers['x-dfe-device-config-token']
		type = 'System Info: Config Token'
		results.append(Result.Result(flow, type, info))
	if ('x-ad-id' in headers.keys()):
		info = headers['x-ad-id']
		type = 'User Info: Ad Tracking ID'
		results.append(Result.Result(flow, type, info))
	if ('Authorization' in headers.keys()):
		info = headers['Authorization']
		type = 'Authorization'
		results.append(Result.Result(flow, type, info))
	if ('x-device-boot-count' in headers.keys()):
		info = headers['x-device-boot-count']
		type = 'System Info: Boot Count'
		results.append(Result.Result(flow, type, info))
	if ('x-device-id' in headers.keys()):
		info = headers['x-device-id']
		type = 'System Info: Device ID'
		results.append(Result.Result(flow, type, info))


def checkResponseHeadersDefault(flow, headers, results):
	if ('Set-Cookie' in headers.keys()):
		info = headers['Set-Cookie']
		type = 'System Info: Cookie'
		results.append(Result.Result(flow, type, info))
	if ('Set-Cookie-1' in headers.keys()):
		info = headers['Set-Cookie-1']
		type = 'System Info: Cookie'
		results.append(Result.Result(flow, type, info))
	if ('Set-Cookie-2' in headers.keys()):
		info = headers['Set-Cookie-2']
		type = 'System Info: Cookie'
		results.append(Result.Result(flow, type, info))
	if ('Content-Type' in headers.keys() and headers['Content-Type'][:5] == 'image' and flow.url.find('app-measurement.com') < 0):
		if (flow.source != 'Google Analytics'):
			if (len(flow.source) > 0):
				flow.source = flow.source + ' Image Download'
			else:
				flow.source = 'Image Download'
	elif ('Content-Type' in headers.keys() and headers['Content-Type'][:4] == 'font'):
		if (len(flow.source) > 0):
			flow.source = flow.source + ' Font Download'
		else:
			flow.source = 'Font Download'

def checkFlowResults(resultType, results):
	for result in results:
		if (result.type == resultType):
			return True
	return False

def syncSource(flow, results):
	for item in results:
		item.source = flow.source
		item.syncSourceLog()

def cleanEncoding(input):
	output = ''
	while (len(input) >= 4):
		output = output + input[:input.find('\\x')]
		input = input[input.find('\\x')+4:]
		if (input[:1] == '_'):
			input = input[2:]
	return output

def fixUrlEncoding(input):
	output = ''
	while (len(input) >= 3):
		output = output + input[:input.find('%')]
		input = input[input.find('%'):]
		temp = input[:3]
		input = input[3:]
		if (temp == '%3A'):
			temp = ':'
		output = output + temp
	return output

def findFormEntry(content, entry):
	line = content[content.find(entry+':'):]
	if (line.find('\n') > -1):
		line = line[:line.find('\n')]
	answer = line[len(entry)+1:].strip()
	return answer

def findJSONSection(content, section):
	part = content[content.find('"'+section+'": {'):]
	temp = part
	part = part[:part.find('\n')+1]
	count = 1
	while count > 0:
		temp = temp[temp.find('\n')+1:]
		line = temp[:temp.find('\n')+1]
		part = part + line
		line = line.strip()
		if (line[:1] == '{'):
			count = count + 1
		elif (line[:1] == '}'):
			count = count - 1
	return part

def findJSONList(content, listName):
	part = content[content.find('"'+listName+'": ['):]
	temp = part
	part = part[:part.find('\n')+1]
	count = 1
	while count > 0:
		temp = temp[temp.find('\n')+1:]
		line = temp[:temp.find('\n')+1]
		part = part + line
		line = line.strip()
		if (line[:1] == '['):
			count = count + 1
		elif (line[:1] == ']'):
			count = count - 1
	part = part[part.find('\n')+1:]
	items = []
	temp = ''
	count = 0
	for line in part.split('\n'):
		if (line.strip()[:1] == '{' or line.strip()[len(line)-2:] == '{'):
			if (count == 0 and len(temp) > 0):
				items.append(temp)
				temp = line
			else:
				temp = temp + line + '\n'
				count = count + 1
		elif (line.strip()[:1] == '}'):
			temp = temp + line + '\n'
			count = count - 1
		else:
			temp = temp + line + '\n'
	items.append(temp)
	return items

def findJSONListNonSpaced(content, listName):
	part = content[content.find('"'+listName+'":'):]
	part = part[part.find('['):]
	count = 1
	index = 1
	while count > 0:
		if (part[index:index+9] == '(cut off)'):
			count = 0
		else:
			if (part[index:index+1] == '['):
				count = count + 1
			elif (part[index:index+1] == ']'):
				count = count - 1
			index = index + 1
	part = part[:index]
	return part

def findJSONItem(content, itemName):
	item = content[content.find(itemName):]
	comma = item[:item.find(',')]
	bracket = item[:item.find('}')]
	if (item.find(',') > -1 and item.find('}') > -1):
		if (len(comma) < len(bracket)):
			item = comma
		else:
			item = bracket
	elif (item.find(',') > -1):
		item = comma
	elif (item.find('}') > -1):
		item = bracket
	item = item[item.find(':')+1:].strip()
	if(item[:1] == '"' and item[len(item)-1:len(item)] == '"'):
		item = item[1:len(item)-1]
	return item

def findJSONGroup(content, groupName):
	bracketindex = len(groupName) + 2
	group = content[content.find(groupName):]
	while bracketindex > (len(groupName) + 1):
		group = group[len(groupName)+1:]
		group = group[group.find(groupName):]
		bracketindex = group.find('{')
	group = group[bracketindex+1:]
	count = 1
	index = 1
	while count > 0:
		if (group[index:index+9] == '(cut off)'):
			count = 0
		else:
			if (group[index:index+1] == '{'):
				count = count + 1
			elif (group[index:index+1] == '}'):
				count = count - 1
			index = index + 1
	group = group[:index+bracketindex]
	return group