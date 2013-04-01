# -*- coding: utf-8 -*-
from inspect import isfunction
from pyweixin import WeiXin
from utils import shorten_url
from datetime import datetime

class BuildConfig:
	def __init__(self, type, platform, data):
		self.type = type
		self.platform = platform
		self.data = data

	type = None
	platform = None
	data = None

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

		if game.iOS_download_url is not None:
			ios_download_shorted_url = shorten_url(game.iOS_download_url)
			if ios_download_shorted_url is not None:
				content = content + u'苹果下载地址\n'
				content = content + ios_download_shorted_url + '\n'
			else:
				content = content + u'无苹果版\n'
		else:
			content = content + u'无苹果版\n'
			content = content + '\n'

	weixin = WeiXin()
	return weixin.to_xml(to_user_name=context.get('ToUserName', None),
            from_user_name=context.get('FromUserName', None),
            create_time=datetime.now().strftime('%s'),
            msg_type='text',
            content=content,
            func_flag=0)

def _build_weixin_raw_text(context, data):
	# FIXME
	weixin = WeiXin()
	return weixin.to_xml(to_user_name=context.get('ToUserName', None),
            from_user_name=context.get('FromUserName', None),
            create_time=datetime.now().strftime('%s'),
            msg_type='text',
            content=data,
            func_flag=0)

class MessageBuilder:
	# message types
	TYPE_DOWNLOAD_URL = 'type_download_url'
	TYPE_RAW_TEXT = 'type_raw_text'

	# platforms
	PLATFORM_WEIXIN = 'weixin'

	@classmethod
	def build(self,  context = None, build_config = None):
		return self._call_build_method(context, build_config.type, build_config.platform, build_config.data)

	

	_build_methods = {
		TYPE_DOWNLOAD_URL : {
			PLATFORM_WEIXIN : _build_weixin_download_urls
		},
		TYPE_RAW_TEXT : {
			PLATFORM_WEIXIN : _build_weixin_raw_text
		}
	}

	@classmethod
	def _call_build_method(self, context, type, platform, data):
		if self._build_methods[type] is not None:
			if isfunction(self._build_methods[type]):
				return self._build_methods[type](context, data)
			elif self._build_methods[type][platform] is not None and isfunction(self._build_methods[type][platform]):
				return self._build_methods[type][platform](context, data)
		raise 'do not support type: %s and platform: %s' % (type, platform)
