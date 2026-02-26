<script lang="ts">
  import { page } from '$app/stores';
  import { onMount } from 'svelte';
  import { worldGet, charactersList, characterCreate, characterDelete, unwrapList, type World, type Character } from '$lib/api';

  const worldId = parseInt($page.params.worldId, 10);
  let world: World | null = null;
  let characters: Character[] = [];
  let loading = true;
  let error = '';
  let newName = '';
  let creating = false;

  async function loadWorld() {
    try {
      world = await worldGet(worldId);
    } catch (e) {
      error = e instanceof Error ? e.message : '세계관 조회 실패';
    }
  }

  async function loadCharacters() {
    try {
      const data = await charactersList(worldId);
      characters = unwrapList(data);
    } catch (e) {
      error = e instanceof Error ? e.message : '캐릭터 목록 실패';
    }
  }

  async function load() {
    loading = true;
    error = '';
    await loadWorld();
    if (world) await loadCharacters();
    loading = false;
  }

  async function addCharacter() {
    if (!newName.trim() || !world) return;
    creating = true;
    try {
      await characterCreate({ world: worldId, name: newName.trim() });
      newName = '';
      await loadCharacters();
    } catch (e) {
      error = e instanceof Error ? e.message : '캐릭터 생성 실패';
    } finally {
      creating = false;
    }
  }

  async function removeCharacter(c: Character) {
    if (!confirm(`"${c.name}" 캐릭터를 삭제할까요?`)) return;
    try {
      await characterDelete(c.id);
      await loadCharacters();
    } catch (e) {
      error = e instanceof Error ? e.message : '삭제 실패';
    }
  }

  onMount(load);
</script>

<svelte:head><title>{world?.name ?? '로딩'} — 에디터</title></svelte:head>

{#if loading}
  <p class="text-gray-500">불러오는 중…</p>
{:else if error || !world}
  <p class="text-red-600">{error || '세계관을 찾을 수 없습니다.'}</p>
{:else}
  <div class="space-y-6">
    <div class="rounded-lg border border-gray-200 bg-white p-4">
      <h2 class="text-lg font-medium">{world.name}</h2>
      {#if world.description}<p class="mt-1 text-sm text-gray-500">{world.description}</p>{/if}
      <p class="mt-2 text-sm"><a href="/editor" class="text-blue-600 underline">← 세계관 목록</a></p>
    </div>

    <div class="rounded-lg border border-gray-200 bg-white p-4">
      <h3 class="font-medium">캐릭터</h3>
      <form on:submit|preventDefault={addCharacter} class="mt-3 flex gap-2">
        <input type="text" bind:value={newName} class="flex-1 rounded border border-gray-300 px-3 py-2 text-sm" placeholder="캐릭터 이름" />
        <button type="submit" disabled={creating || !newName.trim()} class="rounded bg-blue-600 px-4 py-2 text-sm text-white hover:bg-blue-700 disabled:opacity-50">추가</button>
      </form>
      {#if characters.length === 0}
        <p class="mt-3 text-sm text-gray-500">캐릭터가 없습니다. 위에서 추가하세요.</p>
      {:else}
        <ul class="mt-3 space-y-2">
          {#each characters as c}
            <li class="flex items-center justify-between rounded border border-gray-100 bg-gray-50 px-3 py-2">
              <a href="/editor/{worldId}/character/{c.id}" class="font-medium text-blue-600 hover:underline">{c.name}</a>
              <button type="button" on:click={() => removeCharacter(c)} class="text-sm text-red-600 hover:underline">삭제</button>
            </li>
          {/each}
        </ul>
      {/if}
    </div>

    <div class="rounded-lg border border-gray-200 bg-white p-4">
      <h3 class="font-medium">관계도 (마인드맵)</h3>
      <p class="mt-1 text-sm text-gray-500">캐릭터를 선택해 관계를 편집할 수 있습니다.</p>
      <p class="mt-2"><a href="/editor/{worldId}/relations" class="text-blue-600 underline">관계도 편집 →</a></p>
    </div>
  </div>
{/if}

<p class="mt-6"><a href="/" class="text-sm text-blue-600 underline">← 메인</a></p>
