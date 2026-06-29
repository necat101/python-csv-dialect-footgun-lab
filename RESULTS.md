# python-csv-dialect-footgun-lab — Results

Total rows: 832, correct: 820, failed: 12

Breakdown:
- Stdlib methods (15 methods × 52 cases = 780 rows): correct: 780, failed: 0
- Naive split detector (1 method × 52 cases = 52 rows): correct: 40, failed: 12 (expected – naive split fails on quoted commas, embedded newlines, alternate delimiters, escaping)
- **Unexpected failures: 0**

## Per-method

| Method | Correct | Total | Note |
|---|---|---|---|
| preserve_original_csv_text_baseline | 52 | 52 |  |
| csv_reader_default_baseline | 52 | 52 |  |
| csv_reader_declared_dialect_checker | 52 | 52 |  |
| csv_dictreader_header_checker | 52 | 52 |  |
| csv_writer_roundtrip_checker | 52 | 52 |  |
| csv_sniffer_delimiter_demo | 52 | 52 |  |
| csv_sniffer_header_demo | 52 | 52 |  |
| newline_policy_checker | 52 | 52 |  |
| encoding_bom_unicode_observer | 52 | 52 |  |
| numeric_text_policy_checker | 52 | 52 |  |
| quote_escape_policy_checker | 52 | 52 |  |
| ragged_row_policy_checker | 52 | 52 |  |
| dictwriter_policy_checker | 52 | 52 |  |
| naive_split_csv_detector | 40 | 52 | expected naive failures |
| spreadsheet_compatibility_not_tested_marker | 52 | 52 |  |
| external_interoperability_not_tested_marker | 52 | 52 |  |

## Environment

- Python: 3.12.3
- csv module: available
- csv.list_dialects(): ['excel', 'excel-tab', 'unix']
- Platform: Linux-6.17.0-1009-aws-x86_64-with-glibc2.39
- Cases: 52
- Methods: 16
- Subprocesses: 0
- Random seed: 42
- HN thread accessed: yes – https://news.ycombinator.com/item?id=43484382
- Network/API calls during benchmark: none
- External CSV/spreadsheet libraries: none
- Spreadsheet automation (Excel/LibreOffice/Google Sheets): none
