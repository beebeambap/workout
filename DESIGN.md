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

## 4. 출력 규격 (모바일 친화)
- 컨테이너 폭 **720 px**, 높이는 항목 수에 따라 자동(세로 스크롤형 단일 시트).
- 내보내기 시 html2canvas `scale: 2` → 1440px 폭 JPG. 휴대폰에서 그대로 보기 좋음.
- 시트 구성:
  - 헤더: 제목 + 날짜
  - 메모: 옵션 텍스트
  - **단일 테이블**: 모든 항목이 한 표 안에 들어감 (각 항목이 분리된 카드가 아님)
  - 컬럼: `#` (01, 02 …) / 이미지 / 동작(이름·설명) / 세트 × 회
- 이미지: `max-width/height: 100%, width/height: auto` 로 **원본 비율 유지** (자르지 않음).
- 좌측 번호: `String(i+1).padStart(2,'0')`.

## 5. 화면 가독성
- 라이브러리 카드 / 루틴 빌더 / 검색 결과 썸네일 모두 `object-fit: contain` 또는 `max-*` 기반으로 비율 보존.
- 데스크톱: 시트 720px가 그대로 노출, 가로 스크롤 없음.
- 모바일: 시트가 720px 고정이라 가로 스크롤이 생길 수 있으나 캡처/저장된 JPG는 모바일 화면에 맞춰 자연스러운 비율로 보임.

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
