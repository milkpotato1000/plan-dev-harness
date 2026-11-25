import unittest

from fixture_format import format_lines, summarize_lines


class FormatLinesTest(unittest.TestCase):
    def test_empty_input_returns_empty_string(self):
        self.assertEqual(format_lines([]), "")

    def test_only_blank_values_returns_empty_string(self):
        self.assertEqual(format_lines(["", "   ", "\t\n", "\r\n"]), "")

    def test_strips_and_drops_blank_lines(self):
        self.assertEqual(format_lines(["  a  ", "", "b"]), "a\nb\n")

    def test_single_value_gets_one_trailing_newline(self):
        self.assertEqual(format_lines(["x"]), "x\n")

    def test_existing_trailing_newline_not_doubled(self):
        self.assertEqual(format_lines(["x\n"]), "x\n")

    def test_inner_whitespace_preserved(self):
        self.assertEqual(format_lines(["a  b", " c\td "]), "a  b\nc\td\n")

    def test_tabs_and_crlf_stripped_at_edges(self):
        self.assertEqual(format_lines(["\tone\r\n", "two\r\n"]), "one\ntwo\n")

    def test_order_preserved(self):
        self.assertEqual(format_lines(["c", "a", "b"]), "c\na\nb\n")

    def test_input_not_mutated(self):
        original = ["  a ", "", " b"]
        snapshot = list(original)
        format_lines(original)
        self.assertEqual(original, snapshot)

    def test_generator_and_tuple_input(self):
        self.assertEqual(format_lines(v for v in [" p ", " ", "q"]), "p\nq\n")
        self.assertEqual(format_lines(("p", "q")), "p\nq\n")


class SummarizeLinesTest(unittest.TestCase):
    def test_empty_and_blank_input(self):
        self.assertEqual(summarize_lines([]), (0, 0))
        self.assertEqual(summarize_lines(["", "  ", "\t"]), (0, 0))

    def test_strips_and_drops_blank(self):
        self.assertEqual(summarize_lines(["  ab  ", "", "c"]), (2, 3))

    def test_inner_whitespace_counts(self):
        self.assertEqual(summarize_lines(["a  b"]), (1, 4))

    def test_unicode_characters_and_crlf(self):
        self.assertEqual(summarize_lines(["é", "x\r\n"]), (2, 2))

    def test_generator_input_and_no_mutation(self):
        self.assertEqual(summarize_lines(v for v in [" a ", "bc"]), (2, 3))
        original = [" a ", "", "bc "]
        snapshot = list(original)
        summarize_lines(original)
        self.assertEqual(original, snapshot)

    def test_consistent_with_format_lines(self):
        cases = [["  ab  ", "", "c"], ["a  b"], ["é", "x\r\n"], ["x"]]
        for lines in cases:
            count, chars = summarize_lines(lines)
            self.assertEqual(chars, len(format_lines(lines)) - count)


if __name__ == "__main__":
    unittest.main()
