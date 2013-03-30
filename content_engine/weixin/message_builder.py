# -*- coding: utf-8 -*-
from inspect import isfunction
from pyweixin import WeiXin
from utils import shorten_url

def _build_weixin_download_urls(context, data):
	content  = ''
	for game in data:
		content = content + game.name + '\n'

		if game.android_download_url is not None:
			android_download_shorten_url = shorten_url(game.android_download_url)
			if android_download_shorten_url is not None:
				content = content + u'安卓下载地址\n'
				content = content + android_download_shorten_url + '\n'
			else:
				content = content + u'无安卓版\n'
		else:
			content = content + u'无安卓版\n'

		if game.ios_download_url is not None:
			ios_download_shorted_url = shorten_url(game.ios_download_url)
			if ios_download_shorted_url is not None:
				content = content + u'苹果下载地址\n'
				content = content + ios_download_shorted_url + '\n'
			else:
				content = content + u'无苹果版\n'
		else:
			content = content + u'无苹果版\n'
			content = content + '\n'

	context['content'] = content
	context['func_flag'] = 0
	weixin = WeiXin()
	return weixin.to_xml(context)

class MessageBuilder:
	# message types
	TYPE_DOWNLOAD_URL = 'type_download_url'

	# platforms
	PLATFORM_WEIXIN = 'weixin'

	@classmethod
	def build(self, type = None, platform = None, context = None, data = None):
		self._call_build_method(type, platform, context, data)

	

	_build_methods = {
		TYPE_DOWNLOAD_URL : {
			PLATFORM_WEIXIN : _build_weixin_download_urls
		}
	}

	@classmethod
	def _call_build_method(self, type, platform, context, data):
		if self._build_methods[type] is not None:
			if isfunction(self._build_methods[type]):
				return self._build_methods[type](context, data)
			elif self._build_methods[type][platform] is not None and isfunction(self._build_methods[type][platform]):
				return self._build_methods[type][platform](context, data)
		raise 'do not support type: %s and platform: %s' % (type, platform)
