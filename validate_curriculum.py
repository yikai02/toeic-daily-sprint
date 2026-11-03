# -*- coding: utf-8 -*-
"""Sanity-checks curriculum data. Run: python3 validate_curriculum.py [--min-morning 20 --min-afternoon 20]"""
import argparse
import sys

from master_curriculum import DAYS_DATA


def questions(day):
    a = day["afternoon"]
    p7 = a["part7"]
    passages = p7.get("passages") or [p7]
    return (day["morning"]["part5"], a["quick_recall"], a["spaced_traps"],
            [q for p in passages for q in p["questions"]])


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--min-morning", type=int, default=0)
    ap.add_argument("--min-afternoon", type=int, default=0)
    args = ap.parse_args()
    errors = []
    for n in range(1, 26):
        if n not in DAYS_DATA:
            errors.append(f"Day {n} missing"); continue
        morning, recall, traps, p7 = questions(DAYS_DATA[n])
        if len(morning) < args.min_morning:
            errors.append(f"Day {n}: morning {len(morning)} < {args.min_morning}")
        if len(recall) + len(traps) + len(p7) < args.min_afternoon:
            errors.append(f"Day {n}: afternoon {len(recall)+len(traps)+len(p7)} < {args.min_afternoon}")
        for q in morning + traps + p7:
            if q["answer"] not in q["options"]:
                errors.append(f"Day {n}: answer {q['answer']} not in options: {q['question'][:40]}")
            if len(set(q["options"].values())) != len(q["options"]):
                errors.append(f"Day {n}: duplicate options: {q['question'][:40]}")
    print("\n".join(errors) if errors else "All curriculum checks passed ✅")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
