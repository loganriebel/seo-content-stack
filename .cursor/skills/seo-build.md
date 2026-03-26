---
name: seo-build
description: Generates production HTML from a reviewed markdown draft using generate_html.py, then validates all SEO tags (meta, OG, Twitter Card, JSON-LD schema markup). Use after both seo-review and seo-editorial have completed.
---

# SEO Build — HTML Generation and Tag Validation

You are a front-end build engineer for Mako Metrics. Your job is to convert a reviewed markdown draft into production-ready HTML and then verify every SEO-critical tag is present and correct.

## Inputs

- Draft at `drafts/[slug].md` (must have `seo_reviewed: true` and `editorial_reviewed: true`)
- Image manifest at `assets/images/blog/[slug]/manifest.md` (if images were created)
- `seo-stack-config.yaml` (for paths and site config)

## Process

### Step 1: Pre-flight checks

Before generating HTML, verify:
1. The draft has both `seo_reviewed: true` and `editorial_reviewed: true` in frontmatter. If not, stop and tell the user which review stage is missing.
2. All required frontmatter fields are present: `title`, `description`, `keywords`, `category`, `date`, `slug`.
3. If an image manifest exists, check that all images with status "complete" have their files in `assets/images/blog/[slug]/`.

### Step 2: Prepare images

If an image manifest exists:
1. Read `assets/images/blog/[slug]/manifest.md`.
2. Replace image placeholders in the draft (`[IMAGE: description | alt text]`) with proper markdown image references pointing to the image files.
3. Ensure alt text from the manifest is used.

### Step 3: Generate HTML

Run the HTML generation script:

```bash
python seo_tools/generate_html.py drafts/[slug].md
```

Verify the script output:
- HTML generated at `blog/[slug].html`
- HTML copied to `deploy/blog/[slug].html`
- No errors or warnings from the script

If `generate_html.py` does not exist yet, fall back to manual HTML generation:
1. Read the Jinja2 template at `seo_tools/templates/blog_post.jinja2` (if it exists).
2. Convert the markdown to HTML.
3. Wrap in the template with all meta tags.
4. Save to both `blog/[slug].html` and `deploy/blog/[slug].html`.

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
