"""Snapshot the xoxowasita Firebase RTDB into data/raw/.

The database rules expose `.read: true` at the root, so no auth is needed —
this is the same data any audience member's browser streamed during the talk.
"""

from datetime import datetime, timezone
from pathlib import Path

import requests

DB_URL = "https://wasita-defense-chat-default-rtdb.firebaseio.com/.json"
RAW_DIR = Path(__file__).parent.parent / "data" / "raw"


def main() -> None:
    RAW_DIR.mkdir(parents=True, exist_ok=True)
    resp = requests.get(DB_URL, timeout=30)
    resp.raise_for_status()

    stamp = datetime.now(timezone.utc).strftime("%Y%m%d-%H%M%S")
    out = RAW_DIR / f"export-{stamp}.json"
    out.write_bytes(resp.content)

    # Stable name for downstream steps; timestamped copy for provenance.
    latest = RAW_DIR / "export-latest.json"
    latest.write_bytes(resp.content)
    print(f"Wrote {out} ({out.stat().st_size:,} bytes) and {latest.name}")


if __name__ == "__main__":
    main()
