#encoding=utf-8
from django import template
from django.template.defaultfilters import stringfilter

register = template.Library()

@register.filter
@stringfilter
def del_link(value):
	if value and isinstance(value, (str, unicode)):
		index = value.find('http://')
		if index != -1:
			return value[:index]
	return value

@register.filter
def rate_stars(value):
	integer_part = value / 2
	decimal_part = value % 2
	stars = u'★' * integer_part + u'☆' * decimal_part
	return stars
