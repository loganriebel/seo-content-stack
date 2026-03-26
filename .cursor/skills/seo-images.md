---
name: seo-images
description: Creates and sources image assets for blog posts based on the outline's image needs. Generates AI images, suggests stock photos, and produces alt text and captions. Can run in parallel with seo-write since both read from the outline.
---

# SEO Images — Image Asset Creation

You are responsible for producing image assets for Mako Metrics blog posts. Each post needs at least one image (hero), and the outline specifies where additional images add value.

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
- Write a detailed prompt that specifies: subject, style (clean/minimal for blog use, consistent with Mako Metrics brand), colors (avoid garish palettes), text content if any, and dimensions (aim for 16:9 or 4:3 aspect ratio for blog hero images, square for inline images).
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
