# xoxowasita-analysis

Analysis + dashboard for the [xoxowasita](https://github.com/ljchang/xoxowasita)
defense chat — the real-time audience commentary app [@ljchang](https://github.com/ljchang) built for [@wasita](https://github.com/wasita)'s public dissertation defense (July 10, 2026).

## Layout

```text
analysis/    uv + polars pipeline
  extract.py   snapshot the Firebase RTDB (public read) into data/raw/
  tidy.py      → messages.parquet, reactions.parquet, chat.json
  topics.py    MiniLM embeddings → UMAP coords (+ clustering experiments)
  labels.py    hand-assigned topic per message (unsupervised clustering was mush)
  segments.py  the talk reconstructed from chat alone, segment by segment
  merge.py     validate label alignment, emit topics.json + segments.json
data/        raw export + processed tables (committed; the DB is world-readable)
dashboard/   SvelteKit + Tailwind v4 + LayerChart static site
```

## Run the pipeline

```bash
cd analysis
uv run extract.py && uv run tidy.py && uv run topics.py && uv run merge.py
cp ../data/processed/{chat,topics,segments}.json ../dashboard/src/lib/data/
```

## Run the dashboard

```bash
cd dashboard
npm install
npm run dev      # or: npm run build && npm run preview
```

Deploys to GitHub Pages on push to `main` (`.github/workflows/deploy.yml`).
The site is unlisted: `noindex` meta + `robots.txt` disallow.
Enable once in repo Settings → Pages → Source: **GitHub Actions**.
