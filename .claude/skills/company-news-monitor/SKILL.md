---
name: company-news-monitor
description: >
  Monitor recent news for companies, summarizing headlines
  with sources and flagging insolvency risk signals. Use this skill whenever the
  user asks to check news for a bank, financial institution, robo-advisor,
  fintech company, or corporation - including phrases like "news check", "news scan",
  "insolvency check", "credit risk news", "what's happening with [company name]",
  or "monitor [company name]". Also trigger when the user provides a list of
  commercial organizations and wants a news roundup, risk scan, or media summary
  for any of them. The user will supply one or more institution names as
  arguments.
---

# Company News Monitor

Produce a structured news briefing for one or more commpanies,
with special attention to insolvency or credit-risk signals.

## Input

The user provides one or more company names. Examples:

- "Check news for JPMorgan Chase"
- "News scan: Google, Amazon, Meta, Apple"
- "Any insolvency signals for Oracle lately?"

## Procedure

For **each** company supplied by the user, carry out the following steps:

### 1. Search for recent news

Run **at least two** web searches per company to get good coverage. Use
queries like:

- `"<company name>" news <current year>` (include the year so results are
  fresh)
- `"<company name>" financial risk OR insolvency OR downgrade <current year>`

Because the user typically cares about the **last 7 days**, add a time-scoped
qualifier when helpful (e.g. `news today`, `news this week`). Always verify that
the articles you report actually fall within the requested window - discard
anything older.

### 2. Fetch and verify sources

For every promising search hit, use `web_fetch` to open the article and confirm:

- The publication date (must be within the requested time window - default is
  the last 7 days).
- The headline and a short factual summary you can write in your own words.
- The source name and URL.

Do **not** rely solely on search-result snippets; fetch the page to get accurate
dates and details.

### 3. Compile the briefing

Present results grouped by company under a clear heading. For each news
item, include:

- **Headline** - the article's actual headline (or a close paraphrase if
  needed for brevity).
- **Summary** - 1–2 sentences in your own words.
- **Source, link & date** - e.g. *Reuters - https://… - 2026-03-25*

### 4. Flag insolvency / credit-risk signals

After the bullet list for each company, add a short **Risk assessment**
line:

- If any article suggests the company may be heading toward financial
  distress (e.g. credit-rating downgrade, liquidity concerns, regulatory
  intervention, major lawsuit threatening solvency, bank run, large unexpected
  losses), flag it clearly with a ⚠️ marker and a brief explanation.
- If nothing concerning was found, state: "No insolvency-related signals
  identified in this period."

## Output format

```
## <Company Name>

- **<Headline>**
  <Short summary in your own words.>
  *<Source> - <URL> - <YYYY-MM-DD>*

- **<Headline>**
  <Short summary.>
  *<Source> - <URL> - <YYYY-MM-DD>*

**Risk assessment:** <assessment or "No insolvency-related signals identified in this period.">

---
```

Repeat the block above for every company the user listed.

## Important reminders

- If no news is found for an company within the time window, say so
  explicitly - do not fabricate entries.
- Prioritize high-quality sources (major financial news outlets, the
  company's own press releases, regulatory body announcements) over blogs
  or forums.
- The default look-back window is 7 days. If the user specifies a different
  window, honour it.
- When the user supplies multiple companies in a single request, process all
  of them in one response.
