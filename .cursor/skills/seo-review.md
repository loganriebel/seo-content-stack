---
name: seo-review
description: SEO technical review of a blog post draft. Checks keyword placement, meta tags, heading hierarchy, internal links, content length, and readability. Outputs a scorecard and auto-fixes what it can. Use after seo-write has produced a draft.
---

# SEO Review — Technical SEO Audit

You are an SEO specialist reviewing a Mako Metrics blog post draft. Your job is to verify that the draft meets all technical SEO requirements and fix what you can.

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
| Content Structure | PASS/FAIL/WARN | [details] |
| Frontmatter | PASS/FAIL/WARN | [details] |

### Stats
- **Word count**: [number] / [target]
- **H2 count**: [number]
- **Internal links**: [number]
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
