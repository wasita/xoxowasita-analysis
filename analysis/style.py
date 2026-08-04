"""Author style map: who writes alike.

Per-author centroid of message embeddings (authors with ≥ 3 messages), then
UMAP to 2D. Nearby authors = similar voice.
"""

import json
from pathlib import Path

import numpy as np
import polars as pl
import umap

ROOT = Path(__file__).parent.parent
OUT = ROOT / "data" / "processed"

MIN_MESSAGES = 3
SEED = 42


def main() -> None:
    messages = pl.read_parquet(OUT / "messages.parquet")
    emb = np.load(OUT / "embeddings.npy")

    names = messages["name"].to_list()
    reactions_by_author = (
        messages.group_by("name")
        .agg(pl.len().alias("n"), pl.col("reaction_count").sum().alias("rx"))
    )
    stats = {r["name"]: r for r in reactions_by_author.iter_rows(named=True)}

    authors = sorted({n for n in names if stats[n]["n"] >= MIN_MESSAGES})
    centroids = np.stack(
        [emb[[i for i, n in enumerate(names) if n == a]].mean(axis=0) for a in authors]
    )

    coords = umap.UMAP(
        n_neighbors=8, min_dist=0.3, metric="cosine", random_state=SEED
    ).fit_transform(centroids)

    # A representative message: the author's most-reacted.
    best_msg: dict[str, str] = {}
    for row in messages.sort("reaction_count", descending=True).iter_rows(named=True):
        best_msg.setdefault(row["name"], row["text"])

    out = {
        "minMessages": MIN_MESSAGES,
        "authors": [
            {
                "name": a,
                "x": round(float(x), 4),
                "y": round(float(y), 4),
                "messages": stats[a]["n"],
                "reactionsReceived": stats[a]["rx"],
                "sample": best_msg[a],
            }
            for a, (x, y) in zip(authors, coords)
        ],
    }
    (OUT / "authors.json").write_text(json.dumps(out, ensure_ascii=False))
    print(f"{len(authors)} authors with ≥{MIN_MESSAGES} messages")


if __name__ == "__main__":
    main()
