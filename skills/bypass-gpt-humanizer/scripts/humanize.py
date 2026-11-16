#!/usr/bin/env python3
"""Humanize text with the Bypass GPT API. Standard library only.

    python3 humanize.py --mode mini < draft.txt > humanized.txt
    BYPASSGPT_API_KEY=bgk_... python3 humanize.py --file draft.txt --mode light

Long input is split at paragraph boundaries and the parts are rejoined in order.
"""

import argparse
import json
import os
import re
import sys
import urllib.error
import urllib.request

DEFAULT_URL = "https://bypassgpt.si/api/v1/humanize"
FREE_PART_WORDS = 350
KEY_PART_WORDS = 1500


def split_parts(text, limit):
    """Group whole paragraphs into parts of at most `limit` words; an oversized paragraph is split by sentences."""
    paragraphs = [p for p in re.split(r"\n\s*\n", text.strip()) if p.strip()]
    parts, current, count = [], [], 0
    for paragraph in paragraphs:
        pieces = [paragraph]
        if len(paragraph.split()) > limit:
            pieces, buffer, size = [], [], 0
            for sentence in re.split(r"(?<=[.!?])\s+", paragraph):
                n = len(sentence.split())
                if buffer and size + n > limit:
                    pieces.append(" ".join(buffer)); buffer, size = [], 0
                buffer.append(sentence); size += n
            if buffer:
                pieces.append(" ".join(buffer))
        for piece in pieces:
            n = len(piece.split())
            if current and count + n > limit:
                parts.append("\n\n".join(current)); current, count = [], 0
            current.append(piece); count += n
    if current:
        parts.append("\n\n".join(current))
    return parts


def call_api(url, text, mode, key):
    headers = {"Content-Type": "application/json", "User-Agent": "bypassgpt-skill/1.0"}
    if key:
        headers["Authorization"] = "Bearer " + key
    request = urllib.request.Request(url, data=json.dumps({"text": text, "mode": mode}).encode("utf-8"), headers=headers, method="POST")
    try:
        with urllib.request.urlopen(request, timeout=120) as response:
            return json.loads(response.read().decode("utf-8"))
    except urllib.error.HTTPError as error:
        try:
            detail = json.loads(error.read().decode("utf-8")).get("error", {})
        except Exception:
            detail = {}
        raise SystemExit("Error %s (%s): %s" % (error.code, detail.get("code", "unknown"), detail.get("message", "The request failed.")))
    except urllib.error.URLError as error:
        raise SystemExit("Could not reach the service: %s" % error.reason)


def main():
    parser = argparse.ArgumentParser(description="Humanize text with the Bypass GPT API.")
    parser.add_argument("--file", help="Read text from this file instead of standard input.")
    parser.add_argument("--mode", choices=["mini", "light", "pro"], default="mini", help="Rewrite depth (light and pro need an API key).")
    parser.add_argument("--url", default=os.environ.get("BYPASSGPT_API_URL", DEFAULT_URL), help="API endpoint.")
    parser.add_argument("--words", type=int, help="Maximum words per request (default 350 without a key, 1500 with one).")
    args = parser.parse_args()

    key = os.environ.get("BYPASSGPT_API_KEY", "").strip()
    text = open(args.file, encoding="utf-8").read() if args.file else sys.stdin.read()
    if not text.strip():
        raise SystemExit("No text to humanize.")
    limit = args.words or (KEY_PART_WORDS if key else FREE_PART_WORDS)
    parts = split_parts(text, limit)
    outputs = []
    for index, part in enumerate(parts, 1):
        sys.stderr.write("Humanizing part %d of %d...\n" % (index, len(parts)))
        outputs.append(call_api(args.url, part, args.mode, key)["output"])
    sys.stdout.write("\n\n".join(outputs) + "\n")


if __name__ == "__main__":
    main()
