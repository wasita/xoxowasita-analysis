"""Speaker-to-speaker responsivity: who takes the floor after whom.

Turn-taking streams: the main room (thread replies excluded) plus each thread,
as separate chronological sequences. A transition A→B (B speaks right after A,
B ≠ A) counts toward the directed edge B→A ("B responds to A").

Raw counts favor busy people, so each edge also carries a responsivity ratio:
    ratio = P(next speaker is B | previous is A) / P(any turn is B's)
ratio > 1 means B follows A more than B's overall chattiness predicts.
"""

import json
from collections import Counter
from pathlib import Path

import networkx as nx
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

    edges = []
    for (a, b), n in transitions.items():
        if n < MIN_COUNT:
            continue
        expected = after[a] * (turns[b] / total_turns)
        edges.append(
            {
                "source": b,  # B responds to A: edge B -> A
                "target": a,
                "count": n,
                "ratio": round(n / expected, 2) if expected > 0 else None,
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
