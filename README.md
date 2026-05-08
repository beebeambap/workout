# workout

운동 세션 기록기 — 동작 라이브러리, 루틴 빌더, A4/모바일 시트 JPG 출력.

## 시작
- `index.html` 을 브라우저로 열거나, GitHub Pages(`https://beebeambap.github.io/workout/`) 에 접속.
- 로컬 정적 서버 권장: `python3 -m http.server 8000`

## 클라우드 동기화 (선택)
이메일 매직링크 로그인을 통해 운동 기록·라이브러리를 기기 간 동기화할 수 있습니다.
- `firebase-config.example.js` 를 `firebase-config.js` 로 복사 후 Firebase 콘솔의 SDK 구성값 입력
- 미설정 시 동기화 기능만 비활성화되며 로컬 사용은 그대로 가능

## 외부 데이터셋
루틴 빌더의 검색 풀에 다음 공개 데이터셋을 결합합니다.
- **[hasaneyldrm/exercises-dataset](https://github.com/hasaneyldrm/exercises-dataset)** (1,324개 운동, 이미지+GIF)
- 라이선스: **교육·비상업 연구 목적 전용**. 상업 용도 금지.
- 이미지/GIF는 `raw.githubusercontent.com` URL을 직접 참조합니다.

## 문서
- 설계: [DESIGN.md](DESIGN.md)
- 데이터 수집/외부 DB 비교: [exercise-routine-app-plan.md](exercise-routine-app-plan.md)
