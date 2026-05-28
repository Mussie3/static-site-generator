import unittest
from main import extract_title


class TestExtractTitle(unittest.TestCase):
    def test_simple_title(self):
        self.assertEqual(extract_title("# Hello"), "Hello")

    def test_multi_word_title(self):
        self.assertEqual(extract_title("# Tolkien Fan Club"), "Tolkien Fan Club")

    def test_title_with_leading_blank_lines(self):
        markdown = "\n\n# Title\n\nbody"
        self.assertEqual(extract_title(markdown), "Title")

    def test_title_among_other_blocks(self):
        markdown = "Some intro\n\n# The Title\n\n## sub"
        self.assertEqual(extract_title(markdown), "The Title")

    def test_trailing_whitespace_stripped(self):
        self.assertEqual(extract_title("# Hello   "), "Hello")

    def test_h2_does_not_count(self):
        with self.assertRaises(ValueError):
            extract_title("## Only h2\n\n### h3")

    def test_missing_title_raises(self):
        with self.assertRaises(ValueError):
            extract_title("just some text\n\nno header here")


if __name__ == "__main__":
    unittest.main()
