# SEO Content Stack — Project Memory

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

---

## What This Project Is

This is an SEO content pipeline configured in `seo-stack-config.yaml`. It produces blog posts through a **10-stage process** where each stage creates a file that the next stage consumes. **One primary skill** (`seo-write-full`) runs the full pipeline in a **single agent session** with rich context; every stage transition still requires your approval before moving forward.

**Site config:** See `seo-stack-config.yaml` for domain, deploy settings, GTM, and brand voice.
**Draft source of truth:** path configured in `seo-stack-config.yaml` under `paths.drafts`
**Blog HTML (intermediate):** `paths.html_output`
**Blog deploy artifact:** `paths.deploy_output`

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
| 10. Publish | `seo-write-full` → Stage 10 | Updates `content-index.json` + git push |

**Primary instruction file:** `.cursor/skills/seo-write-full.md`

Archived legacy per-stage copies (reference only): `.cursor/skills/archive/`.

---

## How to Work

When the user asks to start or continue a blog post:

1. Run the **first-run setup check** in `seo-write-full.md` — if `seo-stack-config.yaml` has placeholder values, run the setup wizard before anything else.
2. Read `seo-stack-config.yaml` for site configuration.
3. Read `.cursor/rules/seo-brand-voice.mdc` for writing standards.
4. Open **`.cursor/skills/seo-write-full.md`** and follow **"How to determine current stage"** to find where to resume.
5. Execute the **current stage** section in that file exactly (templates, checklists, skill invocations).
6. After completing the stage, present results and wait for user approval before the next stage.

**Do not skip the detailed stage sections** in `seo-write-full.md`. They contain process steps, templates, banned patterns, and quality checks.

---

## Detecting Current Stage

Use the **resume logic in `seo-write-full.md`** (summary):

- Topic only, no slug → Stage 1 Research.
- Check artifacts in reverse order: published in `content-index.json` → QA report → HTML file → draft frontmatter (`editorial_reviewed` / `seo_reviewed`) → images → outline → brief → research.

---

## Critical Rules

1. **Human review gates.** Never auto-advance through stages.
2. **Follow `seo-write-full.md` for the current stage.** Don't paraphrase from memory.
3. **Brand voice is mandatory.** Read `.cursor/rules/seo-brand-voice.mdc` before any writing.
4. **Explicit skill calls** when Stage 4 or Stage 7 require it: `copywriting`, `writing-clearly-and-concisely`, `humanizer`, `copy-editing`.
5. **Artifact chaining.** Verify the previous stage's output exists before starting a stage.
6. **Source tracking.** Statistics and claims must link inline; trace sources to Stage 1 research where possible.
7. **Stage 4 draft path:** use `paths.drafts` from `seo-stack-config.yaml`. Python build tools read from there.
8. **Stage 8 = run Python build tools.** See `seo_tools` paths in config.
9. **Stage 10 Publish = git push to configured branch.** Deploy method and branch are in `seo-stack-config.yaml`.

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
| `seo-stack-config.yaml` | Site config (domain, paths, content defaults, deploy, brand voice) |
| `content-index.json` | Published posts index + pillar structure |
| `.cursor/rules/seo-brand-voice.mdc` | Brand voice rules |
| `.cursor/skills/seo-write-full.md` | **Full 10-stage pipeline** |
| `.cursor/skills/archive/` | Legacy per-stage skills (reference only) |

---

## Architecture Decisions

- **Single-agent over multi-agent:** Eliminates context hand-off errors between stages.
- **SVG over PNG/JPG for AI-generated images:** SVGs render at any resolution, are version-controllable as plain text, and can be created directly by Claude.
- **Git push as deploy:** Auto-deploys on every push to configured branch. No separate upload step.
- **Human gate between every stage:** Prevents compounding errors. A bad brief becomes a bad outline becomes a bad post.
- **`.seo-stack/` as a separate git repo:** Keeps pipeline artifacts (research, drafts, QA reports) out of the main site repo history. Only final HTML files and images travel to the website directory.

---

## Content Inventory

### Published

| Slug | Primary Keyword | Published | Words |
|------|----------------|-----------|-------|
| *(add rows here as you publish)* | | | |

### In Pipeline

None currently.

### Backlog / Ideas

| Slug idea | Angle | Priority |
|-----------|-------|----------|
| *(add content ideas here)* | | |

---

## Todo

- [ ] Complete first-run setup (run `seo-write-full` and follow the setup wizard)
- [ ] Add brand voice rules to `.cursor/rules/seo-brand-voice.mdc`
- [ ] Publish first post through the pipeline (Stage 1–10)
- [ ] Update `content-index.json` with pillar structure

---

## Common Mistakes

**`.seo-stack/` is its own git repo — it does not push with the main site repo.**
Commit pipeline artifacts (research, briefs, outlines, QA reports) from inside `.seo-stack/`. Final HTML and image files live in the parent repo and push with the main site.

**Stage 4 draft must go to the path in `seo-stack-config.yaml` `paths.drafts`, not `.seo-stack/drafts/`.**
The Python build tools look for drafts at the configured path. Writing to the wrong location causes Stage 8 to fail.

**Stage 8 uses Python tools, not direct HTML writing.**
Run `generate_html.py` then `publish.py` — both paths are in `seo_tools` config section.

**Brand voice is in `.cursor/rules/seo-brand-voice.mdc`, not in the skill.**
Always read the rules file before Stage 4 writing.

---

## Changelog

*(Add entries here after each significant pipeline change or publish)*
