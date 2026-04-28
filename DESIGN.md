# 운동 세션 기록기 — 설계서

## 1. 목적
운동 세션을 **이미지 + 동작 설명 + 세트/반복 기록**으로 누적 관리하고,
완성된 루틴을 **A4 규격 JPG**로 내보낸다.
모든 데이터는 브라우저 로컬에 저장되어 별도 서버 없이 단일 HTML로 동작한다.

## 2. 사용자 요구사항 매핑
| # | 요구사항 | 구현 위치 |
|---|---------|----------|
| 1 | 고정 이미지 + 이름 업로드, 설명 선택 입력 | `동작 라이브러리` 탭의 업로드 폼 |
| 2 | 설명/이름 사후 수정 | 라이브러리 카드 → 편집 모달 |
| 3 | 검색으로 동작을 골라 reps/sets 드롭다운 기록 | `루틴 만들기` 탭의 검색 + 드롭다운 |
| 4 | 항목 지속 추가 | 루틴 빌더의 항목 추가 버튼 |
| 5 | 최종 결과물 JPG 저장 | `기록 내역`에서 `JPG 저장` 버튼 (html2canvas) |
| 6 | 지난 데이터 불러오기 | `기록 내역`에서 `불러오기` 버튼 → 루틴 빌더에 항목·메타 채워 넣음 |

## 3. 정보 구조
### 데이터 모델 (localStorage)
```
exercises: [
  { id, name, description, imageDataUrl, createdAt, updatedAt }
]
routines: [
  { id, date, title, memo,
    items: [ { exerciseId, sets, reps } ],
    createdAt }
]
```
- 이미지는 `FileReader`로 base64(`data:image/...`) 변환 후 그대로 저장.
- 키: `workout.exercises.v1`, `workout.routines.v1` (스키마 버전 포함).
- localStorage 용량 제한(~5MB) 고려 — 업로드 시 긴 변(longest side) 800px로 리사이즈 후 JPEG 0.85 품질 인코딩.

### 화면 구성
- **상단 탭 네비게이션**: 라이브러리 / 루틴 만들기 / 기록 내역
- **라이브러리**: 업로드 폼 + 검색 + 카드 그리드(편집 모달)
- **루틴 만들기**: 날짜·제목 메타 → 검색 입력 → 후보 리스트 → 선택 시 항목 푸시 → 항목별 reps/sets 드롭다운
- **기록 내역**: 저장된 루틴 목록 → 클릭 시 A4 미리보기 + JPG 저장 / 삭제

## 4. A4 출력 규격
- 96 DPI 기준 **794 × 1123 px** 컨테이너 고정.
- 내보내기 시 html2canvas `scale: 2` → 인쇄 품질 1588 × 2246 px JPG.
- 페이지 헤더: 날짜·제목, 본문: 항목 카드(이미지 썸네일 + 이름 + sets×reps + 설명).
- 항목이 많으면 자동으로 다음 페이지로 분할(추후 필요 시 N개 단위 페이지네이션).

## 5. 모바일 가독성 (추후 고려)
- 데스크톱: A4 미리보기 그대로.
- 모바일: 카드형 1열 레이아웃, 폰트/이미지 비율 유연 → CSS `@media (max-width: 640px)`로 처리.
- 출력용 컨테이너(`.a4-page`)는 항상 고정 픽셀, 화면 표시는 별도 `.preview-frame`이 transform: scale로 축소.

## 6. 컴포넌트 ↔ 이벤트 흐름
```
[업로드 폼] --submit--> exercises.push --> render(libraryGrid)
[라이브러리 카드 클릭] --> openEditModal --> exercises[i] update --> render
[루틴 검색 입력] --input--> filter exercises --> render(searchResults)
[검색 결과 클릭] --> currentRoutine.items.push({reps:10, sets:3}) --> render(items)
[항목 드롭다운 변경] --> currentRoutine.items[i].sets/reps update
[루틴 저장] --> routines.push --> reset currentRoutine --> render(history)
[기록 내역 카드 클릭] --> renderA4Preview --> [JPG 저장] html2canvas → toDataURL('image/jpeg') → download
[기록 내역의 불러오기] --> currentRoutine = clone(routines[i]) --> 루틴 만들기 탭으로 이동 --> render
   - 저장 시 editingId가 있으면 기존 레코드 덮어쓰기, 없으면 새 레코드로 push
```

## 7. 의존성
- vanilla HTML/CSS/JS (빌드 도구 없음).
- 외부 라이브러리: [`html2canvas`](https://html2canvas.hertzen.com/) CDN — JPG 변환만 담당.

## 8. 한계 / 후속 과제
- 다중 기기 동기화 없음(서버 미사용).
- 이미지가 매우 많을 경우 localStorage 한계 → IndexedDB 마이그레이션 고려.
- 루틴 항목 N개 초과 시 페이지네이션 자동화 필요.
- 검색은 부분 문자열만 지원 → 추후 태그/카테고리 추가 여지.
