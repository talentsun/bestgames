#encoding=utf-8
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

import shutil
from breve import Template, flatten
from breve.tags.html import tags
from utils import make_image
import os

current_file_dir = os.path.split(os.path.realpath(__file__))[0]
t = Template(tags, root=current_file_dir + '/templates/')

class WeixinMessageItem(object):
    def __init__(self, image, title, digest, content):
        self.image = image
        self.title = title
        self.digest = digest
        self.content = content
        self.image_id = -1

class WeixinMessage(object):
    def __init__(self, entity_id, title, items):
        self.entity_id = entity_id
        self.title = title
        self.items = items

def _build_game_image(game):
    content = t.render('screenshots', dict(
        screenshot_path_1 = game.screenshot_path_1,
        screenshot_path_2 = game.screenshot_path_2,
        screenshot_path_3 = game.screenshot_path_3,
        screenshot_path_4 = game.screenshot_path_4
        ))
    return make_image(game.id, content)

def _normalize_content(content):
    url_pos = content.find('http://')
    normalized_content = content
    if url_pos != -1:
        normalized_content = normalized_content[5][:url_pos]
    return normalized_content + u'<br><br><font color="gray">回复游戏名获得该游戏的下载地址</font>'

def build_weixin_message(weixin):
    items = []
    index = 0
    message_title = ''
    if weixin.cover._file is not None and weixin.title is not None and weixin.recommended_reason is not None:
        message_title = weixin.title
        items.append(WeixinMessageItem(image=weixin.cover.path, title=weixin.title, digest=weixin.title, content=weixin.recommended_reason))
        index += 1
    for news in weixin.advices.all():
        title = u'游戏情报站  -  %s' % news.brief_comment
        if index == 0:
            message_title = title
        items.append(WeixinMessageItem(image=news.advice_image.path, title=title, digest=title, content=news.recommended_reason))
        index += 1
    for game in weixin.games.all():
        title = u'%s  -  %s' % (game.name, game.brief_comment)
        if index == 0:
            message_title = title
        if index > 0:
            items.append(WeixinMessageItem(image=game.icon.path, title=title, digest=title, content=_normalize_content(game.recommended_reason)))
        else:
            items.append(WeixinMessageItem(image=_build_game_image(game), title=title, digest=title, content=_normalize_content(game.recommended_reason)))
        index += 1
    for player in weixin.players.all():
        title = u'我是玩家  -  %s' % player.brief_comment
        if index == 0:
            message_title = title
        items.append(WeixinMessageItem(image=player.player_image.path, title=title, digest=title, content=player.recommended_reason))
        index += 1
    return WeixinMessage(weixin.id, message_title, items)