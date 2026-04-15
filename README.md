# SEO Content Stack

A [**gstack**](https://github.com/garrytan/gstack)-style bundle of Cursor skills for end-to-end SEO content: research through publish, with **human approval between stages**.

**Start here:** [SETUP.md](SETUP.md) — fork, configure your brand, then run the pipeline.

> **Neutral template:** This repository intentionally contains **no** vendor-specific product story. Fork it, fill `seo-stack-config.yaml` and `.cursor/rules/seo-brand-voice.mdc`, then add your own content. For brand-specific marketing work, keep drafts in **your** site or product repo.

> **History:** The `master` branch may occasionally be **reset** to stay generic. Fork the repo if you need a stable history for your customized stack.

## What this is

One primary skill (**`seo-write-full`**) runs **10 stages** in a single agent session (research → publish), writing artifacts to disk at each step:

**Research → Brief → Outline → Write → Images → SEO review → Editorial → Build → QA → Publish**

Legacy: the tiny **`seo-content`** skill only points agents at `seo-write-full`.

## The pipeline (artifact chain)

| Stage | Artifact (typical paths) |
|-------|--------------------------|
| 1 Research | `research/[slug].md` |
| 2 Brief | `briefs/[slug].md` |
| 3 Outline | `outlines/[slug].md` |
| 4 Write | `drafts/[slug].md` |
| 5 Images | `assets/images/blog/` |
| 6–7 Reviews | updates `drafts/[slug].md` |
| 8 Build | `blog/`, `deploy/blog/` |
| 9 QA | `qa-reports/[slug].md` |
| 10 Publish | `content-index.json` + git push |

Paths are configurable in `seo-stack-config.yaml` under `paths`.

## Key design ideas

- **Artifact chaining** — each stage consumes the previous file; you can resume from any stage.
- **Human gates** — do not advance until the user approves.
- **Separate SEO vs editorial** — mechanics vs voice (see skill for details).
- **Sources** — statistics and claims should be citable (see Stage 1 and editorial checks in `seo-write-full`).

## Quick start

1. Complete [SETUP.md](SETUP.md) (config, voice, `AGENTS.md`).
2. In Cursor, open `.cursor/skills/seo-write-full.md` and follow the **first-run setup check** if placeholders remain.
3. Say: *Start a new post about [topic]*.

## Customization map

| File | Purpose |
|------|---------|
| `seo-stack-config.yaml` | Domain, paths, deploy, GTM, author, brand_voice defaults |
| `seo-stack-config.example.yaml` | Same structure; copy if you track only an example in git |
| `.cursor/rules/seo-brand-voice.mdc` | Tone, audience, formatting |
| `AGENTS.md` | ICP, positioning, CTAs for the agent |
| `.cursor/rules/seo-first-run.mdc` | Reminds agents not to run the pipeline on placeholders |

## Requirements

- [Cursor](https://cursor.com/) (or compatible editor) with AI agent mode
- Python 3.10+ optional, for `seo_tools/validate_schema.py` and any build scripts you add

## License

MIT
