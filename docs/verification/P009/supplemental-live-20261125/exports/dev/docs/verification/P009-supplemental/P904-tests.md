# P904 test run (includes P901–P903 regression)

- run_at: 2026-11-25T00:34:47Z
- adopted plan: e5a3da0d913d7b253da3d1a2d24e52a4272b801e
- command: python3 -B -m unittest -v test_fixture_format test_fixture_batch

```
test_empty_input_returns_empty_string (test_fixture_format.FormatLinesTest) ... ok
test_existing_trailing_newline_not_doubled (test_fixture_format.FormatLinesTest) ... ok
test_generator_and_tuple_input (test_fixture_format.FormatLinesTest) ... ok
test_inner_whitespace_preserved (test_fixture_format.FormatLinesTest) ... ok
test_input_not_mutated (test_fixture_format.FormatLinesTest) ... ok
test_only_blank_values_returns_empty_string (test_fixture_format.FormatLinesTest) ... ok
test_order_preserved (test_fixture_format.FormatLinesTest) ... ok
test_single_value_gets_one_trailing_newline (test_fixture_format.FormatLinesTest) ... ok
test_strips_and_drops_blank_lines (test_fixture_format.FormatLinesTest) ... ok
test_tabs_and_crlf_stripped_at_edges (test_fixture_format.FormatLinesTest) ... ok
test_consistent_with_format_lines (test_fixture_format.SummarizeLinesTest) ... ok
test_empty_and_blank_input (test_fixture_format.SummarizeLinesTest) ... ok
test_generator_input_and_no_mutation (test_fixture_format.SummarizeLinesTest) ... ok
test_inner_whitespace_counts (test_fixture_format.SummarizeLinesTest) ... ok
test_strips_and_drops_blank (test_fixture_format.SummarizeLinesTest) ... ok
test_unicode_characters_and_crlf (test_fixture_format.SummarizeLinesTest) ... ok
test_invalid_utf8_exit_1_no_stdout (test_fixture_batch.CliTest) ... ok
test_missing_file_exit_1_no_stdout (test_fixture_batch.CliTest) ... ok
test_record_errors_exit_2_still_prints_json (test_fixture_batch.CliTest) ... ok
test_subprocess_cli (test_fixture_batch.CliTest) ... ok
test_success_exit_0_with_json_output (test_fixture_batch.CliTest) ... ok
test_usage_error_uses_argparse_exit_2 (test_fixture_batch.CliTest) ... ok
test_bad_format_value_is_argparse_usage_error (test_fixture_batch.CsvFormatTest) ... ok
test_default_and_json_output_byte_identical_to_p903 (test_fixture_batch.CsvFormatTest) ... ok
test_empty_result_is_header_only (test_fixture_batch.CsvFormatTest) ... ok
test_io_and_decode_errors_exit_1_no_stdout (test_fixture_batch.CsvFormatTest) ... ok
test_quoted_group_row_matches_card_example (test_fixture_batch.CsvFormatTest) ... ok
test_record_errors_exit_2_csv_on_stdout_errors_on_stderr (test_fixture_batch.CsvFormatTest) ... ok
test_special_groups_round_trip_sorted_and_summed (test_fixture_batch.CsvFormatTest) ... ok
test_empty_and_blank_only_input (test_fixture_batch.SummarizeJsonlTest) ... ok
test_empty_group_name_and_blank_lines_record (test_fixture_batch.SummarizeJsonlTest) ... ok
test_extra_keys_ignored (test_fixture_batch.SummarizeJsonlTest) ... ok
test_groups_sorted_duplicates_summed_and_unicode (test_fixture_batch.SummarizeJsonlTest) ... ok
test_invalid_type_variants (test_fixture_batch.SummarizeJsonlTest) ... ok
test_mixed_valid_invalid_keeps_processing_with_line_numbers (test_fixture_batch.SummarizeJsonlTest) ... ok
test_trailing_newline_and_crlf_do_not_change_result (test_fixture_batch.SummarizeJsonlTest) ... ok
test_unicode_counts_code_points (test_fixture_batch.SummarizeJsonlTest) ... ok

----------------------------------------------------------------------
Ran 37 tests in 0.410s

OK
exit=0
```
