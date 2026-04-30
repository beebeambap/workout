#!/usr/bin/env python3
"""
누적식 한글 번역 빌더.

사용법:
  - batches/ 디렉터리의 모든 *.json 을 읽어 data/name_ko.json 에 머지
  - 각 batch 파일은 { "id": {"name_ko": "...", "summary_ko": "..."}, ... } 형태
  - 배치를 추가/수정한 뒤 이 스크립트를 다시 돌리면 결과가 갱신됨

데이터 출처: hasaneyldrm/exercises-dataset (비상업·교육 연구 목적)
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
BATCH_DIR = ROOT / "scripts" / "name_ko_batches"
OUT = ROOT / "data" / "name_ko.json"


def load_all_batches() -> dict:
    """배치 파일들을 알파벳 순으로 읽어 항목 단위 deep-merge.

    같은 ID 에 대해 여러 배치가 부분 필드만 추가하는 경우를 지원한다.
    예) 002a 가 {name_ko, summary_ko} 를 정의하고
       003 가 같은 ID 에 {steps_ko} 만 추가하면 최종은 세 필드 모두 보유.
    """
    merged: dict = {}
    if not BATCH_DIR.exists():
        return merged
    files = sorted(BATCH_DIR.glob("*.json"))
    for f in files:
        with f.open("r", encoding="utf-8") as fp:
            chunk = json.load(fp)
        before = len(merged)
        for k, v in chunk.items():
            if k in merged and isinstance(merged[k], dict) and isinstance(v, dict):
                merged[k].update(v)
            else:
                merged[k] = v
        print(f"  + {f.name}: {len(chunk)} entries (total {before} -> {len(merged)})")
    return merged


def main() -> int:
    print(f"[name_ko build] reading batches from {BATCH_DIR}")
    merged = load_all_batches()
    if not merged:
        print("no batches found", file=sys.stderr)
        return 1
    OUT.parent.mkdir(parents=True, exist_ok=True)
    with OUT.open("w", encoding="utf-8") as fp:
        json.dump(merged, fp, ensure_ascii=False, indent=1, sort_keys=True)
    print(f"[name_ko build] wrote {len(merged)} entries to {OUT.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
