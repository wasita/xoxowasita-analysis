"""Chat sentiment over time.

VADER compound score per message (VADER is tuned for social-media text:
capitalization, punctuation emphasis, emoji, slang), averaged into 2-minute
bins. Also surfaces the most positive and most negative messages for the
dashboard callouts. Sarcasm and affectionate roasting will read as negative —
that's part of the fun and the caption says so.
"""

import json
from pathlib import Path

import polars as pl
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

ROOT = Path(__file__).parent.parent
OUT = ROOT / "data" / "processed"

EVENT_END_MIN = 72
BIN_MIN = 2


def main() -> None:
    messages = pl.read_parquet(OUT / "messages.parquet").filter(
        pl.col("minutes") <= EVENT_END_MIN
    )
    analyzer = SentimentIntensityAnalyzer()

    scored = [
        {
            "id": r["id"],
            "minutes": r["minutes"],
            "compound": analyzer.polarity_scores(r["text"])["compound"],
        }
        for r in messages.iter_rows(named=True)
    ]

    n_bins = EVENT_END_MIN // BIN_MIN
    bins = []
    for b in range(n_bins):
        lo, hi = b * BIN_MIN, (b + 1) * BIN_MIN
        vals = [s["compound"] for s in scored if lo <= s["minutes"] < hi]
        bins.append(
            {
                "minute": lo,
                "mean": round(sum(vals) / len(vals), 3) if vals else None,
                "n": len(vals),
            }
        )

    by_score = sorted(scored, key=lambda s: s["compound"])
    out = {
        "binMinutes": BIN_MIN,
        "bins": bins,
        "mostNegative": [s["id"] for s in by_score[:3]],
        "mostPositive": [s["id"] for s in by_score[-3:][::-1]],
        "overallMean": round(sum(s["compound"] for s in scored) / len(scored), 3),
    }
    (OUT / "sentiment.json").write_text(json.dumps(out))

    msg_text = dict(zip(messages["id"], messages["text"]))
    print("overall mean compound:", out["overallMean"])
    print("most negative:")
    for mid in out["mostNegative"]:
        print("  ", msg_text[mid][:60])
    print("most positive:")
    for mid in out["mostPositive"]:
        print("  ", msg_text[mid][:60])


if __name__ == "__main__":
    main()
