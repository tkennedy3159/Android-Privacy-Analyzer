class Result:
	
	source = ''
	destination = ''
	type = ''
	info = ''
	log = ''
	description = ''
	

	def __init__(self, aApp, aDestination, aSource, aType, aInfo):
		self.source = aSource
		self.destination = aDestination
		self.type = aType
		self.info = aInfo
		self.description = self.setDescription(self.type)
		self.log = 'Source: ' + self.source + '\n' + \
		'Destination: ' + self.destination + '\n' + \
		'Type: ' + self.type + '\n' + \
		'Info: ' + self.info
	
	def setDescription(self, type):
		return ''

	def syncSourceLog(self):
		self.log = 'Source: ' + self.source + '\n' + \
		'Destination: ' + self.destination + '\n' + \
		'Type: ' + self.type + '\n' + \
		'Info: ' + self.info