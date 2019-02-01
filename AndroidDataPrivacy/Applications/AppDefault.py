import AndroidDataPrivacy.Flow as Flow
import AndroidDataPrivacy.Result as Result

source = ''
destination = ''
type = ''
info = ''

def checkBehavior(flow, results):
	if (flow.requestType == 'GET'):
		analyzeGetRequestDefault(flow, results)
	if (flow.requestType == 'POST'):
		analyzePostRequestDefault(flow, results)
	if (flow.requestType == 'HEAD'):
		analyzeHeadRequestDefault(flow, results)
	checkRequestHeadersDefault(flow, flow.requestHeaders, results)
	checkResponseHeadersDefault(flow, flow.responseHeaders, results)

def analyzeGetRequestDefault(flow, results):
	if (checkFlowResults('IP Address', results) == False):
		info = flow.address
		type = 'IP Address'
		results.append(Result.Result(flow.app, flow.destination, flow.source, type, info))

def analyzePostRequestDefault(flow, results):
	if (checkFlowResults('IP Address', results) == False):
		info = flow.address
		type = 'IP Address'
		results.append(Result.Result(flow.app, flow.destination, flow.source, type, info))

def analyzeHeadRequestDefault(flow, results):
	if (checkFlowResults('IP Address', results) == False):
		info = flow.address
		type = 'IP Address'
		results.append(Result.Result(flow.source, flow.destination, flow.source, type, info))

def checkRequestHeadersDefault(flow, headers, results):
	if ('User-Agent' in headers.keys() and checkFlowResults('System Info: User-Agent', results) == False):
		info = headers['User-Agent']
		type = 'System Info: User-Agent'
		results.append(Result.Result(flow.app, flow.destination, flow.source, type, info))
	if ('Cookie' in headers.keys() and checkFlowResults('System Info: Cookie', results) == False):
		info = headers['Cookie']
		type = 'System Info: Cookie'
		results.append(Result.Result(flow.app, flow.destination, flow.source, type, info))

def checkResponseHeadersDefault(flow, headers, results):
	if ('Set-Cookie' in headers.keys() and checkFlowResults('System Info: Cookie', results) == False):
		info = headers['Set-Cookie']
		type = 'System Info: Cookie'
		results.append(Result.Result(flow.app, flow.destination, flow.source, type, info))
	if ('content-type' in headers.keys() and headers['content-type'][:5] == 'image'):
		flow.source = 'Picture Download'

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
	return output

