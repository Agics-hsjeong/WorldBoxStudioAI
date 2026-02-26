"""
시스템 프롬프트 빌더: Character + Relationship + Skill → LLM용 시스템 프롬프트 문자열.
docs/기술_스택_및_아키텍처.md §4 기준.
"""
from .models import Character, Relationship, Skill


def build_system_prompt(character: Character) -> str:
    """캐릭터의 스탯, 관계, 스킬을 반영한 시스템 프롬프트 생성."""
    world_name = character.world.name
    stats = character.stats or {}
    base_prompt = (
        f"당신은 '{world_name}' 세계관의 {character.name}입니다. "
        f"당신의 능력치(지능, 마력 등)는 {stats}에 따라 행동과 말투에 반영됩니다.\n\n"
    )

    relations = Relationship.objects.filter(
        source_character=character
    ).select_related("target_character")
    relation_prompt = "당신의 인간관계는 다음과 같습니다:\n"
    for rel in relations:
        relation_prompt += f"- {rel.target_character.name}: '{rel.relation_type}' (강도: {rel.weight})\n"
    relation_prompt += "\n"

    skills = Skill.objects.filter(character=character)
    skill_prompt = "플레이어가 아래 기술을 사용할 때, 조건에 맞게 화려하게 묘사하세요:\n"
    for skill in skills:
        skill_prompt += f"- {skill.name} (마나 소모: {skill.mana_cost}): {skill.system_effect}\n"

    return base_prompt + relation_prompt + skill_prompt
