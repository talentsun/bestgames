# -*- coding: utf-8 -*-
from portal.models import Game, Redier, Collection, Problem,Weixin
import django_tables2 as tables
from django_tables2.columns import DateTimeColumn, TemplateColumn
from taggit.utils import edit_string_for_tags

class TagColumn(tables.Column):
    def render(self, value):
        return edit_string_for_tags(value.get_query_set())

class SearchResultTable(tables.Table):
    id = tables.Column(orderable=False, visible=False)
    name = tables.Column(orderable=False)
    tags = TagColumn(orderable=False,attrs={"class":"tags"})
    
    class Meta:
        model = Game
        empty_text = u"暂无精品游戏推荐"
        fields = ("entity_ptr_id", "name","tags","category", "description", "nameRel", "gameRel")
        sequence = fields
        attrs = {'class' : 'table table-striped'}

class GameTable(tables.Table):
    id = tables.Column(orderable=False, visible=False)
    name = tables.Column(verbose_name=u'名称', orderable=False)
    presenter = tables.Column(verbose_name=u'推荐人', orderable=False)
    weibo_sync_timestamp = DateTimeColumn(verbose_name=u"微博同步时间",orderable=True)
    status = TemplateColumn(template_name="sync_status_field.html",orderable=False,verbose_name=u"同步状态")
    tags = TagColumn(orderable=False,attrs={"class":"tags"}, verbose_name=u'标签')
    ops = TemplateColumn(template_name="game_field_ops.html",verbose_name=u"操作",orderable=False,attrs={"class":"ops"})
    
    class Meta:
        model = Game
        order_by = "-weibo_sync_timestamp"
        empty_text = u"暂无精品游戏推荐"
        fields = ("name","presenter","weibo_sync_timestamp","status","tags","ops")
        sequence = ("name","presenter","weibo_sync_timestamp","status","tags","ops")
        attrs = {'class' : 'table table-striped'}

class RedierTable(tables.Table):
    id = tables.Column(orderable=False, visible=False)
    game_name = tables.Column(verbose_name=u'游戏', orderable=False)
    title = tables.Column(verbose_name=u'标题', orderable=False)
    presenter = tables.Column(verbose_name=u'推荐人', orderable=False)
    weibo_sync_timestamp = DateTimeColumn(verbose_name=u"微博同步时间",orderable=True)
    status = TemplateColumn(template_name="sync_status_field.html",orderable=False,verbose_name=u"同步状态")
    tags = TagColumn(orderable=False,attrs={"class":"tags"})
    ops = TemplateColumn(template_name="redier_field_ops.html",verbose_name=u"操作",orderable=False,attrs={"class":"ops"})

    class Meta:
        model = Redier
        order_by = "-weibo_sync_timestamp"
        empty_text = u"暂无小兵变大咖"
        fields = ("game_name","title", "presenter","weibo_sync_timestamp","status","tags","ops")
        sequence = ("game_name","title", "presenter","weibo_sync_timestamp","status","tags","ops")
        attrs = {'class' : 'table table-striped'}

class CollectionTable(tables.Table):
    id = tables.Column(orderable=False, visible=False)
    title = tables.Column(orderable=False)
    presenter = tables.Column(orderable=False)
    weibo_sync_timestamp = DateTimeColumn(verbose_name=u"微博同步时间",orderable=True)
    status = TemplateColumn(template_name="sync_status_field.html",orderable=False,verbose_name=u"同步状态")
    tags = TagColumn(orderable=False,attrs={"class":"tags"})
    ops = TemplateColumn(template_name="collection_field_ops.html",verbose_name=u"操作",orderable=False,attrs={"class":"ops"})

    class Meta:
        model = Collection
        order_by = "-weibo_sync_timestamp"
        empty_text = u"暂无游戏合集"
        fields = ("title", "presenter","weibo_sync_timestamp","status","tags","ops")
        sequence = ("title", "presenter","weibo_sync_timestamp","status","tags","ops")
        attrs = {'class' : 'table table-striped'}

class WeixinTable(tables.Table):
    id = tables.Column(orderable=False, visible=False)
    title = tables.Column(orderable=False)
    presenter = tables.Column(orderable=False)
    weibo_sync_timestamp = DateTimeColumn(verbose_name=u"微信同步时间",orderable=True)
    status = TemplateColumn(template_name="sync_status_field.html",orderable=False,verbose_name=u"同步状态")
    tags = TagColumn(orderable=False,attrs={"class":"games"})
    #games = tables

    ops = TemplateColumn(template_name="weixin_field_ops.html",verbose_name=u"操作",orderable=False,attrs={"class":"ops"})

    class Meta:
        model = Weixin
        order_by = "-weibo_sync_timestamp"
        empty_text = u"暂无微信消息"
        fields = ("title", "presenter","weibo_sync_timestamp","status","games","ops")
        sequence = ("title", "presenter","weibo_sync_timestamp","status","games","ops")
        attrs = {'class' : 'table table-striped'}


class ProblemTable(tables.Table):
    id = tables.Column(orderable=False, visible=False)
    title = tables.Column(orderable=False)
    presenter = tables.Column(orderable=False)
    weibo_sync_timestamp = DateTimeColumn(verbose_name=u"微博同步时间",orderable=True)
    status = TemplateColumn(template_name="sync_status_field.html",orderable=False,verbose_name=u"同步状态")
    tags = TagColumn(orderable=False,attrs={"class":"tags"})
    ops = TemplateColumn(template_name="problem_field_ops.html",verbose_name=u"操作",orderable=False,attrs={"class":"ops"})

    class Meta:
        model = Problem
        order_by = "-weibo_sync_timestamp"
        empty_text = u"暂无\"宅，必有一技\""
        fields = ("title", "presenter","weibo_sync_timestamp","status","tags","ops")
        sequence = ("title", "presenter","weibo_sync_timestamp","status","tags","ops")
        attrs = {'class' : 'table table-striped'}

