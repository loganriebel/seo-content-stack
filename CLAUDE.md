# SEO Content Stack — project memory

Update this file when you change pipeline behavior or publish posts so future sessions stay consistent.

## What this is

A **standalone** Cursor pipeline repo. The main instruction file is **`.cursor/skills/seo-write-full.md`** (10 stages, human gates). Configuration lives in **`seo-stack-config.yaml`**; voice and formatting rules in **`.cursor/rules/seo-brand-voice.mdc`**; positioning for agents in **`AGENTS.md`**.

## First run

1. Complete **SETUP.md** (or let `seo-write-full` run its setup wizard).
2. Remove placeholder values from `seo-stack-config.yaml` (`YOUR_SITE_NAME`, `yourdomain.com`, etc.).

## Artifact paths (default)

Defined under `paths` in `seo-stack-config.yaml` — typical layout in this template:

| Area | Location |
|------|----------|
| Research | `research/` |
| Briefs | `briefs/` |
| Outlines | `outlines/` |
| Drafts | `drafts/` |
| Images | `assets/images/blog/` |
| HTML | `blog/` |
| Deploy | `deploy/blog/` |
| QA | `qa-reports/` |
| Index | `content-index.json` |

If this repo is **nested inside a website monorepo**, set `deploy.website_root` and adjust `paths.*` and `seo_tools.*` accordingly.

## Critical rules

1. **Human approval** between stages.
2. **Do not skip** the stage sections inside `seo-write-full.md`.
3. **Brand voice** — read `seo-brand-voice.mdc` before writing or editing drafts.
4. **Build scripts** — only `seo_tools/validate_schema.py` is guaranteed to exist; other `seo_tools` paths are hooks for your own site’s build pipeline.

## Key files

| File | Purpose |
|------|---------|
| `seo-stack-config.yaml` | Site config and paths |
| `SETUP.md` | First-time checklist |
| `AGENTS.md` | Business context for agents |
| `.cursor/rules/seo-brand-voice.mdc` | Voice and formatting |
| `.cursor/rules/seo-first-run.mdc` | Placeholder gate for agents |
| `.cursor/skills/seo-write-full.md` | Full pipeline |
| `.cursor/skills/seo-content.md` | Deprecated pointer to `seo-write-full` |
| `content-index.json` | Published posts and pillars |

## Architecture notes

- **Single skill (`seo-write-full`)** keeps full context across stages.
- **SVG-first images** are recommended in the skill (versionable, scalable).
- **Publish** = git commit + push; your host’s CI/deploy handles go-live.

---

## Content inventory

### Published

| Slug | Primary keyword | Published | Words |
|------|-----------------|-----------|-------|
| *(add rows as you publish)* | | | |

### In pipeline

None — or list active slugs.

---

## Changelog

*(Add dated entries when you change the pipeline or ship posts.)*
