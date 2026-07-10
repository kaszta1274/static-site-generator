import unittest
from generate_page import extract_title

class TestGeneratePage(unittest.TestCase):
    def test_extract_title(self):
        md = """
# Hello

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        title = extract_title(md)
        self.assertEqual(title, "Hello")

    def test_extract_no_title(self):
        md = """
## Hello

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        with self.assertRaises(Exception):
            title = extract_title(md)

    def test_extract_no_title(self):
        md = """
Hello

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        with self.assertRaises(Exception):
            title = extract_title(md)

