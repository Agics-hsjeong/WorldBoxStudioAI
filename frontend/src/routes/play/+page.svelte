<script lang="ts">
  import { onMount } from 'svelte';
  import { worldsList, charactersList, unwrapList, type World, type Character } from '$lib/api';

  let worlds: World[] = [];
  let characters: Character[] = [];
  let selectedWorldId = '';
  let selectedCharId = '';
  let loading = true;
  let error = '';
  let messages: { role: 'user' | 'assistant'; text: string }[] = [];
  let inputText = '';
  let sending = false;

  async function loadWorlds() {
    try {
      const data = await worldsList();
      worlds = unwrapList(data);
    } catch (e) {
      error = e instanceof Error ? e.message : 'API 연결 실패';
    } finally {
      loading = false;
    }
  }

  async function onWorldChange() {
    selectedCharId = '';
    characters = [];
    if (!selectedWorldId) return;
    try {
      const data = await charactersList(parseInt(selectedWorldId, 10));
      characters = unwrapList(data);
    } catch (e) {
      error = e instanceof Error ? e.message : '캐릭터 목록 실패';
    }
  }

  function canChat(): boolean {
    return !!selectedWorldId && !!selectedCharId && !sending;
  }

  async function sendMessage() {
    if (!inputText.trim() || !canChat()) return;
    const text = inputText.trim();
    inputText = '';
    messages = [...messages, { role: 'user', text }];
    sending = true;
    try {
      // TODO: 백엔드 채팅 API 연동 (시스템 프롬프트 + LLM)
      await new Promise((r) => setTimeout(r, 500));
      messages = [...messages, { role: 'assistant', text: `(채팅 API 미연동) "${text}" 에 대한 응답이 여기 표시됩니다. 백엔드 채팅·LLM 연동 후 실제 대화가 가능합니다.` }];
    } catch (e) {
      messages = [...messages, { role: 'assistant', text: `오류: ${e instanceof Error ? e.message : '전송 실패'}` }];
    } finally {
      sending = false;
    }
  }

  onMount(loadWorlds);
</script>

<svelte:head><title>플레이 — WorldBox Studio AI</title></svelte:head>

<div class="space-y-6">
  <div class="rounded-lg border border-gray-200 bg-white p-4">
    <h2 class="text-lg font-medium">플레이</h2>
    <p class="mt-1 text-sm text-gray-500">세계관과 캐릭터를 고른 뒤 대화를 시작하세요. (채팅 API·LLM 연동은 추후)</p>

    {#if loading}
      <p class="mt-3 text-gray-500">불러오는 중…</p>
    {:else}
      <div class="mt-4 flex flex-wrap gap-4">
        <div>
          <label class="block text-xs text-gray-500">세계관</label>
          <select bind:value={selectedWorldId} on:change={onWorldChange} class="mt-0.5 rounded border border-gray-300 px-3 py-2 text-sm">
            <option value="">선택</option>
            {#each worlds as w}
              <option value={w.id}>{w.name}</option>
            {/each}
          </select>
        </div>
        <div>
          <label class="block text-xs text-gray-500">캐릭터</label>
          <select bind:value={selectedCharId} class="mt-0.5 rounded border border-gray-300 px-3 py-2 text-sm" disabled={!selectedWorldId}>
            <option value="">선택</option>
            {#each characters as c}
              <option value={c.id}>{c.name}</option>
            {/each}
          </select>
        </div>
      </div>
    {/if}
  </div>

  {#if selectedWorldId && selectedCharId}
    <div class="rounded-lg border border-gray-200 bg-white p-4">
      <h3 class="font-medium">대화</h3>
      <div class="mt-3 flex h-64 flex-col overflow-y-auto rounded border border-gray-200 bg-gray-50 p-3">
        {#if messages.length === 0}
          <p class="text-sm text-gray-500">메시지를 입력해 대화를 시작하세요.</p>
        {:else}
          {#each messages as msg}
            <div class="mb-2 flex {msg.role === 'user' ? 'justify-end' : 'justify-start'}">
              <span class="max-w-[80%] rounded px-3 py-2 text-sm {msg.role === 'user' ? 'bg-blue-600 text-white' : 'bg-white border border-gray-200'}">{msg.text}</span>
            </div>
          {/each}
        {/if}
      </div>
      <form on:submit|preventDefault={sendMessage} class="mt-3 flex gap-2">
        <input type="text" bind:value={inputText} placeholder="메시지 입력…" class="flex-1 rounded border border-gray-300 px-3 py-2 text-sm" />
        <button type="submit" disabled={!canChat()} class="rounded bg-blue-600 px-4 py-2 text-sm text-white hover:bg-blue-700 disabled:opacity-50">전송</button>
      </form>
    </div>
  {/if}
</div>

<p class="mt-6"><a href="/" class="text-sm text-blue-600 underline">← 메인</a></p>
