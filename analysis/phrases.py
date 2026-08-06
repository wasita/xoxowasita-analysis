"""Phrases born in the chat: recurring n-grams and who coined them.

2–4-grams appearing ≥ 3 times across ≥ 2 authors, stopword-boundary filtered,
longer grams absorb their substrings at equal count. Each phrase carries its
coiner (first use), spread, and occurrence times for a sparkline.
"""

import json
import re
from collections import Counter
from pathlib import Path

import polars as pl

ROOT = Path(__file__).parent.parent
OUT = ROOT / "data" / "processed"

TOKEN_RE = re.compile(r"[a-z][a-z']+")
BOUNDARY_STOP = set(
    "the a an and or but of to in on at for with by from as is are was were be so "
    "it this that i im me my we you your he she they them his her their".split()
)
MIN_COUNT = 3
MIN_AUTHORS = 2


def main() -> None:
    messages = pl.read_parquet(OUT / "messages.parquet").sort("ts")

    occurrences: dict[str, list[dict]] = {}
    for row in messages.iter_rows(named=True):
        tokens = TOKEN_RE.findall(row["text"].lower())
        seen_in_msg: set[str] = set()
        for n in (2, 3, 4):
            for i in range(len(tokens) - n + 1):
                gram = tokens[i : i + n]
                if gram[0] in BOUNDARY_STOP or gram[-1] in BOUNDARY_STOP:
                    continue
                phrase = " ".join(gram)
                if phrase in seen_in_msg:
                    continue
                seen_in_msg.add(phrase)
                occurrences.setdefault(phrase, []).append(
                    {"name": row["name"], "minutes": round(row["minutes"], 2)}
                )

    keep = {
        p: occ
        for p, occ in occurrences.items()
        if len(occ) >= MIN_COUNT and len({o["name"] for o in occ}) >= MIN_AUTHORS
    }
    # Longer phrases absorb substrings with the same occurrence count.
    for p in sorted(keep, key=len, reverse=True):
        if p not in keep:
            continue
        for q in list(keep):
            if q != p and q in p and len(keep[q]) <= len(keep[p]):
                del keep[q]

    phrases = sorted(
        (
            {
                "phrase": p,
                "count": len(occ),
                "authors": len({o["name"] for o in occ}),
                "coiner": occ[0]["name"],
                "firstMinute": occ[0]["minutes"],
                "occurrences": [o["minutes"] for o in occ],
            }
            for p, occ in keep.items()
        ),
        key=lambda d: -d["count"],
    )[:20]

    (OUT / "phrases.json").write_text(json.dumps({"phrases": phrases}, ensure_ascii=False))
    for p in phrases[:10]:
        print(f"  “{p['phrase']}” ×{p['count']} ({p['authors']} people) — coined by {p['coiner']} @ {p['firstMinute']:.0f}m")


if __name__ == "__main__":
    main()
