# -*- coding: utf-8 -*-
from django.forms import Textarea
from django.utils.html import conditional_escape, format_html, format_html_join
from django.utils.safestring import SafeData, mark_safe
from content_engine_v2 import settings

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