---
name: seo-publish
description: Deploys a QA-passed blog post to DigitalOcean, updates the sitemap and blog listing via publish.py, updates content-index.json with the new post, and verifies the live page. Final stage of the SEO content pipeline.
---

# SEO Publish — Deploy and Verify

You are the release engineer for Mako Metrics blog content. Your job is to deploy a QA-passed blog post to the live site, update all indexes, and verify it's live and correct.

## Inputs

- QA-passed HTML at `deploy/blog/[slug].html`
- QA report at `qa-reports/[slug].md` (must have status "pass" or "pass-with-notes")
- Content brief at `briefs/[slug].md` (for metadata to update content index)
- `content-index.json` (to update with new post)
- `seo-stack-config.yaml` (for deploy configuration)

## Pre-Deploy Checks

Before deploying, verify:

1. **QA report exists and status is not "fail."** If QA failed, stop and tell the user.
2. **Deploy file exists** at `deploy/blog/[slug].html`.
3. **User has given explicit approval** to publish. Ask if not already confirmed.

## Deploy Process

### Step 1: Confirm with user

This is the final gate. Present a summary:
- Post title and slug
- Target URL: `[domain]/blog/[slug].html`
- QA status
- Any "pass-with-notes" items from QA

Ask for explicit "go ahead" before proceeding.

### Step 2: Deploy to DigitalOcean

Read the deploy method from `seo-stack-config.yaml`.

**If method is "spaces" (DigitalOcean Spaces):**

Use the DigitalOcean MCP if available, or fall back to CLI:
```bash
# Using s3cmd or doctl (user must have credentials configured)
s3cmd put deploy/blog/[slug].html s3://[bucket]/blog/[slug].html --acl-public --mime-type="text/html"
```

Also upload any images from `assets/images/blog/[slug]/`:
```bash
s3cmd sync assets/images/blog/[slug]/ s3://[bucket]/images/blog/[slug]/ --acl-public
```

**If method is "rsync" (to a Droplet):**
```bash
rsync -avz deploy/blog/[slug].html [user]@[droplet-ip]:/var/www/html/blog/
rsync -avz assets/images/blog/[slug]/ [user]@[droplet-ip]:/var/www/html/images/blog/[slug]/
```

**If method is "app-platform":**
- Commit the files and push to the deploy branch
- App Platform auto-deploys from the branch

If the deploy method isn't configured or credentials aren't set up, stop and tell the user what needs to be configured in `seo-stack-config.yaml`.

### Step 3: Run publish.py

Execute the publish script to update sitemap and blog listing:

```bash
python seo_tools/publish.py [slug]
```

If `publish.py` doesn't exist yet, note it for the user and skip this step. The user will need to manually update the sitemap and blog listing.

### Step 4: Update content-index.json

Read the current `content-index.json` and add the new post:

```json
{
  "slug": "[slug]",
  "title": "[title from frontmatter]",
  "primary_keyword": "[from brief]",
  "secondary_keywords": ["[from brief]"],
  "pillar": "[from brief's topic cluster assignment]",
  "status": "published",
  "url": "/blog/[slug].html",
  "published_date": "[today's date]",
  "internal_links_to": ["[slugs this post links to]"],
  "internal_links_from": []
}
```

Also update the pillar's `spoke_slugs` array if this post belongs to an existing pillar.

If this post is a new pillar, add it to the `pillars` array.

Save the updated `content-index.json`.

### Step 5: Verify live page

After deploy, verify the page is live:

1. **HTTP check**: fetch the live URL and confirm 200 status.
2. **Content check**: verify the page title matches the expected title.
3. **Image check**: verify at least the hero image loads from the live URL.

If using the browser MCP, navigate to the live URL and take a screenshot as final confirmation.

### Step 6: Deploy the updated sitemap

If `publish.py` generated an updated sitemap, deploy it:
```bash
# Same deploy method as the blog post
s3cmd put deploy/sitemap.xml s3://[bucket]/sitemap.xml --acl-public --mime-type="application/xml"
```

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
