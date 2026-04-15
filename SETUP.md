# First-time setup (10–15 minutes)

Use this checklist once after cloning [**loganriebel/seo-content-stack**](https://github.com/loganriebel/seo-content-stack). The pipeline reads **`seo-stack-config.yaml`** and **`.cursor/rules/seo-brand-voice.mdc`** on every run. Placeholder values trigger the setup wizard inside `.cursor/skills/seo-write-full.md`.

## 1. Clone and open in Cursor

```bash
git clone https://github.com/loganriebel/seo-content-stack.git
cd seo-content-stack
```

Open the folder in Cursor (or your editor with AI agent support).

## 2. Configure your site

**Option A — manual:** Copy [`seo-stack-config.example.yaml`](seo-stack-config.example.yaml) to `seo-stack-config.yaml` if you prefer to track only an example in git elsewhere, then edit values. In the default template, `seo-stack-config.yaml` already ships with placeholders — fill:

- `site.name`, `site.domain`, `site.free_tool_url`
- `author.*` and optional `marketing_tags.gtm_id`
- `brand_voice` (tone, audience, topics)
- `deploy.provider`, `deploy.branch`, and `deploy.website_root` if this repo lives **inside** a larger site repo (e.g. set `website_root: ".."`)

**Option B — guided:** In Cursor, ask to run the **seo-write-full** skill. It runs a **first-run setup check** and can ask you questions, then writes answers into `seo-stack-config.yaml`.

## 3. Brand voice rule file

Edit [`.cursor/rules/seo-brand-voice.mdc`](.cursor/rules/seo-brand-voice.mdc): replace the template sections with your real audience, tone, and formatting preferences. Keep high-level alignment with `brand_voice` in the YAML.

## 4. Business context for the agent

Fill in [`AGENTS.md`](AGENTS.md) so research and brief stages use **your** ICP, CTAs, and competitors — not generic placeholders.

## 5. Paths and build tools (optional)

This template ships with **repo-relative** paths (`drafts/`, `blog/`, `deploy/blog/`, `assets/images/blog/`) and only [`seo_tools/validate_schema.py`](seo_tools/validate_schema.py). If you add `generate_html.py` / `publish.py`, update the `seo_tools` section in `seo-stack-config.yaml` to match.

If you embed this folder inside another website monorepo, adjust `paths.*`, `deploy.website_root`, and `seo_tools.*` so they point at your real directories.

## 6. Content index

[`content-index.json`](content-index.json) starts empty. New posts get registered during Stage 10 (Publish) per `.cursor/skills/seo-write-full.md`.

## 7. Quick validation

From repo root, if Python 3.10+ is available and you have generated HTML:

```bash
python seo_tools/validate_schema.py blog/your-post.html
```

See [`seo_tools/validate_schema.py`](seo_tools/validate_schema.py) for required JSON-LD fields.

## 8. Start a post

Ask your agent: *Start a new post about [topic]* and follow **seo-write-full** stage by stage, approving each stage before the next.

---

## Template maintenance

**Project-specific content** (e.g. product verticals, customer stories) should live in **your** product or website repository — not in this public template. This repo may **reset history** occasionally to stay a neutral starter kit; fork if you need a stable custom copy.
