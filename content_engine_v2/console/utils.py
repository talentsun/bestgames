# -*- coding: utf-8 -*-
from django.utils.encoding import force_unicode
from django.utils.functional import wraps

def parse_tags(tagstring):
	if not tagstring:
		return []

	tagstring = force_unicode(tagstring)

	# Special case - if there are no commas or double quotes in the
	# input, we don't *do* a recall... I mean, we know we only need to
	# split on spaces.
	if u',' not in tagstring and u'，' not in tagstring and u'"' not in tagstring:
		words = list(set(split_strip(tagstring, u' ')))
		words.sort()
		return words

	words = []
	buffer = []
	# Defer splitting of non-quoted sections until we know if there are
	# any unquoted commas.
	to_be_split = []
	saw_loose_comma = False
	open_quote = False
	i = iter(tagstring)
	try:
		while True:
			c = i.next()
			if c == u'"':
				if buffer:
					to_be_split.append(u''.join(buffer))
					buffer = []
				open_quote = True
				c = i.next()
				while c != u'"':
					buffer.append(c)
					c = i.next()
				if buffer:
					word = u''.join(buffer).strip()
					if word:
						words.append(word)
					buffer = []
				open_quote = False
			else:
				if not saw_loose_comma and (c == u',' or c == u'，'):
					saw_loose_comma = True
				if c == u'，':
					buffer.append(',')
				else:
					buffer.append(c)
	except StopIteration:
		if buffer:
			if open_quote and (u',' in buffer or u'，' in buffer):
				saw_loose_comma = True
			to_be_split.append(u''.join(buffer))
	if to_be_split:
		if saw_loose_comma:
			delimiter = u','
		else:
			delimiter = u' '
		for chunk in to_be_split:
			words.extend(split_strip(chunk, delimiter))
	words = list(set(words))
	words.sort()
	return words

def split_strip(string, delimiter=u','):
	if not string:
		return []

	words = [w.strip() for w in string.split(delimiter)]
	return [w for w in words if w]

def edit_string_for_tags(tags):
	names = []
	for tag in tags:
		name = tag.name
		if u',' in name or u'，' in name or u' ' in name:
			names.append('"%s"' % name)
		else:
			names.append(name)
	return u', '.join(sorted(names))

def require_instance_manager(func):
	@wraps(func)
	def inner(self, *args, **kwargs):
		if self.instance is None:
			raise TypeError("Can't call %s with a non-instance manager" % func.__name__)
		return func(self, *args, **kwargs)
	return inner