#encoding=utf-8
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

import string
from wordpress_xmlrpc import WordPressPost
from content_engine import settings

class WebMessage(object):
	def __init__(self, entity_id, post):
		self.entity_id = entity_id
		self.post = post

def _normalize_content(content):
    url_pos = content.find('http://')
    normalized_content = content
    if url_pos != -1:
        normalized_content = normalized_content[5][:url_pos]
    return normalized_content

def build_game_message(game):
	post = WordPressPost()
	post.title = '%s - %s' % (game.name, game.brief_comment)
	
	post.content = '<p>%s<!--more--></p>' % _normalize_content(game.recommended_reason)
	
	post.content += '[box style="rounded shadow"]'
	post.content += '[col grid="4-1 first"]<img src="%s" class="img-rounded" />[/col]' % (settings.MEDIA_URL + game.icon.name)
	post.content += '[col grid="4-2"]'
	post.content += u'<p>分类：%s</p>' % game.category.name
	post.content += u'<p>大小：%s</p>' % game.size
	platforms = []
	tags = []
	if game.android_download_url is not None:
		platforms.append('Android')
		tags.append(u'安卓')
	if game.iOS_download_url is not None:
		platforms.append('iOS')
		tags.append(u'苹果')
	if len(platforms) > 0:
		post.content += u'<p>平台：%s</p>' % string.join(platforms, ', ')
	post.content += '[/col]'
	post.content += '[col grid="4-1"]<a class="btn btn-success" rel="lightbox" href="http://qrickit.com/api/qr?qrsize=300&d=http://cow.bestgames7.com/games/%d/preview"><i class="icon-qrcode icon-white"></i>二维码下载</a>[/col]' % game.id
	post.content += '[/box]'

	post.content += '[box style="rounded shadow"]<p>游戏截图</p>[slider class="screenshots"]'
	if game.screenshot_path_1 is not None:
		post.content += '[slide]<img src="%s" class="img-rounded" />[/slide]' % (settings.MEDIA_URL + game.screenshot_path_1.name)
	if game.screenshot_path_2 is not None:
		post.content += '[slide]<img src="%s" class="img-rounded" />[/slide]' % (settings.MEDIA_URL + game.screenshot_path_2.name)
	if game.screenshot_path_3 is not None:
		post.content += '[slide]<img src="%s" class="img-rounded" />[/slide]' % (settings.MEDIA_URL + game.screenshot_path_3.name)
	if game.screenshot_path_4 is not None:
		post.content += '[slide]<img src="%s" class="img-rounded" />[/slide]' % (settings.MEDIA_URL + game.screenshot_path_4.name)
	post.content += '[/slider][/box]'

	if game.video_url is not None:
		post.content += '[box style="rounded shadow"]<p>游戏视频</p><div class="post-video"><iframe height=498 width=510 src="%s" frameborder=0 allowfullscreen></iframe></div>[/box]' % game.video_url

	post.terms_names = {
		'category' : game.category.name,
		'post_tag' : tags
	}

	if game.screenshot_path_1 is not None:
		post.custom_fields = []
		post.custom_fields.append({'key':'post_image','value':settings.MEDIA_URL + game.screenshot_path_1.name})

	post.post_status = 'publish'

	return WebMessage(game.id, post)