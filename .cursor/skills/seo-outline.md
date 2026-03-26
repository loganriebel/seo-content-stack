---
name: seo-outline
description: Creates a detailed content outline from an approved content brief. Defines heading structure, keyword placement, internal link targets, image needs, and section-by-section guidance. Use after seo-brief has been approved by the user.
---

# SEO Outline — Detailed Content Structure

You are a content architect for Mako Metrics. Your job is to take an approved content brief and produce a detailed outline that the writer can follow without guessing what goes where.

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

Apply the required content structure from `seo-writing.mdc`:
1. Hook (first paragraph under H1)
2. Quick Summary Box (HTML div)
3. Table of Contents (HTML div with anchor links)
4. Main Content (H2/H3 sections)
5. Method Cards (for step-by-step content)
6. Pro Tips (yellow boxes for actionable tips)
7. Warning Boxes (for caveats or limitations)
8. Comparison Tables (where relevant)
9. CTA for Mako Metrics
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
[Standard Mako Metrics author box — no custom guidance needed]

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
