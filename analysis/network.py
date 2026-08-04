"""Build the audience connection graph from reactions, replies, and @mentions.

Edges are directed acts of attention: A reacted to B's message, A replied in
B's thread, A @mentioned B. Output is an undirected weighted graph for layout
and communities, with the directed counts preserved per edge.
"""

import json
import re
from collections import Counter
from pathlib import Path

import networkx as nx
import polars as pl

ROOT = Path(__file__).parent.parent
OUT = ROOT / "data" / "processed"
SEED = 42


def main() -> None:
    messages = pl.read_parquet(OUT / "messages.parquet")
    reactions = pl.read_parquet(OUT / "reactions.parquet")

    author_of = dict(zip(messages["id"], messages["name"]))
    # Participants = everyone who messaged OR reacted (some people only reacted).
    names = sorted(set(messages["name"]) | set(reactions["reactor"]))

    # Directed edge counts by type. Self-edges dropped throughout.
    edges: Counter[tuple[str, str, str]] = Counter()

    for row in reactions.iter_rows(named=True):
        src, dst = row["reactor"], author_of[row["msg_id"]]
        if src != dst:
            edges[(src, dst, "reaction")] += 1

    for row in messages.filter(pl.col("parent_id").is_not_null()).iter_rows(named=True):
        src, dst = row["name"], author_of.get(row["parent_id"])
        if dst and src != dst:
            edges[(src, dst, "reply")] += 1

    # @mentions: greedy-match known names (longest first — "Alexis :)" before "alexis ;)"
    # doesn't matter here, but "Mark" vs "mark" style prefixes do).
    for row in messages.iter_rows(named=True):
        for name in sorted(names, key=len, reverse=True):
            if f"@{name}" in row["text"] and name != row["name"]:
                edges[(row["name"], name, "mention")] += 1

    # Collapse to undirected weighted pairs for layout/communities.
    G = nx.Graph()
    G.add_nodes_from(names)
    pair_detail: dict[tuple[str, str], dict] = {}
    for (src, dst, kind), n in edges.items():
        key = tuple(sorted((src, dst)))
        d = pair_detail.setdefault(key, {"weight": 0, "reaction": 0, "reply": 0, "mention": 0})
        d["weight"] += n
        d[kind] += n
    for (a, b), d in pair_detail.items():
        G.add_edge(a, b, weight=d["weight"])

    communities = nx.community.louvain_communities(G, weight="weight", seed=SEED)
    community_of = {name: i for i, members in enumerate(communities) for name in members}

    pos = nx.spring_layout(G, weight="weight", seed=SEED, k=0.28, iterations=300)

    sent = Counter(messages["name"].to_list())
    got = Counter(author_of[m] for m in reactions["msg_id"].to_list())
    gave = Counter(reactions["reactor"].to_list())

    out = {
        "nodes": [
            {
                "name": n,
                "x": round(float(pos[n][0]), 4),
                "y": round(float(pos[n][1]), 4),
                "messages": sent.get(n, 0),
                "reactionsReceived": got.get(n, 0),
                "reactionsGiven": gave.get(n, 0),
                "degree": G.degree(n),
                "community": community_of[n],
            }
            for n in names
        ],
        "edges": [
            {"a": a, "b": b, **d}
            for (a, b), d in sorted(pair_detail.items(), key=lambda kv: -kv[1]["weight"])
        ],
        "nCommunities": len(communities),
    }
    (OUT / "network.json").write_text(json.dumps(out, ensure_ascii=False))

    print(f"{G.number_of_nodes()} nodes, {G.number_of_edges()} edges, {len(communities)} communities")
    for i, members in enumerate(communities):
        top = sorted(members, key=lambda n: -sent.get(n, 0))[:6]
        print(f"  community {i} ({len(members)}): {', '.join(top)}")


if __name__ == "__main__":
    main()
