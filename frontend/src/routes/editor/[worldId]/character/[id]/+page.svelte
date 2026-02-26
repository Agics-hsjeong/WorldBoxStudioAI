<script lang="ts">
  import { page } from '$app/stores';
  import { onMount } from 'svelte';
  import {
    worldGet,
    characterGet,
    characterUpdate,
    skillCreate,
    skillDelete,
    type World,
    type Character,
  } from '$lib/api';

  const worldId = parseInt($page.params.worldId, 10);
  const charId = parseInt($page.params.id, 10);
  let world: World | null = null;
  let character: Character | null = null;
  let loading = true;
  let error = '';
  let name = '';
  let statsJson = '{}';
  let metadataJson = '{}';
  let saving = false;
  // 스킬 추가
  let skillName = '';
  let skillMana = 0;
  let skillEffect = '';
  let addingSkill = false;

  const DEFAULT_STATS_KEYS = ['str', 'agi', 'spirit', 'health', 'int', 'end', 'vitality', 'energy', 'mana', 'recovery', 'resistance', 'leadership'];

  function parseJson(s: string | undefined, fallback: Record<string, unknown>): Record<string, unknown> {
    try {
      const o = JSON.parse(s ?? '{}');
      return typeof o === 'object' && o !== null ? o : fallback;
    } catch {
      return fallback;
    }
  }

  async function load() {
    loading = true;
    error = '';
    try {
      world = await worldGet(worldId);
      character = await characterGet(charId);
      if (character) {
        name = character.name;
        statsJson = JSON.stringify(character.stats || {}, null, 2);
        metadataJson = JSON.stringify(character.metadata || {}, null, 2);
      }
    } catch (e) {
      error = e instanceof Error ? e.message : '조회 실패';
    } finally {
      loading = false;
    }
  }

  async function save() {
    if (!character) return;
    saving = true;
    try {
      const stats = parseJson(statsJson, {}) as Record<string, number>;
      const metadata = parseJson(metadataJson, {});
      await characterUpdate(character.id, { name: name.trim(), stats, metadata });
      await load();
    } catch (e) {
      error = e instanceof Error ? e.message : '저장 실패';
    } finally {
      saving = false;
    }
  }

  async function addSkill() {
    if (!skillName.trim() || !character) return;
    addingSkill = true;
    try {
      await skillCreate({
        character: character.id,
        name: skillName.trim(),
        mana_cost: skillMana,
        system_effect: skillEffect.trim() || '-',
      });
      skillName = '';
      skillMana = 0;
      skillEffect = '';
      await load();
    } catch (e) {
      error = e instanceof Error ? e.message : '스킬 추가 실패';
    } finally {
      addingSkill = false;
    }
  }

  async function removeSkill(skill: { id: number; name: string }) {
    if (!confirm(`"${skill.name}" 스킬을 삭제할까요?`)) return;
    try {
      await skillDelete(skill.id);
      await load();
    } catch (e) {
      error = e instanceof Error ? e.message : '삭제 실패';
    }
  }

  onMount(load);
</script>

<svelte:head><title>{character?.name ?? '캐릭터'} — 에디터</title></svelte:head>

{#if loading}
  <p class="text-gray-500">불러오는 중…</p>
{:else if error || !world || !character}
  <p class="text-red-600">{error || '캐릭터를 찾을 수 없습니다.'}</p>
{:else}
  <div class="space-y-6">
    <p class="text-sm"><a href="/editor/{worldId}" class="text-blue-600 underline">← {world.name} 캐릭터 목록</a></p>

    <div class="rounded-lg border border-gray-200 bg-white p-4">
      <h2 class="text-lg font-medium">기본 정보</h2>
      <div class="mt-3 space-y-3">
        <div>
          <label class="block text-xs text-gray-500">이름</label>
          <input type="text" bind:value={name} class="mt-0.5 w-full max-w-md rounded border border-gray-300 px-3 py-2 text-sm" />
        </div>
        <button type="button" on:click={save} disabled={saving} class="rounded bg-blue-600 px-4 py-2 text-sm text-white hover:bg-blue-700 disabled:opacity-50">
          {saving ? '저장 중…' : '저장'}
        </button>
      </div>
    </div>

    <div class="rounded-lg border border-gray-200 bg-white p-4">
      <h3 class="font-medium">듀얼 스탯 (JSON)</h3>
      <p class="mt-1 text-xs text-gray-500">예: str, agi, spirit, health, int, end, vitality, energy, mana, recovery, resistance, leadership</p>
      <textarea bind:value={statsJson} rows="6" class="mt-2 w-full rounded border border-gray-300 p-2 font-mono text-sm"></textarea>
    </div>

    <div class="rounded-lg border border-gray-200 bg-white p-4">
      <h3 class="font-medium">메타데이터 (JSON)</h3>
      <p class="mt-1 text-xs text-gray-500">선호 음악, 소중한 물건, 자주 가는 곳 등 자유 형식</p>
      <textarea bind:value={metadataJson} rows="6" class="mt-2 w-full rounded border border-gray-300 p-2 font-mono text-sm"></textarea>
    </div>

    <div class="rounded-lg border border-gray-200 bg-white p-4">
      <h3 class="font-medium">스킬 (TRPG)</h3>
      <form on:submit|preventDefault={addSkill} class="mt-3 space-y-2">
        <div class="flex flex-wrap gap-2">
          <input type="text" bind:value={skillName} class="rounded border border-gray-300 px-3 py-2 text-sm" placeholder="스킬 이름" />
          <input type="number" bind:value={skillMana} min="0" class="w-20 rounded border border-gray-300 px-3 py-2 text-sm" placeholder="마나" />
          <input type="text" bind:value={skillEffect} class="min-w-[200px] flex-1 rounded border border-gray-300 px-3 py-2 text-sm" placeholder="효과 설명" />
        </div>
        <button type="submit" disabled={addingSkill || !skillName.trim()} class="rounded bg-gray-700 px-4 py-2 text-sm text-white hover:bg-gray-800 disabled:opacity-50">스킬 추가</button>
      </form>
      {#if character.skills && character.skills.length > 0}
        <ul class="mt-3 space-y-2">
          {#each character.skills as s}
            <li class="flex items-center justify-between rounded bg-gray-50 px-3 py-2 text-sm">
              <span><strong>{s.name}</strong> (마나 {s.mana_cost}) — {s.system_effect}</span>
              <button type="button" on:click={() => removeSkill(s)} class="text-red-600 hover:underline">삭제</button>
            </li>
          {/each}
        </ul>
      {:else}
        <p class="mt-3 text-sm text-gray-500">등록된 스킬이 없습니다.</p>
      {/if}
    </div>

    <div class="rounded-lg border border-gray-200 bg-white p-4">
      <h3 class="font-medium">관계</h3>
      {#if character.source_relations && character.source_relations.length > 0}
        <ul class="mt-2 space-y-1 text-sm">
          {#each character.source_relations as r}
            <li>{r.target_character_name} — {r.relation_type} (강도 {r.weight})</li>
          {/each}
        </ul>
      {:else}
        <p class="mt-2 text-sm text-gray-500">관계가 없습니다. 관계도 편집에서 추가하세요.</p>
      {/if}
      <p class="mt-2"><a href="/editor/{worldId}/relations" class="text-blue-600 underline">관계도 편집 →</a></p>
    </div>
  </div>
{/if}

<p class="mt-6"><a href="/" class="text-sm text-blue-600 underline">← 메인</a></p>
