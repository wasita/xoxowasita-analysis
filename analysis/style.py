"""Author style map: who *types* alike — linguistic style, not topic.

Instead of semantic embeddings (which cluster people by what they discussed),
each author gets an interpretable style vector built from how they write:
paralinguistics (CAPS, !!!, letter-stretching, emoji, laughter, slang) and
function-word rates in the Language Style Matching tradition (pronouns,
articles). Features are z-scored across authors; UMAP lays out the z-matrix.

Only authors with enough signal are mapped (≥ MIN_MESSAGES messages or
≥ MIN_WORDS words). Each author also gets their most distinctive traits
(largest |z|) and their nearest style twin (euclidean in z-space).
"""

import json
import re
from pathlib import Path

import numpy as np
import polars as pl
import umap

ROOT = Path(__file__).parent.parent
OUT = ROOT / "data" / "processed"

MIN_MESSAGES = 5
MIN_WORDS = 25
SEED = 42

WORD_RE = re.compile(r"[A-Za-z']+")
STRETCH_RE = re.compile(r"([A-Za-z])\1{2,}")
LAUGH_RE = re.compile(r"\b(l+o+l+\w*|lmao+\w*|(a?ha){2,}\w*|lolol\w*)\b", re.I)
SLANG = {
    "omg", "omh", "rn", "ngl", "iykyk", "fr", "tho", "bc", "idk", "btw", "af",
    "ftw", "imo", "tbh", "yall", "gonna", "wanna", "gotta", "def", "v", "u",
    "ur", "plz", "pls", "bruh", "og", "ily", "bff", "srsly", "obvi", "legit",
}
NO_APOSTROPHE = {
    "im", "dont", "cant", "didnt", "isnt", "thats", "whats", "ive", "youre",
    "hes", "shes", "wont", "lets", "wasnt", "couldnt", "shouldnt", "its",
}
FIRST_PERSON = {"i", "me", "my", "mine", "im", "ive", "id"}
SECOND_PERSON = {"you", "u", "your", "ur", "youre", "yall"}
ARTICLES = {"a", "an", "the"}


def is_emoji(ch: str) -> bool:
    cp = ord(ch)
    return (
        0x1F000 <= cp <= 0x1FAFF
        or 0x2600 <= cp <= 0x27BF
        or cp in (0x2764, 0x2B50, 0x203C)
    )


# feature key -> (plain label when high, plain label when low)
FEATURES: dict[str, tuple[str, str]] = {
    "words_per_msg": ("writes long messages", "keeps it terse"),
    "caps": ("ALL-CAPS ENERGY", "never shouts"),
    "exclaim": ("exclamation!!! heavy", "no exclamation marks"),
    "stretch": ("letter-stretcherrrr", "never stretches words"),
    "laugh": ("lol/haha on tap", "laughs off-keyboard"),
    "slang": ("fluent internet slang", "writes it out properly"),
    "ellipsis": ("trailing … pauses", "no dramatic pauses"),
    "question": ("asks questions", "all statements"),
    "emoji": ("emoji mid-sentence", "text only"),
    "lower_i": ("lowercase i", "capital I"),
    "no_apos": ("drops apostrophes", "keeps apostrophes"),
    "first_person": ("talks about I/me", "rarely self-refers"),
    "second_person": ("addresses you/u", "rarely addresses others"),
    "articles": ("full articles (a/an/the)", "article-free fragments"),
}


def author_features(texts: list[str]) -> dict[str, float] | None:
    n_msgs = len(texts)
    words = [w for t in texts for w in WORD_RE.findall(t)]
    lower = [w.lower().replace("'", "") for w in words]
    n_words = len(words)
    if n_msgs < MIN_MESSAGES and n_words < MIN_WORDS:
        return None

    alpha_words = [w for w in words if len(w) >= 2 and w.isalpha()]
    i_tokens = [w for w in words if w.lower() == "i"]

    return {
        "words_per_msg": n_words / n_msgs,
        "caps": sum(w.isupper() for w in alpha_words) / max(len(alpha_words), 1),
        "exclaim": sum(t.count("!") for t in texts) / n_msgs,
        "stretch": sum(bool(STRETCH_RE.search(t)) for t in texts) / n_msgs,
        "laugh": sum(bool(LAUGH_RE.search(t)) for t in texts) / n_msgs,
        "slang": sum(w in SLANG for w in lower) / n_words,
        "ellipsis": sum(("..." in t) or ("…" in t) for t in texts) / n_msgs,
        "question": sum("?" in t for t in texts) / n_msgs,
        "emoji": sum(is_emoji(c) for t in texts for c in t) / n_msgs,
        "lower_i": sum(w == "i" for w in i_tokens) / len(i_tokens) if i_tokens else np.nan,
        "no_apos": sum(w in NO_APOSTROPHE for w in lower) / n_words,
        "first_person": sum(w in FIRST_PERSON for w in lower) / n_words,
        "second_person": sum(w in SECOND_PERSON for w in lower) / n_words,
        "articles": sum(w in ARTICLES for w in lower) / n_words,
    }


def describe(z: float, high: str, low: str) -> str:
    label = high if z > 0 else low
    strength = "way" if abs(z) >= 2 else ""
    return f"{label} ({strength} {'above' if z > 0 else 'below'} room average)".replace("( ", "(")


def main() -> None:
    messages = pl.read_parquet(OUT / "messages.parquet")

    texts_by_author: dict[str, list[str]] = {}
    for row in messages.iter_rows(named=True):
        texts_by_author.setdefault(row["name"], []).append(row["text"])

    feats = {
        a: f for a, t in texts_by_author.items() if (f := author_features(t)) is not None
    }
    authors = sorted(feats)
    keys = list(FEATURES)
    X = np.array([[feats[a][k] for k in keys] for a in authors])

    # NaN (e.g. never used "i") -> column mean, then z-score, clip tails.
    col_mean = np.nanmean(X, axis=0)
    X = np.where(np.isnan(X), col_mean, X)
    Z = np.clip((X - X.mean(axis=0)) / X.std(axis=0), -3, 3)

    coords = umap.UMAP(
        n_neighbors=min(8, len(authors) - 1),
        min_dist=0.3,
        metric="euclidean",
        random_state=SEED,
    ).fit_transform(Z)

    dists = np.linalg.norm(Z[:, None, :] - Z[None, :, :], axis=2)
    np.fill_diagonal(dists, np.inf)
    twin = {a: authors[int(np.argmin(dists[i]))] for i, a in enumerate(authors)}

    stats = {
        r["name"]: r
        for r in messages.group_by("name")
        .agg(pl.len().alias("n"), pl.col("reaction_count").sum().alias("rx"))
        .iter_rows(named=True)
    }
    best_msg: dict[str, str] = {}
    for row in messages.sort("reaction_count", descending=True).iter_rows(named=True):
        best_msg.setdefault(row["name"], row["text"])

    out = {
        "minMessages": MIN_MESSAGES,
        "minWords": MIN_WORDS,
        "authors": [
            {
                "name": a,
                "x": round(float(x), 4),
                "y": round(float(y), 4),
                "messages": stats[a]["n"],
                "reactionsReceived": stats[a]["rx"],
                "sample": best_msg[a],
                "styleTwin": twin[a],
                "traits": [
                    {
                        "text": describe(Z[i, j], *FEATURES[keys[j]]),
                        "z": round(float(Z[i, j]), 2),
                    }
                    for j in np.argsort(-np.abs(Z[i]))[:3]
                ],
            }
            for i, (a, (x, y)) in enumerate(zip(authors, coords))
        ],
    }
    (OUT / "authors.json").write_text(json.dumps(out, ensure_ascii=False))

    print(f"{len(authors)} authors mapped (≥{MIN_MESSAGES} msgs or ≥{MIN_WORDS} words)")
    for a in authors[:8]:
        entry = next(e for e in out["authors"] if e["name"] == a)
        print(f"  {a:16} twin={entry['styleTwin']:16} {entry['traits'][0]['text']}")


if __name__ == "__main__":
    main()
