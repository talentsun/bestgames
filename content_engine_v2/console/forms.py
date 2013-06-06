# -*- coding: utf-8 -*-
from django.db import models
from django import forms
from django.forms import Form
from datetime import datetime
from datetimewidget.widgets import DateTimeWidget
from ajax_upload.widgets import AjaxClearableFileInput
from django_select2 import *
from django.utils.translation import ugettext as _

from console.fields import TagField
from console.widgets import CountableTextarea, RichTextEditor
from console.models import Entity, EntityType, Property, EntityType2Property

class EntityForm(Form):
	def __init__(self, entity_type, entity, *args, **kwargs):
		super(EntityForm, self).__init__(*args, **kwargs)
		if entity_type:
			self.entity_type = entity_type
		for e2p in EntityType2Property.objects.filter(entity_type=entity_type).order_by('order'):
			initial = None
			if entity:
				try:
					entity_prop = entity.entityproperty_set.get(property=e2p.property)
					if entity_prop:
						initial = entity_prop.get_value()
				except:
					entity_prop = None
			self.fields[e2p.property.name] = self._build_field(e2p.property, e2p.is_required, initial)

	def _build_field(self, prop, required, initial):
		if prop.type.name == 'char':
			return self._build_char_field(prop, required, initial)
		elif prop.type.name == 'text':
			return self._build_text_field(prop, required, initial)
		elif prop.type.name == 'datetime':
			return self._build_datetime_field(prop, required, initial)
		elif prop.type.name == 'image':
			return self._build_image_field(prop, required, initial)
		elif prop.type.name == 'url':
			return self._build_url_field(prop, required, initial)
		elif prop.type.name == 'choices':
			return self._build_choices_field(prop, required, initial)
		elif prop.type.name == 'tags':
			return self._build_tags_field(prop, required, initial)
		elif prop.type.name == 'richtext':
			return self._build_richtext_field(prop, required, initial)

		return None

	def _build_char_field(self, prop, required, initial):
		field = forms.CharField(label=prop.verbose_name, required=required, initial=initial)
		
		try:
			multiple_line = prop.propertyattr_set.get(type__name='multiple_line')
		except:
			multiple_line = None
		if multiple_line and multiple_line.get_value() > 0:
			field.widget = forms.Textarea()

		try:
			max_length_attr = prop.propertyattr_set.get(type__name='max_length')
		except:
			max_length_attr = None
		if max_length_attr:
			field.max_length = max_length_attr.get_value()
			try:
				countable = prop.propertyattr_set.get(type__name='countable')
			except:
				countable = None
			if countable and countable.get_value() > 0:
				field.widget = CountableTextarea(max_length_attr.get_value())

		self._set_help_text(field, prop)
		return field

	def _build_text_field(self, prop, required):
		field = forms.CharField(label=prop.verbose_name, required=required, widget=forms.Textarea, initial=initial)
		self._set_help_text(field, prop)
		return field

	def _build_datetime_field(self, prop, required, initial):
		try:
			drop_past_attr = prop.propertyattr_set.get(type__name='drop_past')
		except:
			drop_past_attr = None

		if drop_past_attr and drop_past_attr.get_value() > 0:
			field = forms.DateTimeField(label=prop.verbose_name, initial=initial, required=required, widget=DateTimeWidget(options={
					'autoclose' : 'true',
					'showMeridian' : 'true',
					'startDate' : datetime.today().strftime('%Y-%m-%d %H:%M:%S')
					}))
		else:
			field = forms.DateTimeField(label=prop.verbose_name, required=required, initial=initial, widget=DateTimeWidget(options={
					'autoclose' : 'true',
					'showMeridian' : 'true',
					}))

		self._set_help_text(field, prop)
		return field

	def _build_image_field(self, prop, required, initial):
		field = forms.ImageField(label=prop.verbose_name, widget=AjaxClearableFileInput(), initial=initial)
		self._set_help_text(field, prop)
		return field

	def _build_url_field(self, prop, required, initial):
		field = forms.URLField(label=prop.verbose_name, required=required, initial=initial)
		self._set_help_text(field, prop)
		return field

	def _build_choices_field(self, prop, required, initial):
		choices = []
		default_choice = None
		for prop_val in prop.propertyvalue_set.all():
			if prop_val.is_default:
				default_choice = prop_val.get_value()

			verbose_name = prop_val.get_value()
			if prop_val.verbose_name:
				verbose_name = prop_val.verbose_name

			choices.append((prop_val.get_value(), verbose_name))

		field = forms.ChoiceField(choices=choices, label=prop.verbose_name, required=required)

		if initial:
			field.initial = initial
		elif default_choice:
			field.initial = default_choice

		self._set_help_text(field, prop)
		return field

	def _build_tags_field(self, prop, required, initial):
		field = TagField(label=prop.verbose_name, required=required, initial=initial, max_length=100)
		self._set_help_text(field, prop)
		return field

	def _build_richtext_field(self, prop, required, initial):
		field = forms.CharField(label=prop.verbose_name, required=required, widget=RichTextEditor, initial=initial)
		self._set_help_text(field, prop)
		return field

	def _set_help_text(self, field, prop):
		try:
			help_text_attr = prop.propertyattr_set.get(type__name='help_text')
		except:
			help_text_attr = None

		if help_text_attr:
			field.help_text = help_text_attr.get_value()