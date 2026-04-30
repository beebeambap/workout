#!/usr/bin/env python3
"""
자동 번역 베이스라인 생성기.

이미 수동 번역된 항목(scripts/name_ko_batches/001-...) 외의 운동들에 대해
토큰 단위 패턴 매칭으로 한글 이름·간단 요약을 생성합니다.

실행:
  python3 scripts/auto_translate_baseline.py [--src /path/to/exercises.json]

산출:
  scripts/name_ko_batches/999-auto-baseline.json

이후 `python3 scripts/build_name_ko.py` 를 돌리면 data/name_ko.json 으로 머지됩니다.
사용자가 마음에 안 드는 항목은 인앱 [편집] 으로 개별 수정할 수 있고,
정성 번역 배치(002-, 003-, ...)는 999-auto-baseline 보다 알파벳 순서가 빠르므로
build 시 자동 베이스라인을 덮어씁니다.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
BATCH_DIR = ROOT / "scripts" / "name_ko_batches"
OUT_BATCH = BATCH_DIR / "999-auto-baseline.json"
DEFAULT_SRC = "https://raw.githubusercontent.com/hasaneyldrm/exercises-dataset/main/data/exercises.json"

# ---------------------------------------------------------------------------
# 토큰 사전 — 시드 운동명에서 자주 등장하는 영문 토큰을 한글 카타카나·축약 표기로
# ---------------------------------------------------------------------------
TOKEN_KO: dict[str, str] = {
    # 장비
    "barbell": "바벨", "dumbbell": "덤벨", "cable": "케이블", "band": "밴드",
    "kettlebell": "케틀벨", "machine": "머신", "smith": "스미스", "ez": "EZ",
    "ez-bar": "EZ 바", "medicine": "메디신", "ball": "볼", "stability": "스태빌리티",
    "bosu": "보수", "foam": "폼", "roller": "롤러", "rope": "로프", "sled": "슬레드",
    "lever": "레버", "leverage": "레버리지", "weighted": "웨이티드", "wheel": "휠",
    "olympic": "올림픽", "trap": "트랩", "bar": "바", "tire": "타이어",
    "hammer": "해머", "ergometer": "에르고미터", "skierg": "스키어그",
    "elliptical": "일립티컬", "stationary": "스테이셔너리", "stepmill": "스텝밀",
    "bike": "바이크", "rowing": "로잉", "ski": "스키",
    "resistance": "저항", "assisted": "어시스트", "bench": "벤치",
    "preacher": "프리처", "platform": "플랫폼", "box": "박스", "step": "스텝",
    "stick": "스틱", "towel": "타월", "chair": "체어", "wall": "월",
    "floor": "플로어", "mat": "매트", "plate": "플레이트", "disc": "디스크",
    "vest": "베스트", "chain": "체인", "strap": "스트랩", "belt": "벨트",

    # 부위 (토큰)
    "chest": "체스트", "back": "백", "shoulder": "숄더", "shoulders": "숄더",
    "neck": "넥", "arm": "암", "arms": "암", "wrist": "리스트", "wrists": "리스트",
    "forearm": "전완", "forearms": "전완", "calf": "카프", "calves": "카프",
    "thigh": "허벅지", "glute": "글루트", "glutes": "글루트",
    "hamstring": "햄스트링", "hamstrings": "햄스트링", "quad": "쿼드", "quads": "쿼드",
    "tricep": "트라이셉스", "triceps": "트라이셉스", "bicep": "바이셉스", "biceps": "바이셉스",
    "pec": "흉근", "pecs": "흉근", "pectoral": "흉근", "pectorals": "흉근",
    "lat": "랫", "lats": "랫", "ab": "복근", "abs": "복근", "core": "코어",
    "hip": "힙", "hips": "힙", "spine": "척추", "trap": "트랩", "traps": "승모근",
    "delt": "델트", "delts": "델트", "rotator": "로테이터", "cuff": "커프",
    "obliques": "복사근", "adductor": "내전근", "adductors": "내전근",
    "abductor": "외전근", "abductors": "외전근", "groin": "사타구니",
    "knee": "무릎", "ankle": "발목", "elbow": "엘보우",

    # 동작/운동명
    "press": "프레스", "squat": "스쿼트", "deadlift": "데드리프트",
    "curl": "컬", "curls": "컬",
    "extension": "익스텐션", "extensions": "익스텐션",
    "fly": "플라이", "flye": "플라이", "flies": "플라이", "flyes": "플라이",
    "raise": "레이즈", "raises": "레이즈",
    "row": "로우", "rows": "로우",
    "pull": "풀", "pulldown": "풀다운", "pullup": "풀업", "pull-up": "풀업",
    "pullover": "풀오버", "pull-over": "풀오버",
    "push": "푸쉬", "pushup": "푸쉬업", "push-up": "푸쉬업", "pushdown": "푸쉬다운",
    "press-down": "프레스다운",
    "crunch": "크런치", "crunches": "크런치",
    "twist": "트위스트", "twists": "트위스트",
    "lunge": "런지", "lunges": "런지",
    "kickback": "킥백", "kickbacks": "킥백",
    "shrug": "슈러그", "shrugs": "슈러그",
    "dip": "딥", "dips": "딥",
    "plank": "플랭크",
    "sit-up": "싯업", "situp": "싯업", "sit-ups": "싯업", "situps": "싯업",
    "snatch": "스내치", "jerk": "저크", "clean": "클린",
    "thruster": "쓰러스터", "burpee": "버피", "burpees": "버피",
    "jump": "점프", "jumps": "점프", "jumping": "점핑",
    "hop": "홉", "hops": "홉", "skip": "스킵",
    "kick": "킥", "kicks": "킥",
    "step-up": "스텝업", "stepup": "스텝업", "step-ups": "스텝업",
    "lift": "리프트", "lifts": "리프트", "lifting": "리프팅",
    "good-morning": "굿모닝",
    "pulse": "펄스", "pump": "펌프", "march": "마치", "walk": "워크",
    "run": "런", "running": "러닝",
    "hold": "홀드", "holds": "홀드", "static": "스태틱",
    "reach": "리치", "reaches": "리치", "touch": "터치", "touches": "터치",
    "rotation": "로테이션", "rotational": "로테이셔널", "rotate": "로테이트",
    "circle": "서클", "circles": "서클",
    "swing": "스윙", "swings": "스윙",
    "throw": "쓰로우", "slam": "슬램", "slams": "슬램", "wave": "웨이브",
    "stretch": "스트레칭", "stretches": "스트레칭", "stretching": "스트레칭",
    "warm-up": "웜업", "warmup": "웜업", "cool-down": "쿨다운",
    "bridge": "브릿지", "bridges": "브릿지",
    "carry": "캐리", "carries": "캐리", "farmer": "파머",
    "drag": "드래그",
    "rollout": "롤아웃", "roll-out": "롤아웃",

    # 수식어 / 자세
    "alternating": "얼터네이팅", "alternate": "얼터네이트",
    "single": "싱글", "double": "더블", "one": "원", "two": "투", "three": "쓰리",
    "reverse": "리버스", "inverse": "인버스",
    "incline": "인클라인", "decline": "디클라인", "flat": "플랫",
    "wide": "와이드", "narrow": "내로우", "close": "클로즈",
    "wide-grip": "와이드 그립", "close-grip": "클로즈 그립",
    "grip": "그립", "underhand": "언더핸드", "overhand": "오버핸드",
    "neutral": "뉴트럴",
    "standing": "스탠딩", "seated": "시티드", "sitting": "시티드",
    "lying": "라잉", "prone": "프론", "supine": "슈파인",
    "kneeling": "닐링", "half-kneeling": "하프 닐링",
    "bent": "벤트", "bent-over": "벤트오버",
    "over": "오버", "under": "언더", "above": "어보브", "below": "벨로우",
    "forward": "포워드", "backward": "백워드",
    "lateral": "래터럴", "side": "사이드",
    "front": "프론트", "rear": "리어", "back-side": "백사이드",
    "high": "하이", "low": "로우", "mid": "미드", "middle": "미들",
    "concentration": "컨센트레이션",
    "spider": "스파이더", "zottman": "조트만",
    "cross": "크로스", "crossbody": "크로스바디", "cross-body": "크로스바디",
    "goblet": "고블릿", "sumo": "스모", "romanian": "루마니안",
    "stiff": "스티프", "stiff-leg": "스티프 레그", "stiff-legged": "스티프 레그",
    "straight": "스트레이트", "straight-leg": "스트레이트 레그",
    "jefferson": "제퍼슨", "zercher": "저처", "hack": "핵",
    "split": "스플릿", "bulgarian": "불가리안",
    "pistol": "피스톨", "cossack": "코사크", "shrimp": "쉬림프",
    "broad": "브로드", "tuck": "턱", "pike": "파이크",
    "hollow": "할로우",
    "isometric": "아이소메트릭",
    "archer": "아처", "spider-man": "스파이더맨", "spiderman": "스파이더맨",
    "dragon": "드래곤", "cobra": "코브라", "superman": "슈퍼맨",
    "bird": "버드", "dog": "도그", "bird-dog": "버드 도그",
    "mountain": "마운틴", "climber": "클라이머", "climbers": "클라이머",
    "fire": "파이어", "hydrant": "하이드런트", "fire-hydrant": "파이어 하이드런트",
    "donkey": "동키", "frog": "프로그", "starfish": "스타피쉬",
    "turkish": "터키시", "getup": "겟업", "get-up": "겟업",
    "get": "겟", "up": "업", "down": "다운",
    "around": "어라운드", "world": "월드",
    "figure": "피겨", "eight": "에잇",
    "butterfly": "버터플라이",
    "scissor": "시저", "scissors": "시저",
    "good": "굿", "morning": "모닝",
    "good-morning": "굿모닝",
    "muscle-up": "머슬업", "muscleup": "머슬업",
    "chin-up": "친업", "chinup": "친업", "chin": "친",
    "pendlay": "펜들레이",
    "yates": "예이츠",

    # 기타 흔한 토큰
    "with": "+", "and": "+", "to": "→",
    "v": "V", "y": "Y", "t": "T", "x": "X", "i": "I", "l": "L",
    "v-up": "V업", "v-ups": "V업",
    "sit": "싯", "stand": "스탠드",
    "exercise": "운동", "workout": "워크아웃",
    "ball": "볼",

    # 성별 표기 (괄호 안에 들어가는 것)
    "male": "남", "female": "여",

    # 흔한 부위/장기
    "knee": "무릎", "elbow": "팔꿈치", "feet": "발",
    "leg": "레그", "legs": "레그",

    # 자주 나오는 변형
    "weighted": "웨이티드", "loaded": "로디드", "banded": "밴디드",
    "hanging": "행잉", "hang": "행",
    "rolling": "롤링", "rotating": "로테이팅", "twisting": "트위스팅",
    "pressing": "프레싱", "pulling": "풀링",
    "raising": "레이징", "curling": "컬링",
    "explosive": "익스플로시브", "speed": "스피드", "power": "파워",
    "tempo": "템포", "slow": "슬로우", "pause": "포즈",
    "deep": "딥", "shallow": "쉘로우",
    "heavy": "헤비", "light": "라이트",
    "max": "맥스", "1rm": "1RM",
    "isolation": "아이솔레이션", "compound": "컴파운드",
    "negative": "네거티브", "eccentric": "에센트릭", "concentric": "컨센트릭",

    # cardio 관련
    "cardio": "카디오", "aerobic": "에어로빅",
    "interval": "인터벌", "tabata": "타바타",
    "treadmill": "트레드밀",

    # 기타 흔한 단어
    "wide-stance": "와이드 스탠스", "stance": "스탠스",
    "external": "외측", "internal": "내측",
    "rotation": "로테이션",
    "static": "스태틱",
    "active": "액티브",
    "dynamic": "다이내믹",
    "supported": "서포티드",
    "unsupported": "언서포티드",
    "self": "셀프",
    "partner": "파트너",
    "tempo": "템포",

    # 보강분 (베이스라인 1차 검증 후 추가)
    "bend": "벤드", "bends": "벤드",
    "abduction": "외전", "adduction": "내전",
    "bodyweight": "맨몸", "body-weight": "맨몸",
    "pass": "패스", "through": "쓰루",
    "range": "레인지", "motion": "모션",
    "full": "풀", "half": "하프", "quarter": "쿼터",
    "rollerout": "롤아웃", "rollout": "롤아웃", "roll-out": "롤아웃",
    "exercise": "엑서사이즈",
    "russian": "러시안",
    "tibialis": "정강이", "anterior": "전면", "posterior": "후면",
    "good-morning": "굿모닝",
    "v-bar": "V바", "y-bar": "Y바", "t-bar": "T바",
    "rdl": "RDL", "ohp": "OHP",
    "amrap": "AMRAP",
    "isohold": "아이소홀드",
    "wave": "웨이브",
    "hover": "호버", "shoulder-tap": "숄더탭", "tap": "탭", "taps": "탭",
    "skater": "스케이터", "skaters": "스케이터",
    "tuck-jump": "턱 점프",
    "pop": "팝",
    "trunk": "트렁크", "torso": "토르소",
    "biceps-curl": "바이셉스 컬", "triceps-extension": "트라이셉스 익스텐션",

    # 2차 보강 (잔존 영문 토큰 빈도 기준)
    "overhead": "오버헤드",
    "head": "헤드",
    "upright": "업라이트",
    "military": "밀리터리",
    "hands": "양손", "hand": "한손",
    "parallel": "패럴렐",
    "toe": "토", "toes": "토",
    "blaster": "블라스터",
    "behind": "비하인드",
    "attachment": "어태치먼트",
    "body": "바디",
    "support": "서포트", "supports": "서포트",
    "lower": "로워",
    "revers": "리버스", "reverse-grip": "리버스 그립",
    "inner": "안쪽", "outer": "바깥쪽",
    "palms": "양손바닥", "palm": "손바닥",
    "inverted": "인버티드", "inversion": "인버전",
    "suspended": "서스펜디드", "suspension": "서스펜션", "trx": "TRX",
    "pov": "POV",
    "planche": "플란체",
    "hyperextension": "하이퍼익스텐션",
    "against": "어게인스트",
    "walking": "워킹", "walks": "워크",
    "flexor": "굴근", "flexion": "굴곡",
    "arnold": "아놀드",
    "twisted": "트위스티드",
    "plyo": "플라이오", "plyometric": "플라이오메트릭", "plyometrics": "플라이오메트릭",
    "windmill": "윈드밀", "windmills": "윈드밀",
    "extended": "익스텐디드",
    "oblique": "복사근", "obliques": "복사근",
    "between": "비트윈",
    "vertical": "버티컬", "horizontal": "호리존탈",
    "upper": "상부",
    "drop": "드롭",
    "pelvic": "골반",
    "tilt": "틸트",
    "pose": "포즈",
    "squatting": "스쿼팅",
    "raised": "레이즈드",
    "french": "프렌치", "skull": "스컬",
    "bradford": "브래드포드",
    "rocky": "록키",
    "rocking": "로킹",
    "flip": "플립", "flips": "플립",
    "cuban": "쿠반",
    "iron": "아이언",
    "face": "페이스",
    "deltoid": "삼각근",
    "pronation": "프로네이션", "supination": "수피네이션",
    "finger": "핑거",
    "handstand": "핸드스탠드",
    "jack": "잭",
    "landmine": "랜드마인",
    "around-world": "어라운드 월드",
    "around-the-world": "어라운드 월드",

    # 흔한 동작/근육 추가
    "y-raise": "Y 레이즈", "t-raise": "T 레이즈", "i-raise": "I 레이즈",
    "ytwl": "YTWL",
    "wide-hand": "와이드 핸드",
    "diamond": "다이아몬드",
    "hindu": "힌두",
    "scorpion": "스콜피온",
    "knee-up": "니업",
    "leg-press": "레그 프레스",
    "leg-curl": "레그 컬",
    "deadbug": "데드버그", "dead-bug": "데드버그",
    "side-to-side": "사이드 투 사이드",
    "around": "어라운드",
    "world": "월드",
    "scissor": "시저",
    "kicker": "키커",
    "sissy": "시시",
    "siff": "시프",
    "elevated": "엘리베이티드",
    "off": "오프",
    "is": "_DROP_",
    "be": "_DROP_",

    # 영문 그대로 두면 어색한 fillers — 제거 (빈 문자열은 _DROP으로 표기)
    "the": "_DROP_", "of": "_DROP_", "on": "_DROP_", "in": "_DROP_",
    "from": "_DROP_", "to": "_DROP_", "for": "_DROP_", "at": "_DROP_",
    "by": "_DROP_", "into": "_DROP_", "onto": "_DROP_",
    "an": "_DROP_", "a": "_DROP_",
}

# 타깃 근육 한글 (요약용)
TARGET_KO: dict[str, str] = {
    "abs": "복근",
    "pectorals": "가슴",
    "biceps": "이두",
    "triceps": "삼두",
    "glutes": "둔근",
    "delts": "삼각근",
    "upper back": "상부 등",
    "lats": "광배근",
    "calves": "종아리",
    "quads": "대퇴사두",
    "hamstrings": "햄스트링",
    "forearms": "전완",
    "cardiovascular system": "심폐",
    "spine": "척추기립근",
    "traps": "승모근",
    "adductors": "내전근",
    "serratus anterior": "전거근",
    "abductors": "외전근",
    "levator scapulae": "견갑거근",
}

# 장비 한글 (요약용)
EQUIPMENT_KO: dict[str, str] = {
    "body weight": "맨몸",
    "barbell": "바벨",
    "dumbbell": "덤벨",
    "cable": "케이블",
    "band": "밴드",
    "kettlebell": "케틀벨",
    "machine": "머신",
    "smith machine": "스미스 머신",
    "leverage machine": "레버리지 머신",
    "sled machine": "슬레드 머신",
    "medicine ball": "메디신볼",
    "stability ball": "스태빌리티볼",
    "bosu ball": "보수볼",
    "ez barbell": "EZ 바벨",
    "olympic barbell": "올림픽 바벨",
    "trap bar": "트랩바",
    "foam roll": "폼롤러",
    "wheel roller": "휠",
    "roller": "롤러",
    "rope": "로프",
    "tire": "타이어",
    "stationary bike": "실내자전거",
    "elliptical machine": "일립티컬",
    "stepmill machine": "스텝밀",
    "upper body ergometer": "상체 에르고미터",
    "skierg machine": "스키어그",
    "hammer": "해머",
    "assisted": "보조",
    "weighted": "웨이티드",
    "resistance band": "저항 밴드",
}


# 구(phrase) 단계 치환 — 토큰 분리 전에 적용 (어순 보존이 중요한 경우)
PHRASE_KO: dict[str, str] = {
    "exercise ball": "스태빌리티 볼",
    "stability ball": "스태빌리티 볼",
    "medicine ball": "메디신 볼",
    "bosu ball": "보수 볼",
    "ez bar": "EZ 바", "ez-bar": "EZ 바",
    "smith machine": "스미스 머신",
    "leverage machine": "레버리지 머신",
    "sled machine": "슬레드 머신",
    "trap bar": "트랩바", "trap-bar": "트랩바",
    "olympic barbell": "올림픽 바벨",
    "stationary bike": "실내자전거",
    "elliptical machine": "일립티컬",
    "stepmill machine": "스텝밀",
    "upper body ergometer": "상체 에르고미터",
    "skierg machine": "스키어그",
    "resistance band": "저항 밴드",
    "foam roll": "폼롤러", "foam roller": "폼롤러",
    "wheel roller": "휠",
    "rope": "로프",
    "pass through": "패스 쓰루",
    "range of motion": "가동범위",
    "full range of motion": "풀 가동범위",
    "good morning": "굿모닝",
    "muscle up": "머슬업", "muscle-up": "머슬업",
    "chin up": "친업",
    "pull up": "풀업", "pullup": "풀업",
    "push up": "푸쉬업", "pushup": "푸쉬업",
    "sit up": "싯업", "situp": "싯업",
    "step up": "스텝업", "stepup": "스텝업",
    "v up": "V업", "v-up": "V업",
    "bent over": "벤트오버", "bent-over": "벤트오버",
    "stiff leg": "스티프 레그", "stiff-leg": "스티프 레그", "stiff-legged": "스티프 레그",
    "straight leg": "스트레이트 레그", "straight-leg": "스트레이트 레그",
    "wide grip": "와이드 그립", "wide-grip": "와이드 그립",
    "close grip": "클로즈 그립", "close-grip": "클로즈 그립",
    "single arm": "원암", "single-arm": "원암", "one arm": "원암", "one-arm": "원암",
    "double arm": "더블암", "two arm": "투암",
    "single leg": "싱글 레그", "one leg": "원 레그",
    "lying on floor": "플로어 라잉", "on the floor": "플로어",
    "on the wall": "월", "against the wall": "월",
    "rectus femoris": "대퇴직근",
    "lat pulldown": "랫 풀다운",
    "high cable": "하이 케이블",
    "low cable": "로우 케이블",
    "behind the back": "비하인드 더 백",
    "behind the neck": "비하인드 더 넥",
    "behind back": "비하인드 백",
    "behind neck": "비하인드 넥",
    "front squat": "프론트 스쿼트",
    "back squat": "백 스쿼트",
    "overhead squat": "오버헤드 스쿼트",
    "overhead press": "오버헤드 프레스",
    "rear delt": "리어 델트",
    "front delt": "프론트 델트",
    "side delt": "사이드 델트",
    "lateral raise": "래터럴 레이즈",
    "front raise": "프론트 레이즈",
    "rear raise": "리어 레이즈",
    "calf raise": "카프 레이즈",
    "hip thrust": "힙 쓰러스트",
    "glute bridge": "글루트 브릿지",
    "glute kickback": "글루트 킥백",
    "leg curl": "레그 컬",
    "leg extension": "레그 익스텐션",
    "leg press": "레그 프레스",
    "leg raise": "레그 레이즈",
    "hip abduction": "힙 외전",
    "hip adduction": "힙 내전",
    "hip extension": "힙 익스텐션",
    "hip flexion": "힙 플렉션",
    "knee raise": "니 레이즈",
    "knee tuck": "니 턱",
    "knee drive": "니 드라이브",
    "shoulder press": "숄더 프레스",
    "chest press": "체스트 프레스",
    "chest fly": "체스트 플라이",
    "tricep extension": "트라이셉스 익스텐션",
    "triceps extension": "트라이셉스 익스텐션",
    "tricep pushdown": "트라이셉스 푸쉬다운",
    "triceps pushdown": "트라이셉스 푸쉬다운",
    "bicep curl": "바이셉스 컬",
    "biceps curl": "바이셉스 컬",
    "preacher curl": "프리처 컬",
    "concentration curl": "컨센트레이션 컬",
    "hammer curl": "해머 컬",
    "spider curl": "스파이더 컬",
    "drag curl": "드래그 컬",
    "zottman curl": "조트만 컬",
    "wrist curl": "리스트 컬",
    "reverse wrist curl": "리버스 리스트 컬",
    "russian twist": "러시안 트위스트",
    "mountain climber": "마운틴 클라이머",
    "bird dog": "버드 도그", "bird-dog": "버드 도그",
    "fire hydrant": "파이어 하이드런트",
    "donkey kick": "동키 킥",
    "frog jump": "프로그 점프",
    "burpee": "버피",
    "good-morning": "굿모닝",
    "deadlift": "데드리프트",
    "romanian deadlift": "루마니안 데드리프트",
    "stiff leg deadlift": "스티프 레그 데드리프트",
    "sumo deadlift": "스모 데드리프트",
    "trap bar deadlift": "트랩바 데드리프트",
    "snatch grip deadlift": "스내치 그립 데드리프트",
}

_DROP_TOKEN = "_DROP_"


def translate_name(name: str) -> str:
    """구 → 토큰 순으로 사전 적용. 토큰 매칭 안 되면 원문 유지."""
    work = name

    # 1) 구 단계 치환 (긴 것 먼저)
    sorted_phrases = sorted(PHRASE_KO.items(), key=lambda kv: -len(kv[0]))
    for en, ko in sorted_phrases:
        # 단어 경계 + 케이스 무시 + 인접 공백 정리
        pattern = r"(?i)(?<!\w)" + re.escape(en) + r"(?!\w)"
        work = re.sub(pattern, ko, work)

    # 2) 토큰 단계 분리 (공백/괄호/쉼표는 보존)
    parts = re.split(r"(\s+|[(),])", work)
    out: list[str] = []
    for part in parts:
        if not part:
            continue
        if part.isspace() or part in "(),":
            out.append(part)
            continue
        low = part.lower()
        repl: str | None = None
        if low in TOKEN_KO:
            repl = TOKEN_KO[low]
        elif low.endswith("s") and low[:-1] in TOKEN_KO:
            repl = TOKEN_KO[low[:-1]]
        elif low.endswith("'s") and low[:-2] in TOKEN_KO:
            repl = TOKEN_KO[low[:-2]]
        if repl is None and "-" in part:
            sub_parts = part.split("-")
            if all((sp.lower() in TOKEN_KO or sp == "") for sp in sub_parts):
                pieces = [TOKEN_KO[sp.lower()] for sp in sub_parts if sp]
                pieces = [p for p in pieces if p != _DROP_TOKEN]
                repl = " ".join(pieces) if pieces else _DROP_TOKEN
        if repl is None:
            out.append(part)  # 매칭 실패 → 원문 유지
        elif repl == _DROP_TOKEN:
            out.append("")  # filler 제거
        else:
            out.append(repl)

    result = "".join(out)

    # 3) 후처리: 공백 압축 / 괄호 내부 정리 / DROP 으로 인한 잔여 공백 정리
    result = re.sub(r"\s+", " ", result).strip()
    result = re.sub(r"\(\s+", "(", result)
    result = re.sub(r"\s+\)", ")", result)
    result = re.sub(r"\s*,\s*", ", ", result)
    result = re.sub(r"\s+\(", " (", result)
    return result.strip()


def make_summary(target_en: str | None, equipment_en: str | None) -> str:
    target_ko = TARGET_KO.get(target_en or "", target_en or "")
    eq_ko = EQUIPMENT_KO.get(equipment_en or "", equipment_en or "")
    if eq_ko == "맨몸":
        if not target_ko:
            return "맨몸으로 수행하는 운동"
        return f"맨몸으로 {target_ko}을(를) 자극하는 운동"
    if not target_ko:
        return f"{eq_ko}을(를) 사용한 운동"
    return f"{eq_ko}을(를) 사용해 {target_ko}을(를) 자극하는 운동"


def existing_ids() -> set[str]:
    """이미 수동 번역된 배치 파일들에서 ID 모음."""
    ids: set[str] = set()
    for f in BATCH_DIR.glob("*.json"):
        if f.name.startswith("999-"):
            continue
        with f.open("r", encoding="utf-8") as fp:
            ids.update(json.load(fp).keys())
    return ids


def load_src(src: str):
    if src.startswith("http://") or src.startswith("https://"):
        with urllib.request.urlopen(src) as resp:
            return json.loads(resp.read().decode("utf-8"))
    return json.loads(Path(src).read_text(encoding="utf-8"))


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--src", default=DEFAULT_SRC, help="exercises.json URL or path")
    args = ap.parse_args(argv)

    print(f"[auto] loading source: {args.src}")
    data = load_src(args.src)
    skip = existing_ids()
    print(f"[auto] skipping {len(skip)} already-manual entries")

    auto: dict[str, dict[str, str]] = {}
    for e in data:
        if e["id"] in skip:
            continue
        auto[e["id"]] = {
            "name_ko": translate_name(e["name"]),
            "summary_ko": make_summary(e.get("target"), e.get("equipment")),
        }
    OUT_BATCH.parent.mkdir(parents=True, exist_ok=True)
    with OUT_BATCH.open("w", encoding="utf-8") as f:
        json.dump(auto, f, ensure_ascii=False, indent=1, sort_keys=True)
    print(f"[auto] wrote {len(auto)} entries to {OUT_BATCH.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
