"""Speaker-to-speaker responsivity: who takes the floor after whom.

Turn-taking streams: the main room (thread replies excluded) plus each thread,
as separate chronological sequences. A transition A→B (B speaks right after A,
B ≠ A) counts toward the directed edge B→A ("B responds to A").

Raw counts favor busy people, so each edge carries two normalizations:
- ratio = P(next speaker is B | previous is A) / P(any turn is B's);
  ratio > 1 means B follows A more than B's overall chattiness predicts.
- a permutation z: each stream's turn order is shuffled (everyone keeps their
  number of turns), and the observed A→B transition count is z-scored against
  that null. z gates what the dashboard draws as solid.
"""

import json
from collections import Counter
from pathlib import Path

import networkx as nx
import numpy as np
import polars as pl

ROOT = Path(__file__).parent.parent
OUT = ROOT / "data" / "processed"

SEED = 42
MIN_COUNT = 2


def main() -> None:
    messages = pl.read_parquet(OUT / "messages.parquet").sort("ts")

    streams: list[list[str]] = [
        messages.filter(pl.col("parent_id").is_null())["name"].to_list()
    ]
    for _, thread in messages.filter(pl.col("parent_id").is_not_null()).group_by(
        "parent_id"
    ):
        streams.append(thread.sort("ts")["name"].to_list())

    transitions: Counter[tuple[str, str]] = Counter()  # (prev A, next B)
    turns: Counter[str] = Counter()
    for seq in streams:
        turns.update(seq)
        for a, b in zip(seq, seq[1:]):
            if a != b:
                transitions[(a, b)] += 1

    total_turns = sum(turns.values())
    after: Counter[str] = Counter()  # transitions out of A
    for (a, _), n in transitions.items():
        after[a] += n

    # Permutation null: shuffle each stream's order (turn counts preserved).
    N_PERM = 2000
    rng = np.random.default_rng(42)
    null_counts: dict[tuple[str, str], list[int]] = {k: [] for k in transitions}
    perm_streams = [list(s) for s in streams]
    for _ in range(N_PERM):
        perm: Counter[tuple[str, str]] = Counter()
        for seq in perm_streams:
            rng.shuffle(seq)
            for a, b in zip(seq, seq[1:]):
                if a != b:
                    perm[(a, b)] += 1
        for k in null_counts:
            null_counts[k].append(perm.get(k, 0))

    edges = []
    for (a, b), n in transitions.items():
        if n < MIN_COUNT:
            continue
        expected = after[a] * (turns[b] / total_turns)
        null = np.array(null_counts[(a, b)])
        sd = null.std()
        z = (n - null.mean()) / sd if sd > 0 else 0.0
        edges.append(
            {
                "source": b,  # B responds to A: edge B -> A
                "target": a,
                "count": n,
                "ratio": round(n / expected, 2) if expected > 0 else None,
                "z": round(float(z), 2),
            }
        )
    edges.sort(key=lambda e: -e["count"])

    G = nx.DiGraph()
    for e in edges:
        G.add_edge(e["source"], e["target"], weight=e["count"])
    pos = nx.spring_layout(G.to_undirected(), weight="weight", seed=SEED, k=0.5, iterations=300)

    out = {
        "nodes": [
            {
                "name": n,
                "x": round(float(pos[n][0]), 4),
                "y": round(float(pos[n][1]), 4),
                "turns": turns[n],
            }
            for n in G.nodes
        ],
        "edges": edges,
    }
    (OUT / "responsivity.json").write_text(json.dumps(out, ensure_ascii=False))

    print(f"{G.number_of_nodes()} speakers, {len(edges)} edges (count ≥ {MIN_COUNT})")
    for e in edges[:10]:
        print(f"  {e['source']:16} → {e['target']:16} ×{e['count']}  ratio {e['ratio']}")


if __name__ == "__main__":
    main()
