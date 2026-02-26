<script lang="ts">
  import { onMount } from 'svelte';
  import { worldsList, unwrapList, type World } from '$lib/api';

  let worlds: World[] = [];
  let loading = true;
  let error = '';

  onMount(async () => {
    try {
      const data = await worldsList();
      worlds = unwrapList(data);
    } catch (e) {
      error = e instanceof Error ? e.message : 'API 연결 실패';
    } finally {
      loading = false;
    }
  });
</script>

<svelte:head><title>에디터 — WorldBox Studio AI</title></svelte:head>

<div class="rounded-lg border border-gray-200 bg-white p-6">
  <h2 class="text-lg font-medium">에디터</h2>
  <p class="mt-1 text-sm text-gray-500">세계관을 고르면 캐릭터·관계도를 편집할 수 있습니다.</p>

  {#if loading}
    <p class="mt-4 text-gray-500">불러오는 중…</p>
  {:else if error}
    <p class="mt-4 text-red-600">{error}</p>
  {:else if worlds.length === 0}
    <p class="mt-4 text-gray-500">세계관이 없습니다. <a href="/" class="text-blue-600 underline">메인</a>에서 먼저 세계관을 만드세요.</p>
  {:else}
    <ul class="mt-4 space-y-2">
      {#each worlds as w}
        <li>
          <a href="/editor/{w.id}" class="font-medium text-blue-600 hover:underline">{w.name}</a>
          {#if w.description}<span class="ml-2 text-gray-500">— {w.description}</span>{/if}
        </li>
      {/each}
    </ul>
  {/if}
</div>

<p class="mt-4"><a href="/" class="text-sm text-blue-600 underline">← 메인</a></p>
