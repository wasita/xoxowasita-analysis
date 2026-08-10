"""Togetherness: was the room one conversation or many?

For each 2-minute window, the mean pairwise cosine similarity between
messages from *different* authors. High = everyone reacting to the same
thing; low = fragmented side-conversations. Complements drift (which measures
movement across time, not cohesion within it).
"""

import json
from itertools import combinations
from pathlib import Path

import numpy as np
import polars as pl

ROOT = Path(__file__).parent.parent
OUT = ROOT / "data" / "processed"

EVENT_END_MIN = 72
BIN_MIN = 2
MIN_MESSAGES = 3


def main() -> None:
    messages = pl.read_parquet(OUT / "messages.parquet")
    emb = np.load(OUT / "embeddings.npy")
    minutes = messages["minutes"].to_numpy()
    names = messages["name"].to_list()

    bins = []
    for b in range(0, EVENT_END_MIN, BIN_MIN):
        idx = np.where((minutes >= b) & (minutes < b + BIN_MIN))[0]
        pairs = [
            float(np.dot(emb[i], emb[j]))
            for i, j in combinations(idx, 2)
            if names[i] != names[j]
        ]
        bins.append(
            {
                "minute": b,
                "mean": round(float(np.mean(pairs)), 4) if len(idx) >= MIN_MESSAGES and pairs else None,
                "n": len(idx),
            }
        )

    filled = [x for x in bins if x["mean"] is not None]
    peak = max(filled, key=lambda x: x["mean"])
    trough = min(filled, key=lambda x: x["mean"])
    out = {
        "binMinutes": BIN_MIN,
        "bins": bins,
        "peakMinute": peak["minute"],
        "troughMinute": trough["minute"],
        "overallMean": round(float(np.mean([x["mean"] for x in filled])), 4),
    }
    (OUT / "togetherness.json").write_text(json.dumps(out))
    print(f"peak togetherness min {peak['minute']} ({peak['mean']}), trough min {trough['minute']} ({trough['mean']})")


if __name__ == "__main__":
    main()
