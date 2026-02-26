/**
 * 백엔드 API 클라이언트 (DRF)
 */
const getBase = () => (typeof window !== 'undefined' ? import.meta.env.PUBLIC_API_URL : '') || 'http://localhost:8000';

export function apiBase(): string {
  return getBase();
}

export async function api<T>(path: string, init?: RequestInit): Promise<T> {
  const res = await fetch(`${getBase()}${path}`, {
    headers: { 'Content-Type': 'application/json', ...init?.headers },
    ...init,
  });
  if (!res.ok) {
    const text = await res.text();
    throw new Error(text || `HTTP ${res.status}`);
  }
  if (res.status === 204) return undefined as T;
  return res.json();
}

// --- Worlds ---
export interface World {
  id: number;
  name: string;
  description: string;
  characters?: { id: number; name: string }[];
  created_at: string;
  updated_at: string;
}

export interface Paginated<T> {
  count: number;
  next: string | null;
  previous: string | null;
  results: T[];
}

export function worldsList(): Promise<Paginated<World> | World[]> {
  return api<Paginated<World> | World[]>(`/api/worlds/`);
}

export function worldCreate(data: { name: string; description?: string }): Promise<World> {
  return api<World>(`/api/worlds/`, { method: 'POST', body: JSON.stringify(data) });
}

export function worldGet(id: number): Promise<World> {
  return api<World>(`/api/worlds/${id}/`);
}

export function worldUpdate(id: number, data: Partial<World>): Promise<World> {
  return api<World>(`/api/worlds/${id}/`, { method: 'PATCH', body: JSON.stringify(data) });
}

export function worldDelete(id: number): Promise<void> {
  return api<void>(`/api/worlds/${id}/`, { method: 'DELETE' });
}

// --- Characters ---
export interface Character {
  id: number;
  world: number;
  name: string;
  stats: Record<string, number>;
  metadata: Record<string, unknown>;
  skills?: { id: number; name: string; mana_cost: number; system_effect: string }[];
  source_relations?: { id: number; target_character: number; target_character_name: string; relation_type: string; weight: number }[];
  created_at: string;
}

export function charactersList(worldId?: number): Promise<Paginated<Character> | Character[]> {
  const q = worldId != null ? `?world=${worldId}` : '';
  return api<Paginated<Character> | Character[]>(`/api/characters/${q}`);
}

export function characterCreate(data: { world: number; name: string; stats?: Record<string, number>; metadata?: Record<string, unknown> }): Promise<Character> {
  return api<Character>(`/api/characters/`, { method: 'POST', body: JSON.stringify(data) });
}

export function characterGet(id: number): Promise<Character> {
  return api<Character>(`/api/characters/${id}/`);
}

export function characterUpdate(id: number, data: Partial<Character>): Promise<Character> {
  return api<Character>(`/api/characters/${id}/`, { method: 'PATCH', body: JSON.stringify(data) });
}

export function characterDelete(id: number): Promise<void> {
  return api<void>(`/api/characters/${id}/`, { method: 'DELETE' });
}

// --- Relationships ---
export interface Relationship {
  id: number;
  source_character: number;
  target_character: number;
  target_character_name?: string;
  relation_type: string;
  weight: number;
}

export function relationshipsList(): Promise<Paginated<Relationship> | Relationship[]> {
  return api<Paginated<Relationship> | Relationship[]>(`/api/relationships/`);
}

export function relationshipCreate(data: { source_character: number; target_character: number; relation_type: string; weight?: number }): Promise<Relationship> {
  return api<Relationship>(`/api/relationships/`, { method: 'POST', body: JSON.stringify(data) });
}

export function relationshipDelete(id: number): Promise<void> {
  return api<void>(`/api/relationships/${id}/`, { method: 'DELETE' });
}

// --- Skills ---
export interface Skill {
  id: number;
  character: number;
  name: string;
  mana_cost: number;
  system_effect: string;
}

export function skillsList(characterId?: number): Promise<Paginated<Skill> | Skill[]> {
  const q = characterId != null ? `?character=${characterId}` : '';
  return api<Paginated<Skill> | Skill[]>(`/api/skills/${q}`);
}

export function skillCreate(data: { character: number; name: string; mana_cost?: number; system_effect: string }): Promise<Skill> {
  return api<Skill>(`/api/skills/`, { method: 'POST', body: JSON.stringify(data) });
}

export function skillUpdate(id: number, data: Partial<Skill>): Promise<Skill> {
  return api<Skill>(`/api/skills/${id}/`, { method: 'PATCH', body: JSON.stringify(data) });
}

export function skillDelete(id: number): Promise<void> {
  return api<void>(`/api/skills/${id}/`, { method: 'DELETE' });
}

/** DRF pagination 결과에서 results 또는 배열 자체 반환 */
export function unwrapList<T>(data: Paginated<T> | T[]): T[] {
  return Array.isArray(data) ? data : (data as Paginated<T>).results ?? [];
}
