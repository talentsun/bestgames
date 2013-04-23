# -*- coding: utf-8 -*-
import django
from django.db import models
from django.contrib.auth.models import User
from django.utils.encoding import force_unicode
from django.db import models, IntegrityError, transaction
from uuslug import slugify as default_slugify
from django.utils.translation import ugettext_lazy as _, ugettext
from django.db.models.fields.related import ManyToManyRel, RelatedField, add_lazy_relation
from django.db.models.related import RelatedObject
from django.utils.text import capfirst

from console.fields import TagField
from console.utils import require_instance_manager

class ValueType(object):
	VALUE_TYPE_INT = 1
	VALUE_TYPE_STR = 2
	VALUE_TYPE_TEXT = 3
	VALUE_TYPE_TAG = 4

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

class EntityCollection(Entity):
	entity_type = models.ForeignKey(EntityType, verbose_name=u"实体类型")
	entities = models.ManyToManyField(Entity, verbose_name=u"实体", related_name="collection_entities")

	class Meta:
		db_table = u'entity_collections'

# Tag related models
class Tag(models.Model):
	property = models.ForeignKey(Property)
	name = models.CharField(max_length=100)
	slug = models.SlugField(max_length=100)

	def __unicode__(self):
		return '%s:%s' %(self.property.verbose_name, self.name)

	class Meta:
		db_table = u"tags"
		verbose_name = _(u"标签")
		verbose_name_plural = _(u"标签")

	def save(self, *args, **kwargs):
		if not self.pk and not self.slug:
			self.slug = self.slugify(self.name)
			print self.slug
			if django.VERSION >= (1, 2):
				from django.db import router
				using = kwargs.get('using') or router.db_for_write(
					type(self), instance=self)
				kwargs['using'] = using
				trans_kwargs = {'using' : using}
			else:
				trans_kwargs = {}
			i = 0
			while True:
				i += 1
				try:
					sid = transaction.savepoint(**trans_kwargs)
					res = super(Tag, self).save(*args, **kwargs)
					transaction.savepoint_commit(sid, **trans_kwargs)
					return res
				except IntegrityError:
					transaction.savepoint_rollback(sid, **trans_kwargs)
					self.slug = self.slugify(self.name, i)
		else:
			return super(Tag, self).save(*args, **kwargs)

	def slugify(self, tag, i=None):
		slug = default_slugify(tag)
		if i is not None:
			slug += "_%d" % i
		return slug

class TaggedItem(models.Model):
	entity_property = models.ForeignKey('EntityProperty')
	tag = models.ForeignKey(Tag)

	def __unicode__(self):
		return ugettext("%(object)s tagged with %(tag)s" % {
			"object" : self.entity_property,
			"tag" : self.tag
			})

	class Meta:
		db_table = 'tagged_items'

	@classmethod
	def tag_model(cls):
		return cls._meta.get_field_by_name("tag")[0].rel.to

	@classmethod
	def tag_relname(cls):
		return cls._meta.get_field_by_name('tag')[0].rel.related_name

	@classmethod
	def lookup_kwargs(cls, instance):
		return {
			'entity_property_id' : instance.pk
		}

	@classmethod
	def bulk_lookup_kwargs(cls, instances):
		return {
			'entity_property_id__in' : [instance.pk for instance in instances]
		}

	@classmethod
	def tags_for(cls, model, instance=None):
		kwargs = {}

		if instance is not None:
			kwargs['taggeditem__entity_property_id'] = instance.pk
		return Tag.objects.filter(**kwargs).distinct()

class TaggableRel(ManyToManyRel):
	def __init__(self):
		self.related_name = None
		self.limit_choices_to = {}
		self.symmetrical = True
		self.multiple = True
		self.through = None

class TaggableManager(RelatedField):
	def __init__(self, verbose_name=_(u"标签"),
		help_text=_(u"多个标签使用“，”分隔。"), through=None, blank=False):
		self.through = through or TaggedItem
		self.rel = TaggableRel()
		self.verbose_name = verbose_name
		self.help_text = help_text
		self.blank = blank
		self.editable = True
		self.unique = False
		self.creates_table = False
		self.db_column = None
		self.choices = None
		self.serialize = False
		self.null = True
		self.creation_counter = models.Field.creation_counter
		models.Field.creation_counter += 1

	def __get__(self, instance, model):
		if instance is not None and instance.pk is None:
			raise ValueError("%s objects need to have a primary key value "
				"before you can access their tags." % model.__name__)
		manager = _TaggableManager(
			through=self.through, model=model, instance=instance
		)
		return manager

	def contribute_to_class(self, cls, name):
		self.name = self.column = name
		self.model = cls
		cls._meta.add_field(self)
		setattr(cls, name, self)
		if not cls._meta.abstract:
			if isinstance(self.through, basestring):
				def resolve_related_class(field, model, cls):
					self.through = model
					self.post_through_setup(cls)
				add_lazy_relation(
					cls, self, self.through, resolve_related_class
				)
			else:
				self.post_through_setup(cls)

	def post_through_setup(self, cls):
		self.rel.to = self.through._meta.get_field("tag").rel.to
		self.related = RelatedObject(self.through, cls, self)

	def save_form_data(self, instance, value):
		getattr(instance, self.name).set(*value)

	def formfield(self, form_class=TagField, **kwargs):
		defaults = {
			"label": capfirst(self.verbose_name),
			"help_text": self.help_text,
			"required": not self.blank
		}
		defaults.update(kwargs)
		return form_class(**defaults)

	def value_from_object(self, instance):
		if instance.pk:
			return self.through.objects.filter(**self.through.lookup_kwargs(instance))
		return self.through.objects.none()

	def related_query_name(self):
		return self.model._meta.module_name

	def m2m_reverse_name(self):
		return self.through._meta.get_field_by_name("tag")[0].column

	def m2m_target_field_name(self):
		return self.model._meta.pk.name

	def m2m_reverse_target_field_name(self):
		return self.rel.to._meta.pk.name

	def m2m_column_name(self):
		return self.through._meta.get_field('entity_property').column

	def db_type(self, connection=None):
		return None

	def m2m_db_table(self):
		return self.through._meta.db_table

	def extra_filters(self, pieces, pos, negate):
		return []

	def bulk_related_objects(self, new_objs, using):
		return []

class _TaggableManager(models.Manager):
	def __init__(self, through, model, instance):
		self.through = through
		self.model = model
		self.instance = instance

	def get_query_set(self):
		return self.through.tags_for(self.model, self.instance)

	def _lookup_kwargs(self):
		return self.through.lookup_kwargs(self.instance)

	def get_available_tags(self):
		return self.instance.property.tag_set

	@require_instance_manager
	def add(self, *tags):
		str_tags = set([
			t
			for t in tags
			if not isinstance(t, self.through.tag_model())
		])
		tag_objs = set(tags) - str_tags
		# If str_tags has 0 elements Django actually optimizes that to not do a
		# query.  Malcolm is very smart.
		existing = self.through.tag_model().objects.filter(
			name__in=str_tags, property=self.instance.property
		)
		tag_objs.update(existing)

		for new_tag in str_tags - set(t.name for t in existing):
			tag_objs.add(self.through.tag_model().objects.create(property=self.instance.property, name=new_tag))

		for tag in tag_objs:
			self.through.objects.get_or_create(tag=tag, **self._lookup_kwargs())

	@require_instance_manager
	def set(self, *tags):
		self.clear()
		self.add(*tags)

	@require_instance_manager
	def remove(self, *tags):
		self.through.objects.filter(**self._lookup_kwargs()).filter(
			tag__name__in=tags).delete()

	@require_instance_manager
	def clear(self):
		self.through.objects.filter(**self._lookup_kwargs()).delete()

	def most_common(self):
		return self.get_query_set().annotate(
			num_times=models.Count(self.through.tag_relname())
		).order_by('-num_times')

class EntityProperty(models.Model):
	entity = models.ForeignKey(Entity, verbose_name=u"实体")
	property = models.ForeignKey(Property, verbose_name=u"属性")
	value_int = models.IntegerField(verbose_name=u"整形数字", editable=False, null=True)
	value_str = models.CharField(verbose_name=u"字符串", editable=False, max_length=255, null=True)
	value_text = models.TextField(verbose_name=u"长文本", editable=False, null=True)
	value_tag = TaggableManager(verbose_name=u"标签")

	def get_value(self):
		if self.property.value_type == ValueType.VALUE_TYPE_INT:
			return self.value_int
		elif self.property.value_type == ValueType.VALUE_TYPE_STR:
			return self.value_str
		elif self.property.value_type == ValueType.VALUE_TYPE_TEXT:
			return self.value_text
		elif self.property.value_type == ValueType.VALUE_TYPE_TAG:
			return self.value_tag
		else:
			return None

	def set_value(self, val):
		if self.property.value_type == ValueType.VALUE_TYPE_INT:
			self.value_int = val
		elif self.property.value_type == ValueType.VALUE_TYPE_STR:
			self.value_str = val
		elif self.property.value_type == ValueType.VALUE_TYPE_TEXT:
			self.value_text = val
		elif self.property.value_type == ValueType.VALUE_TYPE_TAG:
			self.value_tag.set(*val)

	def compare(self, val):
		if self.property.value_type == ValueType.VALUE_TYPE_INT:
			return self.value_int == int(val)
		elif self.property.value_type == ValueType.VALUE_TYPE_STR:
			return self.value_str == val
		elif self.property.value_type == ValueType.VALUE_TYPE_TEXT:
			return self.value_text == val
		elif self.property.value_type == ValueType.VALUE_TYPE_TAG:
			return set([tag.name for tag in self.value_tag.select_related("tag")]) == set(val)
		return False

	class Meta:
		db_table = u'entity_properties'

def _get_subclasses(model):
	subclasses = [model]
	for f in model._meta.get_all_field_names():
		field = model._meta.get_field_by_name(f)[0]
		if (isinstance(field, RelatedObject) and
			getattr(field.field.rel, "parent_link", None)):
			subclasses.extend(_get_subclasses(field.model))
	return subclasses