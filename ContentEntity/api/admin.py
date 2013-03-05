# -*- coding: utf-8 -*-
from api.models import Hot_Games, GameRediers,Entities,Entities_Tags,Tags,Game_Categories
from django.contrib import admin
from django.db import models
from api.AdminImageWidget import  AdminImageWidget

class TagsAdmin(admin.ModelAdmin):
    model=Tags
    pass

class HotGamesInline(admin.StackedInline):
    model = Hot_Games
    max_num = 1
    extra = 1
    fk_name = "entity_id"
    raw_id_fields=('tag',)

class GameRediersInline(admin.StackedInline):
    model = GameRediers
    extra = 1
    fk_name = "hot_game_id"

class HotGamesAdmin(admin.ModelAdmin):
    pass
#    formfield_overrides = { models.ImageField: {'widget': AdminImageWidget}}

#    inlines = [GameRediersInline]

class EntitiesAdmin(admin.ModelAdmin):
    inlines = [
        HotGamesInline
    ]
    fields = ('type',('is_weibo_recommended','timestamp'),'rating','presenter','recommended_reason')

class GameRediersAdmin(admin.ModelAdmin):
    raw_id_fields=('hot_game_id',)


admin.site.register(Hot_Games,HotGamesAdmin)
admin.site.register(GameRediers,GameRediersAdmin)
admin.site.register(Entities,EntitiesAdmin)
admin.site.register(Entities_Tags)
admin.site.register(Tags)
admin.site.register(Game_Categories)