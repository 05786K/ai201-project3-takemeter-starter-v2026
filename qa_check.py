"""
Validation checks for labels.csv, run before training.

Checks: encoding, label values match the four defined labels, no empty
fields, no suspiciously short (likely trimmed) posts, no duplicate posts,
and the 70%-per-label ceiling from the brief.

Usage: python qa_check.py
"""

import csv
import sys
from collections import Counter

PATH = "labels.csv"
VALID_LABELS = {"question", "personal_experience", "analysis", "opinion"}


def load_rows(path):
    with open(path, "rb") as f:
        raw = f.read()

    try:
        raw.decode("utf-8")
        encoding_ok = True
        decode_error = None
    except UnicodeDecodeError as e:
        encoding_ok = False
        decode_error = str(e)

    has_bom = raw.startswith(b"\xef\xbb\xbf")

    # utf-8-sig strips a leading BOM if present, decodes cleanly either way.
    text = raw.decode("utf-8-sig", errors="replace")
    reader = csv.DictReader(text.splitlines(keepends=True))
    rows = list(reader)
    return rows, encoding_ok, decode_error, has_bom


def check(rows):
    labels = Counter()
    bad_label_rows = []
    empty_text_rows = []
    short_text_rows = []
    empty_label_rows = []
    empty_note_rows = []
    seen_text = Counter()

    for i, row in enumerate(rows, start=2):  # +2: header is line 1
        text_val = (row.get("text") or "").strip()
        label_val = (row.get("label") or "").strip()
        note_val = (row.get("note") or "").strip()

        labels[label_val] += 1

        if label_val not in VALID_LABELS:
            bad_label_rows.append((i, repr(label_val)))

        if not text_val:
            empty_text_rows.append(i)
        elif len(text_val) < 40:
            short_text_rows.append((i, text_val[:60]))

        if not label_val:
            empty_label_rows.append(i)
        if not note_val:
            empty_note_rows.append(i)

        seen_text[text_val.lower().strip()[:120]] += 1

    duplicates = {k: c for k, c in seen_text.items() if c > 1 and k}

    return {
        "labels": labels,
        "bad_label_rows": bad_label_rows,
        "empty_text_rows": empty_text_rows,
        "short_text_rows": short_text_rows,
        "empty_label_rows": empty_label_rows,
        "empty_note_rows": empty_note_rows,
        "duplicates": duplicates,
    }


def report(rows, encoding_ok, decode_error, has_bom, results):
    total = len(rows)
    print(f"Total rows: {total}")
    print(f"UTF-8 valid: {encoding_ok}")
    if not encoding_ok:
        print(f"  decode error: {decode_error}")
    print(f"UTF-8 BOM present: {has_bom}")

    print("\nLabel counts:")
    for label, count in results["labels"].most_common():
        pct = 100 * count / total if total else 0
        print(f"  {label!r}: {count} ({pct:.1f}%)")

    bad = results["bad_label_rows"]
    print(f"\nRows with a label not in {sorted(VALID_LABELS)}: {len(bad)}")
    for i, val in bad[:20]:
        print(f"  line ~{i}: label={val}")

    print(f"\nRows with empty text: {len(results['empty_text_rows'])}")
    print(f"Rows with suspiciously short text (<40 chars): {len(results['short_text_rows'])}")
    for i, snippet in results["short_text_rows"][:20]:
        print(f"  line ~{i}: {snippet!r}")

    print(f"\nRows with empty label: {len(results['empty_label_rows'])}")
    print(f"Rows with empty note: {len(results['empty_note_rows'])}")

    dupes = results["duplicates"]
    print(f"\nPossible duplicate posts (same first 120 chars): {len(dupes)} groups")
    for k, c in list(dupes.items())[:10]:
        print(f"  x{c}: {k!r}")

    max_share = max(results["labels"].values()) / total if total else 0
    print(f"\nNo label above 70%? {'YES' if max_share <= 0.70 else 'NO -- CHECK'}")

    problems = bool(bad) or bool(results["empty_text_rows"]) or bool(results["empty_label_rows"]) or max_share > 0.70
    return problems


def main():
    rows, encoding_ok, decode_error, has_bom = load_rows(PATH)
    results = check(rows)
    problems = report(rows, encoding_ok, decode_error, has_bom, results)
    if not encoding_ok or problems:
        sys.exit(1)


if __name__ == "__main__":
    main()
