"""Chat↔talk coupling: Wasita's study 2 method, turned on her own defense.

Every chat message is scored by cosine similarity between its embedding and
the embedding of what was being said on stage around that moment (the
containing 1-minute transcript window and the one before it — reactions lag).
Same MiniLM model as the message embeddings.

The transcript lives in data/local/ (never committed); this script emits only
derived scores. Talk windows exist for chat minutes 0–66; later messages are
unscored.
"""

import json
import re
from pathlib import Path

import numpy as np
import polars as pl
from sentence_transformers import SentenceTransformer

ROOT = Path(__file__).parent.parent
OUT = ROOT / "data" / "processed"
VTT = ROOT / "data" / "local" / "GMT20260710-190125_Recording.transcript.vtt"

OFFSET_MIN = 17.01  # recording start (19:01:25 GMT) → first chat message (15:18:25 EDT)
MODEL = "all-MiniLM-L6-v2"
MIN_MESSAGES = 5
BIN_MIN = 2


def talk_windows() -> dict[int, str]:
    """Transcript text per 1-minute window on the chat clock."""
    raw = VTT.read_text()
    cues = re.findall(r"(\d\d):(\d\d):(\d\d)\.\d+ --> .*?\n(?:.*?: )?(.*?)\n", raw)
    windows: dict[int, list[str]] = {}
    for h, m, s, text in cues:
        chat_min = int(h) * 60 + int(m) + int(s) / 60 - OFFSET_MIN
        windows.setdefault(int(chat_min // 1), []).append(text.strip())
    return {k: " ".join(v) for k, v in windows.items() if k >= 0}


# Hand-written paraphrases of what was on stage per 2-minute bin (no verbatim
# transcript text ships — same disclosure level as the public segment cards).
BLURBS: dict[int, str] = {
    0: "She opens: how do two strangers become close? Tumblr and the freshman STEM crew",
    2: "The Surgeon General's loneliness stakes; three routes to connection in the literature",
    4: "Control vs naturalism — “nobody connects with a survey” — choosing both",
    6: "The framework: connection as inference through conversation; three-study roadmap",
    8: "Wedding small talk as foraging; the Chris & Phoebe Bridgers story",
    10: "Study 1 design: three-minute chats about one topic, guessing all the rest",
    12: "Study 1 results: one agreement spreads to related topics",
    14: "Conversation repairs bad first impressions; two candidate models of the mind",
    16: "The population mental-map model wins; back to Chris",
    18: "The shared-experience gap; pandemic Slack with Alexis & Clara",
    20: "Building the co-watching app pre-LLM (“raw dogging it”); Love Is Blind",
    22: "Strangers hit friend-level connection; replies and word echoes",
    24: "The secret stream split: Shane between Natalie and Shaina",
    26: "Scoring each chat message against the show's moment",
    28: "The connection boost switches on exactly when screens diverge",
    30: "Blaming minds, not screens; into study 3",
    32: "Mohegan Sun, Krispy Kreme, and Sush's “I can relate”; the disclosure game",
    34: "Relating beats having lived it",
    36: "Rare commonalities count more — they're diagnostic",
    38: "Synthesis: inference through conversation; the two friendships",
    40: "Closing line and applause",
    42: "Thank yous: the committee",
    44: "Thank yous: Thalia; Luke's slide",
    46: "Thank yous: Luke, and Eunice",
    48: "Thank yous: Eshin; the lab",
    50: "Thank yous: the lab, TK stories",
    52: "Thank yous: Grace, Sush, the cohort",
    54: "Thank yous: Alexis; summer schools and Chris",
    56: "Thank yous: Cosmos and the Frank Lab",
    58: "Thank yous: Liz, Romy, Amitai, Jay",
    60: "Thank yous: Noah, Joji the cat, Jackie",
    62: "Thank yous: Lori the English teacher, James, her cousin, her parents",
    64: "Severely over time; reception announced; goodbyes",
    66: "Goodbyes",
}


def main() -> None:
    if not VTT.exists():
        raise SystemExit(f"transcript not found at {VTT} (local-only file)")

    messages = pl.read_parquet(OUT / "messages.parquet")
    msg_emb = np.load(OUT / "embeddings.npy")  # normalized, same model

    windows = talk_windows()
    keys = sorted(windows)
    model = SentenceTransformer(MODEL)
    win_emb = model.encode([windows[k] for k in keys], normalize_embeddings=True)
    win_index = {k: i for i, k in enumerate(keys)}

    scores: list[float | None] = []
    for row, emb in zip(messages.iter_rows(named=True), msg_emb):
        minute = int(row["minutes"] // 1)
        idxs = [win_index[m] for m in (minute - 1, minute) if m in win_index]
        scores.append(
            round(float(max(np.dot(emb, win_emb[i]) for i in idxs)), 4) if idxs else None
        )

    scored = messages.with_columns(pl.Series("coupling", scores)).drop_nulls("coupling")

    # Room coupling per 2-minute bin, with an on-stage blurb and the two
    # best-coupled chat messages as hover samples.
    bins = []
    for b in range(0, 68, BIN_MIN):
        in_bin = scored.filter(
            (pl.col("minutes") >= b) & (pl.col("minutes") < b + BIN_MIN)
        )
        vals = in_bin["coupling"]
        bins.append(
            {
                "minute": b,
                "mean": round(float(vals.mean()), 4) if len(vals) else None,
                "n": len(vals),
                "blurb": BLURBS.get(b),
                "samples": in_bin.sort("coupling", descending=True).head(2)["id"].to_list(),
            }
        )

    # Per-person mean coupling.
    people = (
        scored.group_by("name")
        .agg(pl.len().alias("n"), pl.col("coupling").mean().round(4).alias("mean"))
        .filter(pl.col("n") >= MIN_MESSAGES)
        .sort("mean", descending=True)
    )

    top = scored.sort("coupling", descending=True).head(5)
    bottom = scored.sort("coupling").head(5)

    out = {
        "binMinutes": BIN_MIN,
        "bins": bins,
        "people": people.to_dicts(),
        "mostCoupled": top["id"].to_list(),
        "leastCoupled": bottom["id"].to_list(),
        "overallMean": round(float(scored["coupling"].mean()), 4),
    }
    (OUT / "coupling.json").write_text(json.dumps(out))

    print(f"scored {scored.height} messages, overall mean {out['overallMean']}")
    print("most on-topic people:", [(p['name'], p['mean']) for p in out['people'][:5]])
    print("least:", [(p['name'], p['mean']) for p in out['people'][-3:]])


if __name__ == "__main__":
    main()
