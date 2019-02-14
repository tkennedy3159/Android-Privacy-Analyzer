class Result:
	
	source = ''
	destination = ''
	type = ''
	info = ''
	log = ''

	def __init__(self, aApp, aDestination, aSource, aType, aInfo):
		self.source = aSource
		self.destination = aDestination
		self.type = aType
		self.info = aInfo
		self.log = self.source + ';;;;;' + \
		self.destination + ';;;;;' + \
		self.type + ';;;;;' + \
		self.info

	def syncSourceLog(self):
		self.log = self.source + ';;;;;' + \
        self.destination + ';;;;;' + \
        self.type + ';;;;;' + \
        self.info
