# -*- coding: utf-8 -*-
import sys
import os
from urlparse import urlsplit

from django.shortcuts import render_to_response, get_object_or_404, render, redirect
from console.tables import EntityTable
from console.models import Entity, EntityType, EntityCollection, EntityProperty
from console.forms import EntityForm
from content_engine_v2 import settings

def _redirect_back(request):
    next_url = request.GET.get('next', None)
    print next_url
    if next_url:
        try:
            return redirect(next_url)
        except IndexError:
            return redirect('/')
    else:
        return redirect('/')

def login(request):
    pass

def index(request):
    entities = EntityTable(Entity.objects.all())
    entities.paginate(page=request.GET.get("page",1), per_page=50)
    entities.data.verbose_name = u"内容"

    return render(request, "index.html", {'entities' : entities, 'entity_types' : EntityType.objects.all()})

def add_edit_entity(request, entity_id=None):
    if entity_id:
        entity = get_object_or_404(Entity, id=entity_id)
        entity_type = entity.type
    else:
        entity = None
        entity_type = EntityType.objects.get(id=request.GET.get('type', 1))

    if request.method == 'POST':
        form = EntityForm(entity_type, entity, request.POST, request.FILES)
        if form.is_valid():
            if entity is None:
                entity = Entity()
                entity.type = entity_type
                if request.user.is_authenticated():
                    entity.presenter = request.user
                entity.save()
            for prop in entity_type.properties.all():
                if form.cleaned_data.has_key(prop.name):
                    entity_property, created = EntityProperty.objects.get_or_create(entity=entity, property=prop)
                    val = form.cleaned_data[prop.name]
                    if prop.type.name == 'image':
                        val = val.name
                    if not entity_property.compare(val):
                        entity_property.set_value(val)
                        entity_property.save()
                        
            return _redirect_back(request)
    else:
        form = EntityForm(entity_type, entity)
        wysiwyg_enabled = entity_type.properties.filter(type__name__in=['richtext']).exists()
        print wysiwyg_enabled
    return render(request, 'add_edit_entity.html', {'entity_type' : entity_type, 'form' : form, 'wysiwyg_enabled' : wysiwyg_enabled})

def delete_entity(request, entity_id=None):
    entity = get_object_or_404(Entity, id=entity_id)
    entity.delete()
    return _redirect_back(request)

def preview_entity(request, entity_id=None):
    pass

def logout(request):
    pass