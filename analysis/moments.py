"""Detect collective moments: bursts where the room reacted as one.

A burst = a sliding 60-second window whose (message + reaction) count z-scores
above threshold vs the event baseline. Overlapping windows merge. Each burst
gets its trigger: the most-reacted message inside it. Also: the laugh
leaderboard (😂 received) and thread response latencies.
"""

import json
from pathlib import Path

import numpy as np
import polars as pl

ROOT = Path(__file__).parent.parent
OUT = ROOT / "data" / "processed"

EVENT_END_MIN = 72
Z_THRESHOLD = 1.6
LAUGH = {"😂", "🤣"}


def main() -> None:
    messages = pl.read_parquet(OUT / "messages.parquet").filter(
        pl.col("minutes") <= EVENT_END_MIN
    )
    reactions = pl.read_parquet(OUT / "reactions.parquet")

    # Activity signal: messages + reactions (reaction time proxied by its message).
    step = 0.25  # 15 s hop, 60 s window
    starts = np.arange(0, EVENT_END_MIN - 1 + step, step)
    minutes = messages["minutes"].to_numpy()
    weights = 1 + messages["reaction_count"].to_numpy()
    activity = np.array(
        [weights[(minutes >= s) & (minutes < s + 1)].sum() for s in starts]
    )
    z = (activity - activity.mean()) / activity.std()

    # Merge overlapping hot windows into bursts.
    hot = z >= Z_THRESHOLD
    bursts: list[dict] = []
    i = 0
    while i < len(starts):
        if not hot[i]:
            i += 1
            continue
        j = i
        while j + 1 < len(starts) and hot[j + 1]:
            j += 1
        s, e = float(starts[i]), float(starts[j] + 1)
        window = messages.filter((pl.col("minutes") >= s) & (pl.col("minutes") < e))
        trigger = window.sort("reaction_count", descending=True).head(1)
        bursts.append(
            {
                "start": round(s, 2),
                "end": round(e, 2),
                "peakZ": round(float(z[i : j + 1].max()), 2),
                "nMessages": window.height,
                "nReactions": int(window["reaction_count"].sum()),
                "triggerId": trigger["id"][0] if trigger.height else None,
            }
        )
        i = j + 1

    # Laugh leaderboard: 😂/🤣 received per author.
    author_of = dict(zip(messages["id"], messages["name"]))
    laughs = (
        reactions.filter(pl.col("emoji").is_in(LAUGH))
        .with_columns(pl.col("msg_id").replace_strict(author_of, default=None).alias("author"))
        .drop_nulls("author")
        .group_by("author")
        .len()
        .sort("len", descending=True)
    )

    # Thread response latency (reply ts − parent ts), seconds.
    parents = messages.select(pl.col("id"), pl.col("ts").alias("parent_ts"))
    lat = (
        messages.filter(pl.col("parent_id").is_not_null())
        .join(parents, left_on="parent_id", right_on="id")
        .with_columns(((pl.col("ts") - pl.col("parent_ts")) / 1000).alias("latency_s"))
    )["latency_s"]

    out = {
        "bursts": bursts,
        "laughLeaders": [
            {"name": r["author"], "laughs": r["len"]} for r in laughs.head(8).iter_rows(named=True)
        ],
        "threadLatency": {
            "median_s": round(float(lat.median()), 1),
            "p25_s": round(float(lat.quantile(0.25)), 1),
            "p75_s": round(float(lat.quantile(0.75)), 1),
            "n": lat.len(),
        },
    }
    (OUT / "moments.json").write_text(json.dumps(out, ensure_ascii=False))

    print(f"{len(bursts)} bursts (z ≥ {Z_THRESHOLD}):")
    for b in bursts:
        print(f"  {b['start']:5.1f}–{b['end']:5.1f} min  z={b['peakZ']:4.1f}  {b['nMessages']} msgs")
    print("laughs:", [(r['name'], r['laughs']) for r in out['laughLeaders'][:5]])
    print("thread latency:", out["threadLatency"])


if __name__ == "__main__":
    main()
