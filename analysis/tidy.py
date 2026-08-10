"""Tidy the raw RTDB snapshot into analysis tables and the dashboard bundle.

Inputs:  data/raw/export-latest.json
Outputs: data/processed/messages.parquet   one row per message
         data/processed/reactions.parquet  one row per (message, emoji, reactor)
         data/processed/chat.json          everything the dashboard needs

Notes on the schema (see ljchang/xoxowasita):
- /messages/{pushId}: { name, text, ts, parentId? }  parentId ⇒ thread reply
- /reactions/{msgId}/{emoji}/{clientId}: reactor name
- Reactions carry no timestamp; any reaction timeline must proxy through the
  parent message's ts.
"""

import json
from pathlib import Path

import polars as pl

ROOT = Path(__file__).parent.parent
RAW = ROOT / "data" / "raw" / "export-latest.json"
OUT = ROOT / "data" / "processed"


def load_tables() -> tuple[pl.DataFrame, pl.DataFrame]:
    raw = json.loads(RAW.read_text())

    messages = pl.DataFrame(
        [
            {
                "id": mid,
                "name": m["name"],
                "text": m["text"],
                "ts": m["ts"],
                "parent_id": m.get("parentId"),
            }
            for mid, m in raw["messages"].items()
        ]
    ).sort("ts")

    reactions = pl.DataFrame(
        [
            {"msg_id": mid, "emoji": emoji, "client_id": cid, "reactor": name}
            for mid, emojis in raw.get("reactions", {}).items()
            for emoji, users in emojis.items()
            for cid, name in users.items()
        ]
    )
    # One person on two devices gets two clientIds and can double-react;
    # a reaction is one human's tap, so dedupe on (message, emoji, name).
    reactions = reactions.unique(subset=["msg_id", "emoji", "reactor"], keep="first")
    return messages, reactions


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    messages, reactions = load_tables()

    t0 = messages["ts"].min()
    reaction_counts = reactions.group_by("msg_id").len().rename({"len": "reaction_count"})
    reply_counts = (
        messages.filter(pl.col("parent_id").is_not_null())
        .group_by("parent_id")
        .len()
        .rename({"parent_id": "id", "len": "reply_count"})
    )

    messages = (
        messages.join(reaction_counts, left_on="id", right_on="msg_id", how="left")
        .join(reply_counts, on="id", how="left")
        .with_columns(
            pl.col("reaction_count").fill_null(0),
            pl.col("reply_count").fill_null(0),
            pl.from_epoch("ts", time_unit="ms").alias("datetime"),
            ((pl.col("ts") - t0) / 60_000).alias("minutes"),
        )
    )

    # Attach the message timestamp to each reaction (proxy — see module docstring).
    reactions = reactions.join(
        messages.select("id", "ts", "minutes"), left_on="msg_id", right_on="id"
    )

    messages.write_parquet(OUT / "messages.parquet")
    reactions.write_parquet(OUT / "reactions.parquet")

    # Dashboard bundle: messages with reactions nested, plus event metadata.
    rx_by_msg: dict[str, dict[str, list[str]]] = {}
    for row in reactions.iter_rows(named=True):
        rx_by_msg.setdefault(row["msg_id"], {}).setdefault(row["emoji"], []).append(
            row["reactor"]
        )

    bundle = {
        "meta": {
            "t0": int(t0),
            "n_messages": messages.height,
            "n_authors": messages["name"].n_unique(),
            "n_reactions": reactions.height,
            "n_replies": int(messages["parent_id"].is_not_null().sum()),
        },
        "messages": [
            {
                "id": r["id"],
                "name": r["name"],
                "text": r["text"],
                "ts": r["ts"],
                "minutes": round(r["minutes"], 3),
                "parentId": r["parent_id"],
                "replyCount": r["reply_count"],
                "reactions": rx_by_msg.get(r["id"], {}),
            }
            for r in messages.iter_rows(named=True)
        ],
    }
    (OUT / "chat.json").write_text(json.dumps(bundle, ensure_ascii=False))

    print(
        f"{messages.height} messages, {reactions.height} reactions, "
        f"{messages['name'].n_unique()} authors → {OUT}"
    )


if __name__ == "__main__":
    main()
