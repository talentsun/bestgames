# coding: utf8
import sys
from rule import Rule
from info import Info
from message_builder import MessageBuilder, BuildConfig

class Router(object):
	__instance = None

	@staticmethod
	def get_instance():
		if Router.__instance is None:
			Router.__instance = Router()
		return Router.__instance

	def set(self, pattern, handler=None, replies=None):	
		if pattern and handler is None and replies is None:
			r = pattern
		else:
			r = {
				'name' : pattern,
				'pattern' : pattern,
				'handler' : handler,
				'replies' : replies
			}
		if r is not None:
			r = Rule.convert(r)
			self.routes.extend(r)

	def get(self, name):
		if name is not None:
			return filter(lambda r:r.name==name, self.routes)
		else:
			return self.routes

	def data(self, uid, key, value):
		obj = self.data_cache[uid] = self.data_cache[uid] or {}
		if isinstance(key, str):
			if value is None:
				del obj[key]
			else:
				obj[key] = value
		elif isinstance(key, dict):
			obj.__dict__.update(key)
		return obj

	def wait(self, uid, rule):
		if rule is not None:
			rule = Rule.convert(rule)
			self.wait_rules[uid] = rule

	def rewait(self, uid):
		self.wait(uid, self.last_wait_rules[uid])

	def dialog(self, path):
		pass

	def reply(self, data, cb):
		info = data
		if not isinstance(data, Info):
			info = Info(data)

		if not self.config.get('keepBlank', False) and info.text:
			info.text = info.text.trim()

		rule_list = self.routes
		waiter = self.wait_rules.get(info.user, None)

		if waiter:
			rule_list = [].extend(waiter).extend(self.routes)
			self.last_wait_rules[info.user] = waiter
			self.wait_rules[info.user] = None

		for i in range(0, len(rule_list)):
			rule = rule_list[i]
			if Rule.is_match(info, rule):
				rule.count = i
				result = Rule.execute(info, rule, cb)
				if isinstance(result, str):
					result = BuildConfig(MessageBuilder.TYPE_RAW_TEXT, None, result)
				if result:
					if rule.replies:
						self.wait(info.user, Rule.convert(rule.replies, rule.name))
					return cb(None, result)

		return cb('404', BuildConfig(MessageBuilder.TYPE_RAW_TEXT, None, self.get_status('404') + info.text))
	
	routes = []
	wait_rules = {}
	last_wait_rules = {}
	data_cache = {}
	config = {
		'keepBlank' : True,
		'statusMsg' : {
			'204': u'你的消息已经收到，若未即时回复，还望海涵',
    		'403': u'鉴权失败,你的Token不正确',
    		'404': u'听不懂你说的: ',
    		'500': u'服务器临时出了一点问题，您稍后再来好吗'
		}
	}

	def get_status(self, code):
		return self.config.get('statusMsg', {}).get(str(code), None)
