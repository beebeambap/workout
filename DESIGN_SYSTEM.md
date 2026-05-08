# 디자인 시스템 — 운동 기록기

현재 적용된 모든 시각적 요소·토큰·컴포넌트를 정리합니다.
디자인 고도화·리뉴얼 시 출발점으로 사용하세요.

소스: `index.html` 의 `<style>` 블록 (line 9~).

---

## 1. 디자인 토큰

### 1-1. CSS 변수 (palette 적용 대상)

`:root` 에서 정의되며 테마 변경 시 JS 가 일괄 교체.

| 변수 | 역할 | 기본값 (minimal-latte) |
|---|---|---|
| `--bg` | 페이지 배경 | `#efeae0` |
| `--panel` | 카드·패널 배경 | `#ffffff` |
| `--text` | 본문 텍스트 | `#2c2620` |
| `--muted` | 보조 텍스트·라벨·메타 | `#9c9285` |
| `--accent` | 주 강조 (버튼·테두리·통계 숫자) | `#6b5544` |
| `--accent-soft` | 강조 옅은 배경 (배지·hover) | `#e8dfd2` |
| `--border` | 1px 분할선·테두리 | `#ddd4c4` |
| `--danger` | 위험·삭제 (버튼만) | `#c04a3e` |
| `--ok` | 성공 (현재 거의 미사용) | `#5a8c5a` |
| `--ph` | placeholder·dimmed 배경 | `#f0ebe0` |
| `--shadow` | 패널·모달 기본 그림자 | `0 2px 8px rgba(40,30,20,0.06)` |
| `--radius` | 기본 둥근 모서리 | `10px` |

### 1-2. 3개 팔레트 (`PALETTES` in JS)

| ID | 이름 | 키 컬러 (`--accent`) | 분위기 |
|---|---|---|---|
| `minimal-latte` | 미니멀 라떼 (베이지) | `#6b5544` | 차분, 따뜻 |
| `cool-blue` | 쿨 블루 | `#2563eb` | 차가운, IT |
| `vivid-red` | 비비드 레드 | `#dc2626` | 강렬, 활동 |

테마 변경 시 위 11개 변수 전체가 동시에 바뀜.
`localStorage["workout.palette"]` 영속화.

### 1-3. 카테고리 색상 (`CAT_COLORS` in JS)

운동 부위별 고정 색상 (현재 캘린더 도트 제거 후 막대 차트·뱃지 일부에서만 사용).

| 카테고리 | 색상 |
|---|---|
| 가슴 | `#e57373` (살구빨강) |
| 등 | `#7986cb` (인디고) |
| 어깨 | `#81c784` (연그린) |
| 팔 | `#ff8a65` (오렌지) |
| 복부 | `#ffd54f` (옐로우) |
| 다리 | `#4db6ac` (틸) |
| 유산소 | `#f48fb1` (핑크) |
| 전신 | `#ba68c8` (퍼플) |
| 기타 / 빈 값 | `#90a4ae` (블루그레이) |

### 1-4. 상태 색상 (변수 외 직접 hex 사용)

| 용도 | 색상 |
|---|---|
| 동기화 정상 | `#4caf50` (status dot) |
| 동기화 진행 | `#ffc107` (pulsing) |
| 동기화 오류 | `#e53935` |
| 오프라인 | `#90a4ae` |
| 편집 중 배너 | bg `#fff7e6` / border `#f1c772` / text `#8a5a00` |
| seed 배지 | bg `#e6f4ea` / text `#2e7d32` |
| 시드 GIF placeholder | `var(--ph)` |

---

## 2. 타이포그래피

```css
font-family: -apple-system, BlinkMacSystemFont, "Segoe UI",
             "Noto Sans KR", "Apple SD Gothic Neo", sans-serif;
```

OS 시스템 글꼴. 한글은 노토 / 애플 SD 산돌 지정.

### 사이즈 스케일

| 용도 | px | 비고 |
|---|---|---|
| 통계 큰 숫자 (`.stat-num`) | **26** / 800 weight | accent 컬러 |
| 시트 헤더 제목 | 22 | bold |
| 페이지 헤더 / `h2` / 모달 큰 제목 | 18 | |
| 캘린더 월 라벨 | 17 / 700 | |
| 모달 `h3` | 16 | |
| status dot 옆 작은 X | 16 | |
| 본문 / 인풋 / 카드 이름 / 항목 컨트롤 | **14** | 기본 |
| 라벨 / 부제 / 사이드 정보 | 13 | muted |
| 힌트 / 메타 / 검색 결과 / 통계 라벨·작은 정보 | **12** | muted |
| 배지 / 통계 라벨 / 작은 메타 / status legend | **11** | |
| 캘린더 카테고리 텍스트 | 10 (모바일 9) | |
| src-badge / 시트 작은 글씨 | 9~10 | |

### Weight 사용

- **800**: 통계 큰 숫자, 시트 번호 칩
- **700**: 캘린더 날짜·월 라벨, 카드 강조, 시트 항목 이름
- **600**: 카드 이름, 종목 이름, settings 값, 닉네임
- **400**: 본문 기본
- italic: `name-en` (영문 원문)

---

## 3. 간격·반경·그림자

### Border Radius
| 값 | 사용처 |
|---|---|
| 6px | 작은 칩, status dot, 시트 번호 칩, 메모 input |
| 8px | 일반 인풋·버튼, 검색 결과 박스, 작은 모달 요소 |
| 10px | 패널·카드·shadowed box, 캘린더 셀 (8px) |
| 12px | 모달 |
| 14px | (welcome modal — 모달 내부) |
| 999px | pill·badge (완전 라운드) |

### Padding 패턴
- 인풋: `9px 10px`
- primary 버튼: `9px 16px`
- ghost 버튼: `8px 12px`
- pill: `4~5px 10~12px`
- 패널: `16px`
- 모달: `18px` (large `22~24px`, 모바일 `14px`)
- 카드 메타: `8px 10px`

### Gap 패턴
- 폼 row 사이: 10~12px
- 항목 grid: 8px 10px
- 통계 카드: 10px
- 캘린더 셀: 4px

### Shadow
- 기본 패널: `var(--shadow)` = `0 2px 8px rgba(40,30,20,0.06)` (테마별로 색조 조정됨)
- 모달: `0 12px 40px rgba(0,0,0,0.2)`
- 시트 페이지: `0 6px 24px rgba(0,0,0,0.08)`
- 환영 카드 hover: `0 4~6px 12~16px rgba(0,0,0,0.08)`

---

## 4. 레이아웃

### 컨테이너
```css
main { max-width: 1080px; margin: 0 auto; padding: 20px; }
```

### 헤더
- 우측에 (인증 영역 → 팔레트 select → nav 탭) 가로 정렬
- `flex-wrap: wrap` 으로 모바일에서 줄바꿈

### 그리드
- `.row { grid-template-columns: 1fr 1fr; gap: 12px; }` — 모바일 시 1열
- `.grid` (라이브러리/사전): `repeat(auto-fill, minmax(200px, 1fr))`
- `#dict-grid`, `#lib-grid`: `minmax(150px, 1fr)`, 모바일 720px 이하 → `repeat(3, 1fr)`
- `.cal-grid`: `repeat(7, 1fr)`
- `.monthly-stats`: `repeat(auto-fill, minmax(130px, 1fr))`

### 반응형 브레이크포인트
| 폭 | 변화 |
|---|---|
| ≤ 720px | 모달 padding 축소, 사전·라이브러리 카드 3열 강제, dict-detail 1열 |
| ≤ 640px | `.row` 1열, 캘린더 셀 축소 (`min-height 44px`), search-filters 1열, auth-pill 축소 |
| ≤ 480px | `.item` 컨트롤 폰트·패딩 추가 축소 |

---

## 5. 컴포넌트

### 5-1. 버튼

| 클래스 | 모양 | 용도 |
|---|---|---|
| `.primary` | accent bg, 흰 텍스트, 9×16, 8r | 주 액션 (저장·발송·미리보기) |
| `.ghost` | transparent, accent border, 8×12, 8r | 보조 액션 |
| `.danger` | transparent, danger border, 8×12, 8r | 삭제 |
| `.auth-btn` | accent bg, 6×14, 12px, **600 weight** | 헤더 작은 로그인 버튼 |
| `.edit-btn` | transparent, border muted, 4×8, 11px | 항목 컨트롤 (↑↓·편집·상세) |
| `nav button` | pill (border·999r·8×14), `.active` 시 accent fill | 탭 |
| `.subtab-btn` | 밑줄 underline, active 시 accent border | 기록 내역 서브탭 |
| `.calendar-nav button` | square 8r, 20px 글자 | ‹ 월 › 네비 |
| `.modal-close-x` | 절대 위치 우상단, 22px ×, 호버 시 ph bg | 모달 닫기 |
| `reminder-banner button.primary` / `.ghost` | 6×12, 6r, 12px | 배너 액션 |
| `.auth-logout-x` | 16px ×, 50% radius, opacity 0.7 | pill 내부 로그아웃 |

### 5-2. 폼 요소
```css
input, textarea, select {
  width: 100%; padding: 9px 10px;
  border: 1px solid var(--border); border-radius: 8px;
  font-size: 14px; background: #fff; color: var(--text);
}
textarea { min-height: 60px; resize: vertical; }
label { font-size: 13px; color: var(--muted); margin-bottom: 4px; }
```

`input[type="number"]` (항목 컨트롤): 60px 폭, 중앙 정렬, 모바일 54px.
검색 결과 dropdown: max-height 220px scrollable, border 8r.

### 5-3. 패널 / 카드

**`.panel`** — 기본 콘텐츠 컨테이너
```css
background: var(--panel); border: 1px solid var(--border);
border-radius: var(--radius); padding: 16px;
box-shadow: var(--shadow); margin-bottom: 16px;
```

**`.card`** — 라이브러리·사전 카드
- aspect-ratio 1/1 썸네일 + meta 8×10 padding
- hover: border accent, `translateY(-1px)`
- `.card .name` 14px 600, `.card .desc` 12px muted (2줄 클램프)

### 5-4. 배지 / Pill

| 클래스 | 스타일 | 용도 |
|---|---|---|
| `.badge` | accent-soft bg, 11px, 999r, ml 6px | 카운트 표시 |
| `.src-badge.local` | accent-soft + accent | 내 동작 마킹 |
| `.src-badge.seed` | `#e6f4ea` + `#2e7d32` (진그린) | 시드 동작 마킹 |
| `.dict-detail .chip` | accent-soft, 11px, 600, 999r | 사전 메타 |
| `.auth-pill` | accent-soft + accent, 999r, 양옆 4px / 좌 10px | 로그인 사용자 |
| `.auth-guest-pill` | ph bg + muted text, border 1px | 게스트 모드 |
| `.settings-mode-badge` | 3가지 변종 (guest / auth-on / auth-off), 12px, 700 | 설정 탭 모드 |

### 5-5. 모달

**구조**
```
.modal-bg (fixed, full screen, dim 0.45 alpha)
  └─ .modal (white, 12r, max-w 520px, padding 18px)
       ├─ .modal-close-x (절대 우상단)
       ├─ h3 (16px, mb 12)
       └─ .modal-actions (flex right, gap 8)
```

- 큰 변종: `.modal.modal-lg { max-width: 760px; padding: 22px 24px; }`
- 모바일 ≤ 720px: padding 축소
- 백드롭 클릭·ESC 로 닫기 (welcome modal 만 강제 선택)
- z-index: 모달 50, edit-modal (중첩) 60

**미리보기 이미지**: `.modal img.preview { max-height: 220px; object-fit: contain; bg ph; }`

### 5-6. 인증 UI (헤더 우측 영역)

3가지 상태:
1. **로그인 모드 + 미로그인** → `🔑 로그인` (auth-btn)
2. **게스트 모드 + 미로그인** → `👤 게스트` (auth-guest-pill)
3. **로그인됨** → `🟢 닉네임님 ×` (auth-pill)

`auth-status-dot` 4가지 상태:
| 상태 | 색 | 동작 |
|---|---|---|
| ok | `#4caf50` | 정적 |
| syncing | `#ffc107` | `pulse` 1.2s 무한 |
| error | `#e53935` | 정적 |
| offline | `#90a4ae` | 정적 |

### 5-7. 알림 배너 (`.reminder-banner`)
- bg `accent-soft`, border accent, 10r, padding 10×14
- 우측에 액션 버튼들 (small primary + ghost)
- 게스트 모드 → "💡 로그인 권장" 메시지
- Firebase 미설정 → "백업 권장" 메시지 (legacy)

### 5-8. 편집 배너 (`.editing-banner`)
- 노란 경고 톤: `#fff7e6` bg / `#f1c772` border / `#8a5a00` text
- 8r, padding 8×12, 13px
- "기존 루틴을 편집 중입니다" 안내

### 5-9. 탭 / 서브탭

**메인 탭 (`nav button`)**
- pill, 8×14 padding
- 비활성: transparent + border
- 활성: accent fill + 흰 텍스트

**서브탭 (`.subtab-btn`)**
- underline 스타일
- 비활성: muted, 활성: accent + 3px bottom border + 600 weight

---

## 6. 도메인 컴포넌트

### 6-1. 루틴 항목 (`.item`)
3행 grid:
```
┌────────┬──────────────────┐
│ [img]  │ name + desc      │
├────────┴──────────────────┤
│ ctrl: reps·sets·↑↓·삭제   │
├───────────────────────────┤
│ memo (dashed border, ph)  │
└───────────────────────────┘
```
- `grid-template-areas: "img meta" "ctrl ctrl" "memo memo"`
- `.ic-memo` — dashed 1px border / ph bg → focus 시 solid accent + 흰 bg

### 6-2. 캘린더 셀 (`.cal-day`)

기본 셀: `min-height 64px` (모바일 44px), border 1px, 8r, 패딩 6×5.

| 변형 클래스 | 효과 |
|---|---|
| `.has-workout` | 클릭 가능, hover 시 accent border |
| `.quick-start` | 클릭 가능 (빈 과거/오늘), hover 시 우상단 `+` |
| `.today` | 2px accent border |
| `.future` | opacity 0.45 + 비활성 |
| `.other-month` | ph bg + 0.35 opacity |
| `.lvl-1` ~ `.lvl-4` | accent 14% / 32% / 55% / 80% (color-mix) 배경 강도 |

`.lvl-3/4` 진한 배경에선 날짜·카테고리 텍스트 흰색 자동 반전.

**셀 내부 구조**:
- `.cal-day-num` — 12px 700, 모바일 10px
- `.cal-cats` — 10px 600, 카테고리 한글 이름 inline (`등·팔` 형식)

**히트맵 강도** — 동적/고정 임계값 자동 전환:
- 데이터 ≥ 20일: 일별 총 세트 수의 25/50/75 백분위
- 미만: 고정 (1~9, 10~19, 20~29, 30+)

### 6-3. 통계 카드 (`.stat-card`)
- 흰 bg, 1px border, 10r, 14×10 padding, 중앙 정렬
- `.stat-num` 26px 800 accent
- `.stat-num-sm` 15px (긴 텍스트용)
- `.stat-label` 11px muted, mt 6
- `.stat-card.streak` → 숫자 뒤 자동으로 "일" 접미사

### 6-4. 부위별 막대 차트 (`.cat-bars`)
- 흰 패널, 14px padding, 10r
- 각 행: 60px 라벨 / flex 트랙 / 32px 카운트
- 트랙: 10px 높이, ph bg, 5r
- 채움: 카테고리 색상, `transition: width 0.25s`

### 6-5. 설정 행 (`.settings-row`)
- flex space-between, 12px gap
- 행 사이 1px bottom border (마지막 제외)
- `.settings-label` — 11px uppercase muted, letterspacing 0.5
- `.settings-value` — 14px 600 text
- `.settings-mode-badge` — 3색 변종 pill

### 6-6. 시트 페이지 (`.sheet-page`) — JPG 출력용
- 폭 720px 고정, 패딩 28×24, 흰 bg, 그림자
- `.sheet-header` — accent 2px bottom border, 22px 타이틀
- `.sheet-grid[data-cols="1|2"]` — 1단/2단 항목 그리드
- `.sheet-item` — 32px 번호 / 110px 이미지 / flex 정보 / 70px 세트
  - 2단 시 컬럼·폰트 자동 축소
  - `.compact` 변형: 이미지 영역 생략
- `.si-num` — accent 800 텍스트, accent-soft bg, 6r, 중앙 정렬

### 6-7. 사전 카드·상세 (`.dict-card`, `.dict-detail`)
- 카드: 자연 비율 썸네일 (letterbox 없음)
- 상세: 데스크톱 320px+1fr 2열, 모바일 1열
- `.chip` (사전 메타): accent-soft pill
- `.summary` — ph bg 박스
- `.steps.en` — italic + muted (영문 원문)

### 6-8. 환영 모달 (welcome-modal)
- max-width 380px (작은 모달)
- 중앙 정렬 텍스트
- 세로 2버튼 스택 (gap 10): 큰 primary + 큰 ghost
- 14px font, 14×18 padding
- 닫기 차단 — 강제 선택

### 6-9. 인증 모달 (auth-modal)
- max-width 420px
- 이메일 input (한 줄) + status 메시지 + flex right 버튼

---

## 7. 애니메이션 / 전환

| 대상 | 효과 | 시간 |
|---|---|---|
| `.cal-day` hover (has-workout) | border-color → accent | 즉시 |
| `.cal-day.quick-start::before` (`+`) | opacity 0 → 1 | 0.12s |
| `.card` hover | translateY(-1px), border accent | 0.1s |
| `.welcome-choice` hover | translateY(-2px), shadow | 0.15s |
| `.cat-bar-fill` width | 데이터 변경 시 부드러운 채움 | 0.25s ease |
| `.auth-status-dot.syncing` | opacity 1 ↔ 0.4 펄스 | 1.2s 무한 |

---

## 8. 아이콘 사용

이모지 기반 (외부 아이콘 라이브러리 미사용):

| 이모지 | 용도 |
|---|---|
| 🔑 | 로그인 / 인증 |
| 👤 | 게스트 / 사용자 |
| 📅 | 캘린더 / 기록용 |
| 📋 | 시트 / 공유용 |
| 🏃 | 유산소 |
| 🔥 | 현재 streak |
| 🎨 | AI 프롬프트 |
| 💡 | 권장 알림 |
| ⚙ | 설정 탭 |
| ↑ ↓ | 항목 순서 변경 |
| × | 닫기 / 삭제 |
| ✓ | 저장 완료 |
| ‹ › | 월 네비 |
| · | 카테고리 구분자 |
| + | 빠른 시작 hover |

---

## 9. 일관성 규칙 (현재 적용된)

1. **모든 둥근 모서리는 `--radius`(10px) 또는 그 배수**
2. **accent 1색만 강조** — 보조 강조 없음, 배지·버튼 모두 accent 계열
3. **muted 텍스트는 13px 이하**, 본문은 14px
4. **flex-wrap 항상 켜둠** — 모바일 자동 줄바꿈
5. **inline style 최소화** — 색상·크기 변수만 사용 권장
6. **모달 z-index 50, 중첩 모달 60** 만 사용
7. **버튼 그룹은 flex gap 8px**, 우측 정렬은 `justify-content: flex-end`
8. **danger 색상은 삭제 버튼에만** — 다른 의미로 쓰지 않음

---

## 10. 알려진 비일관 / 개선 후보

리뉴얼 시 다듬을만한 지점:

- **inline `style="..."` 다수**: 원래 정의된 클래스로 흡수 가능
- **편집 배너의 노란 컬러**: `--warning` 변수가 없어 hex 직접 사용. 변수화 필요
- **`#e6f4ea` (seed 배지 그린)**: ok 의미인데 `--ok` 변수가 있는데도 미사용
- **카테고리 색상**: 현재 캘린더 도트 제거 후 막대 차트에서만 활용 → 통합 사용처 재정의
- **status dot 색상**: 변수가 아닌 hex 직접 → `--status-ok / syncing / error / offline` 변수로 통일 가능
- **버튼 크기 4단계** (primary/ghost/edit-btn/auth-btn) — `size` modifier 로 통일 가능
- **모바일 폰트 축소가 미디어 쿼리마다 산발적** — `--text-base` 같은 토큰화 가능
- **다크 모드 미지원** — color-mix 와 변수 구조는 이미 다크모드 친화적 (라이트 변수만 swap 하면 가능)

---

## 11. 참고 — 실제 사용 통계

코드 내 등장 빈도 기준 (대략):

| 토큰 | 사용처 |
|---|---|
| `var(--accent)` | 70+ 곳 (가장 많이) |
| `var(--border)` | 50+ 곳 (분할선) |
| `var(--muted)` | 40+ 곳 (보조 텍스트) |
| `var(--ph)` | 15+ 곳 (placeholder bg) |
| `var(--accent-soft)` | 20+ 곳 (호버·배지) |
| `var(--danger)` | 5 곳 (삭제 한정) |
| `var(--ok)` | 1 곳 (정의만, 사실상 미사용) |

---

이 문서는 `2026-05-08` 기준 `index.html` (8개월간 누적된 시각 시스템) 의 스냅샷입니다.
디자인 리뉴얼 / 컴포넌트 추출 / 다크 모드 추가 등의 베이스라인으로 사용하세요.
