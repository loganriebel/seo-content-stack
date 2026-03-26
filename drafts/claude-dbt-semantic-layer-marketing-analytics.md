---
title: "Claude + dbt Semantic Layer for marketing analytics"
description: "How I’d unify paid media + Salesforce pipeline in dbt, define governed metrics, and let Claude answer marketing questions through the dbt Semantic Layer."
keywords: "dbt semantic layer, metricflow, marketing analytics, claude mcp, dbt mcp, campaign performance"
category: "strategy"
date: "2026-03-25"
---

# Claude + dbt Semantic Layer for marketing analytics

## Hook

'Simple' ad-hoc analsysis are a pain for both stakeholders and analytics practicioners. For stakeholders, they want answers in minutes, not hours or days. For analytics practioners, we want to execute on our larger roadmap and not spend time on ad-hoc work that always seems to pop up.    


## The problem (why this keeps eating your week)

The reason "simple" ad-hoc analysis turns into a time sink isn’t that anyone’s slow. It’s that the system isn’t set up to answer questions quickly.

From the stakeholder side, the question is usually reasonable:

- "What was CPL last week?"
- "Which campaigns drove pipeline?"
- "Did spend go up and results go down?"

From the analytics side, that one question kicks off a chain reaction:

- Paid media data is split across CM360, LinkedIn, Meta, and SEM.
- Pipeline is in Salesforce, shaped like events, not daily spend.
- Campaign identifiers don’t line up cleanly across systems.
- "Conversion" and "lead" mean different things depending on who’s asking.

So the work becomes less about analysis and more about reconciliation. You pull exports, stitch together joins, explain caveats, and then you still end up debating definitions. Meanwhile, the roadmap work sits there untouched.

What I want instead is a setup where the ad-hoc questions get faster without making the numbers less trustworthy:

- Clean and unify the raw data once.
- Define metrics once, in a governed place.
- Let people ask questions in plain English and still get answers that match how we report.
## The stack (in one picture)

Here’s the mental model I’m aiming for:

- dbt does the boring-but-critical work: clean sources, unify grains, build a mart
- the dbt Semantic Layer (MetricFlow) defines metrics like CTR, CPL, and ROAS once
- Claude queries those governed metrics through the dbt MCP server

So when someone asks "CPL by platform last quarter," we’re not spinning up a Tableau dashboard that's only used once. We’re querying a metric definition that already knows what CPL means.

'''mermaid
flowchart LR
  endUser["End user (marketing / revops)"] -->|Question in plain English| claude["Claude"]
  claude -->|Tool call| mcp["dbt MCP server"]
  mcp -->|Metric query| semanticLayer["dbt Semantic Layer (MetricFlow)"]
  semanticLayer -->|Governed SQL| warehouse["Data warehouse"]
  warehouse -->|Results| semanticLayer
  semanticLayer -->|Answer + context| claude
  claude -->|Result| endUser
'''

## Step 1: Build a mart that marketing can actually use

I’m intentionally starting with the data model. If the mart is messy, everything above is built on sand.

Here’s the lineage I want (left to right):

'''mermaid
graph LR
  subgraph rawSources[Raw_sources]
    cm360Raw[CM360_raw]
    linkedinRaw[LinkedIn_ads_raw]
    facebookRaw[Facebook_ads_raw]
    semRaw[SEM_raw]
    sfdcRaw[SFDC_raw]
  end

  subgraph stagingLayer[Staging_layer]
    stgCm360[stg_cm360__campaign_daily]
    stgLinkedIn[stg_linkedin_ads__campaign_daily]
    stgFacebook[stg_facebook_ads__campaign_daily]
    stgSem[stg_sem__campaign_daily]
    stgSfdc[stg_sfdc__leads_and_opps]
  end

  subgraph intermediateLayer[Intermediate_layer]
    intUnion[int_media_platforms_unioned]
    intAttrib[int_sfdc_campaign_attribution]
  end

  subgraph martsLayer[Marts_layer]
    martDaily[mart_campaign_performance_daily]
  end

  subgraph semantic[Semantic_layer]
    metricflow[MetricFlow_models_and_metrics]
  end

  subgraph ai[Claude_via_MCP]
    claudeQueries[Natural_language_queries]
  end

  cm360Raw --> stgCm360
  linkedinRaw --> stgLinkedIn
  facebookRaw --> stgFacebook
  semRaw --> stgSem
  sfdcRaw --> stgSfdc

  stgCm360 --> intUnion
  stgLinkedIn --> intUnion
  stgFacebook --> intUnion
  stgSem --> intUnion

  stgSfdc --> intAttrib

  intUnion --> martDaily
  intAttrib --> martDaily

  martDaily --> metricflow
  metricflow --> claudeQueries
'''

### The dbt layers I use (staging -> intermediate -> marts)

This is the same pattern I keep coming back to in dbt projects because it keeps you honest:

- staging: rename, type cast, light cleanup
- intermediate: reshape the data into something you can model
- marts: the tables you actually want people (and tools) to query

### Staging models (make the platforms look the same)

Each paid media platform gets its own staging model. The job is boring: make columns consistent so you can 'UNION ALL' later without a thousand 'coalesce()' calls.

I normalize to a shared schema like:

- 'date'
- 'campaign_id' (platform-specific ID)
- 'campaign_name' (Makes the IDs human readable)
- 'platform' ('CM360', 'LinkedIn Ads', 'Meta Ads', 'Paid Search')
- Media Metrics: 'Impressions', 'Clicks', 'Cost'

### Intermediate models (union media, keep attribution separate)

This is where I make one controversial choice on purpose: I keep the media union and the SFDC attribution logic separate for as long as possible.

Media data is naturally daily. Salesforce objects are event-shaped. If you mash them together too early, you end up baking assumptions into the model that you’ll fight later.

So I build:

- 'int_media_platforms_unioned': campaign x platform x date with only media metrics
- 'int_sfdc_campaign_attribution': a clean, explicit mapping of SFDC leads/opps back to campaigns (more on this below)

### Mart model (campaign x day)

The mart is the thing I want to stand behind in a meeting: one row per 'campaign_id x date' (plus 'platform' if you want platform-level splits). This is the table that is your source of truth.

'''sql
-- Pseudocode / illustrative only
-- Target grain: campaign_id x date
select
  date,
  campaign_id,
  campaign_name,
  platform,
  impressions,
  clicks,
  spend,
  platform_conversions,
  leads,
  opportunities,
  pipeline_value
from mart_campaign_performance_daily
'''

### The part everyone skips: SFDC-to-media attribution

This is the hardest part of the whole setup, and it’s the part most "unified marketing mart" posts hand-wave.

If you don’t have a reliable join key between paid media and SFDC, you’re not doing attribution, you’re doing a vibe check.

In real life, you usually need an explicit mapping layer, even if it starts simple:

- a 'dim_campaign_mapping' table keyed by UTM campaign / ad platform campaign IDs
- rules for what happens when names drift or campaigns get cloned
- a decision on attribution timing (lead created date vs opp created date vs close won date)

The point isn’t that there’s one right answer. The point is to make your assumptions explicit so you can improve them without rewriting everything.
## Step 2: Put your metrics in the Semantic Layer (so "CPL" means one thing)

This is the piece I’m most excited about, because it turns a dbt project from "a bunch of tables" into "a system with rules."

I like to think about it this way:

- a mart gives you consistent data
- a semantic layer gives you consistent meaning so Claude can make sense of your data and not go wild with hallucinainots or assumptions

If you’ve ever had two dashboards disagree on CPL, this is why. Someone wrote \(spend / leads\) in one place and \(spend / mqls\) in another. Or they filtered out branded in one report and forgot in the other. The Semantic Layer is where you stop letting every query define its own version of reality.

The Semantic Layer doesn’t just make queries easier. It makes wrong queries harder.

One real-world note: full Semantic Layer support is a dbt Cloud feature (Team/Enterprise). If you’re on dbt Core only, you can still structure your project the same way, but you may not get the full metric-serving workflow.

'''yaml
# Real YAML example (adapt to your project)
semantic_models:
  - name: campaign_performance
    model: ref('mart_campaign_performance_daily')
    description: >
      Unified daily campaign performance combining paid media metrics
      from CM360, LinkedIn Ads, Facebook Ads, and SEM with SFDC pipeline data.
    defaults:
      agg_time_dimension: date

    entities:
      - name: campaign
        type: primary
        expr: campaign_name

    dimensions:
      - name: date
        type: time
        type_params:
          time_granularity: day
      - name: platform
        type: categorical
      - name: campaign_name
        type: categorical

    measures:
      - name: total_impressions
        agg: sum
        expr: impressions
      - name: total_clicks
        agg: sum
        expr: clicks
      - name: total_spend
        agg: sum
        expr: spend
      - name: total_leads
        agg: sum
        expr: leads
      - name: total_opportunities
        agg: sum
        expr: opportunities
      - name: total_pipeline_value
        agg: sum
        expr: opp_amount

metrics:
  - name: ctr
    label: "Click-Through Rate"
    type: ratio
    type_params:
      numerator: total_clicks
      denominator: total_impressions
    description: "Ratio of clicks to impressions across all platforms"

  - name: cpl
    label: "Cost Per Lead"
    type: ratio
    type_params:
      numerator: total_spend
      denominator: total_leads
    description: "Media spend divided by SFDC leads attributed to campaign"

  - name: cpopp
    label: "Cost Per Opportunity"
    type: ratio
    type_params:
      numerator: total_spend
      denominator: total_opportunities
    description: "Media spend divided by SFDC opportunities attributed to campaign"

  - name: roas
    label: "Return on Ad Spend"
    type: ratio
    type_params:
      numerator: total_pipeline_value
      denominator: total_spend
    description: "SFDC pipeline value divided by media spend"

  - name: opportunity_rate
    label: "Opportunity Rate"
    type: ratio
    type_params:
      numerator: total_opportunities
      denominator: total_leads
    description: "Ratio of leads that became opportunities"

    - name: lead_conversion_Rate
    label: "Lead Conversion Rate"
    type: ratio
    type_params:
      numerator: total_leads
      denominator: total_clicks
    description: "Ratio of clicks that became clicks"

'''

Two things I watch for immediately with ratio metrics:

- denominators can be zero (a day with zero impressions, or a campaign with zero leads), so you want a plan for nulls/infinity
- people will ask for trends; make sure you’re aggregating at the right grain before you divide

## Step 3: Let Claude query governed metrics through MCP

This is the why for me. Most teams don’t need another dashboard. They need a faster way to answer the dozens of small questions that show up between dashboards and ad platform UIs.

MCP (Model Context Protocol) is the bridge. It lets Claude call tools instead of making things up. Claude asks the dbt MCP server, which returns answers based on your Semantic Layer metrics—not guesswork.

'''json
{
  "mcpServers": {
    "dbt": {
      "command": "uvx",
      "args": ["--env-file", "/path/to/.env", "dbt-mcp"]
    }
  }
}
'''

### Example questions I want marketing to be able to ask

These are the kinds of questions I’m aiming to support without a spreadsheet detour:

- "What was CPL by platform last quarter?"
- "Which campaigns had the highest ROAS in the last 30 days (and did spend change)?"
- "Show total spend trend by month for LinkedIn."
- "Which campaigns had rising spend but flat pipeline?"

If the metrics live in MetricFlow, Claude can ask for the metric and dimensions you’ve defined. That’s the guardrail. You get flexibility, but you don’t get five definitions of the same KPI.
## Caveats (the honest version)

This isn’t magic. A few things matter if you don’t want this to turn into a demo that breaks in week two:

- The dbt Semantic Layer is a dbt Cloud feature (not the free tier). Plan for that upfront.
- Cold starts can be slow. If the first question takes 10 seconds, people will notice.
- This doesn’t replace dashboards. It replaces the back-and-forth when someone asks a one-off question.
- Attribution is still the hard part. If your campaign taxonomy is a mess, the model will faithfully return messy answers.
- Ratio metrics need guardrails. CPL on a day with zero leads shouldn’t throw errors or produce nonsense.

## Closing

I’m using this as a north star for how marketing analytics should work. Empower non-technical stakeholders to get value out of there data that isn't limited to either platform UIs or dashboards that analytics teams build. At the same time, this frees up analtyics teams to focus execution on their roadmaps to drive the future of the marketing org. By having one set of models, one set of metric definitions, and a human-friendly way to query them we can enable true self-service to our stakeholders.

If you’ve tried Claude (or any LLM) against your analytics stack, what worked? What didn’t?
