# -*- coding: utf-8 -*-
from django import forms

from console.widgets import TagWidget
from console.utils import parse_tags, edit_string_for_tags

class TagField(forms.CharField):
	widget = TagWidget

	def clean(self, value):
		value = super(TagField, self).clean(value)
		try:
			return parse_tags(value)
		except ValueError:
			raise forms.ValidationError(_(u'多个标签使用“，”分隔'))