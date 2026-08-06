"""Reaction matrix: who reacts to whom, giver × receiver.

Top-N people by total reaction involvement (given + received). Cell = number
of reactions giver dropped on receiver's messages.
"""

import json
from collections import Counter
from pathlib import Path

import polars as pl

ROOT = Path(__file__).parent.parent
OUT = ROOT / "data" / "processed"

TOP_N = 15


def main() -> None:
    messages = pl.read_parquet(OUT / "messages.parquet")
    reactions = pl.read_parquet(OUT / "reactions.parquet")
    author_of = dict(zip(messages["id"], messages["name"]))

    pair: Counter[tuple[str, str]] = Counter()
    involvement: Counter[str] = Counter()
    for row in reactions.iter_rows(named=True):
        giver, receiver = row["reactor"], author_of[row["msg_id"]]
        pair[(giver, receiver)] += 1
        involvement[giver] += 1
        involvement[receiver] += 1

    names = [n for n, _ in involvement.most_common(TOP_N)]
    cells = [[pair.get((g, r), 0) for r in names] for g in names]

    out = {"names": names, "cells": cells}
    (OUT / "matrix.json").write_text(json.dumps(out, ensure_ascii=False))

    covered = sum(pair.get((g, r), 0) for g in names for r in names)
    print(f"top {TOP_N} people cover {covered}/{reactions.height} reactions")
    top = sorted(pair.items(), key=lambda kv: -kv[1])[:5]
    for (g, r), n in top:
        print(f"  {g} → {r}: {n}")


if __name__ == "__main__":
    main()
