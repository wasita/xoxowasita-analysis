"""Semantic drift: how fast the conversation's meaning moved.

Mean message embedding per 2-minute bin; drift = 1 − cosine similarity between
consecutive non-empty bins. Peaks should land where the talk changed section —
an independent check on the reconstructed segments.
"""

import json
from pathlib import Path

import numpy as np
import polars as pl

ROOT = Path(__file__).parent.parent
OUT = ROOT / "data" / "processed"

EVENT_END_MIN = 72
BIN_MIN = 2


def main() -> None:
    messages = pl.read_parquet(OUT / "messages.parquet")
    emb = np.load(OUT / "embeddings.npy")
    minutes = messages["minutes"].to_numpy()

    n_bins = EVENT_END_MIN // BIN_MIN
    centroids: list[np.ndarray | None] = []
    for b in range(n_bins):
        idx = np.where((minutes >= b * BIN_MIN) & (minutes < (b + 1) * BIN_MIN))[0]
        centroids.append(emb[idx].mean(axis=0) if len(idx) >= 2 else None)

    points = []
    prev: np.ndarray | None = None
    for b, c in enumerate(centroids):
        if c is None:
            continue
        if prev is not None:
            sim = float(np.dot(c, prev) / (np.linalg.norm(c) * np.linalg.norm(prev)))
            points.append({"minute": b * BIN_MIN, "drift": round(1 - sim, 4)})
        prev = c

    (OUT / "drift.json").write_text(json.dumps({"binMinutes": BIN_MIN, "points": points}))
    top = sorted(points, key=lambda p: -p["drift"])[:6]
    print("drift peaks at minutes:", [p["minute"] for p in top])


if __name__ == "__main__":
    main()
