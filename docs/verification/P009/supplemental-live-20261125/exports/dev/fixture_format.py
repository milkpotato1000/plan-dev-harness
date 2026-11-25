"""P009 fixture text helpers (P901)."""


def _normalize(lines):
    stripped = (value.strip() for value in lines)
    return [value for value in stripped if value]


def format_lines(lines):
    """Strip each value, drop blank ones and join with newlines.

    Returns the remaining values joined by "\\n" plus one trailing newline,
    or "" when nothing remains. Inner whitespace and order are preserved and
    the input is never mutated; any iterable of strings is accepted.
    """
    kept = _normalize(lines)
    if not kept:
        return ""
    return "\n".join(kept) + "\n"


def summarize_lines(lines):
    """Return (line_count, char_count) for the format_lines normalization.

    char_count sums the normalized line lengths, excluding the newline
    separators and trailing newline; inner whitespace counts.
    """
    kept = _normalize(lines)
    return len(kept), sum(len(value) for value in kept)
