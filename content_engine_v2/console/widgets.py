# -*- coding: utf-8 -*-
from django import forms
from django.forms import Textarea
from django.utils.html import conditional_escape, format_html, format_html_join
from django.utils.safestring import SafeData, mark_safe
from django.template import Context, Template

from content_engine_v2 import settings
from console.utils import parse_tags, edit_string_for_tags

class TagWidget(forms.TextInput):
	def render(self, name, value, attrs=None):
		if value is not None and not isinstance(value, basestring):
			value_str = edit_string_for_tags([tag for tag in value.select_related("tag")])
		html = super(TagWidget, self).render(name, value_str, attrs)
		html += u'\r\n'
		html += u'<ul id="%s-suggested-tags" class="suggested-tags">' % name
		for tag in value.get_available_tags().all():
			html += u'<li class="taggit-tag">%s</li>' % tag.name
		html += u'</ul>\r\n'
		html += u'<script type="text/javascript">$(document).ready(function(){0});</script>\r\n'
		return format_html(html, mark_safe('{$("#id_%s" ).taggit({tag_selector:"#%s-suggested-tags .taggit-tag"});}' % (name, name)))

class CountableTextarea(Textarea):
	def __init__(self, max_length, attrs=None):
		self.max_length = max_length
		super(CountableTextarea, self).__init__(attrs)

	def render(self, name, value, attrs=None):
		html = super(CountableTextarea, self).render(name, value, attrs)
		html += u'\r\n'
		html += u'<script type="text/javascript" src="{0}js/jquery.simplyCountable.js"></script>\r\n'
		html += u'<script type="text/javascript">$(document).ready(function(){1});</script>\r\n'
		html += u'<p style="margin-top:8px;">已输入 <span id="counter" class="safe">0</span> 字。</p>'
		return format_html(html, settings.STATIC_URL, mark_safe('{$("#id_%s").simplyCountable({maxCount:%d,countDirection:"up"});}' % (name, self.max_length)))

class RichTextEditor(Textarea):
	def render(self, name, value, attrs=None):
		html = super(RichTextEditor, self).render(name, value, attrs)
		html += u'\r\n'
		html += u'{% load wysiwyg %}\r\n'
		print html
		html += u'{%% wysiwyg_editor "id_%s" %%}\r\n' % name
		print html
		html = Template(html).render(None)
		print html
		return html