class Flow:
	
	all = ''
	address = ''
	port = ''
	type = ''
	app = ''
	destination = ''
	source = ''
	url = ''
	request = ''
	requestType = ''
	requestHeaders = {}
	requestContent = ''
	response = ''
	responseHeaders = {}
	responseContent = ''
	
	def __init__(self, aflow):
		self.all = aflow
		self.address = self.getAddress(all)
		self.port = self.getPort(all)
		self.type = self.getType(all)
		if (self.type[0:13] == 'clientconnect'):
			print('', end='')
		if (self.type[0:13] == 'serverconnect'):
			print('', end='')
		if (self.type[0:23] == 'Set new server address:'):
			print('', end='')
		if (self.type[0:7] == 'request'):
			print('', end='')
		if (self.type[0:8] == 'response'):
			print('', end='')
		if (self.type[0:25] == 'Establish TLS with server'):
			print('', end='')
		if (self.type[0:25] == 'Establish TLS with client'):
			print('', end='')
		if (self.type[0:24] == 'ALPN selected by server:'):
			print('', end='')
		if (self.type[0:16] == 'ALPN for client:'):
			print('', end='')
		if (self.type[0:23] == 'HTTP2 Event from client'):
			print('', end='')
		if (self.type[0:23] == 'HTTP2 Event from server'):
			print('', end='')
		if (self.type[0:3] == 'GET' or self.type[0:4] == 'POST' or self.type[0:4] == 'HEAD' or self.type[0:3] == 'PUT' or self.type[0:6] == 'DELETE'):
			self.request = self.separateRequest(all)
			self.response = self.separateResponse(all)
			self.requestHeaders = self.getHeaders(self.request)
			self.responseHeaders = self.getHeaders(self.response)
			self.requestContent = self.getContent(self.request)
			self.responseContent = self.getContent(self.response)
			self.requestType = self.type[0:self.type.find(' ')]
			self.url = self.type[self.type.find(' '):].strip()
			if (self.url.find(' ') > -1):
				self.url = self.url[:self.url.find(' ')]
			self.destination = self.url[self.url.find('://')+3:]
			self.destination = self.destination[:self.destination.find('/')]
	
	def getAddress(self, all):
		if (self.all[0:7] == '::ffff:'):
			address = self.all[7:]
			addrEnd = address.find(':')
			address = address[0:addrEnd]
		else:
			addrEnd = self.all.find(':')
			address = self.all[0:addrEnd]
		return address

	def getPort(self, all):
		if (self.all[0:7] == '::ffff:'):
			port = self.all[7:]
			addrEnd = port.find(':')
			port = port[addrEnd+1:]
			port = port[0:port.find(':')]
		else:
			addrEnd = self.all.find(':')
			port = self.all[addrEnd+1:]
			port = port[0:port.find(':')]
		return port
	
	def getType(self, all):
		if (self.all[0:7] == '::ffff:'):
			port = self.all[7:]
			addrEnd = port.find(':')
			port = port[addrEnd+1:]
			portEnd = port.find(':')
			type = port[portEnd+2:port.find('\n')]
		else:
			addrEnd = self.all.find(':')
			port = self.all[addrEnd+1:]
			portEnd = port.find(':')
			type = port[portEnd+2:port.find('\n')]
		return type
	
	def separateRequest(self, all):
		if (self.type[0:3] == 'GET' or self.type[0:4] == 'POST' or self.type[0:4] == 'HEAD' or self.type[0:3] == 'PUT' or self.type[0:6] == 'DELETE'):
			request = self.all[:self.all.find('<<')].strip()
		else:
			request = ''
		return request

	def separateResponse(self, all):
		if (self.type[0:3] == 'GET' or self.type[0:4] == 'POST' or self.type[0:4] == 'HEAD' or self.type[0:3] == 'PUT' or self.type[0:6] == 'DELETE'):
			response = self.all[self.all.find('<<'):].strip()
		else:
			response = ''
		return response

	def getHeaders(self, part):
		headers = {}
		headerBlock = part[part.find('\n')+1:]
		line = headerBlock[:headerBlock.find('\n')]
		while (line != ''):
			if (line.strip()[0] == ':'):
				line = line[line.find(':')+1:]
			type = line[:line.find(':')].strip()
			value = line[line.find(':')+1:].strip()
			num = 1
			if type in headers:
				type = type + '-1'
			while (type in headers):
				num = num + 1
				type = type[:len(type)-1] + str(num)
			headers[type] = value
			if (headerBlock.find('\n') > -1):
				headerBlock = headerBlock[headerBlock.find('\n')+1:]
				if (headerBlock.find('\n') > -1):
					line = headerBlock[:headerBlock.find('\n')]
				else:
					line = headerBlock
			else:
				line = ''
		if ('user-agent' in headers):
			headers['User-Agent'] = headers['user-agent']
			del headers['user-agent']
		if ('cookie' in headers):
			headers['Cookie'] = headers['cookie']
			del headers['cookie']
		if ('x-dfe-cookie' in headers):
			headers['Cookie'] = headers['x-dfe-cookie']
			del headers['x-dfe-cookie']
		if ('set-cookie' in headers):
			headers['Set-Cookie'] = headers['set-cookie']
			del headers['set-cookie']
		if ('set-cookie-1' in headers):
			headers['Set-Cookie-1'] = headers['set-cookie-1']
			del headers['set-cookie-1']
		if ('set-cookie-2' in headers):
			headers['Set-Cookie-2'] = headers['set-cookie-2']
			del headers['set-cookie-2']
		if ('content-type' in headers):
			headers['Content-Type'] = headers['content-type']
			del headers['content-type']
		if ('authorization' in headers):
			headers['Authorization'] = headers['authorization']
			del headers['authorization']
		return headers

	def getContent(self, part):
		part = part[part.find('\n')+1:]
		line = part[:part.find('\n')]
		while (line != ''):
			if (part.find('\n') > -1):
				part = part[part.find('\n')+1:]
				if (part.find('\n') > -1):
					line = part[:part.find('\n')]
				else:
					line = part
			else:
				part = part[len(line):]
				line = ''
		content = part.strip()
		return content

