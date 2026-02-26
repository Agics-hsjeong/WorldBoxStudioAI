"""
세계관(World), 캐릭터(Character), 관계(Relationship), 스킬(Skill) 모델.
docs/기술_스택_및_아키텍처.md 기준.
"""
from django.db import models


class TimeStampedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class World(TimeStampedModel):
    """세계관 최상위 컨테이너"""
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)

    class Meta:
        verbose_name = "세계관"
        verbose_name_plural = "세계관"

    def __str__(self):
        return self.name


class Character(TimeStampedModel):
    """노코드 페르소나 데이터"""
    world = models.ForeignKey(World, on_delete=models.CASCADE, related_name="characters")
    name = models.CharField(max_length=100)
    stats = models.JSONField(default=dict, blank=True)   # 듀얼 스탯
    metadata = models.JSONField(default=dict, blank=True)  # 심화 메타데이터

    class Meta:
        verbose_name = "캐릭터"
        verbose_name_plural = "캐릭터"

    def __str__(self):
        return f"{self.name} ({self.world.name})"


class Relationship(TimeStampedModel):
    """관계도 (그래프 구조를 RDB로 표현)"""
    source_character = models.ForeignKey(
        Character, related_name="source_relations", on_delete=models.CASCADE
    )
    target_character = models.ForeignKey(
        Character, related_name="target_relations", on_delete=models.CASCADE
    )
    relation_type = models.CharField(max_length=50)  # 스승과 제자, 적대관계, 짝사랑 등
    weight = models.IntegerField(default=1)

    class Meta:
        verbose_name = "관계"
        verbose_name_plural = "관계"
        unique_together = [("source_character", "target_character", "relation_type")]

    def __str__(self):
        return f"{self.source_character.name} -{self.relation_type}- {self.target_character.name}"


class Skill(TimeStampedModel):
    """TRPG 액션/스킬"""
    character = models.ForeignKey(Character, on_delete=models.CASCADE, related_name="skills")
    name = models.CharField(max_length=100)
    mana_cost = models.IntegerField(default=0)
    system_effect = models.TextField(help_text="시스템 프롬프트에 주입될 스킬 효과")

    class Meta:
        verbose_name = "스킬"
        verbose_name_plural = "스킬"

    def __str__(self):
        return f"{self.character.name}: {self.name}"
