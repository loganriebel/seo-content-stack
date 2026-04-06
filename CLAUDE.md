# SEO Content Stack — Project Memory (Mako Metrics)

## Keeping This File Current

This file is the primary memory for this pipeline. It is only useful if it stays accurate. **Update it as part of every session — not as an afterthought.**

**Update incrementally — do not wait until the end of the session.**
Context windows can be exhausted before a session "ends." If you wait, the update may never happen. Instead, update this file immediately after each significant action.

**Update after each significant action:**
- Stage completed on a post → update Content Inventory (move to correct status, note current stage)
- Post published → move to Published table in Content Inventory, add Changelog entry
- Pipeline instruction changed → update the relevant section immediately
- Mistake made → add to Common Mistakes right away, before moving on
- New architecture decision → add to Architecture Decisions with the reason
- Todo item completed → remove it; new task identified → add it immediately

**At minimum, after Stage 10 Publish:**
- Post moved to Published table with correct slug, keyword, date, word count
- Changelog entry written for this post

---

## What This Project Is

This is an SEO content pipeline for Mako Metrics (makometrics.com). It produces blog posts through a **10-stage process** where each stage creates a file that the next stage consumes. **One primary skill** (`seo-write-full`) runs the full pipeline in a **single agent session** with rich context; every stage transition still requires your approval before moving forward.

**Site:** Static HTML, hosted on DigitalOcean App Platform. Auto-deploys from `master` branch.
**Deploy directory:** `deploy/` — DigitalOcean serves from here. Pretty URLs: `deploy/blog/<slug>/index.html`.
**Draft source of truth:** `../seo/drafts/[slug].md` — Python build tools read from here.
**Blog HTML (intermediate):** `../blog/[slug].html`
**Blog deploy artifact:** `../deploy/blog/[slug]/index.html`
**Images:** `../images/blog/[slug].svg` (cover) + inline SVGs
**GTM:** `GTM-KV9N4S6H`

---

## The Pipeline

| Stage | Instruction (within skill) | Artifact |
|-------|----------------------------|----------|
| 1. Research | `seo-write-full` → Stage 1 | `.seo-stack/research/[slug].md` |
| 2. Brief | `seo-write-full` → Stage 2 | `.seo-stack/briefs/[slug].md` |
| 3. Outline | `seo-write-full` → Stage 3 | `.seo-stack/outlines/[slug].md` |
| 4. Write | `seo-write-full` → Stage 4 | `seo/drafts/[slug].md` ← Python tools read from here |
| 5. Images | `seo-write-full` → Stage 5 | `images/blog/[slug].svg` (+ inline SVGs) |
| 6. SEO Review | `seo-write-full` → Stage 6 | `seo/drafts/[slug].md` (updated) |
| 7. Editorial | `seo-write-full` → Stage 7 | `seo/drafts/[slug].md` (updated) |
| 8. Build | `seo-write-full` → Stage 8 | `blog/[slug].html` + `deploy/blog/[slug]/index.html` (via Python) |
| 9. QA | `seo-write-full` → Stage 9 | `.seo-stack/qa-reports/[slug].md` |
| 10. Publish | `seo-write-full` → Stage 10 | Updates `content-index.json` + git push to master |

**Primary instruction file:** `.cursor/skills/seo-write-full.md`

Archived legacy per-stage copies (reference only): `.cursor/skills/archive/`.

---

## How to Work

When the user asks to start or continue a blog post:

1. Read `seo-stack-config.yaml` for site configuration.
2. Read `.cursor/rules/seo-brand-voice.mdc` for writing standards.
3. Open **`.cursor/skills/seo-write-full.md`** and follow **"How to determine current stage"** to find where to resume.
4. Execute the **current stage** section in that file exactly (templates, checklists, skill invocations).
5. After completing the stage, present results and wait for user approval before the next stage.

**Do not skip the detailed stage sections** in `seo-write-full.md`. They contain process steps, templates, banned patterns, and quality checks.

---

## Detecting Current Stage

Use the **resume logic in `seo-write-full.md`** (summary):

- Topic only, no slug → Stage 1 Research.
- Check artifacts in reverse order: published in `content-index.json` → QA report → HTML file in `../blog/` → draft frontmatter (`editorial_reviewed` / `seo_reviewed`) → images in `../images/blog/` → outline → brief → research.

---

## Critical Rules

1. **Human review gates.** Never auto-advance through stages.
2. **Follow `seo-write-full.md` for the current stage.** Don't paraphrase from memory.
3. **Brand voice is mandatory.** Read `.cursor/rules/seo-brand-voice.mdc` before any writing. Stage 4 includes the full banned-phrases list and human-voice signals.
4. **Explicit skill calls** when Stage 4 or Stage 7 require it: `copywriting`, `writing-clearly-and-concisely`, `humanizer`, `copy-editing` — use your environment's skill invocation, not memory-only application.
5. **Artifact chaining.** Verify the previous stage's output exists before starting a stage.
6. **Source tracking.** Statistics and claims must link inline; trace sources to Stage 1 research where possible.
7. **Stage 4 draft goes to `../seo/drafts/[slug].md`.** Python build tools read from `seo/drafts/`. Do NOT write to `.seo-stack/drafts/` — those are pipeline-only artifacts and won't be found by `generate_html.py`.
8. **Stage 8 = run Python build tools.** `python ../seo/seo_tools/generate_html.py [slug]` → produces `blog/[slug].html` + `deploy/blog/[slug]/index.html`. Then `python ../seo/seo_tools/publish.py [slug]` → updates `sitemap.xml` + `blog.html`.
9. **Stage 10 Publish = git push to `master`.** DigitalOcean App Platform auto-deploys from `deploy/` on every push to master. Netlify is not used.

---

## Common Commands

- "Start a new post about [topic]" → `seo-write-full` Stage 1
- "Resume [slug]" → detect stage via `seo-write-full`, continue
- "Pipeline status" → scan artifact directories and report
- "Run stage [N] on [slug]" → jump to that section in `seo-write-full`

---

## Key Files

| File | Purpose |
|------|---------|
| `seo-stack-config.yaml` | Site config (domain, paths, content defaults, deploy) |
| `content-index.json` | Published posts index + pillar structure |
| `.cursor/rules/seo-brand-voice.mdc` | Brand voice rules (activated on drafts/, blog/, etc.) |
| `.cursor/skills/seo-write-full.md` | **Full 10-stage pipeline** |
| `.cursor/skills/archive/` | Legacy per-stage skills (reference only) |

---

## Architecture Decisions

- **Single-agent over multi-agent:** Eliminates context hand-off errors between stages. Research stats, brief angles, and outline structure are all in memory when writing and reviewing.
- **SVG over PNG/JPG for AI-generated images:** SVGs render at any resolution, are version-controllable as plain text, don't require image optimization tooling, and can be created directly by Claude.
- **Git push as deploy:** Netlify auto-deploys on every push to main. No separate upload step.
- **Human gate between every stage:** Prevents compounding errors. A bad brief becomes a bad outline becomes a bad post.
- **`.seo-stack/` as a separate git repo:** Keeps pipeline artifacts (research, drafts, QA reports) out of the main site repo history. Only final HTML files and images travel to `../blog/` and `../images/blog/`.
- **HTML output (not MDX):** Mako Metrics is a static HTML site, not Next.js. Stage 8 writes `../blog/[slug].html` directly. If the site is rebuilt in Next.js, update Stage 8 to output MDX to `../content/blog/`.

---

## Content Inventory

### Published (live at makometrics.com/blog/)

| Slug | Primary Keyword | Published | Words |
|------|----------------|-----------|-------|
| 7-free-ways-spy-competitor-facebook-ads | spy on competitor facebook ads free | (pre-pipeline) | — |
| 7-signs-facebook-ads-creative-fatigue | facebook ads creative fatigue | (pre-pipeline) | — |
| advantage-plus-shopping-campaigns | advantage plus shopping campaigns | (pre-pipeline) | — |
| facebook-ads-cost-benchmarks | facebook ads cost benchmarks | (pre-pipeline) | — |
| facebook-ads-not-converting | facebook ads not converting | (pre-pipeline) | — |
| facebook-ads-roas-benchmark | facebook ads roas benchmark | (pre-pipeline) | — |
| full-funnel-facebook-ads-ecommerce | full funnel facebook ads ecommerce | (pre-pipeline) | — |
| how-much-does-adspy-cost | how much does adspy cost | (pre-pipeline) | — |
| ios-attribution-meta-ads-ecommerce | ios attribution meta ads | (pre-pipeline) | — |
| meta-ad-library-guide | meta ad library guide | (pre-pipeline) | — |
| reverse-engineer-competitor-targeting | reverse engineer competitor facebook targeting | (pre-pipeline) | — |

*Note: posts above were published before this pipeline was set up. They are not tracked in content-index.json.*

### In Pipeline

None currently.

### Backlog / Ideas

| Slug idea | Angle | Priority |
|-----------|-------|----------|
| meta-ads-cpm-benchmarks-2026 | Data post — CPM benchmarks by industry/vertical | High |
| facebook-ads-audience-size-guide | How big should your audience be for Meta ads | High |
| competitor-analysis-meta-ads | How to research what competitors are running | High |
| meta-ads-budget-calculator | Interactive tool angle — how much should you spend | Medium |
| advantage-shopping-vs-manual | Comparison — when to use each | Medium |

---

## Todo

- [ ] Add first post through the new pipeline (Stage 1–10)
- [ ] Update `content-index.json` with pillar structure matching Mako Metrics topic clusters
- [ ] Archive legacy per-stage skills from `.cursor/skills/` to `.cursor/skills/archive/` ✓ (done in migration)
- [ ] Verify blog listing update process — static HTML means `blog.html` may need manual post additions
- [ ] Fill in `site_html.header` and `site_html.footer` in `seo-stack-config.yaml` when ready

---

## Common Mistakes

Mistakes to avoid in this pipeline:

**`.seo-stack/` is its own git repo — it does not push with the main META_Ads_Analyzer repo.**
Running `git push` from `META_Ads_Analyzer/` root does NOT include `.seo-stack/` changes. Commit pipeline artifacts (research, briefs, outlines, QA reports) from inside `.seo-stack/`. The final HTML and SVG files live in the parent repo (`../blog/`, `../images/blog/`, `../deploy/blog/`) and push with the main site.

**Stage 4 draft must go to `../seo/drafts/[slug].md`, not `.seo-stack/drafts/`.**
The Python build tools (`generate_html.py`, `publish.py`) look for drafts in `seo/drafts/`. If you write the draft to `.seo-stack/drafts/`, Stage 8 will fail to find the file. Use the path from `seo-stack-config.yaml` `paths.drafts`.

**Stage 8 uses Python tools, not direct HTML writing.**
The correct Stage 8 flow is:
1. `python ../seo/seo_tools/generate_html.py [slug]` — generates `blog/[slug].html` + `deploy/blog/[slug]/index.html`
2. `python ../seo/seo_tools/publish.py [slug]` — updates `sitemap.xml` + `blog.html` listing

**Hosting is DigitalOcean App Platform, not Netlify.**
Push to `master` (not `main`) → DO auto-deploys from `deploy/`. There is no Netlify involved.

**Blog listing is updated by `publish.py`, not manually.**
`publish.py` updates `blog.html` as part of its run. Don't manually edit `blog.html` to add posts — run `publish.py` instead.

**Brand voice is in `.cursor/rules/seo-brand-voice.mdc`, not in the skill.**
The detailed voice rules (banned phrases, human signals, ICP, audience) live in the Cursor rules file. The skill (`seo-write-full.md`) references this rule. Always read the rule file before Stage 4 writing.

---

## Changelog

**2026-04-06**
- Migrated from legacy 11-skill architecture to single `seo-write-full.md` skill
- Updated `seo-stack-config.yaml`: corrected deploy (DigitalOcean/master), paths (seo/drafts/, deploy/blog/), GTM ID, Python tool paths
- Updated CTAs from /contact → /free-tool
- Preserved `.cursor/rules/seo-brand-voice.mdc` unchanged
- Archived legacy per-stage skills to `.cursor/skills/archive/`
- Created this CLAUDE.md as production-grade project memory
- Preserved existing brand voice from `.cursor/rules/seo-brand-voice.mdc` (unchanged — already excellent)
- Archived legacy per-stage skills to `.cursor/skills/archive/`
