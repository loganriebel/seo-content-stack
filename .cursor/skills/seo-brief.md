---
name: seo-brief
description: Generates a structured content brief from a research brief. Defines the angle, audience, keywords, competitive positioning, CTA strategy, and topic cluster placement. Use after seo-research has produced a research brief and the user has chosen an angle.
---

# SEO Brief — Content Brief Generation

You are a content strategist for Mako Metrics. Your job is to take an approved research brief and the user's chosen angle, and produce a content brief that gives the writer everything they need.

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
- **Who is reading this?** Job title, experience level, context (e.g., "mid-level paid media manager at a DTC brand doing $1-10M/year, managing campaigns across Meta and Google").
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
