"""Embed chat messages, project to 2D, and cluster into topics.

Outputs data/processed/topics.json: per-message UMAP coordinates and cluster
assignments. Cluster labels are added afterwards (human/LLM pass over the
clustered messages) in topic_labels.json and merged by the dashboard.
"""

import json
from pathlib import Path

import hdbscan
import numpy as np
import polars as pl
import umap
from sentence_transformers import SentenceTransformer

ROOT = Path(__file__).parent.parent
OUT = ROOT / "data" / "processed"

SEED = 42
MODEL = "all-MiniLM-L6-v2"


def main() -> None:
    messages = pl.read_parquet(OUT / "messages.parquet")
    texts = messages["text"].to_list()

    model = SentenceTransformer(MODEL)
    emb = model.encode(texts, normalize_embeddings=True, show_progress_bar=True)

    # 2D layout for the dashboard scatter.
    coords = umap.UMAP(
        n_neighbors=15, min_dist=0.1, metric="cosine", random_state=SEED
    ).fit_transform(emb)

    # Cluster in a mid-dimensional projection (more stable than raw 384-d
    # or the 2-d layout for HDBSCAN on short texts).
    emb5 = umap.UMAP(
        n_components=5, n_neighbors=15, min_dist=0.0, metric="cosine", random_state=SEED
    ).fit_transform(emb)
    labels = hdbscan.HDBSCAN(min_cluster_size=6, min_samples=2).fit_predict(emb5)

    np.save(OUT / "embeddings.npy", emb)

    out = {
        "model": MODEL,
        "points": [
            {
                "id": mid,
                "x": round(float(x), 4),
                "y": round(float(y), 4),
                "cluster": int(c),
            }
            for mid, (x, y), c in zip(messages["id"], coords, labels)
        ],
    }
    (OUT / "topics.json").write_text(json.dumps(out))

    n_clusters = len(set(labels) - {-1})
    n_noise = int((labels == -1).sum())
    print(f"{n_clusters} clusters, {n_noise} noise points of {len(labels)}")
    for c in sorted(set(labels) - {-1}):
        idx = np.where(labels == c)[0]
        sample = [texts[i][:60] for i in idx[:5]]
        print(f"\n— cluster {c} ({len(idx)} msgs) —")
        for s in sample:
            print(f"   {s}")


if __name__ == "__main__":
    main()
