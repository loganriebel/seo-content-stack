# SEO Content Stack

A gstack-equivalent system of Cursor AI skills for end-to-end SEO content creation. Inspired by [Garry Tan's gstack](https://github.com/garrytan/gstack), which turns Claude into a virtual engineering team — this project does the same for digital marketing content.

## What This Is

A pipeline of 11 Cursor skills that orchestrate the full lifecycle of an SEO blog post:

**Research → Brief → Outline → Write → Images → SEO Review → Editorial Review → HTML Build → Browser QA → Publish**

Each skill activates a different cognitive mode (researcher, strategist, writer, editor, QA tester, etc.), produces a specific artifact, and requires human approval before the next stage runs.

## The Pipeline

| Stage | Skill | What It Does | Artifact |
|-------|-------|-------------|----------|
| Orchestrator | `seo-content` | Routes to correct stage, tracks progress | — |
| 1. Research | `seo-research` | SERP analysis, Reddit/X/SO mining, GSC data | `research/[slug].md` |
| 2. Brief | `seo-brief` | Angle, keywords, competitive positioning | `briefs/[slug].md` |
| 3. Outline | `seo-outline` | Heading structure, keyword plan, image needs | `outlines/[slug].md` |
| 4. Write | `seo-write` | Draft with human expert voice | `drafts/[slug].md` |
| 5. Images | `seo-images` | AI-generated and stock photo assets | `assets/images/blog/[slug]/` |
| 6. SEO Review | `seo-review` | Keyword, meta, heading, link audit + scorecard | Updated draft |
| 7. Editorial | `seo-editorial` | Voice, accuracy, AI pattern removal | Polished draft |
| 8. Build | `seo-build` | HTML generation + full tag validation | `blog/[slug].html` |
| 9. QA | `seo-qa` | Browser-based visual and functional testing | `qa-reports/[slug].md` |
| 10. Publish | `seo-publish` | Deploy to hosting + verify live | Updated `content-index.json` |

## Key Design Decisions

**Artifact chaining.** Each stage produces a file that the next stage consumes. This creates a traceable chain and lets you resume from any point.

**Human review gates.** Every stage transition requires user approval. The AI proposes, you decide.

**Human voice as a hard requirement.** The writing skill has explicit banned AI patterns (no "in today's digital landscape," no "let's dive in," no hollow intensifiers) and required human signals (first person, specific examples, natural sentence rhythm). A humanizer pass runs within the writing stage itself.

**SEO and editorial review are separate.** SEO review checks discoverability mechanics. Editorial review checks quality and voice. Combining them causes one to compromise the other.

**Topic clustering built in.** The `content-index.json` tracks published content, pillar topics, and internal linking — so each new post is placed within a broader content strategy.

## Setup

1. Clone this repo into your project (or fork it).
2. Edit `seo-stack-config.yaml` with your site's details (domain, author, deploy settings).
3. Edit `.cursor/rules/seo-brand-voice.mdc` with your brand's voice and tone.
4. Start creating content: tell Cursor "start a new post about [topic]" and the orchestrator skill takes over.

## Project Structure

```
.cursor/
  skills/           # 11 pipeline skills
  rules/            # Brand voice and writing rules

seo_tools/
  validate_schema.py  # JSON-LD structured data validator
  templates/          # HTML templates (add your own)

seo-stack-config.yaml  # Site configuration
content-index.json     # Published content index

research/              # Research briefs
briefs/                # Content briefs
outlines/              # Content outlines
drafts/                # Markdown drafts
assets/images/blog/    # Image assets per post
blog/                  # Generated HTML
deploy/blog/           # Deploy-ready HTML
qa-reports/            # QA test results
```

## Customization

This was built for Mako Metrics but designed to generalize. To adapt for your site:

1. **`seo-stack-config.yaml`** — change domain, author, deploy method, content defaults.
2. **`.cursor/rules/seo-brand-voice.mdc`** — rewrite with your brand's voice, audience, and tone.
3. **Skill opening lines** — each skill says "You are a ___ for Mako Metrics." Change to your brand.
4. **CTA references** — skills reference `/free-tool.html`. Change to your CTA target.

## Requirements

- [Cursor](https://cursor.com/) with AI agent mode
- Python 3.10+ (for `validate_schema.py`)
- Your hosting credentials configured for the publish stage

## License

MIT
