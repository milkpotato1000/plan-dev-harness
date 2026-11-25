import contextlib
import csv
import io
import json
import os
import subprocess
import sys
import tempfile
import unittest

from fixture_batch import main, summarize_jsonl

HERE = os.path.dirname(os.path.abspath(__file__))

MIXED = (
    '{"group":"a","lines":[]}\n'
    "\n"
    "[1]\n"
    "{bad\n"
    '{"group":1,"lines":[]}\n'
    '{"group":"a","lines":["ok",2]}'
)


def group(name, records, lines, characters):
    return {"group": name, "records": records, "lines": lines, "characters": characters}


class SummarizeJsonlTest(unittest.TestCase):
    def test_empty_and_blank_only_input(self):
        self.assertEqual(summarize_jsonl(""), {"groups": [], "errors": []})
        self.assertEqual(summarize_jsonl("\n  \n\t\n"), {"groups": [], "errors": []})

    def test_groups_sorted_duplicates_summed_and_unicode(self):
        text = (
            '{"group":"b","lines":["  x ","",""]}\n'
            '{"group":"a","lines":["héllo","w o"]}\n'
            '{"group":"b","lines":["yz"]}\n'
        )
        self.assertEqual(
            summarize_jsonl(text),
            {"groups": [group("a", 1, 2, 8), group("b", 2, 2, 3)], "errors": []},
        )

    def test_mixed_valid_invalid_keeps_processing_with_line_numbers(self):
        self.assertEqual(
            summarize_jsonl(MIXED),
            {
                "groups": [group("a", 1, 0, 0)],
                "errors": [
                    {"line": 3, "code": "not_object"},
                    {"line": 4, "code": "invalid_json"},
                    {"line": 5, "code": "invalid_group"},
                    {"line": 6, "code": "invalid_lines"},
                ],
            },
        )

    def test_invalid_type_variants(self):
        text = "\n".join([
            '"text"',                       # 1 not_object
            "null",                         # 2 not_object
            '{"lines":["a"]}',              # 3 invalid_group (missing)
            '{"group":null,"lines":[]}',    # 4 invalid_group
            '{"group":"g"}',                # 5 invalid_lines (missing)
            '{"group":"g","lines":"abc"}',  # 6 invalid_lines (not array)
            '{"group":5}',                  # 7 first violation only
        ])
        self.assertEqual(
            [(e["line"], e["code"]) for e in summarize_jsonl(text)["errors"]],
            [(1, "not_object"), (2, "not_object"), (3, "invalid_group"),
             (4, "invalid_group"), (5, "invalid_lines"), (6, "invalid_lines"),
             (7, "invalid_group")],
        )
        self.assertEqual(summarize_jsonl(text)["groups"], [])

    def test_empty_group_name_and_blank_lines_record(self):
        text = '{"group":"","lines":["  "," q "]}\n{"group":"z","lines":["", " "]}'
        self.assertEqual(
            summarize_jsonl(text)["groups"],
            [group("", 1, 1, 1), group("z", 1, 0, 0)],
        )

    def test_extra_keys_ignored(self):
        text = '{"group":"g","lines":["ab"],"extra":{"x":1}}'
        self.assertEqual(summarize_jsonl(text)["groups"], [group("g", 1, 1, 2)])

    def test_trailing_newline_and_crlf_do_not_change_result(self):
        base = '{"group":"g","lines":["a b"]}\n{"group":"h","lines":["é"]}'
        expected = summarize_jsonl(base)
        self.assertEqual(summarize_jsonl(base + "\n"), expected)
        self.assertEqual(summarize_jsonl(base.replace("\n", "\r\n") + "\r\n"), expected)
        self.assertEqual(expected["groups"], [group("g", 1, 1, 3), group("h", 1, 1, 1)])

    def test_unicode_counts_code_points(self):
        text = json.dumps({"group": "한글", "lines": ["가나다", "😀"]}, ensure_ascii=False)
        self.assertEqual(summarize_jsonl(text)["groups"], [group("한글", 1, 2, 4)])


class CliTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)

    def write(self, name, data):
        path = os.path.join(self.tmp.name, name)
        with open(path, "wb") as handle:
            handle.write(data)
        return path

    def run_main(self, argv):
        out, err = io.StringIO(), io.StringIO()
        with contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
            code = main(argv)
        return code, out.getvalue(), err.getvalue()

    def test_success_exit_0_with_json_output(self):
        path = self.write("ok.jsonl", '{"group":"é","lines":[" a ","bc"]}\n'.encode("utf-8"))
        code, out, _ = self.run_main([path])
        self.assertEqual(code, 0)
        self.assertEqual(out, '{"groups": [{"group": "é", "records": 1, "lines": 2, "characters": 3}], "errors": []}\n')

    def test_record_errors_exit_2_still_prints_json(self):
        path = self.write("mixed.jsonl", MIXED.encode("utf-8"))
        code, out, _ = self.run_main([path])
        self.assertEqual(code, 2)
        self.assertEqual(json.loads(out), summarize_jsonl(MIXED))

    def test_missing_file_exit_1_no_stdout(self):
        code, out, err = self.run_main([os.path.join(self.tmp.name, "missing.jsonl")])
        self.assertEqual((code, out), (1, ""))
        self.assertIn("cannot read", err)

    def test_invalid_utf8_exit_1_no_stdout(self):
        path = self.write("bad.jsonl", b'{"group":"a","lines":["\xff"]}\n')
        code, out, _ = self.run_main([path])
        self.assertEqual((code, out), (1, ""))

    def test_usage_error_uses_argparse_exit_2(self):
        # Usage errors share exit code 2 with record errors (argparse default).
        with contextlib.redirect_stderr(io.StringIO()):
            with self.assertRaises(SystemExit) as caught:
                main([])
        self.assertEqual(caught.exception.code, 2)

    def test_subprocess_cli(self):
        path = self.write("mixed.jsonl", MIXED.encode("utf-8"))
        proc = subprocess.run(
            [sys.executable, "-B", os.path.join(HERE, "fixture_batch.py"), path],
            capture_output=True, cwd=HERE,
        )
        self.assertEqual(proc.returncode, 2)
        self.assertEqual(json.loads(proc.stdout.decode("utf-8")), summarize_jsonl(MIXED))
        missing = subprocess.run(
            [sys.executable, "-B", os.path.join(HERE, "fixture_batch.py"), path + ".nope"],
            capture_output=True, cwd=HERE,
        )
        self.assertEqual((missing.returncode, missing.stdout), (1, b""))


class CsvFormatTest(unittest.TestCase):
    HEADER = "group,records,lines,characters\r\n"

    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)

    def write(self, name, text):
        path = os.path.join(self.tmp.name, name)
        with open(path, "wb") as handle:
            handle.write(text.encode("utf-8"))
        return path

    def run_cli(self, *args):
        return subprocess.run(
            [sys.executable, "-B", os.path.join(HERE, "fixture_batch.py"), *args],
            capture_output=True, cwd=HERE,
        )

    def test_quoted_group_row_matches_card_example(self):
        path = self.write("q.jsonl", json.dumps({"group": 'a,"b"', "lines": ["xy"]}) + "\n")
        proc = self.run_cli(path, "--format", "csv")
        self.assertEqual(proc.returncode, 0)
        self.assertEqual(proc.stdout, (self.HEADER + '"a,""b""",1,1,2\r\n').encode("utf-8"))
        self.assertEqual(proc.stderr, b"")

    def test_empty_result_is_header_only(self):
        for text in ("", "\n  \n"):
            path = self.write("empty.jsonl", text)
            proc = self.run_cli(path, "--format", "csv")
            self.assertEqual((proc.returncode, proc.stdout), (0, self.HEADER.encode()))

    def test_special_groups_round_trip_sorted_and_summed(self):
        names = ['z,comma', 'q"uote', "new\nline", "é유니코드", ""]
        records = [{"group": n, "lines": [" ab "]} for n in names]
        records.append({"group": "z,comma", "lines": ["c", " "]})  # duplicate group sums
        path = self.write("s.jsonl", "\n".join(json.dumps(r, ensure_ascii=False) for r in records))
        proc = self.run_cli(path, "--format", "csv")
        self.assertEqual(proc.returncode, 0)
        out = proc.stdout.decode("utf-8")
        self.assertTrue(out.startswith(self.HEADER))
        rows = list(csv.reader(io.StringIO(out, newline="")))
        self.assertEqual(rows[0], ["group", "records", "lines", "characters"])
        expected = [[g["group"], str(g["records"]), str(g["lines"]), str(g["characters"])]
                    for g in summarize_jsonl("\n".join(json.dumps(r) for r in records))["groups"]]
        self.assertEqual(rows[1:], expected)
        self.assertEqual([r[0] for r in rows[1:]], sorted(names))
        self.assertIn(["z,comma", "2", "2", "3"], rows[1:])

    def test_record_errors_exit_2_csv_on_stdout_errors_on_stderr(self):
        path = self.write("mixed.jsonl", MIXED)
        proc = self.run_cli(path, "--format", "csv")
        self.assertEqual(proc.returncode, 2)
        self.assertEqual(proc.stdout, (self.HEADER + "a,1,0,0\r\n").encode())
        self.assertEqual(
            proc.stderr.decode().splitlines(),
            ["line 3: not_object", "line 4: invalid_json", "line 5: invalid_group", "line 6: invalid_lines"],
        )

    def test_io_and_decode_errors_exit_1_no_stdout(self):
        missing = self.run_cli(os.path.join(self.tmp.name, "nope.jsonl"), "--format", "csv")
        self.assertEqual((missing.returncode, missing.stdout), (1, b""))
        bad = os.path.join(self.tmp.name, "bad.jsonl")
        with open(bad, "wb") as handle:
            handle.write(b"\xff\n")
        proc = self.run_cli(bad, "--format", "csv")
        self.assertEqual((proc.returncode, proc.stdout), (1, b""))

    def test_bad_format_value_is_argparse_usage_error(self):
        path = self.write("ok.jsonl", '{"group":"a","lines":[]}')
        proc = self.run_cli(path, "--format", "xml")
        self.assertEqual((proc.returncode, proc.stdout), (2, b""))
        self.assertIn(b"invalid choice", proc.stderr)

    def test_default_and_json_output_byte_identical_to_p903(self):
        for text, code in (('{"group":"é","lines":[" a ","bc"]}\n', 0), (MIXED, 2)):
            path = self.write("j.jsonl", text)
            p903 = (json.dumps(summarize_jsonl(text), ensure_ascii=False) + "\n").encode("utf-8")
            default = self.run_cli(path)
            explicit = self.run_cli(path, "--format", "json")
            self.assertEqual((default.returncode, default.stdout), (code, p903))
            self.assertEqual((explicit.returncode, explicit.stdout), (code, p903))
            self.assertEqual(default.stderr, b"")


if __name__ == "__main__":
    unittest.main()
