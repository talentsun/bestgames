# -*- coding: utf-8 -*-
from django.db import models
from django.contrib.auth.models import User

class ValueType(object):
	VALUE_TYPE_INT = 1
	VALUE_TYPE_STR = 2
	VALUE_TYPE_TEXT = 3

class PropertyType(models.Model):
	name = models.CharField(verbose_name=u"属性类型名称", editable=False, max_length=255)
	verbose_name = models.CharField(editable=False, max_length=255)

	class Meta:
		db_table = u'property_types'

class PropertyTypeAttr(models.Model):
	property_type = models.ForeignKey(PropertyType)
	name = models.CharField(editable=False, max_length=255)
	value_type = models.IntegerField(default=ValueType.VALUE_TYPE_INT, editable=False)
	value_int = models.IntegerField(editable=False, null=True)
	value_str = models.CharField(editable=False, max_length=255, null=True)

	def get_value(self):
		if self.value_type == ValueType.VALUE_TYPE_INT:
			return self.value_int
		elif self.value_type == ValueType.VALUE_TYPE_STR:
			return self.value_str
		else:
			return None

	def set_value(self, val):
		if self.value_type == ValueType.VALUE_TYPE_INT:
			self.value_int = val
		elif self.value_type == ValueType.VALUE_TYPE_STR:
			self.value_str = val

	class Meta:
		db_table = u'property_type_attrs'

class Property(models.Model):
	name = models.CharField(verbose_name=u"属性名称", editable=False, max_length=255)
	verbose_name = models.CharField(editable=False, max_length=255)
	type = models.ForeignKey(PropertyType, verbose_name=u"属性类型")
	value_type = models.IntegerField(verbose_name=u"属性值类型", default=ValueType.VALUE_TYPE_INT, editable=False)

	class Meta:
		db_table = u'properties'


class PropertyAttr(models.Model):
	property = models.ForeignKey(Property)
	type = models.ForeignKey(PropertyTypeAttr)
	value_int = models.IntegerField(editable=False, null=True)
	value_str = models.CharField(editable=False, max_length=255, null=True)

	def get_value(self):
		if self.type.value_type == ValueType.VALUE_TYPE_INT:
			return self.value_int
		elif self.type.value_type == ValueType.VALUE_TYPE_STR:
			return self.value_str
		else:
			return None

	def set_value(self, val):
		if self.type.value_type == ValueType.VALUE_TYPE_INT:
			self.value_int = val
		elif self.type.value_type == ValueType.VALUE_TYPE_STR:
			self.value_str = val

	class Meta:
		db_table = u'property_attrs'

class PropertyValue(models.Model):
	property = models.ForeignKey(Property)
	value_int = models.IntegerField(verbose_name=u"整形数字", editable=False, null=True)
	value_str = models.CharField(verbose_name=u"文本", editable=False, max_length=255, null=True)
	value_text = models.TextField(verbose_name="长文本", editable=False, null=True)
	is_default = models.BooleanField(verbose_name=u"默认值", default=False)
	verbose_name = models.CharField(null=True, blank=True, max_length=255)

	def get_value(self):
		if self.property.value_type == ValueType.VALUE_TYPE_INT:
			return self.value_int
		elif self.property.value_type == ValueType.VALUE_TYPE_STR:
			return self.value_str
		elif self.property.value_type == ValueType.VALUE_TYPE_TEXT:
			return self.value_text
		else:
			return None

	def set_value(self, val):
		if self.property.value_type == ValueType.VALUE_TYPE_INT:
			self.value_int = val
		elif self.property.value_type == ValueType.VALUE_TYPE_STR:
			self.value_str = val
		elif self.property.value_type == ValueType.VALUE_TYPE_TEXT:
			self.value_text = val

	class Meta:
		db_table = u'property_values'

class EntityType(models.Model):
	name = models.CharField(verbose_name=u"实体类型名称", editable=False, max_length=255)
	verbose_name = models.CharField(editable=False, max_length=255)
	properties = models.ManyToManyField(Property, verbose_name=u"实体属性", through="EntityType2Property")
	is_collection = models.BooleanField(default=False)

	class Meta:
		db_table = u'entity_types'

class EntityType2Property(models.Model):
	is_required = models.BooleanField(default=True)
	is_id = models.BooleanField(default=False)
	entity_type = models.ForeignKey(EntityType)
	property = models.ForeignKey(Property)
	order = models.IntegerField(null=False)

	class Meta:
		db_table = u'entity_types_properties'

class Entity(models.Model):
	type = models.ForeignKey(EntityType, verbose_name=u"实体类型")
	presenter = models.ForeignKey(User, verbose_name=u"推荐人", blank=True, null=True, on_delete=models.SET_NULL)

	class Meta:
		db_table = u'entities'

class EntityProperty(models.Model):
	entity = models.ForeignKey(Entity, verbose_name=u"实体")
	property = models.ForeignKey(Property, verbose_name=u"属性")
	value_int = models.IntegerField(verbose_name=u"整形数字", editable=False, null=True)
	value_str = models.CharField(verbose_name=u"字符串", editable=False, max_length=255, null=True)
	value_text = models.TextField(verbose_name="长文本", editable=False, null=True)

	def get_value(self):
		if self.property.value_type == ValueType.VALUE_TYPE_INT:
			return self.value_int
		elif self.property.value_type == ValueType.VALUE_TYPE_STR:
			return self.value_str
		elif self.property.value_type == ValueType.VALUE_TYPE_TEXT:
			return self.value_text
		else:
			return None

	def set_value(self, val):
		if self.property.value_type == ValueType.VALUE_TYPE_INT:
			self.value_int = val
		elif self.property.value_type == ValueType.VALUE_TYPE_STR:
			self.value_str = val
		elif self.property.value_type == ValueType.VALUE_TYPE_TEXT:
			self.value_text = val

	class Meta:
		db_table = u'entity_properties'

class EntityCollection(Entity):
	entity_type = models.ForeignKey(EntityType, verbose_name=u"实体类型")
	entities = models.ManyToManyField(Entity, verbose_name=u"实体", related_name="collection_entities")

	class Meta:
		db_table = u'entity_collections'

class Tag(models.Model):
	key = models.CharField(blank=False, null=False, max_length=255)
	value = models.CharField(blank=False, null=False, max_length=255)
	slug = models.CharField(blank=False, null=False, max_length=255)

	class Meta:
		db_table = u"tags"