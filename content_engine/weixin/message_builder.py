# -*- coding: utf-8 -*-
from inspect import isfunction
from pyweixin import WeiXin
from utils import shorten_url
from datetime import datetime

from django.core.cache import cache

class BuildConfig:
	def __init__(self, type, platform, data, cache_key=None, cache_timeout=None):
		self.type = type
		self.platform = platform
		self.data = data
		self.cache_key = cache_key
		self.cache_timeout = cache_timeout

	type = None
	platform = None
	data = None
	cache_key = None
	cache_timeout = None

def _wrap_cache_key_with_platform(cache_key, platform):
	if cache_key and platform:
		return cache_key + '_' + platform
	else:
		return cache_key

def _get_game_android_shorten_download_url_key(game):
	return 'g_' + str(game.id) + '_android_d'

def _get_game_ios_shorten_download_url_key(game):
	return 'g_' + str(game.id) + '_ios_d'

def _build_weixin_download_urls(context, data, cache_key=None, cache_timeout=None):
	content  = ''
	for game in data:
		content = content + game.name + '\n'

		if game.android_download_url is not None:
			android_download_shorten_url = cache.get(_get_game_android_shorten_download_url_key(game))
			if android_download_shorten_url is None:
				android_download_shorten_url = shorten_url(game.android_download_url)
				cache.set(_get_game_android_shorten_download_url_key(game), android_download_shorten_url)

			if android_download_shorten_url is not None:
				content = content + u'安卓下载地址'
				content = content + android_download_shorten_url + '\n'
			else:
				content = content + u'无安卓版\n'
		else:
			content = content + u'无安卓版\n'

		if game.iOS_download_url is not None:
			ios_download_shorted_url = cache.get(_get_game_ios_shorten_download_url_key(game))
			if ios_download_shorted_url is None:
				ios_download_shorted_url = shorten_url(game.iOS_download_url)
				cache.set(_get_game_ios_shorten_download_url_key(game), ios_download_shorted_url)

			if ios_download_shorted_url is not None:
				content = content + u'苹果下载地址'
				content = content + ios_download_shorted_url + '\n'
			else:
				content = content + u'无苹果版\n'
		else:
			content = content + u'无苹果版\n'
		
		content = content + '\n'

	weixin = WeiXin()
	message = weixin.to_xml(to_user_name=context.get('FromUserName', None),
            from_user_name=context.get('ToUserName', None),
            create_time=datetime.now().strftime('%s'),
            msg_type='text',
            content=content,
            func_flag=0)
	
	if cache_key:
		cache.set(_wrap_cache_key_with_platform(cache_key, MessageBuilder.PLATFORM_WEIXIN), message, cache_timeout)
	return message

def _build_weixin_raw_text(context, data, cache_key = None, cache_timeout = None):
	# FIXME
	weixin = WeiXin()
	message = weixin.to_xml(to_user_name=context.get('FromUserName', None),
            from_user_name=context.get('ToUserName', None),
            create_time=datetime.now().strftime('%s'),
            msg_type='text',
            content=data,
            func_flag=0)

	if cache_key:
		cache.set(_wrap_cache_key_with_platform(cache_key, MessageBuilder.PLATFORM_WEIXIN), message, cache_timeout)
	return message

class MessageBuilder:
	# message types
	TYPE_DOWNLOAD_URL = 'type_download_url'
	TYPE_RAW_TEXT = 'type_raw_text'

	# platforms
	PLATFORM_WEIXIN = 'weixin'

	@classmethod
	def build(self,  context = None, build_config = None):
		cache_key = _wrap_cache_key_with_platform(build_config.cache_key, build_config.platform)
		if cache_key and cache.get(cache_key):
			return cache.get(cache_key)
		else:
			return self._call_build_method(context, build_config.type, build_config.platform, build_config.data, build_config.cache_key, build_config.cache_timeout)

	

	_build_methods = {
		TYPE_DOWNLOAD_URL : {
			PLATFORM_WEIXIN : _build_weixin_download_urls
		},
		TYPE_RAW_TEXT : {
			PLATFORM_WEIXIN : _build_weixin_raw_text
		}
	}

	@classmethod
	def _call_build_method(self, context, type, platform, data, cache_key = None, cache_timeout = None):
		if self._build_methods[type] is not None:
			if isfunction(self._build_methods[type]):
				return self._build_methods[type](context, data, cache_key, cache_timeout)
			elif self._build_methods[type][platform] is not None and isfunction(self._build_methods[type][platform]):
				return self._build_methods[type][platform](context, data, cache_key, cache_timeout)
		raise 'do not support type: %s and platform: %s' % (type, platform)
