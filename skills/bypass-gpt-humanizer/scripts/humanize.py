#!/usr/bin/env python3
"""Humanize text with the free tier of the Bypass GPT API. Standard library only.

    python3 humanize.py < draft.txt > humanized.txt
    python3 humanize.py --file draft.txt

Long input is split at paragraph boundaries and the parts are rejoined in order.
The script sends text only to https://bypassgpt.si and uses no account key.
"""

import argparse
import json
import re
import sys
import urllib.error
import urllib.request

API_URL = "https://bypassgpt.si/api/v1/humanize"
PART_WORDS = 350


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


def call_api(text):
    headers = {"Content-Type": "application/json", "User-Agent": "bypassgpt-skill/1.1"}
    request = urllib.request.Request(API_URL, data=json.dumps({"text": text, "mode": "mini"}).encode("utf-8"), headers=headers, method="POST")
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
    parser = argparse.ArgumentParser(description="Humanize text with the free tier of Bypass GPT.")
    parser.add_argument("--file", help="Read text from this file instead of standard input.")
    args = parser.parse_args()

    text = open(args.file, encoding="utf-8").read() if args.file else sys.stdin.read()
    if not text.strip():
        raise SystemExit("No text to humanize.")
    parts = split_parts(text, PART_WORDS)
    outputs = []
    for index, part in enumerate(parts, 1):
        sys.stderr.write("Humanizing part %d of %d...\n" % (index, len(parts)))
        outputs.append(call_api(part)["output"])
    sys.stdout.write("\n\n".join(outputs) + "\n")


if __name__ == "__main__":
    main()
