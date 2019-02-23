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
		results.append(Result.Result(flow.app, flow.destination, flow.source, type, info, flow.all))

def analyzePostRequestDefault(flow, results):
	if (checkFlowResults('IP Address', results) == False):
		info = flow.address
		type = 'IP Address'
		results.append(Result.Result(flow.app, flow.destination, flow.source, type, info, flow.all))

	if (flow.url == 'https://android.clients.google.com/c2dm/register3'):
		flow.source = flow.requestHeaders['app'] + ' Login'
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
	

def analyzeHeadRequestDefault(flow, results):
	if (checkFlowResults('IP Address', results) == False):
		info = flow.address
		type = 'IP Address'
		results.append(Result.Result(flow.source, flow.destination, flow.source, type, info, flow.all))

def analyzePutRequestDefault(flow, results):
	if (checkFlowResults('IP Address', results) == False):
		info = flow.address
		type = 'IP Address'
		results.append(Result.Result(flow.app, flow.destination, flow.source, type, info, flow.all))

def checkRequestHeadersDefault(flow, headers, results):
	if ('User-Agent' in headers.keys() and checkFlowResults('System Info: User-Agent', results) == False):
		info = headers['User-Agent']
		type = 'System Info: User-Agent'
		results.append(Result.Result(flow.app, flow.destination, flow.source, type, info, flow.all))
	if ('Cookie' in headers.keys() and checkFlowResults('System Info: Cookie', results) == False):
		info = headers['Cookie']
		type = 'System Info: Cookie'
		results.append(Result.Result(flow.app, flow.destination, flow.source, type, info, flow.all))
	if ('x-dfe-device-id' in headers.keys() and checkFlowResults('System Info: Device ID', results) == False):
		info = headers['x-dfe-device-id']
		type = 'System Info: Device ID'
		results.append(Result.Result(flow.app, flow.destination, flow.source, type, info, flow.all))
	if ('x-dfe-device-config-token' in headers.keys() and checkFlowResults('System Info: Config Token', results) == False):
		info = headers['x-dfe-device-config-token']
		type = 'System Info: Config Token'
		results.append(Result.Result(flow.app, flow.destination, flow.source, type, info, flow.all))
	if ('x-ad-id' in headers.keys()):
		info = headers['x-ad-id']
		type = 'User Info: Ad Tracking ID'
		results.append(Result.Result(flow.app, flow.destination, flow.source, type, info, flow.all))

def checkResponseHeadersDefault(flow, headers, results):
	if ('Set-Cookie' in headers.keys()):
		info = headers['Set-Cookie']
		type = 'System Info: Cookie'
		results.append(Result.Result(flow.app, flow.destination, flow.source, type, info, flow.all))
	if ('Set-Cookie-1' in headers.keys()):
		info = headers['Set-Cookie-1']
		type = 'System Info: Cookie'
		results.append(Result.Result(flow.app, flow.destination, flow.source, type, info, flow.all))
	if ('Set-Cookie-2' in headers.keys()):
		info = headers['Set-Cookie-2']
		type = 'System Info: Cookie'
		results.append(Result.Result(flow.app, flow.destination, flow.source, type, info, flow.all))
	if ('Content-Type' in headers.keys() and headers['Content-Type'][:5] == 'image'):
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
		if (part[index:index+1] == '['):
			count = count + 1
		elif (part[index:index+1] == ']'):
			count = count - 1
		index = index + 1
	part = part[:index]
	return part
