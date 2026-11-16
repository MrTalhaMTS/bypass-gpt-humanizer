---
description: Rewrite text so it reads more naturally with Bypass GPT, keeping meaning, names and numbers. Pass the text itself or a file path.
argument-hint: [text or file path]
---

Rewrite the text below with the Bypass GPT humanizer. If a file path is given, read that file and rewrite its contents.

Use the `humanize_text` tool from the Bypass GPT connector when it is available. Otherwise run the bundled `humanize.py` script from the `bypass-gpt-humanizer` skill. Return the rewritten text, then list any name, number, date or quotation that changed, if any did.

Text or file: $ARGUMENTS
