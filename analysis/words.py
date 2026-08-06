"""Word frequencies for the chat wordcloud.

Unigrams plus a few salient bigrams, stopworded, case-folded (display keeps
the most common surface form so WASITA can stay loud).
"""

import json
import re
from collections import Counter
from pathlib import Path

import polars as pl

ROOT = Path(__file__).parent.parent
OUT = ROOT / "data" / "processed"

TOKEN_RE = re.compile(r"[A-Za-z][A-Za-z']+")
STOP = set(
    """the a an and or but if of to in on at for with by from as is are was were be
    been am it its it's this that these those i im i'm me my we our you your u ur
    he she they them his her their so too very just really can cant can't could
    would should will wont won't do dont don't did didnt didn't does doesnt not no
    yes have has had having what who whom when where why how all any some more most
    other than then there here also about into over after before out up down off
    again once only own same such rn one two get got go going gonna wanna oh omg
    lol ok okay yeah yay like love wow now still even ever never always let lets
    let's know think see say said feel feeling""".split()
)
KEEP_BIGRAMS = {
    ("krispy", "kreme"),
    ("love", "is"),  # folded into "love is blind" below
    ("mohegan", "sun"),
    ("dr", "wasita"),
    ("mental", "map"),
}


def main() -> None:
    messages = pl.read_parquet(OUT / "messages.parquet")

    counts: Counter[str] = Counter()
    surface: dict[str, Counter[str]] = {}
    for text in messages["text"]:
        tokens = TOKEN_RE.findall(text)
        lower = [t.lower() for t in tokens]
        for raw, tok in zip(tokens, lower):
            if tok in STOP or len(tok) < 3:
                continue
            counts[tok] += 1
            surface.setdefault(tok, Counter())[raw] += 1
        joined = " ".join(lower)
        for phrase in ("love is blind", "krispy kreme", "mohegan sun", "mental map"):
            if phrase in joined:
                counts[phrase] += 1

    # A phrase absorbs its member words' solo counts where it dominates.
    for phrase in ("love is blind", "krispy kreme", "mohegan sun"):
        for w in phrase.split():
            if w in counts and counts[w] <= counts.get(phrase, 0):
                del counts[w]

    words = [
        {
            "text": surface[w].most_common(1)[0][0] if w in surface else w,
            "count": n,
        }
        for w, n in counts.most_common(90)
        if n >= 2
    ]
    (OUT / "words.json").write_text(json.dumps({"words": words}, ensure_ascii=False))
    print(f"{len(words)} words, top: {[(w['text'], w['count']) for w in words[:12]]}")


if __name__ == "__main__":
    main()
