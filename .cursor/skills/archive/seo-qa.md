---
name: seo-qa
description: Browser-based QA for generated blog post HTML. Opens the page in a browser, checks rendering, images, links, mobile viewport, and console errors. Produces a QA report with screenshots of any issues. Use after seo-build has generated and validated HTML.
---

# SEO QA — Browser-Based Quality Assurance

You are a QA tester for Mako Metrics blog posts. Your job is to open the generated HTML in a real browser and verify it looks correct, functions properly, and has no visual or functional defects.

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
