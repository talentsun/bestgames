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
	content = ''
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

	return WeiXin.to_text_xml(to_user_name=context.get('FromUserName', None),
            from_user_name=context.get('ToUserName', None),
            content=content,
            func_flag=0)

def _build_weixin_games(context, data, cache_key=None, cache_timeout=None):
	articles = []
	is_first = True
	for game in data:
		title = '%s - %s' % (game.brief_comment, game.name)
		url_pos = game.recommended_reason.find('http://')
		if url_pos != -1:
			description = game.recommended_reason[:url_pos]
		else:
			description = game.recommended_reason
		if is_first:
			pic_url = 'http://weixin.bestgames7.com/media/%s' % game.screenshot_path_1
			is_first = False
		else:
			pic_url = 'http://weixin.bestgames7.com/media/%s' % game.icon
		# FIXME need a mobile page hosting game
		articles.append({'title' : title, 'description' : description, 'pic_url' : pic_url, 'url' : 'http://www.baidu.com'})
	return WeiXin.to_news_xml(context.get('FromUserName', None), context.get('ToUserName', None), articles)

def _build_weixin_raw_text(context, data, cache_key = None, cache_timeout = None):
	# FIXME
	return WeiXin.to_text_xml(to_user_name=context.get('FromUserName', None),
            from_user_name=context.get('ToUserName', None),
            content=data,
            func_flag=0)

class MessageBuilder:
	# message types
	TYPE_DOWNLOAD_URL = 'type_download_url'
	TYPE_RAW_TEXT = 'type_raw_text'
	TYPE_GAMES = 'type_games'

	# platforms
	PLATFORM_WEIXIN = 'weixin'

	@classmethod
	def build(self,  context = None, build_config = None):
		return self._call_build_method(context, build_config.type, build_config.platform, build_config.data, build_config.cache_key, build_config.cache_timeout)

	_build_methods = {
		TYPE_DOWNLOAD_URL : {
			PLATFORM_WEIXIN : _build_weixin_download_urls
		},
		TYPE_RAW_TEXT : {
			PLATFORM_WEIXIN : _build_weixin_raw_text
		},
		TYPE_GAMES : {
			PLATFORM_WEIXIN : _build_weixin_games
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
