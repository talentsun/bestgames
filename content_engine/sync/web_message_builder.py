#encoding=utf-8
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

import string
from wordpress_xmlrpc import WordPressPost
from content_engine import settings
from django.template.loader import render_to_string
from utils import convert_youku_video_url

class WebMessage(object):
	def __init__(self, entity_id, post):
		self.entity_id = entity_id
		self.post = post

def _normalize_content(content):
    url_pos = content.find('http://')
    normalized_content = content
    if url_pos != -1:
        normalized_content = normalized_content[:url_pos]
    return normalized_content

def _get_game_tags(game):
	tags = []
	if game.android_download_url != '':
		tags.append(u'安卓')
	if game.iOS_download_url != '':
		tags.append(u'苹果')
	return tags

def _get_game_evaluation_tags(evaluation):
	tags = []
	if evaluation.android_download_url != '':
		tags.append(u'安卓')
	if evaluation.iOS_download_url != '':
		tags.append(u'苹果')
	return tags

def _get_game_platforms(game):
	platforms = []
	if game.android_download_url != '':
		platforms.append('Android')
	if game.iOS_download_url != '':
		platforms.append('iOS')
	platforms_str = ''
	if len(platforms) > 0:
		return string.join(platforms, ', ')
	else:
		return ''

def _get_game_evaluation_platforms(evaluation):
	platforms = []
	if evaluation.android_download_url != '':
		platforms.append('Android')
	if evaluation.iOS_download_url != '':
		platforms.append('iOS')
	platforms_str = ''
	if len(platforms) > 0:
		return string.join(platforms, ', ')
	else:
		return ''

def build_game_message(game):
	post = WordPressPost()
	post.title = '%s - %s' % (game.name, game.brief_comment)

	converted_video_url = None
	if game.video_url is not None:
		converted_video_url = convert_youku_video_url(game.video_url)
	post.content = str(render_to_string('game_web.tpl', {
		'content' : _normalize_content(game.recommended_reason),
		'icon' : settings.MEDIA_URL + game.icon.name,
		'category' : game.category.name,
		'size' : game.size,
		'platforms' : _get_game_platforms(game),
		'id' : game.id,
		'android_download_url' : game.android_download_url,
		'iOS_download_url' : game.iOS_download_url,
		'screenshot_path_1' : settings.MEDIA_URL + game.screenshot_path_1.name,
		'screenshot_path_2' : settings.MEDIA_URL + game.screenshot_path_2.name,
		'screenshot_path_3' : settings.MEDIA_URL + game.screenshot_path_3.name,
		'screenshot_path_4' : settings.MEDIA_URL + game.screenshot_path_4.name,
		'video_url' : converted_video_url
	}))

	post.terms_names = {
		'category' : [game.category.name],
		'post_tag' : _get_game_tags(game)
	}

	if game.screenshot_path_1.name != '':
		post.custom_fields = []
		post.custom_fields.append({'key':'post_image','value':settings.MEDIA_URL + game.screenshot_path_1.name})

	post.post_status = 'publish'

	return WebMessage(game.id, post)

def build_news_message(news):
	post = WordPressPost()
	post.title = news.brief_comment

	converted_video_url = None
	if news.video_url is not None:
		converted_video_url = convert_youku_video_url(news.video_url)

	content_items = {'content' : _normalize_content(news.recommended_reason)}
	if news.screenshot_path_1:
		content_items['screenshot_path_1'] = settings.MEDIA_URL + news.screenshot_path_1.name
	if news.screenshot_path_2:
		content_items['screenshot_path_2'] = settings.MEDIA_URL + news.screenshot_path_2.name
	if news.screenshot_path_3:
		content_items['screenshot_path_3'] = settings.MEDIA_URL + news.screenshot_path_3.name
	if news.screenshot_path_4:
		content_items['screenshot_path_4'] = settings.MEDIA_URL + news.screenshot_path_4.name
	content_items['video_url'] = converted_video_url
	post.content = str(render_to_string('news_web.tpl', content_items))

	post.terms_names = {
		'category' : [u'新游预告']
	}

	if news.screenshot_path_1.name != '':
		post.custom_fields = []
		post.custom_fields.append({'key':'post_image','value':settings.MEDIA_URL + news.screenshot_path_1.name})

	post.post_status = 'publish'

	return WebMessage(news.id, post)

def build_collection_message(collection):
	post = WordPressPost()
	post.title = collection.title

	games = []
	for game in collection.games.all():
		games.append({
			'name' : game.name,
			'brief_comment' : game.brief_comment,
			'icon' : settings.MEDIA_URL + game.icon.name,
			'category' : game.category.name,
			'size' : game.size,
			'platforms' : _get_game_platforms(game),
			'id' : game.id,
			'android_download_url' : game.android_download_url,
			'iOS_download_url' : game.iOS_download_url,
			'rating' : game.rating,
			'recommended_reason' : _normalize_content(game.recommended_reason)
			})

	post.content = str(render_to_string('collection_web.tpl', {
		'content' : _normalize_content(collection.recommended_reason),
		'cover' : settings.MEDIA_URL + collection.cover.name,
		'games' : games
	}))

	post.terms_names = {
		'category' : [u'游戏合集']
	}

	post.post_status = 'publish'

	return WebMessage(collection.id, post)

def build_puzzle_message(puzzle):
	post = WordPressPost()
	post.title = puzzle.title

	post.content = str(render_to_string('puzzle_web.tpl', {
		'id' : puzzle.id,
		'image_url' : settings.MEDIA_URL + puzzle.image_url.name,
		'description' : puzzle.description,
		'optiona' : puzzle.option1,
		'optionb' : puzzle.option2,
		'optionc' : puzzle.option3,
		'optiond' : puzzle.option4
	}))

	post.terms_names = {
		'category' : [u'趣味答题']
	}

	post.post_status = 'publish'

	return WebMessage(puzzle.id, post)

def build_evaluation_message(evaluation):
	post = WordPressPost()
	post.title = evaluation.title

	post.content = str(render_to_string('evaluation_web.tpl' {
		'id' : evaluation.id,
		'content' : _normalize_content(evluation.recommended_reason),
		'icon' : settings.MEDIA_URL + evaluation.icon.name,
		'platforms' : _get_game_evaluation_platforms(evaluation),
		'android_download_url' : evaluation.android_download_url,
		'iOS_download_url' : evaluation.iOS_download_url,
		'evaluation_content' : evaluation.content,
	}))

	post.terms_names = {
		'category' : [u'游戏测评']
		'post_tag' : _get_game_evaluation_tags(evaluation)
	}

	post.post_status = 'publish'

	return WebMessage(evaluation.id, post)
