# Bypass GPT Humanizer

Rewrite AI-assisted or stiff, repetitive text so it reads like natural, individually written prose. The rewrite keeps
the meaning, facts, names, numbers, quotations and paragraph order, and keeps the source language. The plugin works
inside Claude through a connector, a skill and a `/humanize` command.

It does not guarantee any AI-detector result. Detectors differ and change. Review every rewrite for accuracy, tone and
citations, and follow the rules about disclosing AI assistance that apply to your school, employer or platform.

## What is included

| Part | What it does |
| --- | --- |
| Connector (`.mcp.json`) | Connects Claude to the remote Bypass GPT server at `https://bypassgpt.si/mcp`. It adds two tools: `humanize_text` and `get_humanizer_usage`. |
| Skill (`skills/bypass-gpt-humanizer`) | Teaches Claude when to humanize text, splits long drafts at paragraph boundaries, and checks that names and numbers are unchanged. |
| Command (`/bypass-gpt-humanizer:humanize`) | Humanize pasted text or a file. |

## Install

- From the Claude directory: open the plugin's listing and install it.
- From a local copy: `claude --plugin-dir ./bypass-gpt-humanizer`, then run `/reload-plugins`.

The plugin asks for one optional setting, a Bypass GPT API key. Claude stores it in secure storage. Leave it empty to
use the free tier.

## Free tier and account key

| | Free tier (no key) | Account key |
| --- | --- | --- |
| Sign-up | None | Free account at https://bypassgpt.si |
| Length | Up to 400 words per call | Up to 2,000 words per connector call |
| Modes | Mini | Mini, Light and Pro, as your plan allows |
| Cost | Shared daily allowance for all users; when it is used up, try again the next day | Spends your account credits |

Create a key in your account settings under API keys. A key is shown once; revoke it there at any time.

## Examples

1. **Humanize a paragraph.** `/bypass-gpt-humanizer:humanize Businesses must utilize digital marketing strategies in
   order to achieve growth.` Claude returns a more natural rewrite with the same meaning.
2. **Humanize a file.** `/bypass-gpt-humanizer:humanize draft.md` Claude reads the file, rewrites it in parts if it is
   long, and lists anything that changed in a name, number or date.
3. **Check what you can use.** Ask "How many words can I humanize right now?" Claude calls `get_humanizer_usage` and
   reports the free allowance left today, or your plan and credits when a key is set.

## What this plugin runs, sends and stores

- **Sends:** the text you ask to rewrite, over HTTPS, to `https://bypassgpt.si` through the connector. If you set the
  optional API key, the connector sends it as an `Authorization: Bearer` header to the same host. Nothing else is sent.
  The plugin does not read your conversation, files you did not name, or Claude's memory.
- **Runs:** only the connector. The plugin contains no scripts or executable code, only Markdown instructions, a
  manifest and an icon. It writes no files and installs nothing.
- **Processing:** Bypass GPT sends the text to the AI model provider it uses to produce the rewrite.
- **Stored:** free-tier text is not saved to a history and is not put in analytics. Requests made with an account key
  follow that account's history setting, like the Bypass GPT website. See the privacy policy for details and retention:
  https://bypassgpt.si/privacy

## Limits and errors

`INVALID_API_KEY` means the key is wrong or revoked. `INSUFFICIENT_CREDITS` or `MODE_LOCKED` means the account is out of
credits or its plan does not include that mode. `FREE_LIMIT_PER_CALL` and `FREE_POOL_EXHAUSTED` mean the free tier limit
was reached. `RATE_LIMITED` means wait a minute and retry.

## Support and policies

- Documentation: https://bypassgpt.si/connect
- Support: https://bypassgpt.si/support
- Privacy policy: https://bypassgpt.si/privacy
- Terms: https://bypassgpt.si/terms
- AI and detector disclaimer: https://bypassgpt.si/ai-disclaimer

## License

MIT. See `LICENSE`.
