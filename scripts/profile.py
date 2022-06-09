from errors import ProfileInvalidationError
from errors import ProfileParseError
import json

class DisrichieProfile:
	path: str = None
	data = None

	def __init__(self, path: str = '{}'):
		self.path = path
		self.parse()
		self.invalidate()
	
	def parse(self):
		if self.path == None: raise ProfileParseError()
		if self.path != '{}': file = open(self.path, 'r')

		try:
			if self.path != '{}': self.data = json.load(file)
			else: self.data = json.loads(self.path) # Load empty JSON
		except json.JSONDecodeError:
			raise ProfileParseError()

		if self.path != '{}': file.close()
	
	def invalidate(self):
		if self.data == None: raise ProfileInvalidationError()

	def details(self) -> str:
		if 'details' not in self.data: return None
		return self.data['details']

	def state(self) -> str:
		if 'state' not in self.data: return None
		return self.data['state']
	
	def large_image_key(self) -> str:
		if 'largeImageKey' not in self.data: return None
		return self.data['largeImageKey']

	def small_image_key(self) -> str:
		if 'smallImageKey' not in self.data: return None
		return self.data['smallImageKey']