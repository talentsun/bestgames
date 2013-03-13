# -*- coding: utf-8 -*-
from api.models import Game, Redier
import django_tables2 as tables
from django_tables2.columns import DateTimeColumn, TemplateColumn
from taggit.utils import edit_string_for_tags

class TagColumn(tables.Column):
    def render(self, value):
        return edit_string_for_tags(value.get_query_set())

class GameTable(tables.Table):
    id = tables.Column(orderable=False, visible=False)
    name = tables.Column(orderable=False)
    presenter = tables.Column(orderable=False)
    sync_weibo_timestamp = DateTimeColumn(verbose_name=u"微博同步时间",orderable=True)
    status = TemplateColumn(template_name="sync_status_field.html",orderable=False,verbose_name=u"同步状态")
    tags = TagColumn(orderable=False,attrs={"class":"tags"})
    ops = TemplateColumn(template_name="games_field_ops.html",verbose_name=u"操作",orderable=False,attrs={"class":"ops"})
    
    class Meta:
        model = Game
        order_by = "-timestamp"
        empty_text = u"暂无精品游戏推荐"
        fields = ("name","presenter","sync_weibo_timestamp","status","tags","ops")
        sequence = ("name","presenter","sync_weibo_timestamp","status","tags","ops")

class RedierTable(tables.Table):
    id = tables.Column(orderable=False, visible=False)
    name = tables.Column(accessor="game.name",orderable=False)
    toll_gate = tables.Column(orderable=False)
    presenter = tables.Column(orderable=False)
    sync_weibo_timestamp = DateTimeColumn(verbose_name=u"微博同步时间",orderable=True)
    status = TemplateColumn(template_name="sync_status_field.html",orderable=False,verbose_name=u"同步状态")
    tags = tables.Column(orderable=False,attrs={"class":"tags"})
    ops = TemplateColumn(template_name="rediers_field_ops.html",verbose_name=u"操作",orderable=False,attrs={"class":"ops"})

    class Meta:
        model = Redier
        order_by = "-timestamp"
        empty_text = u"暂无小兵变大咖"
        fields = ("name","toll_gate", "presenter","sync_weibo_timestamp","status","tags","ops")
        sequence = ("name","toll_gate", "presenter","sync_weibo_timestamp","status","tags","ops")
