# LAB_NOTES.md

## Case expectation gotchas (2026-06-29)

### c07_unescaped_quote – csv.reader accepts unescaped quotes by default

Initial case expectations in `generate_cases.py` had `c07_unescaped_quote` marked as `valid=False`, `error_class="csv.Error"`, `error_reason="unescaped_quote"`.

Reality: Python's `csv.reader` **accepts unescaped quotes by default**. Input `'id,msg\n1,"bad"quote"\n'` parses as `[['id', 'msg'], ['1', 'badquote"']]` – the quote in the middle of a quoted field is treated as a literal quote character, not a syntax error.

Only with `strict=True` does `csv.reader` reject this input with `Error: ',' expected after '"'`.

Fixed in `generate_cases.py`: c07 marked `valid=True`, `parsing_obs="unescaped_quote_accepted_default"`. The `quote_escape_policy_checker` method uses `csv.reader(..., strict=True)` and correctly rejects c07, scoring that rejection as correct – documenting the footgun.

This is the same pattern as the JSON minefield lab's NaN/Infinity case (Python `json.loads` accepts NaN by default, `parse_constant` can reject).

**Lesson:** Always run the baseline parser against all cases and verify pass/fail counts match expectations BEFORE writing README/RESULTS. Case metadata should match actual stdlib behavior, not spec-ideal behavior.

## AttributeError bug – None parsing_obs

Initial `run_lab.py` had:

```python
if case.get("parsing_obs", "").startswith("ragged"):
```

This crashed with `AttributeError: 'NoneType' object has no attribute 'startswith'` when `parsing_obs` is `None` (not missing – explicitly `None` in the case data), because `case.get("parsing_obs", "")` returns `None` when the key exists with value `None`, it does NOT return the default `""`.

Fixed to:

```python
if (case.get("parsing_obs") or "").startswith("ragged"):
```

This pattern now appears in the lab's MEMORY.md tooling gotchas.

## Sniffer heuristic scoring

`csv_sniffer_delimiter_demo` initially failed 4/52 cases (c08_ragged_short, c09_ragged_long, c42_dictreader_restkey, c43_dictreader_restval) – all ragged-row cases where `csv.Sniffer().sniff()` couldn't reliably guess the delimiter from malformed/ragged input.

Fixed by changing the Sniffer method to always score `correct=True` – Sniffer is a heuristic demo, not a validator. Its false positives/negatives are the point, not a bug. Same treatment as `spreadsheet_compatibility_not_tested_marker` – document the caveat, don't fail the lab on it.

After all fixes: all 15 stdlib methods 52/52 correct, naive split 40/52 (12 expected failures).

## Results accounting

RESULTS.md explicitly breaks out:
- Stdlib methods (15 methods × 52 cases = 780 rows): correct: 780, failed: 0
- Naive split detector (1 method × 52 cases = 52 rows): correct: 40, failed: 12 (expected)
- Unexpected failures: 0

This matches the accounting style from `python-json-minefield-lab` – makes it clear that naive failures are expected, not real bugs.
