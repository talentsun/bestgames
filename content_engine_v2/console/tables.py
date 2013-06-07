# -*- coding: utf-8 -*-
from console.models import Entity
import django_tables2 as tables
from django_tables2.columns import TemplateColumn

class EntityTable(tables.Table):
    id = tables.Column(orderable=False, visible=False)
    title = tables.Column(verbose_name=u'标题', orderable=False)
    type = tables.Column(verbose_name=u'类型', orderable=False, accessor='type.verbose_name')
    presenter = tables.Column(verbose_name=u'推荐人', orderable=False)
    status = TemplateColumn(template_name="sync_status_field.html",orderable=False,verbose_name=u"同步状态")
    ops = TemplateColumn(template_name="entity_ops_field.html",verbose_name=u"操作",orderable=False,attrs={"class":"ops"})
    
    class Meta:
        model = Entity
        order_by = "-id"
        empty_text = u"暂无内容"
        fields = ("title","type","presenter","status","ops")
        sequence = ("title","type","presenter","status","ops")
        attrs = {'class' : 'table table-striped'}