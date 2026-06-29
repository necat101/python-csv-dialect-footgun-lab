#!/usr/bin/env python3
"""Generate deterministic CSV dialect / parsing footgun cases."""
import json, csv, io

CASES = []

def add(case_id, category, fake_record, csv_text, context,
        dialect=None,
        delimiter=",", quotechar='"', escapechar=None, lineterminator="\n",
        valid=True,
        row_count=None, field_count=None,
        header_obs=None, dialect_obs=None, parsing_obs=None,
        writer_obs=None, dict_obs=None, sniffer_obs=None,
        numeric_obs=None, unicode_obs=None,
        spreadsheet_obs="not_tested", interoperability="not_tested",
        error_class=None, error_reason=None, naive_should_fail=False,
        **extra):
    CASES.append({
        "case_id": case_id,
        "category": category,
        "fake_record": fake_record,
        "csv_text": csv_text,
        "context": context,
        "dialect": dialect,
        "delimiter": delimiter,
        "quotechar": quotechar,
        "escapechar": escapechar,
        "lineterminator": lineterminator,
        "valid": valid,
        "row_count": row_count,
        "field_count": field_count,
        "header_obs": header_obs,
        "dialect_obs": dialect_obs,
        "parsing_obs": parsing_obs,
        "writer_obs": writer_obs,
        "dict_obs": dict_obs,
        "sniffer_obs": sniffer_obs,
        "numeric_obs": numeric_obs,
        "unicode_obs": unicode_obs,
        "spreadsheet_obs": spreadsheet_obs,
        "interoperability": interoperability,
        "error_class": error_class,
        "error_reason": error_reason,
        "naive_should_fail": naive_should_fail,
        **extra
    })

# simple comma + header
add("c01_simple_comma_header", "valid_csv", "example_user", "id,name\n1,Alice\n2,Bob\n", "valid_csv",
    row_count=3, field_count=2, header_obs="id,name")
# headerless
add("c02_headerless", "valid_csv", "test_order", "1,Alice\n2,Bob\n", "valid_csv",
    row_count=2, field_count=2, header_obs="no_header")
# quoted comma
add("c03_quoted_comma", "quoting_caveat", "sample_address", 'id,addr\n1,"Main St, Apt 4"\n', "quoting_caveat",
    row_count=2, field_count=2, parsing_obs="quoted_comma_ok", naive_should_fail=True)
# quoted newline
add("c04_quoted_newline", "newline_caveat", "example_note", 'id,msg\n1,"hello\nworld"\n', "newline_caveat",
    row_count=2, field_count=2, parsing_obs="quoted_newline_ok", naive_should_fail=True)
# doubled quote
add("c05_doubled_quote", "quoting_caveat", "example_note", 'id,msg\n1,"say ""hi"""\n', "quoting_caveat",
    row_count=2, field_count=2, parsing_obs="doubled_quote_ok")
# escaped quote with escapechar
add("c06_escaped_quote", "quoting_caveat", "example_note", 'id,msg\n1,"say \\"hi\\""\n', "quoting_caveat",
    escapechar="\\", parsing_obs="escapechar_quote", row_count=2, field_count=2)
# unescaped quote negative
add("c07_unescaped_quote", "quoting_caveat", "example_note", 'id,msg\n1,"bad"quote"\n', "quoting_caveat",
    valid=True, parsing_obs="unescaped_quote_accepted_default", error_class=None, error_reason=None, naive_should_fail=True)
# ragged short
add("c08_ragged_short", "ragged_row_caveat", "test_product", "a,b,c\n1,2\n3,4,5\n", "ragged_row_caveat",
    row_count=3, field_count=None, parsing_obs="ragged_short")
# ragged long
add("c09_ragged_long", "ragged_row_caveat", "test_product", "a,b\n1,2,3\n4,5\n", "ragged_row_caveat",
    row_count=3, parsing_obs="ragged_long")
# duplicate header
add("c10_duplicate_header", "header_caveat", "demo_config", "id,id\n1,2\n", "header_caveat",
    row_count=2, header_obs="duplicate_header", dict_obs="duplicate_key_last_wins")
# empty vs missing
add("c11_empty_vs_missing", "header_caveat", "synthetic_profile", "a,b,c\n1,,3\n", "header_caveat",
    row_count=2, parsing_obs="empty_field")
# None empty string
add("c12_none_empty", "writer_policy", "demo_config", "WRITER_NONE_TEST", "writer_policy",
    writer_obs="none_empty_string", valid=True)
# skipinitialspace
add("c13_skipinitialspace", "dialect_caveat", "example_user", "a, b, c\n1, 2, 3\n", "dialect_caveat",
    parsing_obs="skipinitialspace_caveat", row_count=2)
# blank line
add("c14_blank_line", "newline_caveat", "test_order", "a,b\n1,2\n\n3,4\n", "newline_caveat",
    row_count=4, parsing_obs="blank_line")
# CRLF
add("c15_crlf", "newline_caveat", "test_order", "a,b\r\n1,2\r\n", "newline_caveat",
    lineterminator="\r\n", row_count=2, parsing_obs="crlf_ok")
# LF
add("c16_lf", "newline_caveat", "test_order", "a,b\n1,2\n", "newline_caveat",
    lineterminator="\n", row_count=2, parsing_obs="lf_ok")
# CR (old Mac)
add("c17_cr", "newline_caveat", "test_order", "a,b\r1,2\r", "newline_caveat",
    lineterminator="\r", parsing_obs="cr_caveat", row_count=2)
# newline='' policy marker
add("c18_newline_policy", "newline_caveat", "demo_config", "a,b\n1,2\n", "newline_caveat",
    parsing_obs="newline_policy_newline_empty", row_count=2)
# BOM
add("c19_bom_header", "encoding_caveat", "example_user", "\ufeffid,name\n1,Alice\n", "encoding_caveat",
    unicode_obs="bom_header", row_count=2, header_obs="bom_prefixed")
# utf8 text
add("c20_utf8_text", "unicode_caveat", "example_note", "id,msg\n1,café 🐱\n", "unicode_caveat",
    unicode_obs="utf8_ok", row_count=2)
# NFC/NFD header
add("c21_unicode_normalization", "unicode_caveat", "synthetic_profile", "caf\u00e9,cafe\u0301\n1,2\n", "unicode_caveat",
    unicode_obs="nfc_nfd_different", row_count=2, header_obs="unicode_headers")
# emoji
add("c22_emoji_field", "unicode_caveat", "example_note", "id,msg\n1,🙂🚀🐱\n", "unicode_caveat",
    unicode_obs="emoji_ok", row_count=2)
# semicolon delimiter
add("c23_semicolon", "dialect_caveat", "fake_bank_row", "id;name\n1;Alice\n", "dialect_caveat",
    delimiter=";", dialect_obs="semicolon_delimiter", row_count=2, naive_should_fail=True)
# tab delimiter
add("c24_tab", "dialect_caveat", "test_product", "id\tname\n1\tAlice\n", "dialect_caveat",
    delimiter="\t", dialect_obs="tab_delimiter", row_count=2, naive_should_fail=True)
# pipe delimiter
add("c25_pipe", "dialect_caveat", "test_product", "id|name\n1|Alice\n", "dialect_caveat",
    delimiter="|", dialect_obs="pipe_delimiter", row_count=2, naive_should_fail=True)
# decimal comma text
add("c26_decimal_comma", "numeric_text_caveat", "sample_metric", 'id;value\n1;"12,34"\n', "numeric_text_caveat",
    delimiter=";", numeric_obs="decimal_comma_text", row_count=2)
# thousands separator
add("c27_thousands_sep", "numeric_text_caveat", "toy_invoice", 'id,amount\n1,"1,234.56"\n', "numeric_text_caveat",
    numeric_obs="thousands_separator_text", row_count=2, naive_should_fail=True)
# ISO date string
add("c28_iso_date", "numeric_text_caveat", "fictional_event", "id,date\n1,2024-06-01\n", "numeric_text_caveat",
    numeric_obs="date_string_text", row_count=2)
# Excel formula injection caveat
add("c29_formula_injection", "spreadsheet_caveat", "example_note", "id,msg\n1,=SUM(A1:A2)\n", "spreadsheet_caveat",
    spreadsheet_obs="formula_injection_caveat", row_count=2)
# Excel auto date not tested
add("c30_excel_auto_date", "spreadsheet_caveat", "demo_gene_label", "id,label\n1,MAR1\n", "spreadsheet_caveat",
    spreadsheet_obs="excel_auto_date_not_tested", row_count=2)
# gene name not tested
add("c31_gene_name", "spreadsheet_caveat", "demo_gene_label", "id,gene\n1,SEPT2\n", "spreadsheet_caveat",
    spreadsheet_obs="gene_name_not_tested", row_count=2)
# Sniffer correct
add("c32_sniffer_delimiter", "sniffer_caveat", "test_order", "a;b;c\n1;2;3\n4;5;6\n", "sniffer_caveat",
    delimiter=";", sniffer_obs="sniffer_correct", dialect_obs="semicolon_delimiter", row_count=3)
# Sniffer ambiguous
add("c33_sniffer_ambiguous", "sniffer_caveat", "test_order", "a,b\n1,2\n", "sniffer_caveat",
    sniffer_obs="sniffer_ambiguous", row_count=2)
# Sniffer false positive header
add("c34_sniffer_header_fp", "sniffer_caveat", "test_order", "Alice,Bob\nCarol,Dave\n", "sniffer_caveat",
    sniffer_obs="sniffer_header_false_positive", row_count=2, header_obs="no_header_but_sniffer_says_yes")
# Sniffer false negative header
add("c35_sniffer_header_fn", "sniffer_caveat", "test_order", "1,2\n3,4\n", "sniffer_caveat",
    sniffer_obs="sniffer_header_false_negative", row_count=2, header_obs="header_maybe_missed")
# QUOTE_MINIMAL
add("c36_quote_minimal", "writer_policy", "demo_config", "WRITER_QUOTE_MINIMAL", "writer_policy",
    writer_obs="quote_minimal", valid=True)
# QUOTE_ALL
add("c37_quote_all", "writer_policy", "demo_config", "WRITER_QUOTE_ALL", "writer_policy",
    writer_obs="quote_all", valid=True)
# QUOTE_NONE escape
add("c38_quote_none_escape", "writer_policy", "example_note", "WRITER_QUOTE_NONE_ESCAPE", "writer_policy",
    writer_obs="quote_none_escape", escapechar="\\", valid=True)
# QUOTE_NONE no escape negative
add("c39_quote_none_no_escape", "writer_policy", "example_note", "WRITER_QUOTE_NONE_NO_ESCAPE", "writer_policy",
    writer_obs="quote_none_no_escape_negative", valid=False, error_class="csv.Error", error_reason="need_escape")
# QUOTE_NONNUMERIC
add("c40_quote_nonnumeric", "writer_policy", "sample_metric", "WRITER_QUOTE_NONNUMERIC", "writer_policy",
    writer_obs="quote_nonnumeric", valid=True, numeric_obs="float_conversion")
# QUOTE_NONNUMERIC caveat
add("c41_quote_nonnumeric_caveat", "writer_policy", "sample_metric", "WRITER_QUOTE_NONNUMERIC_CAVEAT", "writer_policy",
    writer_obs="quote_nonnumeric_caveat", numeric_obs="bool_fraction_not_universal", valid=True)
# DictReader restkey
add("c42_dictreader_restkey", "dictreader_policy", "test_product", "a,b\n1,2,3,4\n", "dictreader_policy",
    dict_obs="restkey_extra_columns", row_count=2, parsing_obs="ragged_long")
# DictReader restval
add("c43_dictreader_restval", "dictreader_policy", "test_product", "a,b,c\n1,2\n", "dictreader_policy",
    dict_obs="restval_missing_columns", row_count=2, parsing_obs="ragged_short")
# DictWriter extrasaction raise
add("c44_dictwriter_raise", "dictreader_policy", "demo_config", "WRITER_DICT_EXTRAS_RAISE", "dictreader_policy",
    dict_obs="extrasaction_raise", valid=False, error_class="ValueError", error_reason="extrasaction_raise")
# DictWriter extrasaction ignore
add("c45_dictwriter_ignore", "dictreader_policy", "demo_config", "WRITER_DICT_EXTRAS_IGNORE", "dictreader_policy",
    dict_obs="extrasaction_ignore", valid=True)
# field_size_limit
add("c46_field_size_limit", "writer_policy", "example_note", "WRITER_FIELD_SIZE_LIMIT", "writer_policy",
    writer_obs="field_size_policy", valid=True)
# naive split failure quoted comma
add("c47_naive_split", "naive_negative", "sample_address", 'id,addr\n1,"Main St, Apt 4"\n', "naive_negative",
    parsing_obs="naive_split_failure", naive_should_fail=True, row_count=2)
# naive line split failure embedded newline
add("c48_naive_linesplit", "naive_negative", "example_note", 'id,msg\n1,"hello\nworld"\n', "naive_negative",
    parsing_obs="naive_line_split_failure", naive_should_fail=True, row_count=2)
# naive strip/cast locale number
add("c49_naive_locale", "naive_negative", "sample_metric", 'id;value\n1;"12,34"\n', "naive_negative",
    delimiter=";", numeric_obs="naive_locale_cast_failure", naive_should_fail=True, row_count=2)
# schema not tested
add("c50_schema_not_tested", "schema_caveat", "toy_invoice", "id,price\n1,9.99\n", "schema_caveat",
    numeric_obs="schema_validation_not_tested", row_count=2, spreadsheet_obs="not_tested", interoperability="not_tested")
# spreadsheet not tested
add("c51_spreadsheet_not_tested", "spreadsheet_caveat", "fictional_measurement", "id,value\n1,1-2\n", "spreadsheet_caveat",
    spreadsheet_obs="spreadsheet_compatibility_not_tested", row_count=2, interoperability="not_tested")
# external interop not tested
add("c52_external_not_tested", "external_truth_not_tested", "test_order", "id,name\n1,Alice\n", "external_truth_not_tested",
    interoperability="not_tested", spreadsheet_obs="not_tested", row_count=2)

with open("cases.json","w") as f:
    json.dump(CASES, f, indent=2)
print(f"Wrote {len(CASES)} cases to cases.json")
