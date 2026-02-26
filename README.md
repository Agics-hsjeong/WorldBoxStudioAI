# WorldBox Studio AI

세계관(World) 단위의 **인터랙티브 AI 샌드박스** 플랫폼. 노코드로 캐릭터·관계도를 만들고, TRPG형 채팅으로 몰입형 롤플레잉을 제공합니다.

- **기획·기술 문서**: `docs/` (기획 사양서, 기술 스택 및 아키텍처)
- **규칙**: `.cursorrules`, `.cursor/rules/`

---

## 기술 스택

| 구분 | 스택 |
|------|------|
| 프론트 | SvelteKit, Tailwind CSS, (마인드맵: Svelvet 예정) |
| 백엔드 | Django, Django REST Framework |
| DB | PostgreSQL, MinIO |
| AI | LangChain, ChromaDB, LLM (추후) |
| 배포 | Docker, Docker Compose |

---

## 로컬에서 실행

### 1. Docker Compose로 한 번에 띄우기

프로젝트 루트에 **`.env`** 파일을 만들고, 아래 **환경 변수(.env 구조)** 섹션을 참고해 변수를 채운 뒤:

```bash
docker compose up -d
```

**접속 주소** (`.env` 의 `HOST_PUBLIC` / `HOST_LAN` 과 각 `*_PORT` 로 결정)  
- **백엔드 API**: `http://<호스트>:<BACKEND_PORT>`  
- **API 문서(DRF)**: `http://<호스트>:<BACKEND_PORT>/api/`  
- **Django Admin**: `http://<호스트>:<BACKEND_PORT>/admin/` (슈퍼유저 생성 필요)  
- **프론트**: `http://<호스트>:<FRONTEND_PORT>`  
- **MinIO API**: `http://<호스트>:<MINIO_API_PORT>` · **MinIO 콘솔**: `http://<호스트>:<MINIO_CONSOLE_PORT>`  

PostgreSQL는 **Docker 네트워크 내부 전용**이라 호스트에는 포트를 노출하지 않음. 백엔드 컨테이너가 `postgres:5432` 로 접속.

### 2. 백엔드만 로컬에서 실행 (DB는 Docker)

PostgreSQL는 기본적으로 호스트에 포트를 노출하지 않는다. 로컬에서 백엔드를 돌리려면 **docker-compose.yml** 의 `postgres` 서비스에 `ports: - "<POSTGRES_PORT>:5432"` 를 추가한 뒤, `DATABASE_URL=postgres://...@localhost:<POSTGRES_PORT>/worldbox` 로 접속하거나, 백엔드도 컨테이너로 실행하면 된다.

### 3. 프론트엔드만 로컬에서 실행

```bash
cd frontend
npm install
npm run dev
```

`PUBLIC_API_URL` 은 `.env` 에서 읽음 (예: `http://<HOST_PUBLIC>:<BACKEND_PORT>`).

---

## 환경 변수 (.env 구조)

프로젝트 루트에 **`.env`** 파일을 만들고 아래 변수를 채운다. `.env` 는 `.gitignore` 대상이다.

| 구분 | 변수 | 설명 |
|------|------|------|
| **호스트** | `HOST_PUBLIC` | 공인 IP |
| | `HOST_LAN` | LAN IP |
| **포트** | `POSTGRES_PORT` | (선택) 호스트에서 PostgreSQL 직접 접속할 때만 사용. 기본은 Docker 네트워크 내부 전용 |
| | `MINIO_API_PORT` | MinIO API 포트 |
| | `MINIO_CONSOLE_PORT` | MinIO 콘솔 포트 |
| | `BACKEND_PORT` | 백엔드 포트 |
| | `FRONTEND_PORT` | 프론트 포트 |
| **프론트→백엔드** | `PUBLIC_API_URL` | 브라우저가 호출할 API URL (예: `http://<HOST_PUBLIC>:<BACKEND_PORT>`) |
| **Django** | `DJANGO_SECRET_KEY` | 시크릿 키 |
| | `ALLOWED_HOSTS` | 허용 호스트 (쉼표 구분: localhost, 127.0.0.1, 본인 IP 등) |
| | `CORS_ORIGINS` | CORS 허용 오리진 (쉼표 구분: 프론트 접속 URL) |
| **PostgreSQL** | `POSTGRES_USER`, `POSTGRES_PASSWORD`, `POSTGRES_DB` | DB 계정·DB명 |
| **MinIO** | `MINIO_ROOT_USER`, `MINIO_ROOT_PASSWORD` | MinIO 계정 |
| **LLM (선택)** | `OPENAI_API_KEY`, `GEMINI_API_KEY` | 추후 RAG/채팅 연동 시 |

---

## 프로젝트 구조

```
├── backend/          # Django + DRF
│   ├── config/       # 설정
│   └── worlds/       # 세계관·캐릭터·관계·스킬 앱
├── frontend/         # SvelteKit + Tailwind
│   └── src/routes/   # /, /editor, /play
├── docs/             # 기획서, 기술 아키텍처
├── docker-compose.yml
└── .env              # 환경 변수 (직접 생성, .gitignore 대상)
```

---

## API 엔드포인트 (예시)

| 메서드 | 경로 | 설명 |
|--------|------|------|
| GET/POST | /api/worlds/ | 세계관 목록·생성 |
| GET/PUT/DELETE | /api/worlds/:id/ | 세계관 상세 |
| GET/POST | /api/characters/?world=:id | 캐릭터 목록·생성 |
| GET/POST | /api/relationships/ | 관계 목록·생성 |
| GET/POST | /api/skills/ | 스킬 목록·생성 |

---

## 다음 단계 (기획·기술 문서 기준)

- [x] 메인: 세계관 목록·추가
- [x] 에디터: 세계관 선택 → 캐릭터 목록·추가·삭제 → 캐릭터 편집 (이름, 스탯 JSON, 메타데이터 JSON, 스킬 CRUD)
- [x] 에디터: 관계도 (캐릭터 간 관계 유형·강도 추가/삭제)
- [x] 플레이: 세계관·캐릭터 선택, 채팅 UI (전송/표시)
- [ ] 채팅 API·LLM 연동 (`worlds/services.build_system_prompt` + 백엔드 채팅 엔드포인트)
- [ ] @멘션, 스킬 버튼, TRPG GM 로직
- [ ] 마인드맵 캔버스(Svelvet) 시각화
- [ ] RAG(ChromaDB), 장기 기억
- [ ] PWA·반응형
