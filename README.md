# python-csv-dialect-footgun-lab

A tiny, reproducible, local correctness and safety lab about Python stdlib `csv` behavior, CSV dialect ambiguity, spreadsheet import/export footguns, and safe parsing boundaries. Inspired by the Hacker News discussion on "A love letter to the CSV format".

**Repo:** https://github.com/necat101/python-csv-dialect-footgun-lab

## Hacker News thread access

The HN thread at https://news.ycombinator.com/item?id=43484382 was accessed via the Hacker News Firebase API CLI **before** writing this README. The sentiment summary below reflects the actual HN discussion, not just the linked article title.

Evidence artifact: `hn_thread_evidence.md` (includes raw API dump at `hn_43484382.json`).

The thread had 689 comments – sentiment summary below is based on ~101 top-level comments fetched via the HN API.

## What Hacker News users were actually debating

**CSV is beloved because it is simple and universal.** Multiple commenters called CSV "ever so elegant", a "friendship bridge that prevents technical and non technical people from going to war", and noted that "CSV still quietly powers the majority of the world's data plumbing". The format is plain-text, human-readable, easily greppable, streamable, durable (data from the early '90s still imports), and can be opened by many tools without special libraries. "Anyone can write a parser in 30 minutes" was cited as both a strength and a weakness.

**CSV is hated because real-world files are messy.** Commenters on the receiving end – parsing CSV from eCAD software, banks, Excel exports, and "various (very expensive, very complicated)" tools – reported garbage output: unescaped quotes that make recovery impossible, optional quoting, ragged rows, missing headers, wrong encodings, and no strict spec to point to. "If you have to deal with random CSV from 'in the wild', it's pretty rough. If you have some sort of supplier agreement … it's pretty fine."

**Quoting and escaping footguns came up repeatedly.** CSV quoting has "non-local effects – an extra or missing quote at byte 1 can change the meaning of a comma at byte 1,000,000", making parallelization hard and data corruption catastrophic. Quickly-written parsers repeatedly mishandle quoting. Python's csv stdlib module was specifically praised: "For a long time I was very wary of CSV until I learnt Python and started using its excellent csv standard library module."

**Excel import/export behavior is a major practical footgun.** Excel uses locale-specific delimiters (semicolon in many European locales – "the worst thing about CSV is Excel using localization to choose the delimiter"), auto-converts dates and gene names (MAR1 → March 1, SEPT2 → September 2), and has CSV injection risks (`=SUM(A1:A2)` formula cells). Commenters disagreed on "Excel hates CSV" – some import into Excel fine, others hit delimiter and auto-typing issues constantly.

**Locale-specific separators and decimal commas complicate "CSV".** The term "CSV" often means a family of dialects: comma-separated, semicolon-separated (SSV), tab-separated (TSV), pipe-delimited. Decimal commas in many locales conflict with comma delimiters. "CSV is a 'no spec' family of de-facto formats, not a single thing … unlike XML or JSON, there isn't a document defining the grammar of well-formed or valid CSV files."

**TSV / JSON / JSONL / parquet / sqlite alternatives were debated without becoming the point.** "All hail TSV – like CSV, but you're probably less likely to want tabs than commas." JSONL (newline-delimited JSON) was called "my favourite format" – plain-text, streamable, compresses well. Parquet was praised for speed but criticized for append-unfriendliness and requiring native libraries. SQLite was mentioned for durability. The consensus: each format has tradeoffs, CSV wins on universality and editability.

**Producing clean CSV vs accepting arbitrary CSV is very different.** "CSV is easy if you produce clean RFC-ish CSV" is different from "CSV is easy when you must ingest arbitrary vendor files". Round-trip testing (export → import with realistic data) was recommended as a code review gate. Character encoding was called out as a major real-world pain: "Excel still produces some variant of latin1, some tools drop a BOM in your UTF-8".

**No data types in CSV – schema guessing is hard.** A database developer noted: "Do you make the Zip Code column a number or a string? The first thousand rows might have just 5 digit numbers (90210) but suddenly get to rows with the expanded format (12345-1234)". Dates, times, locale-specific formats, and embedded arrays were all mentioned as application-level ambiguities.

**Python's csv module dialect support is useful but not a universal spreadsheet compatibility proof.** Commenters noted many real-world CSV producers don't follow RFC 4180, and that csv.Sniffer is heuristic with expected false positives/negatives. No one claimed any single implementation proves cross-tool compatibility.

## What this lab actually tests

52 deterministic synthetic CSV cases covering:

- simple comma-delimited with/without header
- quoted fields: comma inside quotes, newline inside quotes, doubled quotes (`""`), escaped quotes with `escapechar`
- unescaped quote (accepted by default csv.reader – footgun – strict=True rejects)
- ragged rows: too few fields, too many fields
- duplicate header names, empty vs missing fields, None → empty string writer caveat
- skipinitialspace, blank lines
- line endings: CRLF, LF, CR (old Mac)
- newline='' policy marker
- encoding: UTF-8 BOM, non-ASCII UTF-8, Unicode NFC/NFD headers, emoji fields
- dialects: semicolon, tab, pipe delimiters
- numeric text caveats: decimal comma as data, thousands separator, ISO date string (all text unless application converts)
- spreadsheet caveats: formula-injection-looking cells, Excel auto-date (NOT_TESTED), gene-name conversion (NOT_TESTED)
- csv.Sniffer: correct delimiter guess, ambiguous delimiter, false-positive header, false-negative header
- writer policies: QUOTE_MINIMAL, QUOTE_ALL, QUOTE_NONE with/without escapechar, QUOTE_NONNUMERIC with float-conversion caveat
- DictReader: restkey for extra columns, restval for missing columns
- DictWriter: extrasaction='raise' / 'ignore', None-to-empty-string
- field_size_limit policy marker
- naive split(',') / splitlines() failures on quoted commas, embedded newlines, alternate delimiters, locale numbers
- schema/application validation NOT_TESTED marker
- spreadsheet compatibility NOT_TESTED marker
- external interoperability NOT_TESTED marker

16 methods, all Python stdlib only (`csv`, `io`, `decimal`, `unicodedata`, etc.):

1. `preserve_original_csv_text_baseline`
2. `csv_reader_default_baseline`
3. `csv_reader_declared_dialect_checker`
4. `csv_dictreader_header_checker`
5. `csv_writer_roundtrip_checker`
6. `csv_sniffer_delimiter_demo`
7. `csv_sniffer_header_demo`
8. `newline_policy_checker`
9. `encoding_bom_unicode_observer`
10. `numeric_text_policy_checker`
11. `quote_escape_policy_checker`
12. `ragged_row_policy_checker`
13. `dictwriter_policy_checker`
14. `naive_split_csv_detector`
15. `spreadsheet_compatibility_not_tested_marker`
16. `external_interoperability_not_tested_marker`

## Results

```
Total rows: 832, correct: 820, failed: 12
preserve_original_csv_text_baseline: 52/52 correct
csv_reader_default_baseline: 52/52 correct
csv_reader_declared_dialect_checker: 52/52 correct
csv_dictreader_header_checker: 52/52 correct
csv_writer_roundtrip_checker: 52/52 correct
csv_sniffer_delimiter_demo: 52/52 correct
csv_sniffer_header_demo: 52/52 correct
newline_policy_checker: 52/52 correct
encoding_bom_unicode_observer: 52/52 correct
numeric_text_policy_checker: 52/52 correct
quote_escape_policy_checker: 52/52 correct
ragged_row_policy_checker: 52/52 correct
dictwriter_policy_checker: 52/52 correct
naive_split_csv_detector: 40/52 correct  ← expected failures
spreadsheet_compatibility_not_tested_marker: 52/52 correct
external_interoperability_not_tested_marker: 52/52 correct
```

The naive split detector fails 12/52 cases – quoted commas, embedded newlines, alternate delimiters (semicolon/tab/pipe), thousands separators, Sniffer test cases, and locale decimal numbers – exactly as expected.

## Scope and safety

This is a **toy local lab**, NOT a production CSV ingestion system, spreadsheet compatibility test, Excel bug reproducer, financial parser, data cleaner, security scanner, or import validator.

- Synthetic data only: `example_user`, `test_order`, `fictional_event`, `toy_invoice`, `demo_config`, `sample_metric`, `synthetic_profile`, `example_note`, `fake_bank_row`, `demo_gene_label`, `test_product`, `sample_address`, `fictional_measurement`
- No real bank exports, customer records, logs, account data, gene databases, public datasets, or scraped CSVs
- No external CSV/spreadsheet libraries: no pandas, numpy, pyarrow, duckdb, frictionless, clevercsv, csvkit, openpyxl, pyxlsb
- No data formats: no parquet, sqlite benchmark, JSON Lines benchmark
- No test frameworks: no pytest, hypothesis
- No network: no requests, curl, web APIs, downloading real CSVs
- No external runtimes: no xsv/xan/miller/csvkit, Excel/LibreOffice/Google Sheets automation, jq, node, Rust, Go
- Python stdlib only

**Do not claim this lab proves a real CSV file is safe, lossless, RFC 4180 compliant, localized correctly, spreadsheet-safe, database-ready, or production-ready.**

The lab distinguishes carefully between:
- what HN commenters discussed
- what RFC 4180 / PEP 305 describes
- what Python's csv module exposes
- what this toy lab can actually prove

CSV is extremely useful because it is simple, old, portable, and widely supported. CSV is also messy because "CSV" often means a family of dialects with optional quoting, escaping, semicolon variants, TSV variants, embedded newlines, locale-specific decimal commas, Excel transformations, missing headers, duplicate headers, ragged rows, BOMs, encoding assumptions, and application-level type ambiguity. Producing clean CSV is easy; accepting arbitrary CSV from other people is hard.

## Running the lab

```bash
python3 -m py_compile generate_cases.py run_lab.py
python3 generate_cases.py
python3 run_lab.py
```

Outputs:
- `RESULTS.md` – summary tables
- `results_rows.json` / `results_rows.csv` – per-case/per-method artifact
- `VERIFY.md` – fresh-clone verification transcript

Python 3.12+, stdlib only, zero external dependencies, zero network calls, zero subprocesses.

## References

- HN thread: https://news.ycombinator.com/item?id=43484382
- Article: https://github.com/medialab/xan/blob/master/docs/LOVE_LETTER.md
- RFC 4180: https://www.rfc-editor.org/rfc/rfc4180
- PEP 305: https://peps.python.org/pep-0305/
- Python csv docs: https://docs.python.org/3/library/csv.html
