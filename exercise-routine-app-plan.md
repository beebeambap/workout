# 헬스 루틴 이미지 앱 개발 계획서

> 작성일: 2026-04-29  
> 목적: 헬스 동작 이미지 기반 루틴 카드 생성 앱 개발 레퍼런스

---

## 1. 프로젝트 개요

사용자가 원하는 헬스 동작을 검색하고, 해당 동작의 **이미지 + 이름 + 수행방법 + reps/set** 정보를 조합하여 루틴 이미지 파일로 내보낼 수 있는 웹/앱.

---

## 2. 데이터 수집 전략

### 2-1. 1순위: ExerciseDB API (RapidAPI)

- **URL**: `https://exercisedb.p.rapidapi.com/exercises`
- **데이터**: 운동명, 타깃 근육, 장비, GIF 이미지 URL 포함 1,300개+
- **무료 플랜**: 월 500 requests
- **응답 예시**:

```json
{
  "id": "0001",
  "name": "3/4 Sit-Up",
  "bodyPart": "waist",
  "equipment": "body weight",
  "gifUrl": "https://v2.exercisedb.io/image/...",
  "target": "abs"
}
```

### 2-2. 2순위: wger Workout Manager (완전 무료 오픈소스)

- **API**: `https://wger.de/api/v2/exercise/`
- **이미지 엔드포인트**: `https://wger.de/api/v2/exerciseimage/`
- **장점**: self-hosting 가능 → 트래픽 제한 없음
- **단점**: GIF 없음, 정지 이미지 위주

### 2-3. 이미지 저장 방식 선택

| 방식 | 장점 | 단점 | 권장 시점 |
|------|------|------|-----------|
| gifUrl 직접 참조 | 구현 빠름 | 외부 URL 의존 | 초기 개발/프로토타입 |
| 이미지 다운로드 후 직접 저장 | 안정적, 빠른 로딩 | 초기 수집 비용 | 프로덕션 |

---

## 3. 이미지 일괄 수집 스크립트 (Python)

```python
import requests
import os

RAPIDAPI_KEY = "YOUR_KEY_HERE"
SAVE_DIR = "images/exercises"

os.makedirs(SAVE_DIR, exist_ok=True)

def fetch_all_exercises():
    url = "https://exercisedb.p.rapidapi.com/exercises"
    headers = {
        "X-RapidAPI-Key": RAPIDAPI_KEY,
        "X-RapidAPI-Host": "exercisedb.p.rapidapi.com"
    }
    response = requests.get(url, headers=headers)
    return response.json()

def download_gif(exercise):
    gif_url = exercise["gifUrl"]
    filename = f"{exercise['id']}.gif"
    filepath = os.path.join(SAVE_DIR, filename)

    img_data = requests.get(gif_url).content
    with open(filepath, "wb") as f:
        f.write(img_data)
    print(f"저장 완료: {filename}")

if __name__ == "__main__":
    exercises = fetch_all_exercises()
    for ex in exercises:
        download_gif(ex)
```

---

## 4. DB 스키마 설계

### exercises 테이블

```sql
CREATE TABLE exercises (
  id           TEXT PRIMARY KEY,         -- ExerciseDB ID
  name         TEXT NOT NULL,            -- 영문 원본 이름
  name_ko      TEXT,                     -- 한국어 이름 (번역 or 수동)
  body_part    TEXT,                     -- 운동 부위 (waist, chest 등)
  target       TEXT,                     -- 타깃 근육
  equipment    TEXT,                     -- 장비 (barbell, dumbbell 등)
  gif_url      TEXT,                     -- 원본 or 로컬 저장 경로
  description  TEXT,                     -- 수행방법 (한국어)
  created_at   TIMESTAMP DEFAULT NOW()
);
```

### routines 테이블 (향후 확장)

```sql
CREATE TABLE routines (
  id           SERIAL PRIMARY KEY,
  user_id      TEXT,
  title        TEXT,
  created_at   TIMESTAMP DEFAULT NOW()
);

CREATE TABLE routine_items (
  id           SERIAL PRIMARY KEY,
  routine_id   INT REFERENCES routines(id),
  exercise_id  TEXT REFERENCES exercises(id),
  sets         INT,
  reps         INT,
  order_index  INT                        -- 루틴 내 순서
);
```

---

## 5. 한국어 운동명 및 설명 처리

### 방법 비교

| 방법 | 품질 | 속도 | 비용 |
|------|------|------|------|
| Papago/DeepL API 자동 번역 | 보통 (전문용어 약함) | 빠름 | 유료 |
| Claude API 번역 | 높음 (전문용어 강함) | 보통 | 유료 |
| 수동 매핑 테이블 (핵심 100개) | 최고 | 느림 | 무료 |

### Claude API 활용 번역 예시

```python
import anthropic

client = anthropic.Anthropic(api_key="YOUR_CLAUDE_KEY")

def translate_exercise(name_en, description_en):
    prompt = f"""
헬스 운동 정보를 한국어로 번역해주세요.
- 운동명: {name_en}
- 설명: {description_en}

JSON 형식으로만 응답:
{{"name_ko": "...", "description_ko": "..."}}
"""
    response = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=300,
        messages=[{"role": "user", "content": prompt}]
    )
    return response.content[0].text
```

---

## 6. 추천 기술 스택

```
[데이터 수집]
ExerciseDB API (RapidAPI)
    ↓ Python 일괄 수집 스크립트
    
[저장]
Supabase
  ├── PostgreSQL (운동 메타데이터)
  └── Storage (GIF 이미지 파일)

[백엔드]
FastAPI (Python) 또는 Next.js API Routes

[프론트엔드]
Next.js + Tailwind CSS
  ├── 운동 검색 UI
  ├── 루틴 구성 화면
  └── 루틴 이미지 내보내기 (html2canvas / canvas API)

[배포]
Vercel (프론트) + Supabase (DB/스토리지)
```

---

## 7. 개발 단계별 로드맵

### Phase 1: 데이터 수집 및 DB 구성
- [ ] ExerciseDB API 키 발급 (RapidAPI)
- [ ] Python 스크립트로 전체 운동 데이터 수집
- [ ] GIF 이미지 Supabase Storage 업로드
- [ ] exercises 테이블에 메타데이터 저장
- [ ] 핵심 운동 한국어 번역 (50~100개 우선)

### Phase 2: 검색 기능 구현
- [ ] 운동명 / 근육 부위 / 장비로 필터 검색
- [ ] 운동 상세 카드 (GIF + 이름 + 설명)

### Phase 3: 루틴 구성 기능
- [ ] 루틴에 운동 추가/제거
- [ ] sets / reps 입력
- [ ] 루틴 순서 드래그 정렬

### Phase 4: 이미지 내보내기
- [ ] 루틴 카드 UI 디자인 (운동 이미지 + 정보 조합)
- [ ] html2canvas로 PNG 내보내기
- [ ] SNS 공유용 비율 최적화 (정사각형, 세로형)

---

## 8. 참고 링크

| 리소스 | URL |
|--------|-----|
| ExerciseDB (RapidAPI) | https://rapidapi.com/justin-WFnsXH_t6/api/exercisedb |
| wger API 문서 | https://wger.de/api/v2/ |
| Supabase | https://supabase.com |
| html2canvas | https://html2canvas.hertzen.com |

---

> **다음 단계**: Phase 1 Python 수집 스크립트 실행 → Supabase 테이블 생성 → 데이터 적재
