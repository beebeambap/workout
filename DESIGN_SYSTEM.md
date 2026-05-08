# 디자인 시스템 — 운동 기록기

현재 적용된 모든 시각적 요소·토큰·컴포넌트를 정리합니다.
디자인 고도화·리뉴얼 시 참고.

소스: `index.html` 의 `<style>` 블록 (line 9~).
업데이트: 2026-05-08 (패키지 X+Y+Z 정리 후, OKLCH·다크모드·eyebrow·대시보드 반영)

---

## 1. 디자인 토큰

### 1-1. CSS 변수 (팔레트 적용 대상)

`:root` 에서 정의되며 테마 변경 시 JS 가 일괄 교체.

| 변수 | 역할 | 기본값 (minimal-latte) |
|---|---|---|
| `--bg` | 페이지 배경 | `#efeae0` |
| `--panel` | 카드·패널·모달 배경 | `#ffffff` |
| `--text` | 본문 텍스트 | `#2c2620` |
| `--muted` | 보조 텍스트·라벨·메타 | `#9c9285` |
| `--accent` | 주 강조 (버튼·테두리·통계 숫자) | `#6b5544` |
| `--accent-soft` | 강조 옅은 배경 (배지·hover) | `#e8dfd2` |
| `--border` | 1px 분할선·테두리 | `#ddd4c4` |
| `--danger` | 위험·삭제 (테두리/색상) | `#c04a3e` |
| `--ok` | 정의되어 있으나 미사용 | `#5a8c5a` |
| `--ph` | placeholder·dimmed 배경 | `#f0ebe0` |
| `--shadow` | 패널·모달 기본 그림자 | `0 2px 8px rgba(40,30,20,0.06)` |
| `--radius` | 기본 둥근 모서리 | `10px` |

### 1-2. 의미 색상 토큰 (OKLCH, 모든 팔레트 공통)

라이트 / 다크에서 명도만 보정해 동일 의미 유지.

| 토큰 | 라이트 | 다크 (lift) | 용도 |
|---|---|---|---|
| `--success` | `oklch(50% 0.13 150)` | `oklch(72% 0.14 150)` | (현재 미사용 — `--ok` 대체 후보) |
| `--success-soft` | `oklch(94% 0.04 150)` | `oklch(28% 0.06 150)` | success bg 옅은 톤 |
| `--warning` | `oklch(58% 0.13 75)` | `oklch(76% 0.14 80)` | 편집 중 배너 border, auth-off 모드 배지 border |
| `--warning-soft` | `oklch(94% 0.05 80)` | `oklch(28% 0.07 75)` | 편집 배너 bg, auth-off 배지 bg |
| `--warning-ink` | `oklch(35% 0.10 70)` | `oklch(86% 0.10 80)` | warning 텍스트 |
| `--info` | `oklch(52% 0.12 245)` | `oklch(72% 0.13 245)` | seed 출처 배지 |
| `--info-soft` | `oklch(94% 0.03 250)` | `oklch(28% 0.06 245)` | seed 배지 bg |

### 1-3. 상태 dot 토큰 (인증·동기화)

| 토큰 | 라이트 | 다크 |
|---|---|---|
| `--status-ok` | `oklch(63% 0.16 150)` | `oklch(72% 0.16 150)` |
| `--status-syncing` | `oklch(82% 0.18 90)` | `oklch(82% 0.18 90)` |
| `--status-error` | `oklch(58% 0.21 28)` | `oklch(70% 0.20 28)` |
| `--status-offline` | `oklch(67% 0.04 220)` | `oklch(58% 0.04 220)` |

### 1-4. 간격·폰트 스케일 (Y 패키지에서 도입)

| 토큰 | 값 | 용도 |
|---|---|---|
| `--space-1` | 4px | 미세 gap |
| `--space-2` | 8px | 행 간격 |
| `--space-3` | 12px | 패널 내 섹션 |
| `--space-4` | 16px | 패널 padding |
| `--space-5` | 24px | nav gap |
| `--space-6` | 32px | 큰 분할 |
| `--text-xs` | 11px | 배지·meta |
| `--text-sm` | 12px | 힌트·라벨 |
| `--text-base` | 14px | 본문 |
| `--text-md` | 15px | h2 sub |
| `--text-lg` | 17px | 캘린더 월 라벨 |
| `--text-xl` | 22px | 시트 제목 |
| `--text-2xl` | 26px | stat 큰 숫자 |

> **주의**: 토큰은 정의되었으나 기존 hardcoded 값은 점진 마이그레이션. 새 컴포넌트에서 우선 사용.

---

## 2. 4개 팔레트

| ID | 이름 | 키 컬러 (`--accent`) | 분위기 |
|---|---|---|---|
| `minimal-latte` | 미니멀 라떼 (베이지) | `#6b5544` | 차분, 따뜻 — 기본 |
| `cool-blue` | 쿨 블루 | `#2563eb` | 차가운, IT |
| `vivid-red` | 비비드 레드 | `#dc2626` | 강렬, 활동 |
| `dark` | 🌙 다크 (야간 모드) | `oklch(72% 0.04 60)` | 야간 헬스장 / OS 다크 자동 감지 |

**자동 감지**: 첫 방문 시 `prefers-color-scheme: dark` 면 다크 자동. 이후 사용자 명시 선택 우선.

**OS 테마 변경 감지**: 사용자가 명시 선택 안 했을 때만 OS 변경 따라감.

**저장**: `localStorage["workout.palette"]` 영속화.

---

## 3. 카테고리 색상 (`CAT_COLORS`)

운동 부위별 고정 색상 — OKLCH 인코딩으로 다크 모드에서도 채도 일정.

| 카테고리 | OKLCH | 톤 |
|---|---|---|
| 가슴 | `oklch(70% 0.13 25)` | 살구빨강 |
| 등 | `oklch(64% 0.11 268)` | 인디고 |
| 어깨 | `oklch(76% 0.13 145)` | 연그린 |
| 팔 | `oklch(74% 0.14 50)` | 오렌지 |
| 복부 | `oklch(86% 0.16 92)` | 옐로우 |
| 다리 | `oklch(72% 0.10 195)` | 틸 |
| 유산소 | `oklch(75% 0.10 350)` | 핑크 |
| 전신 | `oklch(66% 0.13 310)` | 퍼플 |
| 기타 / 빈 값 | `oklch(70% 0.025 245)` | 블루그레이 |

**사용처**: `categoryBadge(cat)` 헬퍼 (라이브러리 카드, 기록 행, day-detail 모달, 부위별 막대 차트).

```js
function categoryBadge(cat) {
  if (!cat) return "";
  const c = CAT_COLORS[cat] || CAT_COLORS["기타"];
  return `<span class="badge" style="background:color-mix(in srgb, ${c} 22%, transparent);color:${c};">${escapeHtml(cat)}</span>`;
}
```

---

## 4. 타이포그래피

```css
font-family: -apple-system, BlinkMacSystemFont, "Segoe UI",
             "Noto Sans KR", "Apple SD Gothic Neo", sans-serif;
```

OS 시스템 글꼴. monospace 는 `ui-monospace, SFMono-Regular, "JetBrains Mono", Menlo, monospace`.

### 사이즈 사용표

| 토큰 | px | 사용처 |
|---|---|---|
| `--text-2xl` | 26 / 800 | stat 큰 숫자 |
| `--text-xl` | 22 / bold | 시트 헤더 제목 |
| h2 | 18 / 600 | 페이지·패널 헤더 |
| `--text-lg` | 17 / 700 | 캘린더 월 라벨 |
| h3 / 모달 | 16 | 모달 제목 |
| `--text-base` | 14 | 본문, 인풋, 카드 이름, primary 버튼 |
| 13 | 13 | 라벨, 부제, sheet description |
| `--text-sm` | 12 | 힌트, 메타, 검색 결과, 버튼 sm |
| `--text-xs` | 11 | 배지, 통계 라벨, 버튼 xs |
| 10 / 9 | 10·9 | 캘린더 카테고리 라벨, 시트 작은 글씨 |

### Weight

- **800**: stat-num
- **700**: 캘린더 일자, 카드 강조, 시트 항목 이름
- **600**: 카드·종목 이름, settings 값, 닉네임
- **500**: 본문 강조, 메인 nav 비활성, eyebrow
- **400**: 본문 기본
- italic: `name-en` (영문 원문)

### 숫자 정렬

`font-variant-numeric: tabular-nums` 적용 위치:
- `.stat-num`
- `.cal-day-num`
- `.si-num` (sheet 번호)
- `.badge`
- `.cat-bar-count`
- `.auth-email`
- `input[type="number"]`

---

## 5. 컴포넌트

### 5-1. 버튼

| 클래스 | 모양 | 용도 |
|---|---|---|
| `.primary` | accent fill, 흰 텍스트, 9×16, 8r | 주 액션 |
| `.ghost` | transparent, accent border, 8×12, 8r | 보조 액션 |
| `.danger` | transparent, danger border, 8×12, 8r | 삭제 |
| `.btn-sm` | size 모디파이어 (12px, 6×12) | 작은 버튼 |
| `.btn-xs` | size 모디파이어 (11px, 4×10) | 더 작은 버튼 |
| `.auth-btn` | accent fill, 6×14, 12px, 600 | 헤더 작은 로그인 |
| `.edit-btn` | transparent border, 4×8, 11px | 항목 컨트롤 |
| `nav button` | underline 활성, 14px, 500/600 | 메인 탭 |
| `.subtab-btn` | underline 활성, 14px | 기록 내역 서브탭 |

**조합 사용**: `<button class="ghost btn-xs">` — variant + size

### 5-2. 폼 요소

```css
input, textarea, select {
  width: 100%; padding: 9px 10px;
  border: 1px solid var(--border); border-radius: 8px;
  font-size: 14px; background: var(--panel); color: var(--text);
}
```

`.search-input { max-width: 320px; }` — 라이브러리·기록·사전 toolbar 검색 통일.

### 5-3. 패널 / 카드

**`.panel`** — 기본 콘텐츠 컨테이너
```css
background: var(--panel); border: 1px solid var(--border);
border-radius: var(--radius); padding: 16px;
box-shadow: var(--shadow); margin-bottom: 16px;
```

**`.card`** — 라이브러리·사전 카드
- thumb: aspect-ratio 1/1, **흰색 배경 (#fff)** — 사용자 업로드 흰배경 이미지와 일체감
- meta: 8×10 padding
- hover: border accent, `translateY(-1px)`

### 5-4. Eyebrow (편집 디자인 작은 라벨)

```css
.eyebrow {
  font-family: ui-monospace, ...;
  font-size: 11px; letter-spacing: 0.16em;
  text-transform: uppercase; color: var(--muted);
  font-weight: 500;
  display: flex; align-items: center; gap: 8px;
  margin: 0 0 8px;
}
.eyebrow::before {
  content: ""; display: inline-block; width: 18px; height: 1px;
  background: var(--muted); opacity: 0.5;
}
.eyebrow.eyebrow-plain::before { display: none; }
```

**적용처** — 11개 패널 헤더 + 대시보드 + 검색 섹션:
- `UPLOAD` / `LIBRARY` / `ROUTINE INFO` / `ADD MOVES` / `ITEMS`
- `SHARED ROUTINES` / `PREVIEW · JPG EXPORT` / `DICTIONARY · 1,324 MOVES`
- `ACCOUNT · MODE` / `PROFILE` / `DATA · BACKUP / RESTORE`
- 대시보드 블록: `13주 활동`, `주간 볼륨 (총 세트)` (eyebrow-plain 변형)
- 검색 결과 dropdown: `최근 사용` (`.search-section-header` 별도 클래스, 동일 톤)

### 5-5. 배지 / Pill

| 클래스 | 스타일 | 용도 |
|---|---|---|
| `.badge` | accent-soft bg, 11px, 999r | 카운트 |
| `categoryBadge()` | CAT_COLORS 22% bg + 색상 텍스트 | 부위 표시 |
| `.src-badge.local` | accent-soft + accent | 내 동작 |
| `.src-badge.seed` | **info-soft + info** (코발트 톤) | 시드 동작 |
| `.dict-detail .chip` | accent-soft, 11px, 600, 999r | 사전 메타 |
| `.auth-pill` | accent-soft + accent, 999r | 로그인 사용자 |
| `.auth-guest-pill` | ph + muted, 999r | 게스트 모드 |
| `.settings-mode-badge` | 3 변종 (guest / auth-on / auth-off) | 설정 탭 모드 |

### 5-6. 모달

```
.modal-bg (fixed full screen, 0.45 dim, z-50)
  └─ .modal (var(--panel) bg, 12r, max-w 520, padding 18)
       ├─ .modal-close-x (절대 우상단 ×)
       ├─ h3 (16px, mb 12)
       └─ content
```

- 큰 변종: `.modal.modal-lg` (max-w 760)
- z-index: 50 / 중첩 모달 60 (edit-modal)
- 백드롭·ESC 로 닫기 (welcome modal 만 강제 선택)
- **이미지**: `.modal img.preview` 와 `.dict-detail-img` 모두 **흰바탕 (#fff)** — 카드 thumb 와 일관

### 5-7. 인증 UI (헤더 우측 영역)

3가지 상태:
1. **로그인 모드 + 미로그인** → `🔑 로그인` (auth-btn)
2. **게스트 모드 + 미로그인** → `👤 게스트` (auth-guest-pill)
3. **로그인됨** → `🟢 닉네임님 ×` (auth-pill, 닉네임 없으면 이메일 prefix)

`auth-status-dot` — pulse 애니메이션으로 sync 진행 표시.

### 5-8. 알림 배너 (`.reminder-banner`)
- bg `accent-soft`, border accent, 10r
- 게스트 모드 → "💡 로그인 권장" + `🔑 로그인` 버튼
- 로그인됨 → 숨김 (자동 동기화가 처리)
- Firebase 미설정 → 기존 백업 권장 (legacy)

### 5-9. 편집 배너 (`.editing-banner`)
- bg `var(--warning-soft)` / border `var(--warning)` / text `var(--warning-ink)`
- 8r, padding 8×12, 13px
- "기존 루틴을 편집 중입니다" 안내

### 5-10. 탭 / 서브탭

**메인 탭 (`nav button`) — 파일 인덱스 디자인**
- 라벨만 (라이브러리 / 루틴 / 기록 / 사전 / 설정)
- 비활성: muted, hover 시 text 점진
- 활성: text + 2px accent underline + 600 weight

**서브탭 (`.subtab-btn`) — 메인 nav 와 동일 패턴**
- underline 2px, 활성 시 text + accent underline + 600 weight

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
│ memo (dashed, ph bg)      │
└───────────────────────────┘
```

`grid-template-areas: "img meta" "ctrl ctrl" "memo memo"`

- `.ic-memo` — dashed 1px border / ph bg → focus 시 solid accent + panel bg

### 6-2. 캘린더 셀 (`.cal-day`)

기본: min-height 64px (모바일 44px), 1px border, 8r, var(--panel) bg.

| 변형 | 효과 |
|---|---|
| `.has-workout` | 클릭 가능, hover 시 accent border |
| `.quick-start` | 빈 과거/오늘 클릭 가능, hover 시 우상단 `+` |
| `.today` | 2px accent border |
| `.future` | opacity 0.45 + 비활성 |
| `.other-month` | ph bg + 0.35 opacity |
| `.lvl-1` ~ `.lvl-4` | accent 14% / 32% / 55% / 80% (color-mix with --panel) |

`color-mix` base 가 `var(--panel)` 라 다크/라이트 모두에서 자연스러움.

`.lvl-3/4` 진한 배경에선 텍스트 색상 var(--bg) 로 자동 반전.

**셀 내부**:
- `.cal-day-num` — 12px 700, 모바일 10px
- `.cal-cats` — 10px 600 본문 폰트, 카테고리 한글 이름 inline (`등·팔` 형식)

### 6-3. 13주 대시보드 (`.dashboard-strip`)

캘린더 위 분기 단위 큰 그림.

```
┌─ 13주 활동 [3월 2일 → 5월 8일 · 상대 강도]
│  [7×13 grid: 91 cells]
├─ 주간 볼륨 (총 세트) [이번 주 X · 평균 Y · 최고 Z]
│  [SVG sparkline 240×64]
└──
```

- `.dash-heatmap` — `grid-template-columns: repeat(13, 1fr); grid-template-rows: repeat(7, 1fr); grid-auto-flow: column;`
- `.dash-heatcell` — aspect-ratio 1, 5단계 강도 (lvl-0~4), `cursor: pointer` (lvl-1+ 만)
- 셀 클릭 → 그 날짜의 day-detail 모달
- `.dash-spark` — SVG viewBox 240×64, accent path + 옅은 area fill

### 6-4. 통계 카드 (`.stat-card`)

- var(--panel) bg, 1px border, 10r, 14×10 padding, 중앙 정렬
- `.stat-num` 26px 800 accent (tabular-nums)
- `.stat-num-sm` 15px (긴 텍스트용)
- `.stat-label` 11px muted, mt 6
- `.stat-card.streak` → 숫자 뒤 자동 "일" 접미사

### 6-5. 부위별 막대 차트 (`.cat-bars`)

- var(--panel) bg, 14×16 padding, 10r
- 각 행: 60px 라벨 / flex 트랙 / 32px 카운트
- 트랙: 10px 높이, ph bg, 5r
- 채움: CAT_COLORS 솔리드, `transition: width 0.25s`

### 6-6. 설정 행 (`.settings-row`)
- flex space-between, 12px gap, 1px bottom border (마지막 제외)
- `.settings-label` — 11px uppercase muted, letterspacing 0.5
- `.settings-value` — 14px 600 text
- `.settings-mode-badge` — 3색 변종 pill

### 6-7. 검색 결과 dropdown (`.search-results`)

- `<ul>` 스타일링: max-height 220px, scroll, 1px border
- `.search-section-header` — 최근 사용 섹션 라벨 (eyebrow 스타일과 동일 톤)
- 각 li: 36px 썸네일 + 이름·메타 + 상세 버튼
- `<li data-source data-refid>` 클릭 → 항목 추가
- 빈 검색 + 필터 미적용 시 → 최근 사용 동작 8개 노출

### 6-8. 시트 페이지 (`.sheet-page`) — JPG 출력용
- 폭 720px 고정, 28×24 padding, **흰바탕 (#fff)** — 다크 모드와 무관
- `.sheet-grid[data-cols="1|2"]` — 1단/2단 항목 그리드
- `.sheet-item` — 32px 번호 / 110px 이미지 / flex 정보 / 70px 세트
- 2단 시 컬럼·폰트 자동 축소

### 6-9. 환영 모달 (welcome-modal)
- max-width 380px, 중앙 정렬
- 세로 2버튼 스택 (gap 10): primary + ghost
- 닫기 차단 — 강제 선택

### 6-10. 인증 모달 (auth-modal)
- max-width 420px
- 이메일 input + status 메시지 + flex right 버튼

---

## 7. 이모지 시스템

| 이모지 | 용도 |
|---|---|
| 🔑 | 로그인 / 인증 |
| 👤 | 게스트 / 사용자 |
| 📅 | 캘린더 / 기록용 / 오늘 복제 |
| 📋 | 시트 / 공유용 |
| 🏃 | 유산소 |
| 🔥 | 현재 streak |
| 🌙 | 다크 모드 |
| 🎨 | AI 프롬프트 |
| 💡 | 권장 알림 |
| ↑ ↓ | 항목 순서 변경 |
| × | 닫기 / 삭제 |
| ✓ | 저장 완료 |
| ‹ › | 월 네비 |
| · | 카테고리 / 메타 구분자 |
| + | 빠른 시작 hover |

---

## 8. 인터랙션 / 전환

| 대상 | 효과 | 시간 |
|---|---|---|
| body bg/color | 테마 전환 시 | 0.2s ease |
| `.cal-day` hover | border-color → accent | 즉시 |
| `.cal-day.quick-start::before` (`+`) | opacity 0 → 1 | 0.12s |
| `.dash-heatcell:hover` | outline 1px accent | 즉시 |
| `.card` hover | translateY(-1px), border accent | 0.1s |
| `.welcome-choice` hover | translateY(-2px), shadow | 0.15s |
| `.cat-bar-fill` width | 데이터 변경 시 부드러운 채움 | 0.25s ease |
| nav button | color, border-color | 0.15s ease |
| auth-status-dot | sync 시 pulse | 1.2s 무한 |

---

## 9. 일관성 규칙

1. **둥근 모서리는 `--radius`(10px) 또는 의미별**: 6/8/12/999
2. **의미 색상은 토큰 사용** — semantic token 우선, hex 직접 지정 금지
3. **흰색 배경 `#fff` 은 이미지 영역 한정** (카드 thumb, 모달 image, 시트) — 그 외엔 `var(--panel)`
4. **muted 텍스트는 13px 이하**, 본문은 14px
5. **flex-wrap 항상 켜둠** — 모바일 자동 줄바꿈
6. **모달 z-index 50, 중첩 모달 60** 만 사용
7. **버튼 변형 + 사이즈 조합**: `<button class="ghost btn-xs">` 같은 식
8. **danger 색상은 삭제 버튼에만** — 다른 의미로 쓰지 않음
9. **숫자는 tabular-nums** — stat·badge·input[number]
10. **다크 모드는 변수 swap**: 컴포넌트 CSS 는 변수만 사용 (`#fff` 하드코딩은 위 3번 예외만)

---

## 10. 변경 이력 (요약)

| 패키지 | 핵심 변경 |
|---|---|
| **시각 격상** (OKLCH 토큰) | semantic 색상 4종, 다크 모드 4번째 팔레트, tabular-nums, .eyebrow 유틸 신설 |
| **최근 사용 + Quick Repeat** | recentExercises LRU, search dropdown 상단 섹션, 오늘 복제 버튼 (history·day-detail) |
| **13주 대시보드** | dashboard-strip, dash-heatmap (7×13), dash-spark SVG sparkline |
| **패키지 X** (네비 통일) | 메인 nav pill → underline (파일 인덱스 디자인), 서브탭 톤 일치 |
| **패키지 Z** (정리) | eyebrow 11개 패널 + 대시보드, CAT_COLORS OKLCH, categoryBadge 헬퍼, src-badge.seed → info |
| **패키지 Y** (토큰) | --space, --text 스케일, .btn-sm/.btn-xs modifier, library/dict thumb 흰바탕 |

---

## 11. 알려진 비일관 / 후속 정리

리뉴얼 시 다듬을만한 잔존 지점:

- **`--ok` 정의되어 있으나 미사용** — `--success` 와 의미 중복. 제거 또는 alias
- **inline `style="margin-top: 8px;"` 산발적 잔존** — 일부는 utility 클래스로 흡수 가능
- **모바일 폰트 사이즈 미디어 쿼리** — `--text-*` 토큰을 모바일 자동 축소하도록 미디어 쿼리에서 재정의 가능 (현재는 컴포넌트 별로 override)
- **편집 배너 노란색 단독 컴포넌트** — 일반화 가능한 alert 시스템으로 추후 확장
- **카테고리 배지의 sub-category** — 현재 grey neutral. CAT_COLORS desaturated 변형으로 교체 검토

---

이 문서는 `2026-05-08` 기준 `index.html` 의 시각 시스템 스냅샷입니다.
