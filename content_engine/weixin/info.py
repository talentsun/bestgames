class Info(object):
	def __init__(self, json):
		self.user =  json.get('FromUserName', None)
		self.sp = json.get('ToUserName', None)
		self.create_time = json.get('CreateTime', None)
		self.type = json.get('MsgType', None)
		self.text = json.get('Content', None)
		self.lat = json.get('Location_X', None)
		self.lng = json.get('Location_Y', None)
		self.scale = json.get('Scale', None)
		self.label = json.get('Label', None)
		self.pic = json.get('PicUrl', None)
		self.event = json.get('Event', None)
		self.event_key = json.get('EventKey', None)

	type = 'text'
	user = None
	sp = None
	create_time = None
	text = None
	lat = None
	lng = None
	scale = None
	label = None
	pic = None
	event = None
	event_key = None
	origin_json = None
	reply = None
	flag = 0

	def is_text(self):
		return self.type == 'text'

	def is_location(self):
		return self.type == 'location'

	def is_image(self):
		return self.type == 'image'

	def is_link(self):
		return self.type == 'link'

	def is_event(self):
		return self.type == 'event'

