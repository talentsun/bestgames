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