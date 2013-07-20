#encoding=utf-8
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

import shutil
from utils import make_image
import os
from django.template.loader import render_to_string

current_file_dir = os.path.split(os.path.realpath(__file__))[0]

class WeixinMessageItem(object):
    def __init__(self, image, title, digest, content, sourceurl=None):
        self.image = image
        self.title = title
        self.digest = digest
        self.content = content
        self.sourceurl = sourceurl
        self.image_id = -1

class WeixinMessage(object):
    def __init__(self, entity_id, title, items):
        self.entity_id = entity_id
        self.title = title
        self.items = items

def _build_game_image(game):
    content = str(render_to_string('screenshots_weixin.tpl', {
        'screenshot_path_1' : game.screenshot_path_1.path,
        'screenshot_path_2' : game.screenshot_path_2.path,
        'screenshot_path_3' : game.screenshot_path_3.path,
        'screenshot_path_4' : game.screenshot_path_4.path
        }))
    return make_image(game.id, content)

def _normalize_content(game):
    content = game.recommended_reason
    url_pos = content.find('http://')
    normalized_content = content
    if url_pos != -1:
        normalized_content = normalized_content[5][:url_pos]
    interger_part = game.rating / 2
    decimal_part = game.rating % 2
    stars = u'★' * interger_part + u'☆' * decimal_part
    return normalized_content + u'<br><br>推荐指数: %s<br>分类: %s<br>大小: %s<br><br><font color="gray">点击“阅读原文”下载游戏</font>' % (stars, game.category.name, game.size)

def build_weixin_message(weixin):
    items = []
    index = 0
    message_title = ''
    if weixin.cover.name != u'' and weixin.title != u'' and weixin.recommended_reason != u'':
        message_title = weixin.title
        items.append(WeixinMessageItem(image=weixin.cover.path, title=weixin.title, digest=weixin.title, content=weixin.recommended_reason))
        index += 1
    for news in weixin.news.all():
        title = u'游戏情报站  -  %s' % news.brief_comment
        if index == 0:
            message_title = title
        items.append(WeixinMessageItem(image=news.screenshot_path_1.path, title=title, digest=title, content=news.recommended_reason + u'<br><br><font color="gray">点击“阅读原文”查看更多</font>', sourceurl=u'http://cow.bestgames7.com/d/%s/' % news.id))
        index += 1
    for game in weixin.games.all():
        title = u'%s  -  %s' % (game.name, game.brief_comment)
        if index == 0:
            message_title = title
        if index > 0:
            items.append(WeixinMessageItem(image=game.icon.path, title=title, digest=title, content=_normalize_content(game), sourceurl=u'http://cow.bestgames7.com/d/%s/' % game.id))
        else:
            items.append(WeixinMessageItem(image=_build_game_image(game), title=title, digest=title, content=_normalize_content(game), sourceurl=u'http://cow.bestgames7.com/d/%s/' % game.id))
        index += 1
    for player in weixin.players.all():
        title = u'我是玩家  -  %s' % player.brief_comment
        if index == 0:
            message_title = title
        items.append(WeixinMessageItem(image=player.image_url.path, title=title, digest=title, content=player.recommended_reason))
        index += 1
    for puzzle in weixin.puzzles.all():
        title = u'趣味答题  -  %s' % puzzle.title
        if index == 0:
            message_title = title
        content = puzzle.description + '<br>'
        content += 'A.' + puzzle.option1 + '<br>'
        content += 'B.' + puzzle.option2 + '<br>'
        content += 'C.' + puzzle.option3 + '<br>'
        content += 'D.' + puzzle.option4 + '<br></br>'
        content += u'<font color="gray">回复"答题"，参与答题得积分换礼品的活动吧</font><br>'
        items.append(WeixinMessageItem(image=puzzle.image_url.path, title=title, digest=title, content=content))
        index += 1
    return WeixinMessage(weixin.id, message_title, items)
