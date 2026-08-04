"""Affect trajectory: what the room felt, minute by minute, via emoji.

Every reaction emoji is mapped to one affect family (assignments below are a
judgment call, documented here). Counts per 2-minute bin, reaction time
proxied by the reacted-to message's timestamp. Message-text affect is left
alone — the emoji channel is the clean signal.
"""

import json
from pathlib import Path

import polars as pl

ROOT = Path(__file__).parent.parent
OUT = ROOT / "data" / "processed"

EVENT_END_MIN = 72
BIN_MIN = 2

FAMILIES: dict[str, dict] = {
    "love": {"label": "love", "glyphs": ["💜", "🤍", "❤️", "💕", "✨", "🥰"]},
    "laugh": {"label": "laughter", "glyphs": ["😂", "🤣"]},
    "awe": {"label": "awe & fire", "glyphs": ["💯", "🔥", "😮", "🤯", "🧠", "🦄"]},
    "verklempt": {"label": "happy tears", "glyphs": ["🥹", "😭", "🥺"]},
    "cheer": {"label": "applause", "glyphs": ["👏", "🎉", "🥳", "🙌", "💪", "👍"]},
}


def main() -> None:
    reactions = pl.read_parquet(OUT / "reactions.parquet").filter(
        pl.col("minutes") <= EVENT_END_MIN
    )
    family_of = {g: fam for fam, d in FAMILIES.items() for g in d["glyphs"]}
    n_bins = EVENT_END_MIN // BIN_MIN

    series = {fam: [0] * n_bins for fam in FAMILIES}
    other = 0
    for row in reactions.iter_rows(named=True):
        fam = family_of.get(row["emoji"])
        if fam is None:
            other += 1
            continue
        series[fam][min(int(row["minutes"] // BIN_MIN), n_bins - 1)] += 1

    out = {
        "binMinutes": BIN_MIN,
        "families": [
            {
                "key": fam,
                "label": d["label"],
                "glyph": d["glyphs"][0],
                "total": sum(series[fam]),
                "bins": series[fam],
            }
            for fam, d in FAMILIES.items()
        ],
        "unmapped": other,
    }
    (OUT / "affect.json").write_text(json.dumps(out, ensure_ascii=False))

    for f in out["families"]:
        print(f"{f['glyph']} {f['label']:12} {f['total']}")
    print("unmapped:", other)


if __name__ == "__main__":
    main()
