"""P009 fixture JSONL group summary (P903)."""

import argparse
import csv
import io
import json
import sys

CSV_FIELDS = ("group", "records", "lines", "characters")

from fixture_format import summarize_lines


def _record_error(value):
    """Return the first contract violation code for a parsed value, or None."""
    if not isinstance(value, dict):
        return "not_object"
    if not isinstance(value.get("group"), str):
        return "invalid_group"
    lines = value.get("lines")
    if not isinstance(lines, list) or not all(isinstance(item, str) for item in lines):
        return "invalid_lines"
    return None


def summarize_jsonl(text):
    """Group JSONL records by name and summarize their normalized lines.

    Returns {"groups": [...sorted by group name...], "errors": [...by line...]}
    with 1-based physical line numbers. Blank lines are skipped; processing
    continues after an invalid line and only its first violation is recorded.
    """
    totals = {}
    errors = []
    for number, raw in enumerate(text.splitlines(), start=1):
        if not raw.strip():
            continue
        try:
            value = json.loads(raw)
        except ValueError:
            errors.append({"line": number, "code": "invalid_json"})
            continue
        code = _record_error(value)
        if code:
            errors.append({"line": number, "code": code})
            continue
        line_count, char_count = summarize_lines(value["lines"])
        entry = totals.setdefault(value["group"], [0, 0, 0])
        entry[0] += 1
        entry[1] += line_count
        entry[2] += char_count
    groups = [
        {"group": name, "records": r, "lines": n, "characters": c}
        for name, (r, n, c) in sorted(totals.items())
    ]
    return {"groups": groups, "errors": errors}


def groups_to_csv(groups):
    """Render group summaries as CSV text (header + rows, \\r\\n line endings)."""
    buffer = io.StringIO(newline="")
    writer = csv.writer(buffer)
    writer.writerow(CSV_FIELDS)
    for item in groups:
        writer.writerow([item[field] for field in CSV_FIELDS])
    return buffer.getvalue()


def main(argv=None):
    """CLI: summarize a UTF-8 JSONL file; exit 0 ok, 2 record errors, 1 I/O."""
    parser = argparse.ArgumentParser(description="Summarize JSONL groups.")
    parser.add_argument("input", metavar="INPUT", help="UTF-8 JSONL file")
    parser.add_argument("--format", choices=("json", "csv"), default="json",
                        help="output format (default: json)")
    args = parser.parse_args(argv)
    try:
        with open(args.input, encoding="utf-8") as handle:
            text = handle.read()
    except (OSError, UnicodeDecodeError) as exc:
        print(f"fixture_batch: cannot read {args.input}: {exc}", file=sys.stderr)
        return 1
    result = summarize_jsonl(text)
    if args.format == "csv":
        sys.stdout.write(groups_to_csv(result["groups"]))
        for error in result["errors"]:
            print(f"line {error['line']}: {error['code']}", file=sys.stderr)
    else:
        sys.stdout.write(json.dumps(result, ensure_ascii=False) + "\n")
    return 2 if result["errors"] else 0


if __name__ == "__main__":
    sys.exit(main())
