class Result:
	
	source = ''
	destination = ''
	type = ''
	info = ''
	flowContent = ''
	log = ''
	logFull = ''

	def __init__(self, aApp, aDestination, aSource, aType, aInfo, aflowContent):
		self.source = aSource
		self.destination = aDestination
		self.type = aType
		self.info = aInfo
		self.flowContent = aflowContent
		self.log = self.source + ';;;;;' + \
		self.destination + ';;;;;' + \
		self.type + ';;;;;' + \
		self.info
		self.logFull = self.log + ';;;;;' + '\n\n' + self.flowContent

	def __init__(self, flow, aType, aInfo):
		self.source = flow.source
		self.destination = flow.destination
		self.type = aType
		self.info = aInfo
		self.flowContent = flow.all
		self.log = self.source + ';;;;;' + \
		self.destination + ';;;;;' + \
		self.type + ';;;;;' + \
		self.info
		self.logFull = self.log + ';;;;;' + '\n\n' + self.flowContent

	def syncSourceLog(self):
		self.log = self.source + ';;;;;' + \
        self.destination + ';;;;;' + \
        self.type + ';;;;;' + \
        self.info
		self.logFull = self.log + ';;;;;' + '\n\n' + self.flowContent
