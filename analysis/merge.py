"""Merge hand labels + UMAP coords + segments into the dashboard bundle.

Rewrites data/processed/topics.json (hand labels replace the failed
unsupervised clusters) and writes segments.json. Asserts label alignment
against the message author sequence.
"""

import json
from pathlib import Path

import polars as pl

from labels import LABELS, TOPICS
from segments import SEGMENTS, VERDICT

ROOT = Path(__file__).parent.parent
OUT = ROOT / "data" / "processed"


def main() -> None:
    messages = pl.read_parquet(OUT / "messages.parquet")
    assert messages.height == len(LABELS), f"{messages.height} msgs vs {len(LABELS)} labels"

    mismatches = [
        (i, row_name, label_name)
        for i, (row_name, (label_name, _)) in enumerate(
            zip(messages["name"], LABELS)
        )
        if row_name != label_name
    ]
    assert not mismatches, f"label misalignment at rows: {mismatches[:5]}"

    umap_points = {
        p["id"]: p for p in json.loads((OUT / "topics.json").read_text())["points"]
    }
    points = [
        {
            "id": mid,
            "x": umap_points[mid]["x"],
            "y": umap_points[mid]["y"],
            "topic": topic,
        }
        for mid, (_, topic) in zip(messages["id"], LABELS)
    ]
    (OUT / "topics.json").write_text(
        json.dumps({"topics": TOPICS, "points": points}, ensure_ascii=False)
    )
    (OUT / "segments.json").write_text(
        json.dumps({"segments": SEGMENTS, "verdict": VERDICT}, ensure_ascii=False)
    )

    counts = pl.Series([t for _, t in LABELS]).value_counts(sort=True)
    print(counts)
    print(f"{len(SEGMENTS)} segments written")


if __name__ == "__main__":
    main()
