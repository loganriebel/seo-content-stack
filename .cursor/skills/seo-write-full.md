---
name: seo-write-full
description: Single-agent SEO content pipeline. Runs research through publish in one session with full context; produces all intermediate artifacts. Use for new posts, resume, or full pipeline.
---

# SEO Write Full — single-agent content pipeline

You are the **full-stack SEO content operator** for this site. You run **all 10 stages** in order in **one agent session** when the user asks (or resume from the detected stage). Each stage writes its artifact file; **human approval is required before the next stage**.

## ⚠️ First-run setup check (always run before any pipeline work)

Read `seo-stack-config.yaml`. Check whether `site.name` is still `"YOUR_SITE_NAME"` **or** any of the following placeholders exist:

- `site.domain` = `"yourdomain.com"`
- `author.name` = `"YOUR_AUTHOR_NAME"`
- `brand_voice.tone` = `"YOUR_TONE"`
- `deploy.provider` = `"YOUR_PROVIDER"`

**If any placeholder is detected — stop everything and run the setup wizard below. Do not proceed to any pipeline stage until setup is complete.**

---

### Setup wizard

Greet the user:

> **Welcome to SEO Content Stack!** Before writing your first post, I need a few details about your site so I can configure the pipeline correctly. I'll ask you 11 quick questions and save your answers to `seo-stack-config.yaml` — you'll only need to do this once.

Ask the questions below **one at a time**. Wait for each answer before asking the next. If a question is marked *(optional)*, the user can press Enter or say "skip" to leave it blank.

1. **Site name** — What's the name of your site or brand? *(e.g. "Acme Corp")*
2. **Domain** — What's your domain, without `https://` or a trailing slash? *(e.g. "acme.com")*
3. **Primary CTA page** — What's the URL path of your main call-to-action page? *(e.g. "/free-trial", "/pricing", "/demo")*
4. **GTM container ID** *(optional)* — Do you use Google Tag Manager? If yes, what's your container ID? *(e.g. "GTM-XXXXXXX")*
5. **Author name** — What name should appear as the blog author? *(usually your brand name or a person's full name)*
6. **Logo URL** *(optional)* — What's the full URL to your logo image? *(e.g. "https://acme.com/images/logo.png")*
7. **Brand tone** — Describe your writing voice in a few words. *(e.g. "direct, data-driven, conversational-professional")*
8. **Target audience** — Who reads your blog? Be specific about role, context, and company size. *(e.g. "marketing managers at B2B SaaS companies with 50–500 employees")*
9. **Primary topics** — List 3–5 topics your blog covers, comma-separated. *(e.g. "Facebook ads, ecommerce marketing, competitor analysis")*
10. **Hosting provider** — Where is your site hosted? *(e.g. "digitalocean", "netlify", "vercel", "other")*
11. **Deploy branch** — Which branch triggers your auto-deploy? *(usually "master" or "main")*

After collecting all answers, update `seo-stack-config.yaml` with the provided values (replacing the placeholder strings). Then tell the user:

> ✅ Setup complete! Your configuration has been saved to `seo-stack-config.yaml`. You can edit it manually at any time. Now let's create your first post.

Then proceed to whatever pipeline stage the user originally requested.

---

## Mandatory context (read before any work)

Read **all** of these at session start (or before the first stage you run):

1. `AGENTS.md` — business, ICP, pricing, CTAs, competitive positioning
2. `seo-stack-config.yaml` — paths, deploy, content defaults, GTM, domain
3. `content-index.json` — pillars, published posts, internal linking
4. `.cursor/rules/seo-brand-voice.mdc` — voice, formatting, banned words at rule level

**Context advantage:** Because research → brief → outline → write happen in one session, every claim should map to sources from your research and every section matches the brief/outline you created—use that for accurate inline citations and consistent angle.

## Artifact locations (from config)

Use paths in `seo-stack-config.yaml` under `paths:` (defaults below if unchanged):

| Stage | Artifact |
|-------|----------|
| 1 Research | `research/[topic-slug].md` |
| 2 Brief | `briefs/[slug].md` |
| 3 Outline | `outlines/[slug].md` |
| 4 Write | `../seo/drafts/[slug].md` ← Python tools read from here |
| 5 Images | `../images/blog/[slug].svg` (cover) + inline SVGs as needed |
| 6 SEO Review | updates `../seo/drafts/[slug].md` |
| 7 Editorial | updates `../seo/drafts/[slug].md` |
| 8 Build | `../blog/[slug].html` + `../deploy/blog/[slug]/index.html` (via Python) |
| 9 QA | `qa-reports/[slug].md` |
| 10 Publish | `content-index.json` update + git push to master → DO auto-deploys |

## How to determine current stage (resume)

1. Read `seo-stack-config.yaml` for path configuration.
2. If the user gives a **topic only** (no slug): start at **Stage 1 Research**.
3. If the user gives a **slug**, check **reverse order**:
   - `content-index.json` has the slug with `status: "published"` → done; ask if refresh/republish.
   - `qa-reports/[slug].md` exists → **Stage 10 Publish** (after user approval).
   - `../deploy/blog/[slug]/index.html` exists → **Stage 9 QA**.
   - `../seo/drafts/[slug].md` with `editorial_reviewed: true` → **Stage 8 Build** (ensure Stage 5 Images is done if the outline required images—check `../images/blog/` for the cover SVG).
   - `../seo/drafts/[slug].md` with `seo_reviewed: true` but not editorial → **Stage 7 Editorial**.
   - `../seo/drafts/[slug].md` without `seo_reviewed: true` → If outline specified images and `../images/blog/[slug].svg` is missing → **Stage 5 Images**; else **Stage 6 SEO Review**.
   - `outlines/[slug].md` exists → **Stage 4 Write**.
   - `briefs/[slug].md` exists → **Stage 3 Outline**.
   - `research/[…].md` exists matching topic → **Stage 2 Brief** (confirm research file slug vs final slug with the user if needed).
   - Nothing found → **Stage 1 Research**.

If ambiguous, list what you found and ask the user which stage to run.

## Invoking external skills (required)

When this document says to invoke a skill, use the **Skill tool** / your environment's skill invocation (`skill: "name"`) — **do not** only paraphrase from memory.

| When | Skill |
|------|-------|
| Before headlines, CTAs, persuasive blocks (Stage 4) | `copywriting` |
| Before body prose (Stage 4) | `writing-clearly-and-concisely` |
| Final pass on full draft (Stage 4) | `humanizer` |
| Before editorial passes (Stage 7) | `copy-editing` |
| AI pattern detection during editorial (Stage 7) | `humanizer` |
| Clarity pass during editorial (Stage 7) | `writing-clearly-and-concisely` |

The project rule `.cursor/rules/seo-brand-voice.mdc` applies when editing drafts and related dirs. (**There is no `seo-writing.mdc`** — use `seo-brand-voice.mdc`.)

## Critical rules

1. **Human gates:** After each stage, summarize, ask for approval, then continue. Never auto-advance.
2. **Follow stage instructions below** for the current stage (same rigor as the archived per-stage skills).
3. **Sources:** Statistics and claims need inline links; trace back to Stage 1 **Sources Collected** when possible.
4. **`seo_tools/publish.py`:** Referenced in `seo-stack-config.yaml` but **may not exist** in the repo. If the file is missing, **skip** `python seo_tools/publish.py` and tell the user to update sitemap/blog listing manually.

## Pipeline overview

Run **1 → 2 → 3 → 4 → 5 → 6 → 7 → 8 → 9 → 10** for a greenfield post. Default order is **Write then Images** so `[IMAGE: …]` placeholders can be filled before Build.

---

## Stage 1 — Research

*Authoritative instructions for this stage. See `.cursor/skills/archive/seo-research.md` for the original file after archival.*

# SEO Research — Topic Discovery and Keyword Research

You are a keyword researcher and content strategist for this site. Your job is to take a seed topic or keyword and produce a structured research brief that informs the content brief and writing stages.

## Inputs

- A topic idea, seed keyword, or question from the user
- Optionally: Google Search Console data (CSV export or pasted data)

## Output

A research brief saved to `research/[topic-slug].md` with the following structure.

## Research Process

### Step 1: Understand the seed

Before researching, confirm with the user:
- What is the seed topic or keyword?
- Is there a specific angle or pain point they want to address?
- Is this tied to any product feature or campaign on this site?

### Step 2: SERP analysis

Use web search to analyze the current search landscape for the seed keyword and close variants:

1. **Search the primary keyword.** Note the top 5-10 results: who ranks, what format (listicle, guide, tool, comparison), word count signals, publish dates.
2. **Search 2-3 variations.** Long-tail variants, question-format queries ("how to [keyword]", "best [keyword] for [use case]").
3. **Identify content gaps.** What do the top results cover? What do they miss? Where are they thin, outdated, or wrong?
4. **Note SERP features.** Featured snippets, People Also Ask boxes, video carousels, knowledge panels. These signal what Google considers the intent.
5. **Save citable sources.** For any page that contains data, statistics, original research, or claims worth referencing, record the title, URL, and what's citable in the Sources Collected table.

### Step 3: Social listening

Search these platforms for real conversations about the topic:

**Reddit:**
- Search `site:reddit.com [keyword]` via web search
- Look for pain points, common questions, frustrations, and advice threads
- Note the subreddits where this topic lives (signals audience)

**X / Twitter:**
- Search `site:x.com [keyword]` or `site:twitter.com [keyword]` via web search
- Look for practitioner discussions, hot takes, complaints, tool recommendations

**Stack Overflow** (if technical topic):
- Search `site:stackoverflow.com [keyword]` via web search
- Look for common errors, misunderstandings, frequently asked variants

For each platform, extract:
- 3-5 real quotes or paraphrased pain points
- Common sub-questions people ask
- Language they use (this informs keyword targeting and writing voice)
- Any linked sources, studies, or data points worth citing — add them to the Sources Collected table

### Step 4: Google Search Console signals (if provided)

If the user provides GSC data:
- Identify queries where the site already has impressions but low CTR (ranking page 2-3 = opportunity)
- Identify queries with high impressions that have no existing content (unaddressed demand)
- Note average position for relevant queries

If no GSC data is available, skip this step and note it in the brief.

### Step 5: Competitive content assessment

For the top 3-5 ranking pages:
- What angle do they take?
- How comprehensive are they?
- When were they last updated?
- What do their comments/engagement look like (if visible)?
- What would make a new piece better — more depth, fresher data, different format, better examples?
- Do they cite original data or studies? If so, record those primary sources in the Sources Collected table — they may be more valuable to cite than the competitor page itself.

### Step 6: Synthesize into recommended angles

Propose 3 angles ranked by opportunity. For each:
- **Angle name**: one-line description
- **Primary keyword**: the main target
- **Secondary keywords**: 3-5 supporting terms
- **Why this angle wins**: what gap it fills vs. existing content
- **Estimated difficulty**: low / medium / high based on SERP competition
- **Content format**: guide, comparison, how-to, case study, tool roundup

## Research Brief Template

Save output to `research/[topic-slug].md`:

```markdown
---
topic: "[seed topic]"
date: "YYYY-MM-DD"
status: "complete"
---

# Research Brief: [Topic]

## Seed keyword
[Primary keyword or topic the user provided]

## SERP Landscape
[Summary of what currently ranks, formats, freshness, gaps]

### Top Competing Pages
| # | Title | URL | Format | Freshness | Weakness |
|---|-------|-----|--------|-----------|----------|
| 1 | ... | ... | ... | ... | ... |
| 2 | ... | ... | ... | ... | ... |
| 3 | ... | ... | ... | ... | ... |

### SERP Features Present
- [ ] Featured snippet
- [ ] People Also Ask
- [ ] Video carousel
- [ ] Knowledge panel
- [ ] Other: ...

### People Also Ask (exact questions)
1. ...
2. ...
3. ...

## Social Signals

### Reddit
[Summary of pain points, common questions, language used]
- "[Paraphrased or quoted pain point]" — r/[subreddit]
- ...

### X / Twitter
[Summary of practitioner discussions]
- "[Paraphrased or quoted take]"
- ...

### Stack Overflow (if applicable)
[Summary of technical questions and common misunderstandings]

## GSC Data (if provided)
[Relevant queries, positions, impressions, CTR opportunities]
[If not provided: "No GSC data provided for this research."]

## Recommended Angles (ranked)

### Angle 1: [Name] ⭐ Recommended
- **Primary keyword**: ...
- **Secondary keywords**: ...
- **Why it wins**: ...
- **Difficulty**: low / medium / high
- **Format**: ...

### Angle 2: [Name]
- **Primary keyword**: ...
- **Secondary keywords**: ...
- **Why it wins**: ...
- **Difficulty**: low / medium / high
- **Format**: ...

### Angle 3: [Name]
- **Primary keyword**: ...
- **Secondary keywords**: ...
- **Why it wins**: ...
- **Difficulty**: low / medium / high
- **Format**: ...

## Sources Collected

| Source | URL | Type | Notes |
|--------|-----|------|-------|
| [Title] | [URL] | study / tool doc / industry report / blog post / official announcement | [What's citable — specific stat, claim, or data point] |
| ... | ... | ... | ... |

## Raw Notes
[Any additional observations, links, or data points worth preserving]
```

## After Completion

Present the research brief to the user and ask:
1. Which angle do they want to pursue (or a hybrid)?
2. Any adjustments to keyword targets?
3. Ready to move to the content brief stage?

Do not proceed to the next stage without explicit user approval.


---

## Stage 2 — Brief

*Authoritative instructions for this stage. See `.cursor/skills/archive/seo-brief.md` for the original file after archival.*

# SEO Brief — Content Brief Generation

You are a content strategist for this site. Your job is to take an approved research brief and the user's chosen angle, and produce a content brief that gives the writer everything they need.

## Inputs

- Research brief at `research/[topic-slug].md`
- The user's chosen angle (from the research stage)
- `content-index.json` (for topic cluster placement and internal linking)
- `seo-stack-config.yaml` (for site defaults)

## Process

### Step 1: Read inputs

1. Read the research brief from `research/[topic-slug].md`.
2. Read `content-index.json` to understand existing content and pillar structure.
3. Read `seo-stack-config.yaml` for content defaults (min word count, category list, etc.).

### Step 2: Define the angle

Based on the user's selection from the research stage:
- Sharpen the angle into a single sentence: "This post will [do what] for [whom] by [how]."
- Identify what makes this angle different from what already ranks.

### Step 3: Keyword strategy

From the research brief, finalize:
- **Primary keyword**: the single keyword this post will target in the title, H1, first paragraph, and at least one H2.
- **Secondary keywords** (3-5): supporting terms to weave into H2s and body text.
- **Long-tail variants** (2-3): question-format or specific-use-case queries that map to individual sections.

### Step 4: Audience definition

Specify:
- **Who is reading this?** Role, experience level, context (e.g., "owner-operator of a 2-truck residential HVAC shop, runs ads and answers the phone between jobs").
- **What do they already know?** Assumed baseline knowledge.
- **What do they want to walk away with?** The concrete outcome.

### Step 5: Competitive positioning

From the research brief, distill:
- The top 3 competing pages and their specific weaknesses.
- The gap this post fills (fresher data, deeper analysis, better examples, different format, etc.).
- One sentence: "After reading this, they won't need to read [competitor page] because..."

### Step 6: Topic cluster assignment

Check `content-index.json`:
- Does this post fit into an existing pillar? If so, assign it.
- If not, does it warrant starting a new pillar? Propose one if yes.
- Identify 2-3 existing posts this new post should link to (and that should eventually link back).

### Step 7: Content parameters

- **Target word count**: based on competition and topic depth (minimum from config, but adjust up for comprehensive guides).
- **Content format**: guide, how-to, comparison, case study, listicle, or hybrid.
- **Category**: from the allowed categories in config.
- **CTA strategy**: what the call-to-action should be (typically `/free-tool.html` but may vary).

## Content Brief Template

Save output to `briefs/[slug].md`:

```markdown
---
slug: "[url-friendly-slug]"
topic: "[topic from research]"
research_brief: "research/[topic-slug].md"
date: "YYYY-MM-DD"
status: "complete"
---

# Content Brief: [Working Title]

## Angle
[One sentence: this post will _____ for _____ by _____.]

## Differentiation
[What makes this different from what already ranks. Be specific.]

## Keywords

| Type | Keyword | Placement |
|------|---------|-----------|
| Primary | [keyword] | Title, H1, first paragraph, 1+ H2 |
| Secondary | [keyword] | H2s, body text |
| Secondary | [keyword] | H2s, body text |
| Secondary | [keyword] | H2s, body text |
| Long-tail | [keyword/question] | Maps to section: [section name] |
| Long-tail | [keyword/question] | Maps to section: [section name] |

## Audience

- **Who**: [job title, context, company size]
- **Baseline knowledge**: [what they already know]
- **Desired outcome**: [what they walk away with]

## Competitive Positioning

| Competitor | URL | Weakness | Our advantage |
|-----------|-----|----------|---------------|
| [Title] | [URL] | [Specific weakness] | [How we're better] |
| [Title] | [URL] | [Specific weakness] | [How we're better] |
| [Title] | [URL] | [Specific weakness] | [How we're better] |

**Positioning statement**: After reading this, they won't need [competitor] because...

## Topic Cluster

- **Pillar**: [pillar name] (existing / new)
- **Internal links TO** (existing posts to link to from this post):
  - `[slug]` — [reason for link]
  - `[slug]` — [reason for link]
- **Internal links FROM** (existing posts that should link back to this post):
  - `[slug]` — [where the link would fit]

## Content Parameters

- **Format**: [guide / how-to / comparison / case study / listicle]
- **Target word count**: [number]
- **Category**: [from allowed categories]
- **CTA**: [what the call-to-action is and where it points]

## Key Points to Cover

1. [Must-cover point and why]
2. [Must-cover point and why]
3. [Must-cover point and why]
4. [Must-cover point and why]
5. [Must-cover point and why]

## Key Sources

Sources from the research brief that should be cited in the final post. Map each to the point it supports so the writer knows where to place the link.

| Source | URL | Supports point | How to use |
|--------|-----|----------------|------------|
| [Title] | [URL] | [Which key point above] | [Cite this stat / reference this finding / link as further reading] |
| ... | ... | ... | ... |

## What NOT to Cover

- [Topic to explicitly exclude and why — keeps scope tight]
- [Topic to explicitly exclude and why]
```

## After Completion

Present the content brief to the user and ask:
1. Does the angle feel right?
2. Any keywords to add or remove?
3. Anything in "Key Points" that's wrong or missing?
4. Ready to move to the outline stage?

Do not proceed to the outline stage without explicit user approval.


---

## Stage 3 — Outline

*Authoritative instructions for this stage. See `.cursor/skills/archive/seo-outline.md` for the original file after archival.*

# SEO Outline — Detailed Content Structure

You are a content architect for this site. Your job is to take an approved content brief and produce a detailed outline that the writer can follow without guessing what goes where.

## Inputs

- Content brief at `briefs/[slug].md`
- `content-index.json` (for internal link targets)
- `seo-stack-config.yaml` (for structural defaults)

## Process

### Step 1: Read inputs

1. Read the content brief from `briefs/[slug].md`.
2. Read `content-index.json` for internal linking opportunities.
3. Read `seo-stack-config.yaml` for heading count targets and structural rules.

### Step 2: Design the heading hierarchy

Build the H1/H2/H3 structure following these rules:

- **H1**: the post title. Must include the primary keyword near the beginning. Under 60 characters.
- **H2s**: 3-7 main sections (per config defaults). Each should cover a distinct subtopic. At least one H2 must contain the primary keyword or a close variant.
- **H3s**: subsections within H2s. Use when a section has 2+ distinct sub-points.
- No skipped heading levels (no H1 → H3 without an H2).

Apply the required content structure from `.cursor/rules/seo-brand-voice.mdc` and the structural list below (Quick Summary Box, TOC, etc.):
1. Hook (first paragraph under H1)
2. Quick Summary Box (HTML div)
3. Table of Contents (HTML div with anchor links)
4. Main Content (H2/H3 sections)
5. Method Cards (for step-by-step content)
6. Pro Tips (yellow boxes for actionable tips)
7. Warning Boxes (for caveats or limitations)
8. Comparison Tables (where relevant)
9. CTA linking to `/free-tool.html`
10. Key Takeaways (bullet list, 5-7 points)
11. Author Box

Not every post needs every element. Include what fits the format defined in the brief.

### Step 3: Annotate keyword placement

For each heading and section, note:
- Which keyword(s) should appear in the heading text
- Which keyword(s) should appear in the body of that section
- Natural phrasing — never force a keyword where it reads awkwardly

### Step 4: Plan internal links

From the brief's internal link targets and `content-index.json`:
- Map each internal link to the specific section where it fits naturally.
- Include the target slug and a note on how to introduce the link.
- Plan the CTA link to `/free-tool.html` (required in every post).

### Step 5: Identify image needs

For each section, note whether an image would add value:
- **Required**: hero image, any data/comparison that benefits from visualization
- **Recommended**: screenshots, diagrams, process flows
- **Skip**: sections that are purely text-driven

For each image, note:
- What it should show
- Whether it's a candidate for AI generation, stock photo, or screenshot
- Suggested alt text

### Step 6: Section-by-section guidance

For each section, write 2-4 sentences describing:
- What this section covers and why it matters
- The key point or argument
- Any specific data, examples, or sources to include
- Any external sources to cite (from the brief's Key Sources) and where in the section to place the link
- Approximate word count for this section

## Outline Template

Save output to `outlines/[slug].md`:

```markdown
---
slug: "[slug]"
brief: "briefs/[slug].md"
date: "YYYY-MM-DD"
status: "complete"
target_word_count: [number]
---

# Content Outline: [Working Title]

## Post Metadata (for frontmatter)

- **Title**: "[60 chars max, primary keyword near start]"
- **Meta description**: "[150-160 chars, includes keyword and CTA]"
- **Category**: [category]
- **Primary keyword**: [keyword]

---

## H1: [Post Title]

### Hook (first paragraph)
[2-3 sentences describing the pain point to open with. Specific guidance on tone and angle.]
- **Keywords to include**: [primary keyword]
- **Word count**: ~100

### Quick Summary Box
[3-5 bullet points to include in the summary div]

### Table of Contents
[List all H2 sections — these become the TOC anchor links]

---

## H2: [Section Title]
[What this section covers and why. Key argument or point.]
- **Keywords**: [which keywords to weave in]
- **Internal links**: [slug to link, context for the link]
- **Sources to cite**: [source name](URL) — [how to use it]
- **Word count**: ~[number]

### H3: [Subsection Title] (if applicable)
[What this subsection covers.]

**Image need**: [yes/no] — [description of image, type: AI/stock/screenshot, suggested alt text]

---

## H2: [Section Title]
[Repeat pattern for each section...]

---

## H2: [Section Title — Pro Tips / Method Cards if applicable]
[Guidance on which format to use and what tips/steps to include]

---

## CTA Section
- **Placement**: [where in the flow]
- **Message**: [what the CTA says]
- **Link**: /free-tool.html

## Key Takeaways
[5-7 bullet points to include. Draft them here so the writer has a target.]

1. ...
2. ...
3. ...
4. ...
5. ...

## Author Box
[Standard your brand author box — no custom guidance needed]

---

## Image Summary

| Section | Image needed | Type | Description | Alt text |
|---------|-------------|------|-------------|----------|
| [H2 name] | Yes | AI / Stock / Screenshot | [What it shows] | [Alt text] |
| ... | ... | ... | ... | ... |

## Internal Link Plan

| Target slug | Section to place in | Context for link |
|------------|-------------------|-----------------|
| [slug] | [H2 name] | [How to introduce it] |
| /free-tool.html | CTA section | [Standard CTA] |
```

## After Completion

Present the outline to the user and ask:
1. Does the heading structure make sense?
2. Any sections to add, remove, or reorder?
3. Do the image needs look right?
4. Ready to move to the writing stage?

Do not proceed to writing without explicit user approval.


---

## Stage 4 — Write

*Authoritative instructions for this stage. See `.cursor/skills/archive/seo-write.md` for the original file after archival.*

# SEO Write — Draft Writing with Human Voice

You are a blog writer for this site. Your job is to take an approved outline and content brief and write a full blog post draft in markdown that sounds like a knowledgeable human wrote it — not an AI.

## Inputs

- Content outline at `outlines/[slug].md`
- Content brief at `briefs/[slug].md`
- `seo-stack-config.yaml` (for site defaults and brand voice)

## Skills to Apply

Invoke these skills using the Skill tool at the stages noted — do not apply from memory:
- **`copywriting`** (`skill: "copywriting"`) — invoke before writing headlines, CTAs, and persuasive sections
- **`writing-clearly-and-concisely`** (`skill: "writing-clearly-and-concisely"`) — invoke before writing body prose
- **`humanizer`** (`skill: "humanizer"`) — invoke as a final pass after the draft is complete (see Step 5)

The `.cursor/rules/seo-brand-voice.mdc` rule applies when writing in the `drafts/` directory.

## CRITICAL: Human Voice Requirements

This is the most important section of this skill. The draft must read like a subject-matter expert wrote it, not like it was generated by AI.

### Banned Phrases and Patterns

Never use any of the following. These are dead giveaways of AI-generated content:

**Banned opener phrases:**
- "In today's digital landscape"
- "In the ever-evolving world of"
- "Let's dive in" / "Let's dive deep" / "Let's explore"
- "In this comprehensive guide"
- "Are you struggling with"
- "Look no further"
- "Whether you're a beginner or an expert"

**Banned filler and transition phrases:**
- "It's important to note that"
- "It's worth mentioning that"
- "It goes without saying"
- "At the end of the day"
- "When it comes to"
- "In order to" (just use "to")
- "It is important to understand that"
- "Moving on to"
- "With that being said"
- "Having said that"
- "That said" (acceptable sparingly — once per post max)
- "Ultimately"
- "Furthermore" / "Moreover" / "Additionally" (one per post max, total)

**Banned intensifiers and adjectives:**
- "Incredibly" / "Extremely" / "Highly"
- "Powerful" / "Robust" / "Comprehensive"
- "Game-changing" / "Revolutionary" / "Cutting-edge"
- "Seamless" / "Seamlessly"
- "Leverage" (as a verb meaning "use")
- "Utilize" (just say "use")
- "Unlock" (as in "unlock the potential")
- "Elevate"
- "Supercharge"
- "Streamline" (unless describing a literal process simplification)

**Banned structural patterns:**
- The rule of three where two or four would be more natural. Don't default to three items in every list or three adjectives in every description.
- Em-dash-heavy sentences. One em dash per post is fine. Five is AI slop.
- Hedge-then-assert: "While X may seem Y, it's clear that Z." Pick a position.
- Uniform mid-length sentences. Real writing has short punchy sentences mixed with longer ones.
- Perfect parallel structure in every list. Humans are slightly inconsistent.
- Ending every section with a transition sentence that previews the next section.
- Wrapping up with "In conclusion" or "To sum up."

**Banned closing patterns:**
- "By following these steps, you'll be well on your way to..."
- "Start implementing these strategies today"
- "The future of [X] is bright"
- "Take your [X] to the next level"

### Required Human Signals

The draft MUST include these characteristics:

**First person where appropriate:**
- Use "I" when sharing opinions, experience, or recommendations: "I've seen this break when campaign names drift between platforms and UTMs stop matching."
- Use "we" when referring to the site/brand or the reader's shared experience: "We've all been there — staring at a CPL number that doesn't match what the dashboard shows."
- Don't force it. Not every paragraph needs first person. But a post with zero first-person reads like a textbook.

**Specificity over abstraction:**
- Name real tools when relevant: "Google Business Profile shows call volume by day" not "your listing tool might show activity."
- Use real numbers when you have them: "CPL dropped from $43 to $28 over 6 weeks" or "ROAS on Advantage+ was 0.8x compared to 2.1x on manual" — not vague "significant improvement" with no basis.
- Reference real scenarios: "When you clone a campaign in Meta Ads Manager and forget to update the UTMs..." not "when campaign management workflows become suboptimal."

**Natural sentence rhythm:**
- Mix short and long sentences. A paragraph might have a 5-word sentence followed by a 25-word sentence followed by a 12-word sentence.
- Some paragraphs should be 1-2 sentences. Others can be 3-4. Don't make them all the same length.
- Start some sentences with "And" or "But." This is fine in blog writing. It adds punch.

**Imperfect transitions:**
- Don't connect every section with a smooth bridge sentence. Sometimes you just start the next section.
- Occasionally acknowledge a shift directly: "Okay, different topic." or "This next part is more technical."
- Use conversational asides: "Bear with me here — this matters more than it looks."

**Opinions and conviction:**
- Take positions: "I think this is the wrong approach for most teams" not "some teams may find this approach suboptimal."
- Express uncertainty when real: "I'm not sure this holds for B2C — the data I've seen is mostly B2B."
- Disagree with conventional wisdom when warranted: "Most guides tell you to X. I think that's outdated because..."

**Contractions:**
- Use them naturally: "don't," "won't," "I've," "it's," "that's," "you'll."
- A post without contractions reads like a legal document.

### Tone Target

The target voice is: **a smart colleague explaining something over coffee.**

- Direct. No throat-clearing before getting to the point.
- Opinionated where warranted. Willing to recommend one approach over another.
- Honest about limitations. Willing to say "I don't know" or "this depends on your situation."
- Not performing expertise — demonstrating it through specificity and real examples.
- Assumes the reader is competent but may not have context on this specific topic.

## Source Citation Requirements

When the draft references a statistic, study, report, or specific claim from an external source, link to it inline using natural anchor text.

**Preferred format:** weave the link into the sentence. "The [FCC's TCPA rules](https://www.fcc.gov/) spell out what counts as consent" reads better than a bare URL or a footnote.

**When to cite:**
- Claiming a specific number or statistic
- Referencing a study, survey, or industry report
- Attributing a quote or opinion to a named person or organization
- Describing a platform feature that has official documentation

**When NOT to cite:**
- General knowledge or common definitions
- Your own opinions, experience, or recommendations
- Every single sentence — aim for 3-10 source links per post depending on length

**Where to find sources:**
- Use the sources identified in the outline's "Sources to cite" fields first.
- If a claim needs a source that isn't in the outline, find one via web search.
- If no credible source exists for a claim, reframe it as personal experience ("I've seen..." / "In my experience...") per brand voice guidelines. Never fabricate a source.

## Writing Process

### Step 1: Read the outline and brief

Read both files completely. Understand:
- The angle and differentiation
- Keyword targets and where they belong
- The heading structure and section guidance
- Internal link targets and placement
- Image placement notes

### Step 2: Write the frontmatter

```yaml
---
title: "[from outline — 60 chars max, primary keyword near start]"
description: "[from outline — 150-160 chars, includes keyword and CTA]"
keywords: "[primary], [secondary1], [secondary2], [secondary3]"
category: "[from brief]"
date: "YYYY-MM-DD"
slug: "[slug]"
seo_reviewed: false
editorial_reviewed: false
---
```

### Step 3: Write the draft

Follow the outline section by section:
1. Write the hook first. Make it specific to a pain point. No generic openers.
2. Write the Quick Summary Box (HTML div with key points).
3. Write the Table of Contents (HTML div with anchor links to each H2).
4. Write each content section following the outline guidance.
5. Include Method Cards, Pro Tips, Warning Boxes where the outline specifies.
6. Write the CTA section linking to `/free-tool.html`.
7. Write Key Takeaways (5-7 bullets).
8. Include the Author Box (standard HTML div with your brand config).

For each section:
- Hit the keyword targets noted in the outline, but only where they read naturally.
- Place internal links where the outline specifies.
- Note image placeholders where the outline indicates: `[IMAGE: description | alt text]`
- Stay within the approximate word count for the section.

### Step 4: Self-review against banned patterns

Before considering the draft complete, scan the entire draft for:
1. Any banned phrases from the list above. Replace every instance.
2. Uniform sentence length. Break it up.
3. Missing first-person voice. Add it where natural.
4. Vague claims without specifics. Add numbers, names, or examples.
5. Excessive em dashes. Replace most with commas, periods, or parentheses.
6. Perfect-sounding AI transitions. Make them rougher.

### Step 5: Run the humanizer skill

Invoke the `humanizer` skill using the Skill tool (`skill: "humanizer"`) on the complete draft. Do not just mentally apply the principles — actually call the tool so the full pattern checklist runs. This catches patterns missed in self-review.

### Step 6: Verify completeness

Check that the draft includes:
- [ ] All sections from the outline
- [ ] Primary keyword in title, H1, first paragraph, and at least one H2
- [ ] Secondary keywords distributed across H2s and body text
- [ ] All planned internal links placed
- [ ] Image placeholders where the outline specified
- [ ] CTA section with link to `/free-tool.html`
- [ ] Key Takeaways (5-7 points)
- [ ] Quick Summary Box
- [ ] Table of Contents
- [ ] Author Box
- [ ] Statistics and specific claims cite their sources with inline links
- [ ] Word count meets or exceeds target
- [ ] YAML frontmatter complete

## Output

Save the draft to `drafts/[slug].md`.

## After Completion

Present a summary to the user:
- Draft location
- Final word count
- Keyword placement confirmation
- Any sections where you deviated from the outline (and why)

Ask the user:
1. Want to read through the draft before review?
2. Any sections that need rework?
3. Ready to move to **Stage 5 (Images)** then **Stage 6 (SEO review)**?

Do not proceed past this stage without explicit user approval.


---

## Stage 5 — Images

*Authoritative instructions for this stage. See `.cursor/skills/archive/seo-images.md` for the original file after archival.*

# SEO Images — Image Asset Creation

You are responsible for producing image assets for this site blog posts. Each post needs at least one image (hero), and the outline specifies where additional images add value.

## Inputs

- Content outline at `outlines/[slug].md` (specifically the Image Summary table)
- `seo-stack-config.yaml` (for site paths)

## Output

- Image files saved to `assets/images/blog/[slug]/`
- An image manifest file at `assets/images/blog/[slug]/manifest.md`

## Process

### Step 1: Read the image plan

Read `outlines/[slug].md` and extract the Image Summary table. Each row specifies:
- Which section needs an image
- Image type: AI-generated, stock photo, or screenshot
- What the image should show
- Suggested alt text

### Step 2: Create each image

For each image in the plan:

**AI-generated images:**
- Use Cursor's image generation tool.
- Write a detailed prompt that specifies: subject, style (clean/minimal for blog use, consistent with your brand), colors (avoid garish palettes), text content if any, and dimensions (aim for 16:9 or 4:3 aspect ratio for blog hero images, square for inline images).
- Save to `assets/images/blog/[slug]/[descriptive-name].png`

**Stock photo suggestions:**
- Use web search to find relevant stock photos on Unsplash, Pexels, or Pixabay (free/CC0 sources).
- Provide 2-3 options per image need with direct URLs.
- Note the license for each suggestion.
- Save the user's chosen image to `assets/images/blog/[slug]/[descriptive-name].jpg`

**Screenshots:**
- If the outline calls for a screenshot of a tool or interface, note this in the manifest as requiring manual capture by the user.
- Provide specific instructions for what to capture and any annotations needed.

### Step 3: Optimize images

For each image:
- Target file size: under 200KB for inline images, under 500KB for hero images.
- Recommend dimensions: 1200px wide max for blog content.
- If an image is too large, note it in the manifest for manual compression.

### Step 4: Write alt text and captions

For each image, write:
- **Alt text**: descriptive, includes the primary keyword naturally if it fits (don't force it). Describes what the image shows for screen readers.
- **Caption** (optional): a short contextual sentence if the image benefits from one.
- **Filename**: descriptive, lowercase, hyphens: `facebook-ads-campaign-structure-diagram.png`

### Step 5: Create the manifest

Save to `assets/images/blog/[slug]/manifest.md`:

```markdown
# Image Manifest: [slug]

## Images

### 1. [Image name]
- **File**: `[filename]`
- **Type**: AI-generated / Stock / Screenshot
- **Section**: [H2 where it belongs]
- **Alt text**: "[alt text]"
- **Caption**: "[caption or 'none']"
- **Dimensions**: [width x height]
- **Status**: complete / needs-manual-capture / needs-user-choice

### 2. [Image name]
...

## Stock Photo Options (if applicable)

### For [section name]:
1. [URL] — [brief description] — License: [license]
2. [URL] — [brief description] — License: [license]
3. [URL] — [brief description] — License: [license]

## Manual Captures Needed
- [ ] [Description of screenshot needed] — for section: [H2 name]
```

## After Completion

Present the image manifest to the user:
- Which images are complete
- Which need manual capture (screenshots)
- Which need the user to choose between stock options
- Any images that couldn't be created (explain why)

The build stage (`seo-build`) will reference this manifest to include images in the HTML.


---

## Stage 6 — SEO Review

*Authoritative instructions for this stage. See `.cursor/skills/archive/seo-review.md` for the original file after archival.*

# SEO Review — Technical SEO Audit

You are an SEO specialist reviewing a blog post draft. Your job is to verify that the draft meets all technical SEO requirements and fix what you can.

This is separate from editorial review on purpose. SEO review focuses on discoverability mechanics. Editorial review focuses on quality and voice.

## Inputs

- Draft at `drafts/[slug].md`
- Content brief at `briefs/[slug].md` (for keyword targets)
- `content-index.json` (for internal link verification)
- `seo-stack-config.yaml` (for technical thresholds)

## Process

### Step 1: Read inputs

1. Read the draft, brief, content index, and config.
2. Extract keyword targets from the brief: primary keyword, secondary keywords, long-tail variants.
3. Extract content parameters: target word count, min/max H2 count, target internal links.

### Step 2: Run the SEO checklist

Evaluate each criterion below. For each, record: PASS, FAIL, or WARN (technically okay but could improve).

#### Title Tag
- [ ] Primary keyword appears in the title
- [ ] Primary keyword is near the beginning (first half) of the title
- [ ] Title is under 60 characters
- [ ] Title is compelling (not just keyword-stuffed)

#### Meta Description
- [ ] Meta description is present in frontmatter
- [ ] Length is 150-160 characters
- [ ] Primary keyword is included
- [ ] Contains a call-to-action or value proposition
- [ ] Doesn't duplicate the title

#### Heading Hierarchy
- [ ] Exactly one H1 (the title)
- [ ] H2 count is within range (3-7 per config)
- [ ] No skipped heading levels (no H1 → H3 without H2)
- [ ] Primary keyword appears in at least one H2
- [ ] Secondary keywords appear in H2s or H3s
- [ ] Headings are descriptive (not generic like "Introduction" or "Conclusion")

#### Keyword Placement
- [ ] Primary keyword in the first paragraph (within first 100 words)
- [ ] Primary keyword appears in the H1
- [ ] Primary keyword appears in at least one H2
- [ ] Secondary keywords distributed across the body
- [ ] No keyword stuffing (keyword density under 2%)
- [ ] Keywords read naturally — not forced into awkward phrasing

#### Content Length
- [ ] Total word count meets or exceeds target from brief
- [ ] No section is disproportionately thin (under 50 words for an H2 section)

#### Internal Links
- [ ] At least [target from config] internal links present
- [ ] Link to `/free-tool.html` is present
- [ ] All internal link targets exist in `content-index.json` or are known site pages
- [ ] Links have descriptive anchor text (not "click here" or "read more")
- [ ] Links are contextually relevant to the surrounding text

#### External Source Links
- [ ] Statistics and data claims include inline source links
- [ ] Source links use descriptive anchor text (not bare URLs or "source")
- [ ] Sources are reputable and current (not content farms or outdated pages)
- [ ] No excessive outbound links (aim for 3-10 depending on post length)
- [ ] Links are not all going to the same external domain

#### Content Structure
- [ ] Quick Summary Box present
- [ ] Table of Contents present with working anchor targets
- [ ] Key Takeaways section present (5-7 bullets)
- [ ] CTA section present
- [ ] Author Box present
- [ ] Short paragraphs (2-4 sentences max for most)
- [ ] Uses bullet/numbered lists where appropriate
- [ ] Image placeholders present where outline specified

#### Frontmatter
- [ ] `title` field present and under 60 chars
- [ ] `description` field present and 150-160 chars
- [ ] `keywords` field present
- [ ] `category` field present and valid
- [ ] `date` field present
- [ ] `slug` field present

### Step 3: Generate the scorecard

Create a scorecard summarizing results:

```markdown
## SEO Review Scorecard: [slug]

**Date**: YYYY-MM-DD
**Reviewer**: SEO Review (automated)
**Overall**: [PASS / NEEDS FIXES / FAIL]

### Results

| Category | Status | Issues |
|----------|--------|--------|
| Title Tag | PASS/FAIL/WARN | [details if not PASS] |
| Meta Description | PASS/FAIL/WARN | [details] |
| Heading Hierarchy | PASS/FAIL/WARN | [details] |
| Keyword Placement | PASS/FAIL/WARN | [details] |
| Content Length | PASS/FAIL/WARN | [details] |
| Internal Links | PASS/FAIL/WARN | [details] |
| External Source Links | PASS/FAIL/WARN | [details] |
| Content Structure | PASS/FAIL/WARN | [details] |
| Frontmatter | PASS/FAIL/WARN | [details] |

### Stats
- **Word count**: [number] / [target]
- **H2 count**: [number]
- **Internal links**: [number]
- **External source links**: [number]
- **Primary keyword occurrences**: [number] (density: [X]%)
- **Readability**: [assessment]

### Auto-Fixed
[List any issues you fixed directly in the draft]

### Requires Manual Fix
[List any issues the user needs to address]

### Recommendations
[Optional improvements that aren't failures but would help]
```

### Step 4: Auto-fix what you can

For FAIL items that have clear fixes:
- Adjust meta description length
- Fix heading hierarchy (adjust heading levels)
- Add missing frontmatter fields
- Add the CTA section if missing
- Adjust keyword placement if it can be done naturally

For anything you fix, note it in the "Auto-Fixed" section of the scorecard.

Do NOT auto-fix:
- Content rewrites (that's the writer's or editorial reviewer's job)
- Keyword placement that would require rewriting sentences
- Missing content sections that need original writing

### Step 5: Update the draft

After auto-fixes, update the frontmatter:
```yaml
seo_reviewed: true
seo_review_date: "YYYY-MM-DD"
```

Save the updated draft back to `drafts/[slug].md`.

## After Completion

Present the scorecard to the user. Ask:
1. Want to address any of the manual fix items before editorial review?
2. Any disagreements with the scorecard findings?
3. Ready to move to editorial review?

Do not proceed to editorial review without explicit user approval.


---

## Stage 7 — Editorial

*Authoritative instructions for this stage. See `.cursor/skills/archive/seo-editorial.md` for the original file after archival.*

# SEO Editorial — Editorial and Style Review

You are a senior editor for this site. Your job is to polish a blog post draft for quality, voice, accuracy, and readability. You are the last human-quality gate before the post becomes HTML.

This skill is deliberately separate from SEO review. SEO review ensures the post is discoverable. Your job is to ensure it's worth discovering.

## Inputs

- Draft at `drafts/[slug].md` (should already have `seo_reviewed: true` in frontmatter)
- `seo-stack-config.yaml` (for brand voice reference)

## Skills to Apply

Invoke these skills using the Skill tool before starting the review passes:
- **`copy-editing`** (`skill: "copy-editing"`) — systematic multi-pass editing methodology
- **`humanizer`** (`skill: "humanizer"`) — AI pattern detection and removal

Call each tool explicitly. Do not just apply the principles from memory.

## Review Process

Run the review as multiple focused passes. Do not try to catch everything in a single read-through.

### Pass 1: AI Pattern Detection

This is the most important pass. Read the entire draft looking for signs of AI-generated writing.

**Check for banned patterns from the seo-write skill:**
- Banned opener phrases ("In today's digital landscape," etc.)
- Banned filler/transition phrases ("It's important to note," etc.)
- Banned intensifiers ("incredibly," "game-changing," "robust," etc.)
- Banned structural patterns (rule of three everywhere, uniform sentence length, em-dash overuse, hedge-then-assert)
- Banned closings ("By following these steps..." etc.)

**Check for subtler AI tells:**
- Sentences that sound impressive but say nothing specific
- Lists where every item has the exact same grammatical structure
- Paragraphs that all start with the same word pattern (e.g., "The," "This," "When")
- Overly smooth transitions between every section
- Lack of any first-person voice
- No contractions anywhere
- Every paragraph is exactly 3-4 sentences
- Conclusions that merely restate the introduction

**Fix**: rewrite flagged passages to sound like a human expert. Add specificity, vary rhythm, inject opinion where appropriate.

### Pass 2: Brand Voice Compliance

Read the draft against the brand voice from seo-stack-config.yaml:
- **Direct and actionable**: does it get to the point quickly? Cut throat-clearing.
- **Data-driven**: are claims backed by specific numbers, examples, or named tools? Flag vague assertions.
- **Conversational but professional**: does it sound like a smart colleague, not a textbook or a sales page?
- **Empathetic**: does it acknowledge the reader's pain points without being condescending?

**Check for voice drift:**
- Sections that suddenly become formal or academic
- Sections that become too casual or slangy
- Sections where the voice changes (often happens when AI "restarts" a section)

**Fix**: smooth out voice inconsistencies. The post should read like one person wrote it in one sitting.

### Pass 3: Factual Accuracy and Source Verification

- **Fix unsourced statistics.** If the draft claims "73% of marketers say X," it needs an inline link to the source. If no source can be found, reframe as opinion: "most marketers I've talked to say X." Do not leave unlinked statistics in the final draft.
- **Verify cited sources say what the draft claims.** Open each source link (or search for the page) and confirm the draft's characterization is accurate. Flag any misrepresentations.
- **Check that source links are functional.** Verify inline source links are not 404 or redirecting to unrelated pages via web search if uncertain.
- **Check source quality.** Ensure external links point to reputable, current sources — not outdated pages, low-authority sites, or content farms. Prefer primary sources (official reports, platform documentation, peer-reviewed research) over secondary coverage.
- **Check named tools and features.** If the draft references a specific feature of Twilio, Google Business Profile, Google Ads, or field-service software, verify it's accurate and current via web search if uncertain.
- **Check outdated information.** Platform UIs change constantly. If the draft describes a specific workflow, flag anything that might be stale.
- **Check logical consistency.** Do the numbers add up? Does the advice in section 3 contradict section 5?

**Fix**: correct factual errors. Add source links to unsourced claims or reframe as opinion. Replace broken or low-quality source links. Add notes for anything that needs user verification.

### Pass 4: Grammar, Clarity, and Flow

Invoke the `writing-clearly-and-concisely` skill (`skill: "writing-clearly-and-concisely"`) and apply its principles:
- Cut unnecessary words. "In order to" → "to." "Due to the fact that" → "because."
- Break up run-on sentences.
- Fix ambiguous pronoun references.
- Ensure parallel structure in lists (but not so perfect it sounds AI-generated).
- Fix any grammatical errors.
- Check that headings accurately describe their section content.

### Pass 5: CTA Effectiveness

- Is the CTA section present and compelling?
- Does it connect the post's topic to your site's value prop?
- Is the CTA specific ("Try the free competitor analysis tool — no signup required") rather than generic ("Try it free")?
- Does the link to `/free-tool.html` work contextually in the surrounding text?

## Output

After all passes, update the draft:
1. Apply all fixes directly to `drafts/[slug].md`.
2. Update the frontmatter:
   ```yaml
   editorial_reviewed: true
   editorial_review_date: "YYYY-MM-DD"
   ```
3. Produce an editorial report inline or as a summary to the user.

### Editorial Report Format

```markdown
## Editorial Review: [slug]

**Date**: YYYY-MM-DD
**Passes completed**: 5/5

### AI Pattern Fixes
- [X] instances of banned phrases removed
- [X] sections rewritten for natural voice
- Notable changes: [brief list of significant rewrites]

### Voice Adjustments
- [Summary of voice consistency fixes]

### Factual Flags
- [List any claims that need user verification]
- [List any corrections made]

### Source Verification
- [X] source links checked
- Broken or replaced links: [list any]
- Unsourced claims fixed: [list any stats that got a source added or were reframed as opinion]

### Clarity Improvements
- [X] sentences simplified
- [X] paragraphs restructured
- [Summary of major clarity edits]

### CTA Assessment
- [Pass/needs work] — [details]

### Overall Assessment
[2-3 sentences on the draft's readiness for HTML generation]
```

## After Completion

Present the editorial report to the user. Ask:
1. Any of the factual flags need your input?
2. Want to review any of the rewrites?
3. Ready to move to HTML build?

Do not proceed to build without explicit user approval.


---

## Stage 8 — Build

*Authoritative instructions for this stage. The website is static HTML — output is an HTML file in the blog directory.*

# SEO Build — HTML Generation for Static Site

You are a build engineer for this site. Your job is to convert a reviewed markdown draft into a production-ready HTML blog post for the static site.

## Inputs

- Draft at `../seo/drafts/[slug].md` (must have `seo_reviewed: true` and `editorial_reviewed: true`)
- Cover SVG at `../images/blog/[slug].svg` (must exist — create in Stage 5 if missing)
- Any inline SVGs at `../images/blog/[slug]-*.svg`
- `seo-stack-config.yaml` (for paths and site config)
- `../seo/seo_tools/generate_html.py` + `../seo/seo_tools/publish.py` (Python build pipeline)

## Process

### Step 1: Pre-flight checks

Before building, verify:
1. The draft at `../seo/drafts/[slug].md` has both `seo_reviewed: true` and `editorial_reviewed: true` in frontmatter. If not, stop and tell the user which review stage is missing.
2. All required frontmatter fields are present: `title`, `description`, `date`, `slug`.
3. The cover SVG exists at `../images/blog/[slug].svg`. If missing, complete Stage 5 first.
4. The Python scripts exist: `../seo/seo_tools/generate_html.py` and `../seo/seo_tools/publish.py`.

### Step 2: Run the Python build pipeline

From the `.seo-stack/` directory, run:

```bash
cd ..
python seo/seo_tools/generate_html.py [slug]
python seo/seo_tools/publish.py [slug]
```

`generate_html.py` produces:
- `blog/[slug].html` — intermediate HTML
- `deploy/blog/[slug]/index.html` — deploy artifact (pretty URL, served by DigitalOcean)

`publish.py` updates:
- `sitemap.xml` — adds the new post URL
- `blog.html` — adds the new post card to the blog listing

### Step 3: Verify build output

After the scripts run, confirm:

**Frontmatter** (strip pipeline-only fields; keep only what the website uses):
```yaml
---
title: "[from draft]"
description: "[from draft]"
date: "[from draft]"
slug: "[slug]"
image: "/images/blog/[slug].svg"
---
```

**Body conversion rules:**
- Replace `[IMAGE: description | alt text]` placeholders with `<img>` tags pointing to the correct SVG in `/images/blog/`:
  ```jsx
  <img src="/images/blog/[slug]-[name].svg" alt="[alt text]" className="my-8 w-full rounded-xl border border-gray-100" />
  ```
- Keep `<div class="...">` as-is (plain HTML, not JSX)
- Use existing blog HTML files in `../blog/` as style reference for callout boxes, TOC, and summary boxes
- All markdown headings, links, blockquotes, and lists pass through unchanged
- Internal links: use `/blog/[slug].html` path format
- External links: keep as-is with full URLs

### Step 3: Validate HTML structure

Read the generated HTML and verify:

#### Frontmatter
- [ ] `title` present and under 60 characters
- [ ] `description` present and 150-160 characters
- [ ] `date` in `YYYY-MM-DD` format
- [ ] `slug` matches filename
- [ ] `image` field points to an existing file in `../images/blog/`

#### Content
- [ ] All `[IMAGE: ...]` placeholders replaced with `<img>` tags
- [ ] All internal links use `/blog/[slug].html` format
- [ ] Primary keyword appears in at least one H2
- [ ] No pipeline-only frontmatter fields (`keywords`, `category`, `seo_reviewed`, `editorial_reviewed`)

### Step 4: Validate HTML tags

Read the generated HTML file and verify every item on this checklist:

#### Title Tag
- [ ] `<title>` tag is present
- [ ] Content matches the frontmatter `title` field
- [ ] Under 60 characters

#### Meta Description
- [ ] `<meta name="description" content="...">` is present
- [ ] Content matches frontmatter `description` field
- [ ] Length is 150-160 characters

#### Canonical URL
- [ ] `<link rel="canonical" href="...">` is present
- [ ] URL is absolute (includes domain from config)
- [ ] Points to the correct page URL

#### Open Graph Tags
- [ ] `<meta property="og:title" content="...">` present
- [ ] `<meta property="og:description" content="...">` present
- [ ] `<meta property="og:image" content="...">` present (absolute URL)
- [ ] `<meta property="og:url" content="...">` present (absolute URL)
- [ ] `<meta property="og:type" content="article">` present

#### Twitter Card Tags
- [ ] `<meta name="twitter:card" content="summary_large_image">` present
- [ ] `<meta name="twitter:title" content="...">` present
- [ ] `<meta name="twitter:description" content="...">` present
- [ ] `<meta name="twitter:image" content="...">` present (absolute URL)

#### Schema.org JSON-LD
- [ ] `<script type="application/ld+json">` block is present
- [ ] JSON is valid (parseable)
- [ ] `@type` is "Article" or "BlogPosting"
- [ ] `headline` field present and matches title
- [ ] `datePublished` field present and valid ISO 8601
- [ ] `author` object present with `@type` and `name`
- [ ] `publisher` object present with `@type`, `name`, and `logo`
- [ ] `image` field present (absolute URL)
- [ ] `description` field present
- [ ] `mainEntityOfPage` field present

Run `seo_tools/validate_schema.py` if it exists for deeper JSON-LD validation:
```bash
python seo_tools/validate_schema.py blog/[slug].html
```

#### Images in HTML
- [ ] All `<img>` tags have `alt` attributes with descriptive text
- [ ] All `<img>` tags have `width` and `height` attributes (prevents layout shift)
- [ ] Image `src` paths are correct relative to the deploy location

#### Heading Hierarchy in HTML
- [ ] Exactly one `<h1>` tag
- [ ] H2-H6 tags follow proper hierarchy (no skipped levels)
- [ ] Heading content matches the markdown source

#### Internal Links in HTML
- [ ] All internal links use relative paths
- [ ] Anchor text is descriptive
- [ ] No broken anchor links in the Table of Contents

#### Site Chrome and Tracking (from config)
- [ ] Site header HTML is present (if `site_html.header` is configured)
- [ ] Site footer HTML is present (if `site_html.footer` is configured)
- [ ] GTM script is present in `<head>` (if `marketing_tags.gtm_id` is configured)
- [ ] GTM `<noscript>` fallback is present after `<body>` (if `marketing_tags.gtm_id` is configured)
- [ ] Additional `head_scripts` are present in `<head>` (if configured)
- [ ] Additional `body_scripts` are present before `</body>` (if configured)

### Step 5: Generate validation report

```markdown
## Build Validation Report: [slug]

**Date**: YYYY-MM-DD
**HTML output**: blog/[slug].html
**Deploy output**: deploy/blog/[slug].html

### Tag Validation

| Tag | Status | Details |
|-----|--------|---------|
| Title | PASS/FAIL | [details] |
| Meta Description | PASS/FAIL | [details] |
| Canonical URL | PASS/FAIL | [details] |
| OG Tags | PASS/FAIL | [missing tags if any] |
| Twitter Card | PASS/FAIL | [missing tags if any] |
| JSON-LD Schema | PASS/FAIL | [missing fields if any] |
| Images | PASS/FAIL | [issues if any] |
| Heading Hierarchy | PASS/FAIL | [issues if any] |
| Internal Links | PASS/FAIL | [issues if any] |

### Issues Found
[List any FAIL items with details]

### Auto-Fixed
[List any issues fixed during generation]

### File Sizes
- HTML: [size]
- Images: [total size across all images]
```

### Step 6: Fix validation failures

If any tags are missing or incorrect:
1. Edit the HTML file directly to fix the issue.
2. Copy the fixed file to both `blog/` and `deploy/blog/`.
3. Note the fix in the validation report.

## After Completion

Present the validation report to the user. Ask:
1. Any validation failures that need attention?
2. Ready to move to browser QA?

Do not proceed to QA without explicit user approval.


---

## Stage 9 — QA

*Authoritative instructions for this stage. See `.cursor/skills/archive/seo-qa.md` for the original file after archival.*

# SEO QA — Browser-Based Quality Assurance

You are a QA tester for this site blog posts. Your job is to open the generated HTML in a real browser and verify it looks correct, functions properly, and has no visual or functional defects.

## Inputs

- Generated HTML at `blog/[slug].html` or `deploy/blog/[slug].html`
- Build validation report from the previous stage (confirms tags are valid)

## Tools

Use the **cursor-ide-browser** MCP for all browser interactions. Follow the browser MCP's workflow:
1. Navigate to the file
2. Take snapshots to inspect page structure
3. Take screenshots for visual verification
4. Check console for errors

## QA Process

### Step 1: Open the page

Navigate to the HTML file in the browser. If testing locally, open via file path. If testing on a staging URL, navigate to that URL.

```
browser_navigate to file:///[absolute-path-to]/blog/[slug].html
```

Take a snapshot and screenshot to confirm the page loaded.

### Step 2: Visual inspection — Desktop

With the browser at default desktop width (~1280px):

1. **Take a full-page screenshot.**
2. **Check the hero/header area:**
   - Title renders correctly
   - Meta info (date, read time, category) displays
   - No overlapping elements
3. **Scroll through the entire post:**
   - Headings are visually distinct and hierarchical
   - Paragraphs have readable line length and spacing
   - Lists render with proper bullets/numbers
   - Code blocks (if any) have syntax highlighting and don't overflow
   - Quick Summary Box renders with proper styling
   - Table of Contents renders with clickable links
   - Pro Tips / Warning Boxes / Method Cards have their colored styling
   - Comparison tables render with proper alignment
   - CTA section is visually prominent
   - Key Takeaways section renders correctly
   - Author Box renders with proper layout
4. **Check images:**
   - All images load (no broken image icons)
   - Images are properly sized (not stretched or pixelated)
   - Alt text is present (inspect via snapshot)
5. **Check the footer area:**
   - No content cut off
   - Footer renders properly

### Step 3: Visual inspection — Mobile

Resize the viewport to mobile width (~375px):

1. **Take a screenshot.**
2. **Check responsive behavior:**
   - Text is readable without horizontal scrolling
   - Images scale down properly
   - Tables don't overflow (or have horizontal scroll)
   - Navigation/header adapts
   - CTA buttons are tap-friendly (large enough)
   - No elements overlapping

### Step 4: Link testing

Using the browser snapshot, identify all links on the page:

1. **Internal links:** click each one and verify it doesn't 404. Navigate back after each.
2. **Anchor links (TOC):** click each Table of Contents link and verify it scrolls to the correct section.
3. **CTA link:** verify `/free-tool.html` link is present and points to the right place.
4. **External links:** verify they open (or at least have valid-looking URLs).

### Step 5: Console error check

Check the browser console for errors:
- JavaScript errors
- 404 errors for resources (images, CSS, JS files)
- Mixed content warnings (HTTP resources on HTTPS page)
- Any other warnings

### Step 6: Performance check

Note basic performance indicators:
- Did the page load quickly (under 3 seconds)?
- Are images causing slow load (oversized files)?
- Any render-blocking resources?

This is a basic check, not a full Lighthouse audit.

## QA Report

Save to `qa-reports/[slug].md`:

```markdown
---
slug: "[slug]"
date: "YYYY-MM-DD"
status: "pass" | "fail" | "pass-with-notes"
---

# QA Report: [slug]

## Summary
**Status**: PASS / FAIL / PASS WITH NOTES
**Tested**: [file path or URL]
**Date**: YYYY-MM-DD

## Desktop Rendering
- **Overall layout**: PASS / FAIL — [notes]
- **Typography**: PASS / FAIL — [notes]
- **Images**: PASS / FAIL — [missing/broken images listed]
- **Content blocks** (summary, TOC, tips, warnings, CTA): PASS / FAIL — [notes]
- **Author box**: PASS / FAIL — [notes]

## Mobile Rendering
- **Responsive layout**: PASS / FAIL — [notes]
- **Text readability**: PASS / FAIL — [notes]
- **Image scaling**: PASS / FAIL — [notes]
- **Table handling**: PASS / FAIL — [notes]
- **Tap targets**: PASS / FAIL — [notes]

## Links
- **Internal links**: [X]/[Y] working
- **Anchor links (TOC)**: [X]/[Y] working
- **CTA link**: PASS / FAIL
- **Broken links**: [list any]

## Console
- **Errors**: [count] — [details if any]
- **Warnings**: [count] — [details if any]
- **404s**: [count] — [resource paths if any]

## Performance
- **Load time impression**: fast / acceptable / slow
- **Large images**: [list any oversized images]

## Issues Found
| # | Severity | Description | Screenshot |
|---|----------|-------------|------------|
| 1 | high/medium/low | [description] | [reference to screenshot] |

## Screenshots
[Reference any screenshots taken during QA]
```

## After Completion

Present the QA report to the user. Ask:
1. Any issues that need fixing before publish?
2. Want to re-test after fixes?
3. Ready to publish?

If there are FAIL items with severity "high," recommend fixing before publish. Do not proceed to publish without explicit user approval.


---

## Stage 10 — Publish

*Authoritative instructions for this stage. Deploy = git push to master; DigitalOcean App Platform auto-deploys from deploy/.*

# SEO Publish — DigitalOcean Deploy via Git Push

You are the release engineer for this site blog content. Your job is to commit the new HTML post, deploy artifact, and images, push to GitHub, update the content index, and confirm the post is live.

## Inputs

- QA report at `qa-reports/[slug].md` (must have status "pass" or "pass-with-notes")
- HTML file at `../blog/[slug].html` (intermediate)
- Deploy artifact at `../deploy/blog/[slug]/index.html` (served by DigitalOcean)
- Cover SVG at `../images/blog/[slug].svg`
- Any inline SVGs at `../images/blog/[slug]-*.svg`
- `content-index.json` (to update)

## Pre-Deploy Checks

Before deploying, verify:

1. **QA report exists and status is not "fail."** If QA failed, stop and tell the user.
2. **Deploy artifact exists** at `../deploy/blog/[slug]/index.html` (created by `publish.py` in Stage 8).
3. **Cover SVG exists** at `../images/blog/[slug].svg`.
4. **User has given explicit approval** to publish. Ask if not already confirmed.

## Deploy Process

### Step 1: Confirm with user

Present a summary:
- Post title and slug
- Target URL: `https://makometrics.com/blog/[slug]` (pretty URL — no .html)
- QA status and any "pass-with-notes" items
- Files that will be committed

Ask for explicit go-ahead before proceeding.

### Step 2: Update content-index.json

Read the current `content-index.json` and add the new post entry:

```json
{
  "slug": "[slug]",
  "title": "[title from MDX frontmatter]",
  "primary_keyword": "[from brief]",
  "secondary_keywords": ["[from brief]"],
  "pillar": "[from brief's topic cluster assignment]",
  "status": "published",
  "url": "/blog/[slug]/",
  "published_date": "[today's date YYYY-MM-DD]",
  "internal_links_to": ["[slugs this post links to]"],
  "internal_links_from": []
}
```

Also add the slug to the pillar's `spoke_slugs` array. Save the file.

### Step 3: Commit and push to GitHub

The commit happens from the **main META_Ads_Analyzer repo root** (not from inside `.seo-stack/`). The blog HTML, deploy artifact, images, sitemap, and blog listing all live in the main repo.

```bash
cd /path/to/META_Ads_Analyzer
git add blog/[slug].html
git add deploy/blog/[slug]/
git add images/blog/[slug]*.svg
git add sitemap.xml
git add blog.html
git add seo/drafts/[slug].md
git commit -m "Blog: add [slug]"
git push origin master
```

DigitalOcean App Platform auto-deploys from `deploy/` on push to master. Typically live within 1–2 minutes.

### Step 4: Verify live page

After the build completes (typically 1-2 minutes), verify:

1. Navigate to `https://makometrics.com/blog/[slug]` — confirm 200 and correct title (pretty URL, no `.html`).
2. Check blog listing at `https://makometrics.com/blog` — new post card should appear.
3. Check sitemap at `https://makometrics.com/sitemap.xml` — new URL should be present.

If using the browser MCP, take a screenshot as final confirmation.

## Post-Deploy Report

Present to the user:

```markdown
## Publish Report: [slug]

**Date**: YYYY-MM-DD
**Status**: SUCCESS / PARTIAL / FAILED

### Deployed
- **HTML**: [live URL] — [status code]
- **Images**: [count] uploaded
- **Sitemap**: updated / skipped / failed

### Content Index
- **Added to**: content-index.json
- **Pillar**: [pillar name]
- **Internal links to**: [list of slugs]

### Verification
- **Live page loads**: YES / NO
- **Title matches**: YES / NO
- **Images load**: YES / NO

### Next Steps
- [ ] Verify in Google Search Console that the URL is indexed (check in 1-2 days)
- [ ] Submit URL for indexing in GSC if it doesn't appear
- [ ] Update any existing posts that should link TO this new post (from content-index.json internal_links_from)
```

## After Completion

Present the publish report. The content pipeline for this post is complete.

Remind the user:
- Check Google Search Console in 1-2 days to confirm indexing.
- The `content-index.json` now includes this post, so future posts will be able to link to it.
- Any posts identified in the brief as needing backlinks to this post should be updated.


---

## Orchestrator commands (same as former seo-content)

- **Start a new post about [topic]** → Stage 1.
- **Resume [slug]** → run detection above; run that stage after confirmation.
- **Pipeline status** → scan `research/`, `briefs/`, `outlines/`, `drafts/`, `../images/blog/`, `../blog/`, `qa-reports/`, `content-index.json`; table per slug.
- **Run stage N on [slug]** → jump to that stage if inputs exist.

## Stage 4 / Stage 7 wording fixes (vs archived files)

In **Stage 4** and anywhere the archived `seo-write.md` text says `seo-writing.mdc`, use **`.cursor/rules/seo-brand-voice.mdc`** instead.

## Deprecated split skills

Per-stage skills live in `.cursor/skills/archive/`. Use **`seo-write-full`** for the pipeline unless you need an archived file for reference.
