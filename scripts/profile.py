from __future__ import annotations
import datetime
from errors import ProfileInvalidationError
from errors import ProfileParseError
import json

class Profile:
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

	def client_id(self) -> int:
		if 'client_id' not in self.data or \
			not isinstance(self.data['client_id'], int) or \
			not self.data['client_id']: return 0
		
		return int(self.data['client_id'])

	def details(self) -> str:
		if 'details' not in self.data or \
			not isinstance(self.data['details'], str) or \
			not self.data['details']: return None
		return str(self.data['details'])

	def state(self) -> str:
		if 'state' not in self.data or \
			not isinstance(self.data['state'], str) or \
			not self.data['state']: return None
		return str(self.data['state'])
	
	def start_timestamp(self) -> float:
		if 'displayElapsed' not in self.data or \
			not isinstance(self.data['displayElapsed'], bool) or \
			not self.data['displayElapsed']: return None
		
		return float(datetime.datetime.now().timestamp())

	def large_image(self) -> str:
		if 'largeImage' not in self.data or \
			not isinstance(self.data['largeImage'], str) or \
			not self.data['largeImage']: return None
		
		return str(self.data['largeImage'])

	def small_image(self) -> str:
		if 'smallImage' not in self.data or \
			not isinstance(self.data['smallImage'], str) or \
			not self.data['smallImage']: return None
		
		return str(self.data['smallImage'])

	def large_image_text(self) -> str:
		if 'largeImageText' not in self.data or \
			not isinstance(self.data['largeImageText'], str) or \
			not self.data['largeImageText']: return None
		
		return str(self.data['largeImageText'])
	
	def small_image_text(self) -> str:
		if 'smallImageText' not in self.data or \
			not isinstance(self.data['smallImageText'], str) or \
			not self.data['smallImageText']: return None
		
		return str(self.data['smallImageText'])
	
	def buttons(self) -> list[dict]:
		if 'buttons' not in self.data or \
			len(self.data['buttons']) < 1: return None
		for button in self.data['buttons']:
			if 'label' not in button or not button['label'] or \
				'url' not in button or not button['url'] or \
					len(button) < 1:
				self.data['buttons'].remove(button)
				continue

		return list[dict](self.data['buttons'])