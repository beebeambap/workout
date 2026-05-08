// 이 파일을 복사하여 firebase-config.js 로 저장한 뒤 실제 값을 채워넣으세요.
// firebase-config.js 는 .gitignore 에 등록되어 커밋되지 않습니다.
//
// 값 확인 위치:
//   Firebase 콘솔 → 프로젝트 설정(⚙️) → 일반 → 내 앱 → SDK 설정 및 구성 → 구성
//
// 참고: Firebase Web API key 는 공개되어도 안전하도록 설계되어 있으며,
//       실제 보안은 Authentication + Firestore 보안 규칙 + 인증 도메인 제한으로 보장됩니다.

window.firebaseConfig = {
  apiKey:            "AIzaSy...YOUR_API_KEY",
  authDomain:        "YOUR_PROJECT_ID.firebaseapp.com",
  projectId:         "YOUR_PROJECT_ID",
  storageBucket:     "YOUR_PROJECT_ID.appspot.com",
  messagingSenderId: "1234567890",
  appId:             "1:1234567890:web:abcdef1234567890",
};
