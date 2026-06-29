# VERIFY.md — Fresh-clone verification

```console
$ git clone https://github.com/necat101/python-csv-dialect-footgun-lab.git verify_clone
Cloning into 'verify_clone'...
$ cd verify_clone
$ python3 -m py_compile generate_cases.py run_lab.py
$ python3 generate_cases.py
Wrote 52 cases to cases.json
$ python3 run_lab.py
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
naive_split_csv_detector: 40/52 correct
spreadsheet_compatibility_not_tested_marker: 52/52 correct
external_interoperability_not_tested_marker: 52/52 correct
Wrote RESULTS.md, results_rows.json/csv
```

Environment:
- Python: 3.12.3
- Platform: Linux-6.17.0-1009-aws-x86_64-with-glibc2.39
- csv module: available (stdlib)
- csv.list_dialects(): ['excel', 'excel-tab', 'unix']
- Cases: 52
- Methods: 16
- Subprocesses: 0
- Random seed: 42
- HN thread accessed: yes – https://news.ycombinator.com/item?id=43484382
- Network/API calls during benchmark: none
- External CSV/spreadsheet libraries: none
- Spreadsheet automation: none

The naive split detector failing 12/52 cases is expected – quoted commas, embedded newlines, alternate delimiters, thousands separators, and locale decimal numbers all break naive split(',') / splitlines() parsing.
```
