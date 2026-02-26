<script lang="ts">
  import { page } from '$app/stores';
  import { onMount } from 'svelte';
  import {
    worldGet,
    charactersList,
    relationshipsList,
    relationshipCreate,
    relationshipDelete,
    unwrapList,
    type World,
    type Character,
    type Relationship,
  } from '$lib/api';

  const worldId = parseInt($page.params.worldId, 10);
  let world: World | null = null;
  let characters: Character[] = [];
  let relations: Relationship[] = [];
  let loading = true;
  let error = '';
  let sourceId = '';
  let targetId = '';
  let relationType = '스승과 제자';
  let weight = 1;
  let submitting = false;

  const RELATION_TYPES = ['스승과 제자', '짝사랑', '적대관계', '혼인', '과거 연인', '동료', '친구', '가족'];

  async function load() {
    loading = true;
    error = '';
    try {
      world = await worldGet(worldId);
      const [charData, relData] = await Promise.all([
        charactersList(worldId),
        relationshipsList(),
      ]);
      characters = unwrapList(charData);
      const charIds = new Set(characters.map((c) => c.id));
      relations = unwrapList(relData).filter(
        (r) => charIds.has(r.source_character) && charIds.has(r.target_character)
      );
    } catch (e) {
      error = e instanceof Error ? e.message : '조회 실패';
    } finally {
      loading = false;
    }
  }

  function getCharName(id: number): string {
    return characters.find((c) => c.id === id)?.name ?? `#${id}`;
  }

  async function addRelation() {
    const sid = parseInt(sourceId, 10);
    const tid = parseInt(targetId, 10);
    if (!sid || !tid || sid === tid) {
      error = '서로 다른 두 캐릭터를 선택하세요.';
      return;
    }
    submitting = true;
    try {
      await relationshipCreate({
        source_character: sid,
        target_character: tid,
        relation_type: relationType,
        weight,
      });
      sourceId = '';
      targetId = '';
      await load();
    } catch (e) {
      error = e instanceof Error ? e.message : '관계 추가 실패';
    } finally {
      submitting = false;
    }
  }

  async function removeRelation(r: Relationship) {
    if (!confirm(`"${getCharName(r.source_character)}" ↔ "${getCharName(r.target_character)}" 관계를 삭제할까요?`)) return;
    try {
      await relationshipDelete(r.id);
      await load();
    } catch (e) {
      error = e instanceof Error ? e.message : '삭제 실패';
    }
  }

  onMount(load);
</script>

<svelte:head><title>관계도 — {world?.name ?? '에디터'}</title></svelte:head>

{#if loading}
  <p class="text-gray-500">불러오는 중…</p>
{:else if error && !world}
  <p class="text-red-600">{error}</p>
{:else if world}
  <div class="space-y-6">
    <p class="text-sm"><a href="/editor/{worldId}" class="text-blue-600 underline">← {world.name} 캐릭터 목록</a></p>

    <div class="rounded-lg border border-gray-200 bg-white p-4">
      <h2 class="text-lg font-medium">관계도</h2>
      <p class="mt-1 text-sm text-gray-500">캐릭터 간 관계를 추가하세요. (스승/제자, 짝사랑, 적대 등)</p>

      <form on:submit|preventDefault={addRelation} class="mt-4 flex flex-wrap items-end gap-3">
        <div>
          <label class="block text-xs text-gray-500">캐릭터 A</label>
          <select bind:value={sourceId} class="mt-0.5 rounded border border-gray-300 px-3 py-2 text-sm">
            <option value="">선택</option>
            {#each characters as c}
              <option value={c.id}>{c.name}</option>
            {/each}
          </select>
        </div>
        <div>
          <label class="block text-xs text-gray-500">관계 유형</label>
          <select bind:value={relationType} class="mt-0.5 rounded border border-gray-300 px-3 py-2 text-sm">
            {#each RELATION_TYPES as t}
              <option value={t}>{t}</option>
            {/each}
          </select>
        </div>
        <div>
          <label class="block text-xs text-gray-500">캐릭터 B</label>
          <select bind:value={targetId} class="mt-0.5 rounded border border-gray-300 px-3 py-2 text-sm">
            <option value="">선택</option>
            {#each characters as c}
              <option value={c.id}>{c.name}</option>
            {/each}
          </select>
        </div>
        <div>
          <label class="block text-xs text-gray-500">강도</label>
          <input type="number" bind:value={weight} min="1" max="10" class="mt-0.5 w-16 rounded border border-gray-300 px-2 py-2 text-sm" />
        </div>
        <button type="submit" disabled={submitting || !sourceId || !targetId} class="rounded bg-blue-600 px-4 py-2 text-sm text-white hover:bg-blue-700 disabled:opacity-50">
          {submitting ? '추가 중…' : '관계 추가'}
        </button>
      </form>

      {#if relations.length === 0}
        <p class="mt-4 text-sm text-gray-500">등록된 관계가 없습니다.</p>
      {:else}
        <ul class="mt-4 space-y-2">
          {#each relations as r}
            <li class="flex items-center justify-between rounded border border-gray-100 bg-gray-50 px-3 py-2 text-sm">
              <span>{getCharName(r.source_character)} <span class="text-gray-500">— {r.relation_type} (강도 {r.weight}) —</span> {r.target_character_name ?? getCharName(r.target_character)}</span>
              <button type="button" on:click={() => removeRelation(r)} class="text-red-600 hover:underline">삭제</button>
            </li>
          {/each}
        </ul>
      {/if}
    </div>
  </div>
{/if}

<p class="mt-6"><a href="/" class="text-sm text-blue-600 underline">← 메인</a></p>
