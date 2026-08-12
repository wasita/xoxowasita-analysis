# HANDOFF — xoxowasita-analysis

_Snapshot taken 2026-08-12, before returning the lab laptop. Everything below describes state as of that date._

## What this is

Analysis pipeline and dashboard for the live audience chat from Wasita's public
dissertation defense on July 10, 2026. The chat app itself (`xoxowasita.com`)
was built by ljchang and lives at https://github.com/ljchang/xoxowasita; this
repo only consumes its data. `analysis/` is a uv + polars pipeline that snapshots
the Firebase realtime database, tidies it into parquet and JSON, embeds messages
with MiniLM, projects them with UMAP, and computes a stack of derived measures
(sentiment, affect families, burstiness, semantic drift, responsivity, reaction
matrix, coined phrases, chat-to-talk coupling, a togetherness index).
`dashboard/` is a SvelteKit + Tailwind 4 + LayerChart static site that renders
nineteen sections over that output.

The dataset is 340 messages from 57 named participants with 547 emoji reactions
and 64 replies. The conceptual joke, which the dashboard leans on, is that the
defense audience became participants in exactly the co-watching-plus-chat
paradigm the dissertation is about, and the coupling analysis applies her own
Study 2 method to her own talk.

## Where it stands

- Branch: `main` at `26bcb1e` ("purple-heart favicon and title, Luke linked to
  his GitHub", 2026-08-10). `main` tracks `origin/main` and is level with it.
  Nothing committed is unpushed.
- **The local `gh-pages` branch is not unpushed work.** It has one commit,
  `4b14723` ("deploy: f518a04", 2026-08-06), and no upstream configured, which
  makes `git branch -vv` show it with no tracking bracket and makes it look
  stranded. It is not. That exact commit is an ancestor of `origin/gh-pages`,
  which sits two commits further along at `70021b5`; both of those later
  commits are empty "retrigger pages build" commits with the identical tree
  hash, so local `gh-pages` and `origin/gh-pages` have byte-identical content.
  `git diff gh-pages origin/gh-pages` is empty. There is nothing on it to
  rescue.
- What that branch actually is: build output. On Aug 6 the deploy workflow was
  briefly switched to publish by pushing `dashboard/build` to a `gh-pages`
  branch (`f518a04`), and this commit is the artifact of that. On Aug 9,
  `718b4ed` reverted to the `actions/deploy-pages` approach because the
  environment policy allowed `main`. The branch is now vestigial. It is safe to
  delete locally and safe to leave alone.
- Deploy: `.github/workflows/deploy.yml` builds `dashboard/` on push to `main`
  with `BASE_PATH=/xoxowasita-analysis` and publishes via
  `actions/deploy-pages`. Repo Settings, Pages, Source must be set to **GitHub
  Actions** once per repo.
- Untracked: `.claude/` only.

## Uncommitted work on the old laptop

Very little, and none of it is source.

- **`.claude/settings.local.json` — untracked. DISPOSABLE / machine-specific.**
  A permission allowlist from past Claude Code sessions. Worth one read before
  discarding, because it is the only record of how the local transcript was
  produced: it shows `ffmpeg` converting
  `~/Downloads/Wasita Mahaphanit Meeting Recording Jul 10.mp4` to 16 kHz mono
  `data/local/talk.wav`, and `unzip` pulling
  `GMT20260710-190125_Recording.transcript.vtt` out of
  `~/Downloads/wasita_public_defense_recording.zip`. All paths are
  `/Users/wasita/...` and will not transfer.
- **`data/local/GMT20260710-190125_Recording.transcript.vtt` — 100 KB, ignored
  by `.gitignore` (`data/local/`), deliberately never committed. CARRY OVER.**
  See Landmines; this is the one file the pipeline needs that GitHub does not
  have.
- `data/processed/embeddings.npy` (510 KB) and `kmeans_labels.npy` are ignored
  by `*.npy` in `.gitignore`. Disposable: `topics.py` regenerates them, at the
  cost of downloading the MiniLM weights again.
- `analysis/.venv/`, `__pycache__/`, `dashboard/node_modules/`,
  `dashboard/build/`, `dashboard/.svelte-kit/` are all regenerable.

Everything else, including the raw Firebase export and all processed JSON and
parquet, is committed, on purpose, because the database is world-readable.

## Open threads

- The dashboard was still being actively extended on Aug 10 (chat-to-talk
  coupling, the togetherness index, coupling hover showing the on-stage blurb
  and the closest chat echoes per bin, then colour and favicon polish). There is
  no TODO file and no obviously half-finished section, so it appears to be at a
  natural stopping point, but that is an inference from the commit log rather
  than from a written plan.
- `dashboard/src/lib/components/Replay.svelte` exists but is parked. A comment
  in `dashboard/src/routes/+page.svelte` explains why: the video replay shows
  unpublished studies, so it stays out until the dissertation is published.
  Commit `e1b2188` did this deliberately. Revisit after publication.
- The blog post in `wasita.github.io` has a `<!-- DATA SLOT -->` waiting on
  numbers from this repo. §5 of `wasita.github.io/blogpost-revision-notes.md`
  says exactly what to look for, in priority order: whether reaction density
  spikes at the Tumblr disclosure and the Mohegan Sun story rather than at the
  results (that would be Chapter 3 replicating in her own data); the simple
  totals; whether people reacted to each other rather than only to her; and the
  emoji distribution. It also warns not to let that section run long.
- `analysis/labels.py` carries hand-assigned topic labels because unsupervised
  clustering "was mush". If new data ever arrives, those labels are manual work
  that will need redoing.

## Picking this up again

```bash
git clone https://github.com/wasita/xoxowasita-analysis.git
cd xoxowasita-analysis

# pipeline (needs uv; Python >= 3.13)
cd analysis
uv run extract.py && uv run tidy.py && uv run topics.py && uv run merge.py
cp ../data/processed/{chat,topics,segments}.json ../dashboard/src/lib/data/

# dashboard
cd ../dashboard
npm install
npm run dev              # or npm run build && npm run preview
```

The other analysis scripts (`sentiment.py`, `affect.py`, `burstiness.py`,
`drift.py`, `responsivity.py`, `matrix.py`, `phrases.py`, `words.py`,
`network.py`, `moments.py`, `style.py`, `togetherness.py`, `coupling.py`) are
run the same way and each writes its own JSON into `data/processed/`, which then
has to be copied into `dashboard/src/lib/data/`. That copy step is manual; there
is no build script that does it.

First things to check: that `data/local/` has the transcript in it (nothing
downstream of `coupling.py` or `segments.py` will run without it), and that the
Pages source is still set to GitHub Actions if a deploy has not run in a while.

## Landmines

- **The Zoom transcript is not in git.** `analysis/coupling.py` hard-codes
  `data/local/GMT20260710-190125_Recording.transcript.vtt` and
  `analysis/segments.py` validates against it. `data/local/` is gitignored on
  purpose (the recording covers unpublished studies), so a fresh clone cannot
  reproduce `coupling.json` or re-verify `segments.json`. Copy that file off the
  laptop. It can in principle be regenerated from the Zoom recording zip in
  Downloads, but only if that zip is also preserved. The same transcript is what
  §8 of the blog post revision notes was verified against, so it matters twice.
- **Named private-ish data is committed.** `data/raw/export-latest.json` and
  everything derived from it contain the real names and full message text of 57
  people who chatted during the defense, plus who reacted to whom. This was a
  considered decision (the Firebase rules expose `.read: true` at the root, so
  the data was already public to anyone with the URL) and the deployed site is
  unlisted via a `noindex` meta tag and a `robots.txt` disallow. Still: the
  repo is the durable copy, and if the repo is public the data is public in a
  much more findable form than a Firebase URL. Worth a deliberate decision
  rather than an inherited one.
- The Firebase database URL is in `analysis/extract.py` in the clear. That is
  fine, it needs no auth and holds nothing else, but it means anyone with the
  repo can re-pull the chat.
- No `.env` anywhere and no credentials required.
- `uv.lock` pins a heavy dependency set: `sentence-transformers`, `umap-learn`,
  `hdbscan`. First `uv run` on a new machine will be slow and will pull model
  weights from the network.
- Local `gh-pages` looks unpushed and is not. Do not try to "rescue" it; see
  above.
