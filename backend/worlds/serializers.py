from rest_framework import serializers
from .models import World, Character, Relationship, Skill


class SkillSerializer(serializers.ModelSerializer):
    class Meta:
        model = Skill
        fields = ("id", "name", "mana_cost", "system_effect")


class RelationshipSerializer(serializers.ModelSerializer):
    target_character_name = serializers.CharField(source="target_character.name", read_only=True)

    class Meta:
        model = Relationship
        fields = ("id", "target_character", "target_character_name", "relation_type", "weight")


class CharacterSerializer(serializers.ModelSerializer):
    skills = SkillSerializer(many=True, read_only=True)
    source_relations = RelationshipSerializer(many=True, read_only=True)

    class Meta:
        model = Character
        fields = ("id", "world", "name", "stats", "metadata", "skills", "source_relations", "created_at")


class CharacterListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Character
        fields = ("id", "name", "world")


class WorldSerializer(serializers.ModelSerializer):
    characters = CharacterListSerializer(many=True, read_only=True)

    class Meta:
        model = World
        fields = ("id", "name", "description", "characters", "created_at", "updated_at")
