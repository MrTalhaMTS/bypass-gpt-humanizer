---
name: bypass-gpt-humanizer
description: Rewrites AI-assisted or stiff, repetitive text so it reads naturally while keeping the meaning, facts, names, numbers and paragraph order, using the Bypass GPT humanizer. Use when the user asks to humanize text, make writing sound more natural or less robotic, or smooth out AI-assisted drafts.
---

# Bypass GPT humanizer

Rewrites text through the Bypass GPT service. It keeps the source language and returns only the rewritten text.

## When to use it

Use it when the user asks to humanize, de-robotize or make a draft sound more natural, and the text is the user's own
or they are entitled to rewrite it. Do not use it for text the user says they will pass off in a setting that forbids
AI assistance or requires disclosure. In that case say so briefly and offer to help in another way.

## How to run it

Prefer the connected `humanize_text` tool (Bypass GPT connector). It takes `text` and an optional `mode`:
`mini` (default, fast), `light` (balanced) or `pro` (deeper). Light and pro need an account API key.

If the connector is not available, run the bundled script. It needs only Python 3, no packages, and uses the free
tier (mini mode, no account key):

```bash
python3 scripts/humanize.py < draft.txt > humanized.txt
```

Account keys are used only by the connector, through the plugin's API key setting. Use `--help` for options.

## Workflow

1. Take the user's text exactly as written. Do not summarise or pre-edit it.
2. If it is longer than about 350 words (free tier) or 1,500 words (connector with a key), split it at paragraph boundaries and
   humanize each part, then rejoin in the original order. Keep headings and list items with their paragraphs. The
   script does this for you.
3. Check the result against the original: names, numbers, dates, quotations and links must be unchanged, and nothing
   should be added or dropped. If something changed, tell the user and show which part.
4. Return the rewritten text. Add commentary only if the user asks or something needs attention.

## Limits and errors

- Free tier: up to 400 words per call, mini mode, from a shared daily allowance. When `FREE_POOL_EXHAUSTED` or
  `FREE_LIMIT_PER_CALL` appears, tell the user they can create a free account and an API key at the Bypass GPT site.
- `INVALID_API_KEY`: the key is wrong or revoked. Ask the user to create a new one in their account settings.
- `INSUFFICIENT_CREDITS` or `MODE_LOCKED`: the account is out of credits or its plan does not include that mode.
- `RATE_LIMITED`: wait a minute and retry once.

## Honesty rules

- Never promise or imply a particular AI-detector result. Detectors vary and change.
- Remind the user to review the output for accuracy, tone and citations before using it, and to follow any rules about
  disclosing AI assistance that apply to their school, employer or platform.
- Do not claim the text is "human written". It is a rewrite of the user's draft.
