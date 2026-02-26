from django.contrib import admin
from .models import World, Character, Relationship, Skill


@admin.register(World)
class WorldAdmin(admin.ModelAdmin):
    list_display = ("name", "created_at")


@admin.register(Character)
class CharacterAdmin(admin.ModelAdmin):
    list_display = ("name", "world", "created_at")
    list_filter = ("world",)


@admin.register(Relationship)
class RelationshipAdmin(admin.ModelAdmin):
    list_display = ("source_character", "relation_type", "target_character", "weight")


@admin.register(Skill)
class SkillAdmin(admin.ModelAdmin):
    list_display = ("name", "character", "mana_cost")
