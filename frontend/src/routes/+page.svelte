<script lang="ts">
  import { onMount } from 'svelte';
  import { worldsList, worldCreate, unwrapList, type World } from '$lib/api';

  let worlds: World[] = [];
  let loading = true;
  let error = '';
  let createName = '';
  let createDesc = '';
  let creating = false;

  async function load() {
    try {
      const data = await worldsList();
      worlds = unwrapList(data);
      error = '';
    } catch (e) {
      error = e instanceof Error ? e.message : 'API 연결 실패';
    } finally {
      loading = false;
    }
  }

  async function createWorld() {
    if (!createName.trim()) return;
    creating = true;
    try {
      await worldCreate({ name: createName.trim(), description: createDesc.trim() });
      createName = '';
      createDesc = '';
      await load();
    } catch (e) {
      error = e instanceof Error ? e.message : '생성 실패';
    } finally {
      creating = false;
    }
  }

  onMount(load);
</script>

<section class="rounded-lg border border-gray-200 bg-white p-6 shadow-sm">
  <h2 class="mb-4 text-lg font-medium">세계관 목록</h2>
  {#if loading}
    <p class="text-gray-500">불러오는 중…</p>
  {:else if error}
    <p class="text-red-600">{error}</p>
    <p class="mt-2 text-sm text-gray-500">백엔드가 실행 중인지 확인하세요.</p>
  {:else if worlds.length === 0}
    <p class="text-gray-500">등록된 세계관이 없습니다. 아래에서 새로 만드세요.</p>
  {:else}
    <ul class="space-y-2">
      {#each worlds as w}
        <li class="flex items-center gap-2">
          <a href="/editor/{w.id}" class="font-medium text-blue-600 hover:underline">{w.name}</a>
          <span class="text-gray-400">(id: {w.id})</span>
        </li>
      {/each}
    </ul>
  {/if}
</section>

<section class="mt-6 rounded-lg border border-gray-200 bg-white p-6 shadow-sm">
  <h3 class="mb-3 text-sm font-medium text-gray-700">세계관 추가</h3>
  <form on:submit|preventDefault={createWorld} class="flex flex-col gap-3 sm:flex-row sm:items-end">
    <div class="flex-1">
      <label for="world-name" class="block text-xs text-gray-500">이름</label>
      <input id="world-name" type="text" bind:value={createName} class="mt-0.5 w-full rounded border border-gray-300 px-3 py-2 text-sm" placeholder="예: 에버그린데일" />
    </div>
    <div class="flex-1">
      <label for="world-desc" class="block text-xs text-gray-500">설명 (선택)</label>
      <input id="world-desc" type="text" bind:value={createDesc} class="mt-0.5 w-full rounded border border-gray-300 px-3 py-2 text-sm" placeholder="간단한 설명" />
    </div>
    <button type="submit" disabled={creating || !createName.trim()} class="rounded bg-blue-600 px-4 py-2 text-sm font-medium text-white hover:bg-blue-700 disabled:opacity-50">
      {creating ? '생성 중…' : '추가'}
    </button>
  </form>
</section>

<nav class="mt-6 flex gap-4 text-sm">
  <a href="/editor" class="text-blue-600 underline">에디터</a>
  <a href="/play" class="text-blue-600 underline">플레이</a>
</nav>
