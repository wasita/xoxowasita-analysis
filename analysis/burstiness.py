"""Author burstiness: steady commentators vs spike-posters.

Goh–Barabási burstiness index over an author's inter-message intervals:
    B = (σ − μ) / (σ + μ)   ∈ [−1, 1]
B → −1: metronome. B ≈ 0: Poisson-random. B → 1: silence, then a flurry.
Only authors with ≥ 5 messages inside the live event (intervals need n−1 ≥ 4).
"""

import json
from pathlib import Path

import numpy as np
import polars as pl

ROOT = Path(__file__).parent.parent
OUT = ROOT / "data" / "processed"

EVENT_END_MIN = 72
MIN_MESSAGES = 5


def main() -> None:
    messages = pl.read_parquet(OUT / "messages.parquet").filter(
        pl.col("minutes") <= EVENT_END_MIN
    )

    rows = []
    for (name,), group in messages.group_by("name"):
        if group.height < MIN_MESSAGES:
            continue
        t = np.sort(group["minutes"].to_numpy())
        gaps = np.diff(t)
        mu, sigma = gaps.mean(), gaps.std()
        rows.append(
            {
                "name": name,
                "b": round(float((sigma - mu) / (sigma + mu)), 3),
                "messages": group.height,
                "meanGapMin": round(float(mu), 2),
            }
        )
    rows.sort(key=lambda r: -r["b"])

    (OUT / "burstiness.json").write_text(
        json.dumps({"minMessages": MIN_MESSAGES, "authors": rows}, ensure_ascii=False)
    )
    for r in rows[:5] + rows[-3:]:
        print(f"  {r['name']:16} B={r['b']:+.2f}  n={r['messages']}")


if __name__ == "__main__":
    main()
