from rest_framework import viewsets
from .models import World, Character, Relationship, Skill
from .serializers import (
    WorldSerializer,
    CharacterSerializer,
    RelationshipSerializer,
    SkillSerializer,
)


class WorldViewSet(viewsets.ModelViewSet):
    queryset = World.objects.all()
    serializer_class = WorldSerializer


class CharacterViewSet(viewsets.ModelViewSet):
    queryset = Character.objects.select_related("world").prefetch_related(
        "skills", "source_relations__target_character"
    )
    serializer_class = CharacterSerializer

    def get_queryset(self):
        qs = super().get_queryset()
        world_id = self.request.query_params.get("world")
        if world_id:
            qs = qs.filter(world_id=world_id)
        return qs


class RelationshipViewSet(viewsets.ModelViewSet):
    queryset = Relationship.objects.select_related("source_character", "target_character")
    serializer_class = RelationshipSerializer


class SkillViewSet(viewsets.ModelViewSet):
    queryset = Skill.objects.select_related("character")
    serializer_class = SkillSerializer

    def get_queryset(self):
        qs = super().get_queryset()
        character_id = self.request.query_params.get("character")
        if character_id:
            qs = qs.filter(character_id=character_id)
        return qs
